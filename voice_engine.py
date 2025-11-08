# voice_engine.py
import threading
import queue
import time
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel


@dataclass
class EngineConfig:
    sample_rate: int = 16000             # 16 kHz para o VAD do WebRTC
    frame_ms: int = 20                   # 10/20/30 ms são válidos no VAD
    vad_mode: int = 2                    # 0=mais sensível ... 3=mais agressivo
    max_silence_ms: int = 800            # silêncio para “fechar” a frase
    min_utterance_ms: int = 300          # não enviar ruído muito curto
    device: str = "cpu"                  # "cpu" | "cuda"
    compute_type: str = "auto"           # "auto" tenta int8/int16/fp16 se possível
    model_name: str = "small"            # "tiny"/"base"/"small"/"medium"/"large-v3"
    language: Optional[str] = "pt"       # força PT; ou None para auto
    beam_size: int = 1                   # 1 = greedy (mais rápido)


class VoiceEngine:
    """
    Captura áudio do microfone, faz VAD com WebRTC e envia ‘falas’ completas
    para o faster-whisper. Chama on_text(texto) quando termina cada fala.
    """
    def __init__(self, on_text: Callable[[str], None], config: EngineConfig = EngineConfig()):
        self.on_text = on_text
        self.cfg = config

        # Whisper
        self.model = WhisperModel(
            self.cfg.model_name,
            device=self.cfg.device,
            compute_type=self.cfg.compute_type
        )

        # VAD
        self.vad = webrtcvad.Vad(self.cfg.vad_mode)
        self.frame_bytes = int(self.cfg.sample_rate * (self.cfg.frame_ms / 1000.0))  # amostras
        self.frame_bytes *= 2  # int16 = 2 bytes por amostra

        # Filas & threads
        self._audio_q: "queue.Queue[bytes]" = queue.Queue(maxsize=50)
        self._running = threading.Event()
        self._worker_t: Optional[threading.Thread] = None

        # stream de captura
        self._stream: Optional[sd.InputStream] = None

    # ========================= Public API =========================

    def start_async(self):
        """Inicia captura e reconhecimento em thread própria."""
        if self._running.is_set():
            return
        self._running.set()

        # Áudio: 16 kHz, mono, int16, blocos de ~20ms
        self._stream = sd.InputStream(
            samplerate=self.cfg.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=int(self.cfg.sample_rate * self.cfg.frame_ms / 1000),
            callback=self._sd_callback,
        )
        self._stream.start()

        self._worker_t = threading.Thread(target=self._recognize_loop, daemon=True)
        self._worker_t.start()

    def stop(self):
        self._running.clear()
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        if self._worker_t and self._worker_t.is_alive():
            self._worker_t.join(timeout=1.0)

    # ========================= Internals ==========================

    def _sd_callback(self, indata, frames, time_info, status):
        if status:
            # Você pode logar underrun/overrun aqui
            pass
        # bytes little-endian PCM16 mono
        chunk: bytes = indata.tobytes()
        # fatiar em frames exatos para o VAD
        for start in range(0, len(chunk), self.frame_bytes):
            piece = chunk[start:start + self.frame_bytes]
            if len(piece) == self.frame_bytes:
                try:
                    self._audio_q.put_nowait(piece)
                except queue.Full:
                    # Se a fila encher, descarte (mantém baixa latência)
                    pass

    def _recognize_loop(self):
        # buffers da fala atual
        voiced_frames: list[bytes] = []
        speech_active = False
        last_voice_time = 0.0
        min_utt_frames = int(self.cfg.min_utterance_ms / self.cfg.frame_ms)
        max_silence_frames = int(self.cfg.max_silence_ms / self.cfg.frame_ms)

        def is_speech(frame_bytes: bytes) -> bool:
            # VAD exige 16kHz mono PCM16 little-endian
            return self.vad.is_speech(frame_bytes, sample_rate=self.cfg.sample_rate)

        while self._running.is_set():
            try:
                frame = self._audio_q.get(timeout=0.2)
            except queue.Empty:
                # checar fechamento por silêncio caso a fila esteja vazia
                if speech_active and (time.time() - last_voice_time) * 1000 >= self.cfg.max_silence_ms:
                    self._flush_utterance(voiced_frames, min_utt_frames)
                    voiced_frames = []
                    speech_active = False
                continue

            if is_speech(frame):
                voiced_frames.append(frame)
                speech_active = True
                last_voice_time = time.time()
            else:
                if speech_active:
                    # ainda estamos dentro da janela de silêncio?
                    voiced_frames.append(frame)  # guarda mais um pouco para transições
                    if (time.time() - last_voice_time) * 1000 >= self.cfg.max_silence_ms:
                        self._flush_utterance(voiced_frames, min_utt_frames)
                        voiced_frames = []
                        speech_active = False
                # se não estamos falando, simplesmente ignora frames silenciosos

    def _flush_utterance(self, frames: list[bytes], min_utt_frames: int):
        if len(frames) < min_utt_frames:
            return  # muito curto; ignore

        audio_bytes = b"".join(frames)
        # bytes -> int16 -> float32 normalizado
        arr = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        # Transcrição (síncrona para simplificar). Tende a ser bem rápida localmente.
        segments, info = self.model.transcribe(
            arr,
            language=self.cfg.language,
            beam_size=self.cfg.beam_size,
            vad_filter=False,          # já fizemos VAD
            word_timestamps=False
        )

        text = "".join(seg.text for seg in segments).strip()
        if text:
            try:
                self.on_text(text)
            except Exception:
                pass

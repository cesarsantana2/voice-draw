# app.py
import tkinter as tk
from ui_canvas import UICanvas
from voice_engine import VoiceEngine
from nlp_parser import parse_command


class State:
    def __init__(self):
        self.last_text = ""


def on_transcript(text, ui: UICanvas, state: State):
    if not text or not text.strip():
        return

    print(f"[voz] -> {text}")
    state.last_text = text

    try:
        cmd = parse_command(text)
        print("[DEBUG CMD]:", cmd)

        if not cmd:
            ui.after(0, lambda: ui.set_status(
                "Não entendi. Diga algo como: 'círculo azul raio 40 em x 100 y 120'."
            ))
            return

        if not cmd.get("shape"):
            ui.after(0, lambda: ui.set_status(
                f"Não identifiquei a forma (círculo, quadrado, triângulo, linha, ponto)."
            ))
            return

        if not cmd.get("ok"):
            ui.after(0, lambda: ui.set_status(cmd.get("hint") or "Comando incompleto."))
            return

        # saneamento / defaults
        shape   = cmd["shape"]
        color   = cmd.get("color") or "black"
        x       = int(cmd.get("x") or 100)
        y       = int(cmd.get("y") or 100)
        th      = int(cmd.get("thickness") or 2)
        fill    = bool(cmd.get("fill") or False)
        radius  = int(cmd.get("radius") or 40)
        side    = int(cmd.get("side") or 60)
        x2      = int(cmd.get("x2") or (x + 100))
        y2      = int(cmd.get("y2") or y)

        def apply_on_ui():
            if shape == "circle":
                ui.draw_circle(x, y, radius, color=color, thickness=th, fill=fill)
            elif shape == "square":
                ui.draw_square(x, y, side, color=color, thickness=th, fill=fill)
            elif shape == "triangle":
                ui.draw_triangle(x, y, side, color=color, thickness=th, fill=fill)
            elif shape == "line":
                ui.draw_line(x, y, x2, y2, color=color, thickness=th)
            elif shape == "point":
                ui.draw_point(x, y, thickness=th, color=color)
            ui.set_status(f"✅ Feito: {shape} ({color})")
            state.last_text = ""

        ui.after(0, apply_on_ui)

    except Exception as e:
        # mostra o erro sem quebrar a UI
        print("[ERROR on_transcript]", repr(e))
        ui.after(0, lambda e=e: ui.set_status(f"Erro ao processar: {e}"))


def main():
    root = tk.Tk()
    root.title("VoiceDraw - Desenho por Voz")
    try:
        root.state("zoomed")
    except Exception:
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda ev: root.attributes("-fullscreen", False))

    ui = UICanvas(root)  # já faz pack no __init__
    state = State()

    engine = VoiceEngine(
        on_text=lambda text: on_transcript(text, ui, state)
    )

    ui.set_status("Fale: 'círculo azul raio 40 em x 100 y 120' (G liga/desliga a grade)")
    engine.start_async()
    root.mainloop()


if __name__ == "__main__":
    main()

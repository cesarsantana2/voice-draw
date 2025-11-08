# ⚙️ Guia de Instalação e Execução — VoiceDraw

Este documento orienta o processo completo de instalação e execução do **VoiceDraw**, desde a configuração do ambiente até os primeiros testes com comandos de voz.

---

## 🧩 Requisitos do sistema

Antes de iniciar, verifique se o seu ambiente atende aos seguintes pré-requisitos:

| Requisito                 | Descrição                                      |
| ------------------------- | ---------------------------------------------- |
| **Python**                | Versão 3.10 ou superior                        |
| **Sistema operacional**   | Windows, macOS ou Linux com suporte ao Tkinter |
| **Bibliotecas de áudio**  | Microfone funcional e `PyAudio` instalado      |
| **Dependências externas** | `SpeechRecognition`, `Pillow`, `regex`         |

> 💡 **Dica:** no Linux, talvez seja necessário instalar pacotes adicionais para suporte ao microfone (ex: `portaudio19-dev`, `ffmpeg`).

---

## 🧱 Passo 1 — Clonar o repositório

Abra o terminal e execute:

```bash
git clone git@github.com:cesarsantana2/voice-draw.git
cd voice-draw
```

Se preferir usar HTTPS:

```bash
git clone https://github.com/cesarsantana2/voice-draw.git
```

---

## 🧰 Passo 2 — Criar e ativar o ambiente virtual

### Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

```bash
python -m venv .venv
.venv\Scripts\activate
```

> 🧠 **Por que usar ambiente virtual?**
> Para isolar as dependências do projeto e evitar conflitos com outros pacotes instalados no sistema.

---

## 📦 Passo 3 — Instalar dependências

Execute o comando abaixo dentro do ambiente virtual:

```bash
pip install -r requirements.txt
```

### Se o arquivo `requirements.txt` ainda não existir, instale manualmente:

```bash
pip install SpeechRecognition PyAudio Pillow regex
```

---

## 🎤 Passo 4 — Testar o microfone

Antes de rodar a aplicação, confirme que o microfone está funcionando corretamente:

```bash
python -m speech_recognition
```

Fale algo — o sistema deve exibir a transcrição no terminal.

Se aparecer um erro de `OSError: No Default Input Device Available`, verifique as permissões de microfone nas configurações do sistema.

---

## 🪟 Passo 5 — Executar a aplicação

Execute o comando principal:

```bash
python app.py
```

Ao iniciar, o programa abrirá uma janela gráfica semelhante a esta:

```
+-------------------------------------+
|           VoiceDraw Canvas          |
|-------------------------------------|
| 🎤 Aguardando comando de voz...     |
|                                     |
| [Círculo Azul desenhado ✅]         |
+-------------------------------------+
```

---

## 🗣️ Passo 6 — Enviar seu primeiro comando de voz

Tente comandos simples em português, como:

* “Desenhar círculo azul raio 100 em x 300 y 300”
* “Desenhar quadrado verde lado 150 em x 200 y 200 preenchido”
* “Limpar tela”

O sistema interpretará sua fala, exibirá o comando reconhecido no console e desenhará automaticamente no **canvas**.

---

## 💾 Passo 7 — Exportar desenhos

Para salvar o resultado do desenho atual:

1. Clique em **Arquivo → Exportar** no menu (ou use o atalho `Ctrl + E`).
2. Escolha o formato (`.png`, `.jpg` ou `.bmp`).
3. O arquivo será salvo automaticamente na pasta `exports/`.

---

## 🧹 Passo 8 — Encerrando e limpando o ambiente

Quando quiser encerrar a sessão, basta desativar o ambiente virtual:

```bash
deactivate
```

Se desejar remover todas as dependências:

```bash
rm -rf .venv/
```

---

## 🧠 Solução de problemas comuns

| Problema                                     | Causa provável                   | Solução                                                   |
| -------------------------------------------- | -------------------------------- | --------------------------------------------------------- |
| `No module named tkinter`                    | Tkinter não instalado no sistema | Instale manualmente (`sudo apt install python3-tk`)       |
| `OSError: No Default Input Device Available` | Microfone não detectado          | Verifique permissões e dispositivos de entrada            |
| `ImportError: No module named pyaudio`       | Falta de dependência de áudio    | Instale `pip install pyaudio` ou `brew install portaudio` |

---

## 🧩 Dica final

Se quiser usar o VoiceDraw sem microfone, é possível digitar os comandos diretamente no terminal para testes rápidos:

```bash
python app.py --text "desenhar círculo azul raio 100"
```

---

> ✅ Agora o VoiceDraw está pronto para uso!
> Explore, desenhe e contribua para tornar a tecnologia mais acessível a todos.

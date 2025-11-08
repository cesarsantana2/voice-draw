"""
export.py
Funções para exportar o desenho do canvas para arquivo de imagem.

No MVP vamos usar o ImageGrab do Pillow para capturar o conteúdo da janela.
Depois podemos evoluir para exportar SVG ou salvar comandos em JSON.
"""

from PIL import ImageGrab

def export_png(canvas, output_path: str = "saida.png") -> None:
    """
    Exporta o canvas atual para um arquivo PNG.
    Basicamente tira um 'print' da área onde o canvas está.
    """
    # Garantir que tudo está renderizado antes de capturar
    canvas.update()

    # Coordenadas absolutas da janela (parte do SO)
    x0 = canvas.winfo_rootx()
    y0 = canvas.winfo_rooty()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()

    # Captura da área e salvamento
    screenshot = ImageGrab.grab(bbox=(x0, y0, x1, y1))
    screenshot.save(output_path, "PNG")

    print(f"[+] Imagem salva com sucesso em: {output_path}")

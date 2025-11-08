# shapes.py
# Funções utilitárias para desenhar primitivas no Tkinter Canvas.
# Cada função retorna o ID do item criado no canvas (int).

from typing import Optional

def draw_point(c, x: int, y: int, color: str, w: int) -> int:
    """
    Desenha um ponto como um pequeno círculo preenchido.
    w controla o diâmetro aproximado (2*w).
    """
    return c.create_oval(x - w, y - w, x + w, y + w, fill=color, outline=color, width=0)

def draw_line(c, x1: int, y1: int, x2: int, y2: int, color: str, w: int) -> int:
    """Desenha uma reta entre (x1,y1) e (x2,y2)."""
    return c.create_line(x1, y1, x2, y2, fill=color, width=w)

def draw_circle(c, cx: int, cy: int, r: int, color: str, w: int, fill: bool = False) -> int:
    """Desenha um círculo de centro (cx,cy) e raio r."""
    fill_color: Optional[str] = color if fill else ""
    return c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=w, fill=fill_color)

def draw_square(c, cx: int, cy: int, lado: int, color: str, w: int, fill: bool = False) -> int:
    """Desenha um quadrado centralizado em (cx,cy) com lado especificado."""
    h = lado / 2
    fill_color: Optional[str] = color if fill else ""
    return c.create_rectangle(cx - h, cy - h, cx + h, cy + h, outline=color, width=w, fill=fill_color)

def draw_triangle(c, cx: int, cy: int, lado: int, color: str, w: int, fill: bool = False) -> int:
    """
    Desenha um triângulo equilátero centralizado em (cx,cy).
    O ponto superior fica acima do centro; base horizontal.
    """
    import math
    h = (math.sqrt(3) / 2) * lado
    # Coordenadas dos 3 vértices (equilátero, centrado pelo baricentro)
    pts = [
        cx,           cy - 2 * h / 3,   # topo
        cx - lado/2,  cy + h / 3,       # base esquerda
        cx + lado/2,  cy + h / 3        # base direita
    ]
    fill_color: Optional[str] = color if fill else ""
    return c.create_polygon(*pts, outline=color, width=w, fill=fill_color)

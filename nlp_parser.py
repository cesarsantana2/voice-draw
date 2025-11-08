# nlp_parser.py
import re

# Números até 4 dígitos (bom o suficiente pro nosso canvas)
_NUM = r'(\d{1,4})'


def _norm(s: str) -> str:
    """Normaliza texto reconhecido pelo STT."""
    s = s.lower()
    s = s.replace(' ', ' ').replace('\u00a0', ' ')
    # tira separador de milhar e normaliza decimal
    s = s.replace('.', '')
    s = s.replace(',', '.')
    return s


def _to_int(txt: str):
    try:
        return int(float(txt))
    except Exception:
        return None


def parse_command(text: str) -> dict:
    t = _norm(text)

    # ---------- forma ----------
    shape = None
    if re.search(r'\b(círculo|circulo)\b', t):
        shape = "circle"
    elif re.search(r'\bquadrad[oa]\b', t):
        shape = "square"
    elif re.search(r'\btriângulo\b|\btriangulo\b', t):
        shape = "triangle"
    elif re.search(r'\blinha\b', t):
        shape = "line"
    elif re.search(r'\bponto\b', t):
        shape = "point"

    # ---------- cor ----------
    color = None
    for pt, en in [
        (r'vermelh[oa]', 'red'),
        (r'azul', 'blue'),
        (r'pret[oa]', 'black'),
        (r'verd[ea]', 'green'),
        (r'amarel[oa]', 'yellow'),
    ]:
        if re.search(rf'\b{pt}\b', t):
            color = en
            break

    # ---------- parâmetros numéricos ----------

    # raio 100
    m_radius = re.search(rf'raio\s*{_NUM}', t)

    # lado 120 / lá do 120 / la do 120 (STT adora isso)
    m_side = re.search(
        rf'(?:lado|l\s*ado|l[áa]\s*do)\D*{_NUM}',
        t
    )

    # em x 300 y 300
    # em x300 y300
    # x300, y300
    # aceita "em" opcional e qualquer separador não-numérico entre X e Y
    m_xy = re.search(
        rf'(?:em\s*)?x\s*{_NUM}\D+?y\s*{_NUM}',
        t
    )

    # até x 800 y 900 / até x800, y900 ...
    m_xy2 = re.search(
        rf'at[eé]\s*x\s*{_NUM}\D+?y\s*{_NUM}',
        t
    )

    # espessura 3 / grossura 3
    m_th = re.search(
        rf'(?:espessura|grossura)\D*{_NUM}',
        t
    )

    # preenchido / cheio
    m_fill = re.search(
        r'\b(preenchid[oa]s?|chei[oa]s?)\b',
        t
    )

    # ---------- extrai valores ----------

    radius = _to_int(m_radius.group(1)) if m_radius else None
    side = _to_int(m_side.group(1)) if m_side else None

    if m_xy:
        x = _to_int(m_xy.group(1))
        y = _to_int(m_xy.group(2))
    else:
        x = y = None

    if m_xy2:
        x2 = _to_int(m_xy2.group(1))
        y2 = _to_int(m_xy2.group(2))
    else:
        x2 = y2 = None

    thickness = _to_int(m_th.group(1)) if m_th else None
    fill = bool(m_fill)

    cmd = {
        "ok": True,
        "shape": shape,
        "color": color,
        "radius": radius,
        "side": side,
        "x": x,
        "y": y,
        "x2": x2,
        "y2": y2,
        "thickness": thickness,
        "fill": fill,
        "hint": ""
    }

    # ---------- validações + mensagens amigáveis ----------

    if not shape:
        cmd["ok"] = False
        cmd["hint"] = "Não identifiquei a forma (círculo, quadrado, triângulo, linha, ponto)."
        return cmd

    if shape == "circle" and radius is None:
        cmd["ok"] = False
        cmd["hint"] = "Faltou o raio. Ex.: 'círculo azul raio 100 em x 300 y 300'."

    if shape in ("square", "triangle") and side is None:
        cmd["ok"] = False
        cmd["hint"] = "Faltou o lado. Ex.: 'quadrado vermelho lado 120 em x 600 y 500'."

    if shape in ("circle", "square", "triangle", "point") and (x is None or y is None):
        cmd["ok"] = False
        cmd["hint"] = "Faltou a posição. Use 'em x 300 y 300'."

    if shape == "line":
        if x is None or y is None or x2 is None or y2 is None:
            cmd["ok"] = False
            cmd["hint"] = (
                "Para linha use algo como: "
                "'desenhar linha preta de x 100 y 900 até x 800 y 900 espessura 4'."
            )

    return cmd

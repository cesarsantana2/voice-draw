# `nlp_parser.py`

Responsável por transformar frases em português em um **comando estruturado** compreensível pela aplicação.

---

## Exemplo de entrada

```text
desenhar círculo azul raio 100 em x 300 y 300 espessura 3
```

## Saída esperada (exemplo)

```json
{
  "ok": true,
  "shape": "circle",
  "color": "blue",
  "radius": 100,
  "x": 300,
  "y": 300,
  "thickness": 3,
  "fill": false,
  "hint": ""
}
```

---

## Principais responsabilidades

* **Normalizar o texto**
  Converter tudo para minúsculas, remover acentos, pontuação desnecessária e espaços duplicados.

* **Detectar a forma geométrica**
  Identifica palavras-chave como:

  * `círculo`
  * `quadrado`
  * `triângulo`
  * `linha`
  * `ponto`

* **Extrair parâmetros**
  Reconhece e converte valores numéricos associados a palavras como:

  * `raio`
  * `lado`
  * `x`
  * `y`
  * `x2`
  * `y2`
  * `espessura`

* **Detectar cor**
  Mapeia cores em português para o formato padrão em inglês usado pelo Tkinter, por exemplo:

  * `vermelho` → `red`
  * `azul` → `blue`
  * `verde` → `green`
  * `preto` → `black`
  * `amarelo` → `yellow`

* **Detectar preenchimento**
  Palavras como `preenchido` ou `cheio` indicam que a forma deve ser desenhada com `fill=True`.

* **Gerar feedback amigável (`hint`)**
  Caso o comando não seja reconhecido ou esteja incompleto, o parser retorna:

  ```python
  {"ok": False, "hint": "Comando incompleto: especifique raio ou coordenadas."}
  ```

---

## Fluxo resumido

1. Recebe o texto bruto do reconhecimento de voz (string);
2. Normaliza e limpa o texto;
3. Aplica regras de detecção (formas, cores, parâmetros);
4. Monta um dicionário padronizado para o módulo `app.py`;
5. Retorna `ok=True` se o comando for válido.

---

## Exemplo completo de uso

```python
from nlp_parser import parse_command

text = "desenhar círculo azul raio 100 em x 300 y 300 espessura 3"
cmd = parse_command(text)

if cmd["ok"]:
    print("Forma reconhecida:", cmd["shape"])
else:
    print("Erro:", cmd["hint"])
```

Saída:

```bash
Forma reconhecida: circle
```

---

## Observações técnicas

* O módulo é **independente da interface gráfica** (não depende de Tkinter).
* Pode ser testado isoladamente em um script Python.
* Foi projetado para ser **extensível** — novas formas ou cores podem ser adicionadas facilmente.
* O parser é determinístico (sem uso de IA): usa expressões regulares e mapeamentos fixos.

---

> **Resumo:**
> O `nlp_parser.py` é o coração da interpretação semântica do VoiceDraw.
> Ele traduz comandos em português falado em instruções estruturadas e seguras para o canvas.
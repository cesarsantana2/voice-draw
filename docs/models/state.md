# `state.py`

O módulo `state.py` é responsável por **armazenar e gerenciar o estado atual do desenho** dentro da aplicação VoiceDraw. Ele atua como uma camada de persistência temporária, permitindo que o sistema saiba o que foi desenhado, qual foi o último comando e como restaurar o canvas se necessário.

---

## Função principal

* Manter o histórico de formas desenhadas e comandos executados;
* Permitir operações como *desfazer (undo)*, *refazer (redo)* ou *limpar* o canvas;
* Facilitar o salvamento e exportação de estados atuais.

---

## Principais responsabilidades

* **Armazenar o histórico de comandos**
  Cada forma desenhada gera um registro no dicionário `state`, incluindo tipo, coordenadas, cor e espessura.

* **Gerenciar operações de controle**

  * `add_shape(shape_data)`: adiciona uma nova forma ao histórico.
  * `undo()`: remove a última forma desenhada.
  * `redo()`: restaura uma forma removida anteriormente.
  * `clear()`: limpa o histórico e o canvas.

* **Integração com `ui_canvas`**

  * Sempre que uma forma é desenhada, `state` armazena uma cópia dos parâmetros.
  * Facilita a re-renderização completa do canvas quando necessário.

* **Exportação do estado**

  * Pode ser salvo como JSON através do módulo `export.py`.
  * Exemplo de estado:

  ```json
  [
    {
      "shape": "circle",
      "color": "blue",
      "x": 300,
      "y": 300,
      "radius": 100,
      "fill": false
    },
    {
      "shape": "line",
      "x": 50,
      "y": 50,
      "x2": 200,
      "y2": 100
    }
  ]
  ```

---

## Estrutura geral do módulo

```python
class State:
    def __init__(self):
        self.shapes = []
        self.redo_stack = []

    def add_shape(self, shape_data):
        self.shapes.append(shape_data)
        self.redo_stack.clear()

    def undo(self):
        if self.shapes:
            shape = self.shapes.pop()
            self.redo_stack.append(shape)
            return shape
        return None

    def redo(self):
        if self.redo_stack:
            shape = self.redo_stack.pop()
            self.shapes.append(shape)
            return shape
        return None

    def clear(self):
        self.shapes.clear()
        self.redo_stack.clear()
```

---

## Fluxo de uso

```mermaid
graph TD;
    A[app.py] --> B[state.add_shape()];
    B --> C[state.undo()];
    C --> D[ui_canvas limpa e redesenha];
    D --> E[Usuário visualiza resultado];
```

---

## Exemplo de uso

```python
from state import State

state = State()

# Adiciona uma forma
state.add_shape({"shape": "circle", "x": 100, "y": 200, "radius": 50})

# Desfaz a última ação
state.undo()

# Restaura a ação desfeita
state.redo()

# Limpa todo o histórico
state.clear()
```

---

## Observações técnicas

* O módulo `state.py` não depende de Tkinter nem de áudio — é puramente lógico.
* Atua como uma camada de dados que permite a reconstrução do canvas.
* Pode futuramente suportar **checkpointing** (salvar versões específicas).
* Facilita a integração com o módulo `export.py` para gerar relatórios e reproduções.

---

> **Resumo:**
> O `state.py` é o controlador de memória do VoiceDraw. Ele registra cada ação de desenho, permitindo desfazer, refazer e exportar o estado do canvas.

# ui_canvas.py
import tkinter as tk

class UICanvas(tk.Canvas):
    def __init__(self, master, show_grid=True):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)

        self.show_grid = show_grid
        self.bind("<KeyPress-g>", self.toggle_grid)
        self.focus_set()

        self.draw_grid()

    def toggle_grid(self, event=None):
        self.show_grid = not self.show_grid
        self.delete("grid")
        if self.show_grid:
            self.draw_grid()

    def draw_grid(self):
        if not self.show_grid:
            return

        width = 2000
        height = 2000
        step = 50  

        for x in range(0, width, step):
            color = "#d0d0d0" if x % 200 else "#a0a0a0"
            self.create_line(x, 0, x, height, fill=color, tags="grid")
            if x % 200 == 0:
                self.create_text(x + 2, 10, text=str(x), anchor="nw", fill="#505050", tags="grid")

        for y in range(0, height, step):
            color = "#d0d0d0" if y % 200 else "#a0a0a0"
            self.create_line(0, y, width, y, fill=color, tags="grid")
            if y % 200 == 0:
                self.create_text(2, y + 2, text=str(y), anchor="nw", fill="#505050", tags="grid")

        self.create_text(5, 5, text="X", anchor="nw", fill="black", tags="grid")
        self.create_text(5, height - 15, text="Y", anchor="sw", fill="black", tags="grid")

    def safe_int(self, v, default=0):
        try:
            return int(v)
        except:
            return default

    def set_status(self, msg):
        print("[status]", msg)

    def draw_circle(self, x, y, radius, color="black", thickness=2, fill=False):
        x = self.safe_int(x)
        y = self.safe_int(y)
        radius = self.safe_int(radius)

        fill_color = color if fill else ""
        self.create_oval(x - radius, y - radius, x + radius, y + radius,
                         outline=color, width=self.safe_int(thickness), fill=fill_color)

# ui_canvas.py (apenas o método alterado)

    def draw_square(self, x, y, side, color="black", thickness=2, fill=False):
        x = int(x); y = int(y); side = int(side)
        h = side // 2
        fill_color = color if fill else ""
        self.create_rectangle(x - h, y - h, x + h, y + h, outline=color, width=thickness, fill=fill_color)


    def draw_triangle(self, x, y, side, color="black", thickness=2, fill=False):
        x = int(x); y = int(y); side = int(side)
        h = side * 0.866  # altura do equilátero
        # centrado em (x,y)
        pts = [
            x,           y - (2/3)*h,        # topo
            x - side/2,  y + (1/3)*h,        # base esquerda
            x + side/2,  y + (1/3)*h         # base direita
        ]
        fill_color = color if fill else ""
        self.create_polygon(pts, outline=color, width=thickness, fill=fill_color)

    def draw_line(self, x1, y1, x2, y2, color="black", thickness=2):
        self.create_line(self.safe_int(x1), self.safe_int(y1),
                         self.safe_int(x2), self.safe_int(y2),
                         fill=color, width=self.safe_int(thickness))

    def draw_point(self, x, y, thickness=4, color="black"):
        x = self.safe_int(x)
        y = self.safe_int(y)
        self.create_oval(x-2, y-2, x+2, y+2, fill=color, outline=color, width=self.safe_int(thickness))

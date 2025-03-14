import tkinter as tk
from tkinter import Canvas
from multiprocessing import Process
from random import randint


class AnimatedLine:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.line_id = self.create_random_line()
        self.start_animations()


    def create_random_line(self):
        return self.canvas.create_line(
            randint(0, self.width),
            randint(0, self.height),
            randint(0, self.width),
            randint(0, self.height),
            width=randint(1, 10)
        )

    def change_color(self):
        color = "#{:06x}".format(randint(0, 0xFFFFFF))
        self.canvas.itemconfig(self.line_id, fill=color)
        self.canvas.after(100, self.change_color)

    def change_thickness(self):
        width = randint(1, 10)
        self.canvas.itemconfig(self.line_id, width=width)
        self.canvas.after(100, self.change_thickness)

    def change_position(self):
        new_coords = (
            randint(0, self.width),
            randint(0, self.height),
            randint(0, self.width),
            randint(0, self.height)
        )
        self.canvas.coords(self.line_id, *new_coords)
        self.canvas.after(100, self.change_position)

    def start_animations(self):
        self.change_color()
        self.change_thickness()
        self.change_position()


class AnimatedCircle:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.circle_id = self.create_random_circle()
        self.start_animations()

    def create_random_circle(self):
        radius = randint(10, 50)
        x = randint(radius, self.width - radius)
        y = randint(radius, self.height - radius)
        return self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill="#{:06x}".format(randint(0, 0xFFFFFF)),
            outline=""
        )

    def change_color(self):
        color = "#{:06x}".format(randint(0, 0xFFFFFF))
        self.canvas.itemconfig(self.circle_id, fill=color, outline=color)
        self.canvas.after(100, self.change_color)

    def change_size_and_position(self):
        new_radius = randint(10, 50)
        x = randint(new_radius, self.width - new_radius)
        y = randint(new_radius, self.height - new_radius)
        self.canvas.coords(
            self.circle_id,
            x - new_radius, y - new_radius,
            x + new_radius, y + new_radius
        )
        self.canvas.after(100, self.change_size_and_position)

    def start_animations(self):
        self.change_color()
        self.change_size_and_position()


class ChildWindow:
    WIDTH = 500
    HEIGHT = 500

    def __init__(self, position):
        self.position = position
        self.window = tk.Tk()
        self.canvas = Canvas(self.window, bg="white", width=self.WIDTH, height=self.HEIGHT)
        self.setup_window()

    def setup_window(self):
        self.window.title(f"Окно {self.position}")
        self.add_process_label()
        self.position_window()
        self.canvas.pack(expand=True)
        self.create_content()

    def add_process_label(self):
        pid = Process().pid
        label = tk.Label(self.window, text=f"Номер процесса: {pid}")
        label.pack()

    def position_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        if self.position == "справа":
            x = screen_width - self.WIDTH - 50
        else:
            x = 50

        y = (screen_height - self.HEIGHT) // 2
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def create_content(self):
        if self.position == "слева":
            AnimatedLine(self.canvas, self.WIDTH, self.HEIGHT)
        else:
            AnimatedCircle(self.canvas, self.WIDTH, self.HEIGHT)

    def run(self):
        self.window.mainloop()


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Лабораторная работа 1")
        self.setup_main_window()
        self.create_buttons()

    def setup_main_window(self):
        width, height = 400, 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        buttons = [
            ("Открыть правое окно", "справа"),
            ("Открыть левое окно", "слева")
        ]

        for text, position in buttons:
            btn = tk.Button(
                frame,
                text=text,
                command=lambda pos=position: Process(
                    target=ChildWindow(pos).run
                ).start()
            )
            btn.pack(pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = MainWindow()
    app.run()
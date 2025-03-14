import tkinter as tk
from tkinter import Canvas
from multiprocessing import Process, freeze_support, Queue
from random import randint
import os


class AnimateFigure:
    def __init__(self, canvas, width, height, shape_type):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.shape_id = self.make_shape(shape_type)
        self.animate(shape_type)

    def random_color(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def make_shape(self, shape_type):
        if shape_type == "line":
            return self.canvas.create_line(
                randint(0, self.width), randint(0, self.height),
                randint(0, self.width), randint(0, self.height),
                width=randint(1, 10)
            )
        else:
            r = randint(10, 50)
            x, y = randint(r, self.width - r), randint(r, self.height - r)
            return self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=self.random_color(), outline=""
            )

    def update(self, shape_type):
        if shape_type == "line":
            self.canvas.itemconfig(self.shape_id, fill=self.random_color(), width=randint(1, 10))
            self.canvas.coords(self.shape_id,
                               randint(0, self.width), randint(0, self.height),
                               randint(0, self.width), randint(0, self.height))
        else:
            r = randint(10, 50)
            x, y = randint(r, self.width - r), randint(r, self.height - r)
            self.canvas.itemconfig(self.shape_id, fill=self.random_color(), outline="")
            self.canvas.coords(self.shape_id, x - r, y - r, x + r, y + r)
        self.canvas.after(100, self.update, shape_type)

    def animate(self, shape_type):
        self.update(shape_type)


def run_child_window(position, queue):
    """Функция для запуска дочернего окна в отдельном процессе"""
    window = tk.Tk()
    window.title(f"Окно {position}")

    def on_closing():
        queue.put(position)
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    WIDTH, HEIGHT = 500, 500
    canvas = Canvas(window, bg="white", width=WIDTH, height=HEIGHT)

    tk.Label(window, text=f"Номер процесса: {os.getpid()}").pack()

    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
    x = screen_width - WIDTH - 50 if position == "справа" else 50
    y = (screen_height - HEIGHT) // 2
    window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    canvas.pack(expand=True)

    # Запуск анимации
    AnimateFigure(canvas, WIDTH, HEIGHT, "line" if position == "слева" else "circle")

    window.mainloop()


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Лабораторная работа 1")
        self.processes = {}
        self.queues = {}
        self.setup()
        self.add_buttons()
        self.check_queues()

    def setup(self):
        width, height = 300, 100
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (screen_width - width) // 2, (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def start_process(self, position, button):
        """Создание нового процесса"""
        button.config(state="disabled")
        queue = Queue()
        self.queues[position] = queue
        process = Process(target=run_child_window, args=(position, queue), daemon=True)
        process.start()
        self.processes[position] = (process, button)

    def on_window_close(self, position):

        if position in self.processes:
            _, button = self.processes[position]
            button.config(state="normal")
            del self.processes[position]
            del self.queues[position]

    def check_queues(self):
        """Проверка очередей на наличие сообщений о закрытии окон"""
        for position, queue in list(self.queues.items()):
            if not queue.empty():
                closed_position = queue.get()
                self.on_window_close(closed_position)
        self.root.after(100, self.check_queues)

    def add_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        for text, pos in [("Открыть правое окно", "справа"), ("Открыть левое окно", "слева")]:
            button = tk.Button(frame, text=text)
            button.config(command=lambda p=pos, b=button: self.start_process(p, b))
            button.pack(pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    freeze_support()
    MainWindow().run()
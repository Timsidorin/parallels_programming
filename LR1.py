import tkinter as tk
from tkinter import Canvas
from multiprocessing import Process, current_process
from random import randint
from itertools import cycle

def change_line_color(canvas, line_id, colors):
    """Функция для изменения цвета линии."""
    color = next(colors)
    canvas.itemconfig(line_id, fill=color)
    canvas.after(100, change_line_color, canvas, line_id, colors)

def change_line_thickness(canvas, line_id):
    """Функция для изменения ширины линии."""
    width = randint(1, 10)
    canvas.itemconfig(line_id, width=width)
    canvas.after(100, change_line_thickness, canvas, line_id)

def create_new_window(position):
    # Создаем новое окно
    new_window = tk.Tk()
    new_window.title(f"Окно {position}")

    # Выводим номер процесса
    pid = current_process().pid
    label = tk.Label(new_window, text=f"Номер процесса: {pid}")
    label.pack()

    # Устанавливаем положение окна
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    window_width = 500
    window_height = 500

    if position == "справа":
        x = screen_width - window_width - 50  # Отступ 50 пикселей от правого края
        y = (screen_height - window_height) // 2
    elif position == "слева":
        x = 50  # Отступ 50 пикселей от левого края
        y = (screen_height - window_height) // 2

    # Создаем холст
    canvas = Canvas(new_window, bg="white", width=window_width, height=window_height)
    canvas.pack(expand=True)

    # Рисуем линию
    line_id = canvas.create_line(10, 10, 200, 50, width=2)

    # Цикл цветов для линии
    colors = cycle(["red", "green", "blue", "yellow", "purple", "orange"])

    # Запускаем смену цвета
    change_line_color(canvas, line_id, colors)

    # Запускаем смену толщины
    change_line_thickness(canvas, line_id)

    # Устанавливаем геометрию окна
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    new_window.mainloop()

def main():
    # Создание главного окна
    root = tk.Tk()
    root.title("Главное окно")

    # Устанавливаем размеры окна
    window_width = 400
    window_height = 300

    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Вычисляем координаты для центрирования окна
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Устанавливаем геометрию окна
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Создаем фрейм для кнопок
    button_frame = tk.Frame(root)
    button_frame.pack(expand=True)

    # Кнопка для открытия окна справа
    right_button = tk.Button(
        button_frame,
        text="Открыть правое окно",
        command=lambda: Process(target=create_new_window, args=("справа",)).start()
    )
    right_button.pack(pady=10)

    # Кнопка для открытия окна слева
    left_button = tk.Button(
        button_frame,
        text="Открыть левое окно",
        command=lambda: Process(target=create_new_window, args=("слева",)).start()
    )
    left_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
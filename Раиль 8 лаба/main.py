"""
Шабаев Раиль ИСТбд-23
Требуется написать ООП с графическим интерфейсом в соответствии со своим вариантом.
Должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных не использовать.
При необходимости сохранять информацию в файлах, разделяя значения запятыми (CSV файлы) или пробелами. Для GUI использовать библиотеку tkinter.

Вариант - 8
Объекты – сектора круга
Функции: проверка пересечения
визуализация
раскраска
поворот вокруг одной из граничных вершин
"""


from tkinter.messagebox import showerror, showwarning, showinfo
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
import math

class DraggableArcs:
    def __init__(self, canvas):
        self.canvas = canvas
        self.arcs = []
        # Привязываем события для каждой дуги
        for arc in self.arcs:
            self.canvas.tag_bind(arc, "<ButtonPress-1>", self.on_button_press)
            self.canvas.tag_bind(arc, "<B1-Motion>", self.on_mouse_drag)
            self.canvas.tag_bind(arc, "<ButtonPress-3>", self.on_right_button_press)
            self.canvas.tag_bind(arc, "<B3-Motion>", self.on_right_mouse_drag)

        self.offset_x = 0
        self.offset_y = 0
        self.start_angle = 0
        self.center_x = 0
        self.center_y = 0
        self.current_arc = None

    def on_button_press(self, event):
        self.current_arc = self.canvas.find_closest(event.x, event.y)[0]
        x, y = self.canvas.coords(self.current_arc)[:2]
        self.offset_x = event.x - x
        self.offset_y = event.y - y

    def on_mouse_drag(self, event):
        if self.current_arc:
            self.canvas.move(self.current_arc, event.x - self.offset_x - self.canvas.coords(self.current_arc)[0],
                             event.y - self.offset_y - self.canvas.coords(self.current_arc)[1])

    def on_right_button_press(self, event):
        self.current_arc = self.canvas.find_closest(event.x, event.y)[0]
        coords = self.canvas.coords(self.current_arc)
        self.center_x = (coords[0] + coords[2]) / 2
        self.center_y = (coords[1] + coords[3]) / 2
        self.start_angle = self.calculate_angle(event.x, event.y)

    def on_right_mouse_drag(self, event):
        if self.current_arc:
            current_angle = self.calculate_angle(event.x, event.y)
            angle_diff = current_angle - self.start_angle

            # Обновляем угол
            start = self.canvas.itemcget(self.current_arc, "start")
            new_start = (float(start) - angle_diff) % 360
            self.canvas.itemconfig(self.current_arc, start=new_start)

            # Обновляем начальный угол для следующего движения
            self.start_angle = current_angle

    def open_file(self):
        # Открываем диалог для выбора файла
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    # Разбиваем строку на части
                    parts = line.strip().split(', ')
                    x0, y0, x1, y1 = map(int, parts[:4])
                    width = int(parts[4])
                    fill = parts[5]
                    start = int(parts[6])
                    extent = int(parts[7])

                    # Создаем дугу на основе данных из файла
                    arc = self.canvas.create_arc((x0, y0), (x1, y1), width=width, fill=fill, start=start, extent=extent)
                    self.arcs.append(arc)

                    # Привязываем события для новой дуги
                    self.canvas.tag_bind(arc, "<ButtonPress-1>", self.on_button_press)
                    self.canvas.tag_bind(arc, "<B1-Motion>", self.on_mouse_drag)
                    self.canvas.tag_bind(arc, "<ButtonPress-3>", self.on_right_button_press)
                    self.canvas.tag_bind(arc, "<B3-Motion>", self.on_right_mouse_drag)

    def show_information_about_program(self):
        window = tk.Tk()
        window.title("Окно информации")
        window.geometry('%dx%d+%d+%d' % (1400, 400, 250, 250))
        label = tk.Label(window, text="--Руководство к приложению--\n"
                                      "В данной программе, пользователь работает с секторами кругов. Примечание:\n"
                                      "1. Файл должен иметь расширение .txt (имя файла любое) и находиться в директории проекта.\n"
                                      "2. Txt-файл содержит информацию о секторах кругов, где каждая строка описывает один сектор.\n"
                                      "3. Каждая строка состоит из 8 объектов, разделенных запятыми:\n"
                                      "   - Первые четыре числа: координаты прямоугольника, который задаёт сектор круга: x0, y0, x1, y1\n"
                                      "   - Далее идут ширина, цвет, стартовый и конечный угол\n"
                                      "4. Для того чтобы проверить пересечение между секторами, можно нажать на кнопку 'Найти пересечение'\n"
                                      "5. Чтобы изменить цвет сектора круга достаточно выбрать сектор круга и нажать на 'Изменить цвет'\n"
                                      "6. Для того чтобы повернуть сектор, пользователю нужно выбрать одну из вершин данного сектора при помощи ПКМ. \n"
                                      "А затем поворачивать в нужную сторону(по часовой или против часовой стрелки).\n",
                         font=("Tahoma ", 17, "bold"))
        label.pack()

    def calculate_angle(self, mouse_x, mouse_y):
        # Вычисляем угол между центром дуги и курсором мыши
        return math.degrees(math.atan2(mouse_y - self.center_y, mouse_x - self.center_x))

    def find_first_intersection(self):
        for x in range(0, 600):
            for y in range(0, 600):
                if self.check_intersection(x, y):
                    return (x, y)
        return None

    def check_intersection(self, x, y):
        overlapping_arcs = self.canvas.find_overlapping(x, y, x, y)
        return len(overlapping_arcs) >= 2

    def show_intersection(self):
        intersection_point = self.find_first_intersection()
        if intersection_point:
            x, y = intersection_point
            tk.messagebox.showinfo("Пересечение", "Пересечение найдено!")
        else:
            tk.messagebox.showinfo("Пересечение", "Пересечений не найдено.")

    def change_color(self):
        if self.current_arc:
            color = colorchooser.askcolor()[1]  # Получаем выбранный цвет
            if color:
                self.canvas.itemconfig(self.current_arc, fill=color)  # Меняем цвет сектора

root = tk.Tk()
root.geometry('%dx%d+%d+%d' % (1366, 860, 270, 130))
root.title('8 лаба ООП Сектора Кругов')
canvas = tk.Canvas(root, width=800, height=820, bg='white', highlightbackground="black")
canvas.place(x=0,y=0)
draggable_arcs = DraggableArcs(canvas)
# Кнопки
button_open_file = tk.Button(root, text="Открыть файл", command=draggable_arcs.open_file, font=("Arial", 22))
button_open_file.place(x=950, y=40, width=290)
# Добавляем кнопку для поиска пересечений
button = tk.Button(root, text="Найти пересечение", command=draggable_arcs.show_intersection, font=("Arial", 22))
button.place(x=950, y=140)
# Добавляем кнопку для изменения цвета
button_color = tk.Button(root, text="Изменить цвет", command=draggable_arcs.change_color, font=("Arial", 22))
button_color.place(x=950, y=240, width=290)
button_info = tk.Button(root, text="Информация", command=draggable_arcs.show_information_about_program, font=("Arial", 22))
button_info.place(x=950, y=340, width=290)
root.mainloop()

import tkinter as tk
from tkinter import messagebox

class DraggableArcs:
    def __init__(self, canvas):
        self.canvas = canvas
        self.arcs = []

        # Создаем дуги и добавляем их в список
        self.arcs.append(canvas.create_arc((10, 10), (300, 300), width=2, fill="orange",
                                           start=0, extent=90))

        self.arcs.append(canvas.create_arc((50, 50), (600, 600), width=2, fill="blue",
                                           start=0, extent=20))
        self.arcs.append(canvas.create_arc((20, 20), (450, 450), width=2, fill="red",
                                           start=0, extent=60))

        # Привязываем события для каждой дуги
        for arc in self.arcs:
            self.canvas.tag_bind(arc, "<ButtonPress-1>", self.on_button_press)
            self.canvas.tag_bind(arc, "<B1-Motion>", self.on_mouse_drag)
            self.canvas.tag_bind(arc, "<ButtonRelease-3>", self.on_button_release)

        self.offset_x = 0
        self.offset_y = 0
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

    def on_button_release(self, event):
        self.current_arc = None

    def find_first_intersection(self): # метод который нужно пофиксить
        # Проверяем пересечения для всех возможных точек на канвасе
        for x in range(0, 600):  # Ширина канваса
            for y in range(0, 600):  # Высота канваса
                if self.check_intersection(x, y):
                    return (x, y)  # Возвращаем первую точку пересечения

        return None  # Если пересечений не найдено

    def check_intersection(self, x, y):
        # Проверяем, находится ли точка в закрашенной области двух или более дуг
        overlapping_arcs = self.canvas.find_overlapping(x, y, x, y)
        return len(overlapping_arcs) >= 2

    def show_intersection(self):
        intersection_point = self.find_first_intersection()
        if intersection_point:
            x, y = intersection_point
            print(f"Пересечение в точке: ({x}, {y})")
            tk.messagebox.showinfo("Пересечение", f"Пересечение в точке: ({x}, {y})")
        else:
            print("Пересечений не найдено.")
            tk.messagebox.showinfo("Пересечение", "Пересечений не найдено.")


root = tk.Tk()
root.geometry('1280x720')
root.title('Canvas Demo - Arc')

canvas = tk.Canvas(root, width=600, height=600, bg='white')
canvas.pack(anchor=tk.CENTER, expand=True)

draggable_arcs = DraggableArcs(canvas)

# Добавляем кнопку для поиска пересечений
button = tk.Button(root, text="Найти пересечение", command=draggable_arcs.show_intersection)
button.pack(pady=10)

root.mainloop()
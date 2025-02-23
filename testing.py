import tkinter as tk

class DraggableArc:
    def __init__(self, canvas):
        self.canvas = canvas
        self.arc = canvas.create_arc((10, 10), (300, 300), width=2, fill="orange",
                                      start=0, extent=90)
        self.canvas.tag_bind(self.arc, "<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.arc, "<B1-Motion>", self.on_mouse_drag)
        self.canvas.tag_bind(self.arc, "<ButtonRelease-1>", self.on_button_release)

        self.offset_x = 0
        self.offset_y = 0

    def on_button_press(self, event):
        # Сохраняем смещение между курсором и объектом
        x, y = self.canvas.coords(self.arc)[:2]
        self.offset_x = event.x - x
        self.offset_y = event.y - y

    def on_mouse_drag(self, event):
        # Перемещаем объект
        self.canvas.move(self.arc, event.x - self.offset_x - self.canvas.coords(self.arc)[0],
                         event.y - self.offset_y - self.canvas.coords(self.arc)[1])

    def on_button_release(self, event):
        # Здесь можно добавить логику, если нужно что-то сделать при отпускании кнопки
        pass

root = tk.Tk()
root.geometry('800x600')
root.title('Canvas Demo - Arc')

canvas = tk.Canvas(root, width=600, height=600, bg='white')
canvas.pack(anchor=tk.CENTER, expand=True)

draggable_arc = DraggableArc(canvas)

root.mainloop()
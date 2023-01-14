from tkinter import *
from tkinter import messagebox as mb
from math import acos, sqrt, pi

array_coords = []


def show_dot(x, y, array_coords):
    x1, y1, x2, y2 = (x - 3), (y - 3), (x + 3), (y + 3)

    colour = "#000fff000"

    canvas.create_oval(x1, y1, x2, y2, fill=colour)

    array_coords.append([x, y])


def clean_table():
    entry_x.delete(0, END)
    entry_y.delete(0, END)


def erase(array_coords):
    canvas.delete("all")
    array_coords.clear()
    result.config(stat=NORMAL)
    result.delete(0, END)
    result.config(stat=DISABLED)


def erase_triangle():
    canvas.delete('triangle')


def calculate_angle(max_coord):
    max_angle = 0

    for i in range(len(array_coords) - 2):
        j = i + 1

        while j != len(array_coords) - 1:
            ab = sqrt(
                (array_coords[i][0] - array_coords[j][0]) ** 2 + (array_coords[i][1] - array_coords[j][1]) ** 2)
            ac = sqrt(
                (array_coords[i][0] - array_coords[j + 1][0]) ** 2 + (array_coords[i][1] - array_coords[j + 1][1]) ** 2)
            bc = sqrt((array_coords[j][0] - array_coords[j + 1][0]) ** 2 + (
                    array_coords[j][1] - array_coords[j + 1][1]) ** 2)

            angle_ab = acos((bc ** 2 + ac ** 2 - ab ** 2) / (2 * bc * ac))
            angle_ac = acos((ab ** 2 + ac ** 2 - bc ** 2) / (2 * ab * ac))
            angle_bc = acos((ab ** 2 + bc ** 2 - ac ** 2) / (2 * ab * bc))

            if angle_ab * 180 / pi == 180 or angle_ac * 180 / pi == 180 or angle_bc * 180 / pi == 180:
                break

            if angle_ab > max_angle or angle_ac > max_angle or angle_bc > max_angle:
                max_angle = max(angle_ab, angle_ac, angle_bc, max_angle)
                max_coord.clear()
                max_coord.append([array_coords[i][0], array_coords[i][1]])
                max_coord.append([[array_coords[j][0], array_coords[j][1]]])
                max_coord.append([array_coords[j + 1][0], array_coords[j + 1][1]])

            j += 1

    return max_angle * 180 / pi


def show_result(res):
    result.config(stat=NORMAL)
    result.delete(0, END)
    result.insert(0, res)
    result.config(stat=DISABLED)


def on_button(event, key=3):
    global array_coords
    max_coord = []

    if key == 1:
        x = entry_x.get()
        y = entry_y.get()
        if x.isdigit() and y.isdigit():
            show_dot(int(x), int(y), array_coords)
            clean_table()
        else:
            mb.showerror("Ошибка", "Были переданы не цифры.")
            return 1
    elif key == 2:
        if len(array_coords) < 3:
            mb.showerror("Ошибка", "Количество точек меньше 3-х")
            return 1

        erase_triangle()

        res = calculate_angle(max_coord)

        if res == 0:
            mb.showerror("Ошибка", "Координаты не образуют треугольник")
            return 1

        canvas.create_polygon(*max_coord, fill="red", tag="triangle")

        show_result("{:.6f}".format(res) + "°")
    elif key == 3:
        show_dot(event.x, event.y, array_coords)
    else:
        erase(array_coords)


planimetric = Tk()
planimetric.title('Планиметрические задачи')

# Поле для рисования
canvas = Canvas(planimetric, width=600, height=920, bg='white')
canvas.bind("<Button-1>", on_button)

# Кнопки
clear = Button(planimetric, text="Стереть", width=100, command=lambda: on_button('pass', 4))
calculate = Button(planimetric, text="Посчитать", width=100, command=lambda: on_button('pass', 2))
point = Button(planimetric, text="Поставить точку", command=lambda: on_button('pass', 1))

# Текст
label_x = Label(text="x:")
label_y = Label(text="y:")

# Поле ввода
entry_x = Entry()
entry_y = Entry()
result = Entry(width=100)

# Размещение
canvas.pack(side=LEFT)
label_x.pack(anchor=N)
entry_x.pack(anchor=N)
label_y.pack(anchor=N)
entry_y.pack(anchor=N)
point.pack(anchor=N)
clear.pack(side=BOTTOM)
calculate.pack(side=BOTTOM)
result.pack(side=RIGHT)

# Настройка окна
planimetric.resizable(0, 0)
planimetric.geometry('920x700')
result.config(stat=DISABLED)

planimetric.mainloop()

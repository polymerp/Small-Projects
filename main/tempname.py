from tkinter import *
import random

class GUI:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width="800", height="600",
                        background="black")
        self.canvas.pack()

        self.bob_box = Box(self.canvas, 100, 100)
        self.bob = self.bob_box.box_id

        self.canvas.bind("<space>", self.mouse_clicked)
        self.canvas.focus_set()
        self.start_text = self.canvas.create_text(100, 100, text="Click to start",
                                        fill="red",
                                        font="Times 26 italic")
        self.box_list = []

        self.window.mainloop()

    def move_stuff(self):
        # print(canvas.coords(bob))
        self.bob_box.move()
        for box in self.box_list:
            box.move()

        self.window.after(16, self.move_stuff)

    def mouse_clicked(self, event):
        hit = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        print("DETECTED")
        if self.bob in hit:
            print("You hit bob!")
            self.bob_box.change_colour()

        else:
            print("You missed")
        if self.start_text in hit:
            self.canvas.delete(self.start_text)
            self.move_stuff()

    def new_box(self, event):
        self.box_list.append(Box(self.canvas, event.x, event.y))


class Box:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.box_id = self.canvas.create_rectangle(x, y, x+100, y+100, fill="blue")
        self.change_colour()
        self.x_vel = 4
        self.y_vel = 0

    def change_colour(self):
        self.canvas.itemconfig(self.box_id, fill=f"#{random.randint(0, 0xFFFFFF):06x}")

    def move(self):
        # print(canvas.coords(bob))
        self.canvas.move(self.box_id, self.x_vel, self.y_vel)
        if (self.canvas.coords(self.box_id)[2] > 800 or
                self.canvas.coords(self.box_id)[0] < 0):
            self.x_vel = -self.x_vel
        if (self.canvas.coords(self.box_id)[3] > 600 or
                self.canvas.coords(self.box_id)[1] < 0):
            self.y_vel = -self.y_vel
        else:
            self.y_vel += 1

        # canvas.create_rectangle(*canvas.coords(bob))


GUI()

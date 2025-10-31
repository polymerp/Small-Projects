from tkinter import Frame, Tk, StringVar, Label


root = Tk()
var = StringVar()
a_label = Label(root,textvariable = var ).pack()

history = []
def keyup(e):
    print(e)
    if  e.keycode in history :
        history.pop(history.index(e.keycode))

        var.set(str(history))

def keydown(e):
    print(e)
    if not e.keycode in history :
        history.append(e.keycode)
        var.set(str(history))

frame = Frame(root, width=200, height=200)
frame.bind("<KeyPress>", keydown)
frame.bind("<KeyRelease>", keyup)
frame.pack()
frame.focus_set()
root.mainloop()
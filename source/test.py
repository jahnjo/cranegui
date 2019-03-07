from Tkinter import *
from PIL import ImageTk, Image


master = Tk()
canvas = Canvas(master,width=200,height=200)
canvas.pack()

test = [[75,75],[125,75],[125,125],[75,125]]
canvas.create_polygon(test, fill='white', outline='black')

L = ImageTk.PhotoImage(Image.open("L.png"))
canvas.create_image((100,100),image=L)

master.mainloop()
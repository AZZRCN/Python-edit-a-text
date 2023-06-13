from tkinter import Button
from tkinter import Tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL.ImageTk import PhotoImage
from tkinter import Scale
from tkinter import Toplevel
root = Tk()
img = ""
text = ScrolledText(master=root,width=10,height=10)
text.grid(column=2,row=0,rowspan=2)
def size():
    top = Toplevel(master=root)
    def hup():text.configure(height=int(text.winfo_height()/13) + 1)
    def hdown():text.configure(height=int(text.winfo_height()/13) - 1)
    def wup():text.configure(width=int(text.winfo_width()/7) + 1)
    def wdown():text.configure(width=int(text.winfo_width()/7) - 1)
    Button(master=top,text="↑",command=hdown).grid(column=0,row=0)
    Button(master=top,text="←",command=wdown).grid(column=2,row=0)
    Button(master=top,text="↓",command=hup).grid(column=0,row=1)
    Button(master=top,text="→",command=wup).grid(column=2,row=1)
    x = Scale(master=top,from_=1,to=100,tickinterval=5,length=200)
    x.grid(column=1,row=0,rowspan=2)
    y = Scale(master=top,from_=1,to=100,tickinterval=5,length=200)
    y.grid(column=3,row=0,rowspan=2)
    def csize():
        text.configure(width=y.get(),height=x.get())
    Button(master=top,text="生效",command=csize).grid(row = 3,column=0,columnspan=4)
def ctp():
    global img
    img=PhotoImage(Image.open(askopenfilename(title="选择文件", filetypes=(("png", "*.png"),))))
    text.image_create("insert",image=img)
Button(master=root,text="℗",command=ctp).grid(column=0,row=1,sticky='nw')
Button(master=root,text="Size",command=size).grid(column=0,row=0,sticky='nw')
root.mainloop()

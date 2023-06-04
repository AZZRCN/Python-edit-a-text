import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import windnd
import qrcode
import os
from time import localtime
import pyperclip
import time
from tkinter.messagebox import showerror
root = tk.Tk()
def wait(a: float):
    time.sleep(a)
path = ""
def editfile():
    global path
    top = tk.Toplevel()
    top.title("编辑")
    text = tk.Text(master=top)
    text.grid(column=0, row=1)
    if (path != ""):
        try:
            text.insert('1.0', str(open(path, encoding='utf-8').read()))
        except BaseException:
            text.insert('1.0', str(open(path, encoding='gbk').read()))
    def 保存():
        global path
        if (path == ""):
            path = filedialog.asksaveasfilename()
        else:
            filenewpath = path
        open(filenewpath, "w").write(text.get('1.0', tk.END))

    def 新建():
        nonlocal text
        global path
        path = ""
        text.destroy()
        text = tk.Text(master=top)
        text.grid(column=0, row=1, columnspan=3)

    def 退出():
        root.quit()

    def 取消():
        top.destroy()

    def 制作二维码():
        qrcode_info = tk.Toplevel()
        qrcode_info.title("二维码，仅限文字")
        def Esc(event):
            if (event.keycode == 27):  # Esc
                qrcode_info.destroy()
        qrcode_info.bind("<Key>", Esc)
        tk.Label(master=qrcode_info, text="二维码大小:").grid(column=3, row=3)
        版本 = tk.Entry(master=qrcode_info, width=2)
        版本.grid(column=4, row=3)
        版本.insert('0', "1")
        tk.Label(master=qrcode_info, text="纠错能力:").grid(column=5, row=3)
        纠错 = tk.Entry(master=qrcode_info, width=1)
        纠错.grid(column=6, row=3)
        纠错.insert('0', "1~4")
        tk.Label(master=qrcode_info, text="像素大小:").grid(column=3, row=4)
        单像素大小 = tk.Entry(master=qrcode_info, width=2)
        单像素大小.grid(column=4, row=4)
        单像素大小.insert('0', "1")
        border_label = tk.Label(master=qrcode_info, text="边框像素数:")
        border_label.grid(column=5, row=4)
        边框 = tk.Entry(master=qrcode_info, width=2)
        边框.grid(column=6, row=4)
        边框.insert('0', "1")
        infromation = tk.Label(master=qrcode_info, text="信息:")
        infromation.grid(column=3, row=5)
        信息 = tk.Entry(master=qrcode_info)
        信息.grid(column=4, row=5, columnspan=3)
        def use_info():
            nonlocal text
            nonlocal 信息
            信息.delete(0, tk.END)
            信息.insert(0, text.get('1.0', tk.END))
        文本 = tk.Button(master=qrcode_info, text="用文本内信息", command=use_info)
        文本.grid(column=5, row=7)
        def make():
            nonlocal 版本
            nonlocal 纠错
            nonlocal 单像素大小
            nonlocal 边框
            nonlocal 信息
            if (纠错.get() == "" or 版本.get() == "" or 单像素大小.get() == "" or 信息 == ""):
                messagebox.showerror("失败!", "有东西是空的!")
                return
            qr = qrcode.QRCode(version=int(版本.get()), error_correction=int(纠错.get())  # e
                               , box_size=int(
                单像素大小.get()), border=int(边框.get()))
            qr.add_data(信息.get())
            qr.make(fit=True)
            qr = qr.make_image()
            qr.show()
            if messagebox.askokcancel():
                pyperclip.copy(qr)
            del qr
        制作 = tk.Button(master=qrcode_info, text="制作", command=make)
        制作.grid(column=3, row=7)

    def 打开():
        nonlocal text
        global path
        old_path = path
        path = filedialog.askopenfilename(
            title="Select txt file", filetypes=(("txt files", "*.txt"),))
        if ("" != path != old_path):
            text.destroy()
            text = tk.Text(master=top)
            text.grid(column=0, row=1, columnspan=3)
            try:
                text.insert('1.0', str(open(path, encoding="utf-8").read()))
            except BaseException:
                text.insert('1.0', str(open(path, encoding="gbk").read()))
        else:
            messagebox.showerror("错了!", "选个真的txt")

    def get_time():
        t = localtime()
        t = str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + " " + str(t.tm_year) + "\\" + str(t.tm_mon) + "\\" + str(t.tm_mday)
        text.insert("insert",t)
    # def 集成调用():
    menubar = tk.Menu(top)  # 菜单
    top['menu'] = menubar  # 顶级窗口能使用菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    test_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    menubar.add_cascade(label="测试", menu=test_menu)
    file_menu.add_command(label="新建", command=新建)
    file_menu.add_command(label="打开", command=打开)
    file_menu.add_command(label="保存", command=保存)
    file_menu.add_command(label="取消", command=取消)
    file_menu.add_command(label="退出", command=退出)
    file_menu.add_command(label="生成二维码", command=制作二维码)
    file_menu.add_command(label="插入时间", command=get_time)
    # 为列表中添加内容


def dropfile(filename):
    global path
    path = filename[0].decode('gbk')


windnd.hook_dropfiles(root, func=dropfile)
tk.Button(master=root, text="编辑", command=editfile).grid(column=4, row=3)

root.title("AZZR文本编辑器v1.0.0")  # 标题
# autopytoexe无法使用
# root.iconbitmap("MC.ico")  # 图标
# root.iconphoto(True, tk.PhotoImage(file="./MC.png"))
root.mainloop()

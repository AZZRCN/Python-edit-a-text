import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import windnd
import qrcode
from time import localtime
root = tk.Tk()
path = ""
def editfile():
    global path
    top = tk.Toplevel()
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
        open(path, "w").write(text.get('1.0', tk.END))
    def 新建():
        global path
        path = ""
        text.delete('1.0','END')
    def 退出():
        root.quit()
    def 取消更改():
        top.destroy()
    def 制作二维码():
        qrcode_info = tk.Toplevel()
        信息 = tk.Entry(master=qrcode_info)
        信息.insert('0',"请输入信息")
        信息.grid(column=4, row=5, columnspan=3)
        def use_info():
            nonlocal text
            nonlocal 信息
            信息.delete(0, tk.END)
            信息.insert(0, text.get('1.0', tk.END))
        文本 = tk.Button(master=qrcode_info, text="用文本内信息", command=use_info)
        文本.grid(column=5, row=7)
        def make():
            nonlocal 信息
            qr = qrcode.QRCode(version=1, error_correction=1, box_size=1, border=1)
            qr.add_data(信息.get())
            qr.make(fit=True)
            qr = qr.make_image()
            qr.show()
            if not messagebox.askokcancel("是否保留?","确定表示保留,反之删除"):
                del qr
        制作 = tk.Button(master=qrcode_info, text="制作", command=make)
        制作.grid(column=3, row=7)
    def 打开():
        global path
        path = filedialog.askopenfilename(
            title="Select txt file", filetypes=(("txt files", "*.txt"),))
        if ("" != path):
            text.delete('0','END')
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
    menubar = tk.Menu(top)  # 菜单
    top['menu'] = menubar  # 顶级窗口能使用菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    test_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    menubar.add_cascade(label="测试", menu=test_menu)
    file_menu.add_command(label="新建", command=新建)
    file_menu.add_command(label="打开", command=打开)
    file_menu.add_command(label="保存", command=保存)
    file_menu.add_command(label="取消更改", command=取消更改)
    file_menu.add_command(label="退出", command=退出)
    file_menu.add_command(label="生成二维码", command=制作二维码)
    file_menu.add_command(label="插入时间", command=get_time)
def dropfile(filename):
    global path
    path = filename[0].decode('gbk')
windnd.hook_dropfiles(root, func=dropfile)
tk.Button(master=root, text="编辑", command=editfile).grid(column=4, row=3)
root.title("AZZR文本编辑器v1.0.0")
root.mainloop()
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from windnd import hook_dropfiles
import qrcode
from time import localtime
import base64
root = tk.Tk()
path = ""


def editfile():
    print(root.winfo_width(), root.winfo_height())
    global path
    top = tk.Toplevel(root)
    text = tk.Text(master=top)
    text.grid(column=0, row=1)
    # 废弃:与屏幕缩放有关(设置)
    # def textresize(event):
    #    text.configure(width=int(event.width*0.8))
    #    print(event.width,event.height)
    # top.bind('<Configure>',textresize)
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
        text.delete('1.0', 'end')

    def 退出():
        top.destroy()

    def 取消更改():
        text.delete('1.0', 'end')
        text.insert('1.0', open(path).read())

    def 制作二维码():
        qrcode_info = tk.Toplevel(top)
        信息 = tk.Entry(master=qrcode_info)
        信息.grid(column=4, row=5, columnspan=3)

        def use_info():
            nonlocal text
            nonlocal 信息
            信息.delete(0, tk.END)
            信息.insert(0, text.get('1.0', tk.END))

        def make():
            qr = qrcode.QRCode(version=1, error_correction=1,
                               box_size=1, border=1)
            qr.add_data(信息.get())
            qr.make(fit=True)
            qr.make_image().show()
            if not messagebox.askokcancel("是否保留?", "确定表示保留,反之删除"):
                del qr
        tk.Button(master=qrcode_info, text="制作",
                  command=make).grid(column=3, row=7)

    def 打开():
        global path
        path = filedialog.askopenfilename(
            title="Select txt file", filetypes=(("txt files", "*.txt"),))
        if ("" != path):
            text.delete('1.0', 'end')
            try:
                text.insert('1.0', str(open(path, encoding="utf-8").read()))
            except BaseException:
                text.insert('1.0', str(open(path, encoding="gbk").read()))

    def get_time():
        t = localtime()
        text.insert("insert", (str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(
            t.tm_sec) + " " + str(t.tm_year) + "/" + str(t.tm_mon) + "/" + str(t.tm_mday)))

    def base64edcode():
        b64edcode = tk.Toplevel(top)
        信息 = tk.Text(master=b64edcode)
        信息.grid(column=4, row=5, columnspan=3)
        def use_info():
            nonlocal text
            nonlocal 信息
            信息.delete('1.0','end')
            信息.insert('1.0', text.get('1.0', tk.END))
        def b6e():
            temp = base64.b64encode(信息.get('1.0','end').encode(encoding='utf-8'))
            信息.delete('1.0','end')
            信息.insert('1.0', temp)
            del temp
        def b6d():
            temp = base64.b64decode(信息.get('1.0','end'))
            信息.delete('1.0','end')
            信息.insert('1.0', temp.decode('utf8'))
            del temp
        tk.Button(master=b64edcode, text="用文本内信息",command=use_info).grid(column=5, row=7)
        tk.Button(master=b64edcode, text="编码",command=b6e).grid(column=4, row=7)
        tk.Button(master=b64edcode, text="解码",command=b6d).grid(column=6, row=7)
        
    menubar = tk.Menu(top)  # 菜单
    top['menu'] = menubar  # 顶级窗口能使用菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    test_menu = tk.Menu(menubar, tearoff=0)
    final_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    menubar.add_cascade(label="测试", menu=test_menu)
    menubar.add_cascade(label="完结-功能", menu=final_menu)
    file_menu.add_command(label="新建", command=新建)
    file_menu.add_command(label="打开", command=打开)
    file_menu.add_command(label="保存", command=保存)
    file_menu.add_command(label="取消更改", command=取消更改)
    file_menu.add_command(label="退出", command=退出)
    file_menu.add_command(label="生成二维码", command=制作二维码)
    file_menu.add_command(label="插入时间", command=get_time)
    final_menu.add_command(label="编->base64<-解", command=base64edcode)


def dropfile(filename):
    global path
    path = filename[0].decode('gbk')


hook_dropfiles(root, func=dropfile)
tk.Button(master=root, text="编辑", command=editfile).grid(column=4, row=3)
root.mainloop()

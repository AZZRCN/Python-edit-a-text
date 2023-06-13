from windnd import hook_dropfiles
from base64 import b64decode
from base64 import b64encode
from time import localtime
from qrcode import QRCode
from hashlib import new
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesnocancel
from tkinter.messagebox import askokcancel
from tkinter.scrolledtext import ScrolledText
from pyperclip import copy
from tkinter import StringVar
from tkinter import Toplevel
from tkinter import Button
from tkinter import Entry
from tkinter import OptionMenu
from tkinter import Text
from tkinter import Menu
from tkinter import Tk
from math import sqrt
root = Tk()
path = ""
def useinfo(from_:Entry|Text|ScrolledText,
            to_:Entry|Text|ScrolledText,
            from_index:tuple[str]|None,
            to_index:str|int) -> None:
    """
    ==========轻型重量函数==========\n
    #所有定义皆为此函数特有\n
    from_,to_应为具有get()和insert()属性的控件\n
    Entry:from_index是None, to_index是'x'(str)|x(int)\n
    Text|ScrolledText:from_index是('x.x','x.x')(tuple,str,两个), to_index是'x.x'(str)
    """
    if(type(from_) == Entry and (from_index[0].split('.') > 1 or len(from_index[1].split('.')) > 1)):#小大
        print("E1")
        return
    if((type(from_) == Text or type(from_) == ScrolledText) and (len(from_index[0].split('.')) == 1 or (from_index[1] != 'end' and len(from_index[1].split('.')) == 1))):#大小
        print("E2")
        return
    if(type(to_) == Entry and len(to_index.split('.')) > 1):#小大
        print("E3")
        return
    if((type(to_) == Text or type(to_) == ScrolledText) and len(to_index.split('.')) == 1):#大小
        print("E4")
        return
    temp = ""
    if(type(from_) == Text or type(from_) == ScrolledText):
        temp = from_.get(from_index[0], from_index[1])
    elif(type(from_) == Entry):
        temp = from_.get()
    if(type(to_) == Text or type(to_) == ScrolledText):
        to_.delete('1.0','end')
        to_.insert(to_index,temp)
    elif(type(to_) == Entry):
        to_.delete('0','end')
        to_.insert(str(to_index),temp)

def editfile():
    global path
    top = Toplevel(root)
    text = ScrolledText(master=top)
    text.grid(column=0, row=1)
    if (path != ""):
        try:
            text.insert('1.0', str(open(path, encoding='utf-8').read()))
        except BaseException:
            text.insert('1.0', str(open(path, encoding='gbk').read()))

    def 保存():
        global path
        if (path == ""):
            path = asksaveasfilename()
        open(path, "w").write(text.get('1.0', 'end'))

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
        qrcode_info = Toplevel(top)
        信息 = Entry(master=qrcode_info)
        信息.grid(column=4, row=5, columnspan=3)
        def make():
            qr = QRCode(version=1, error_correction=1, box_size=1, border=1)
            qr.add_data(信息.get())
            qr.make(fit=True)
            qr.make_image().show()
        Button(master=qrcode_info, text="制作",command=make).grid(column=3, row=7)
        Button(master=qrcode_info, text="引用文本信息",command=lambda:useinfo(text,信息,('1.0','end'),'0')).grid(column=4, row=7)

    def 打开():
        global path
        newpath = askopenfilename(title="选择文件", filetypes=(("所有种类", "*.*"),))
        if ("" != newpath):
            text.delete('1.0', 'end')
            path = newpath
            try:
                text.insert('1.0', str(open(path, encoding="utf-8").read()))
            except BaseException:
                text.insert('1.0', str(open(path, encoding="gbk").read()))

    def 获取时间():
        t = localtime()
        text.insert("insert", (str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(
            t.tm_sec) + " " + str(t.tm_year) + "/" + str(t.tm_mon) + "/" + str(t.tm_mday)))
    
    def b64编码解码():
        b64edcode = Toplevel(top)
        信息 = ScrolledText(master=b64edcode)
        信息.grid(column=4, row=5, columnspan=3)
        def b6(code):
            if (code):
                temp = b64encode(信息.get('1.0', 'end').encode(
                    encoding='utf8')).decode('utf8')
            else:
                temp = b64decode(信息.get('1.0', 'end')).decode('utf8')
            信息.delete('1.0', 'end')
            信息.insert('1.0', temp)
            del temp
        Button(master=b64edcode, text="用文本内信息",
               command=lambda:useinfo(text,信息,('1.0','end'),'1.0')).grid(column=5, row=7)
        Button(master=b64edcode, text="编码",
               command=lambda: b6(1)).grid(column=4, row=7)
        Button(master=b64edcode, text="解码",
               command=lambda: b6(0)).grid(column=6, row=7)
    def 计算哈希():
        hash_top = Toplevel(master=top)
        string = StringVar()
        hlist = OptionMenu(hash_top,string,'sha1','sha224','sha256','sha384','sha512','md5')
        string.set('md5')
        hlist.grid(column=0,row=0)
        信息 = ScrolledText(master=hash_top)
        信息.grid(column=1,row=0,rowspan=3)
        Button(master=hash_top,text="引用",command=lambda:useinfo(text,信息,('1.0','end'),'1.0')).grid(column=0,row=2)
        def make():
            temp = Toplevel(master=hash_top)
            t = new(string.get())
            t.update(信息.get('1.0','end').encode("gbk"))
            t = t.hexdigest()
            text = ScrolledText(master=temp,width=int(len(t)/4),height=4)
            text.insert('1.0',t)
            text.grid(column=1,row=1)
            Button(master=temp,text="复制",command=lambda:copy(t)).grid(column=1,row=0)
        makebutton = Button(master=hash_top,text="制作",command=make)
        makebutton.grid(column=0,row=1)
        
        
    menubar = Menu(top)  # 菜单
    top['menu'] = menubar  # 顶级窗口能使用菜单
    file_menu = Menu(menubar, tearoff=0)
    test_menu = Menu(menubar, tearoff=0)
    tool_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    menubar.add_cascade(label="测试", menu=test_menu)
    menubar.add_cascade(label="完结-功能", menu=tool_menu)
    file_menu.add_command(label="新建", command=新建)
    file_menu.add_command(label="打开", command=打开)
    file_menu.add_command(label="保存", command=保存)
    file_menu.add_command(label="取消更改", command=取消更改)
    file_menu.add_command(label="退出", command=退出)
    file_menu.add_command(label="生成二维码", command=制作二维码)
    file_menu.add_command(label="插入时间", command=获取时间)
    tool_menu.add_command(label="编->base64<-解", command=b64编码解码)
    tool_menu.add_command(label="哈希", command=计算哈希)


def dropfile(filename):
    global path
    path = filename[0].decode('gbk')


hook_dropfiles(root, func=dropfile)
Button(master=root, text="编辑", command=editfile).grid(column=4, row=3)
root.mainloop()

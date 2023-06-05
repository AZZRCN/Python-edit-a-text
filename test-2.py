
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
import tkinter as tk
 
window = tk.Tk()
window.title("窗口缩放")
 
#设置窗口大小，并将窗口放置在屏幕中央
width = 400
height = 400
g_screenwidth = window.winfo_screenwidth()
g_screenheight = window.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (g_screenwidth-width)/2, (g_screenheight-height)/2)
window.geometry(alignstr)
 
#设置窗口背景为白色
window.config(bg='white')
#设置窗口最小尺寸
window.minsize(width, height)
 
#采用frame上添加Text方式，可根据窗口进行像素级缩放
frame1 = tk.Frame(window, width=400, height=400)
frame1.pack_propagate(0)
frame1.place(x=0, y=0)
 
text1 = tk.Text(frame1)
text1.pack(fill="both", expand="yes") 
save_width = width
save_height = height
 
#窗口尺寸调整处理函数
def WindowResize(event):
	global save_width
	global save_height
	
	new_width = window.winfo_width()
	new_height = window.winfo_height()
	
	if new_width == 1 and new_height == 1:
		return
	if save_width != new_width or save_height != new_height:
		frame1.config(width=new_width, height=new_height)
	save_width = new_width
	save_height = new_height
 
#绑定窗口变动事件
window.bind('<Configure>', WindowResize)
 
window.mainloop()
import tkinter as tk
config = open("config.txt").read().split("\n")
print(config)
cnt = 0
config_dict=[]
for i in config:
    config_dict.append(i.split(":"))
    print(config_dict[cnt])
    cnt += 1
a = tk.Tk()
b = tk.Label(master=a,text=config_dict)
b.configure(text=config_dict)
b.grid(column=1,row=1)
a.mainloop()
config = open("config.txt").read().split("\n")
print(config)
cnt = 0
config_dict=[]
for i in config:
    config_dict.append(i.split("=\""))
    print(config_dict[cnt])
    cnt += 1
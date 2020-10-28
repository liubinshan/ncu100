a = "http://100.ncu.edu.cn/xyfc/xyhd/index.htm"
a = a[:-4] + "{0:s}".format(str(1)) + a[-4:]
print(a)
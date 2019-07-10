import os

# 视频类型分类
def getVideoFiles(request):
    path = "F:/Pycharm/PyCharm 2017.3.7/CookiesAndSessions/app/static/upfile"  # 设置路径
    dirs = os.listdir(path)  # 获取指定路径下的文件
    for i in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == ".mp4":  # 筛选mp4文件
            print(i)
        if os.path.splitext(i)[1] == ".flv":  # 筛选mp4文件
            print(i)
        if os.path.splitext(i)[1] == ".rm":  # 筛选mp4文件
            print(i)
        if os.path.splitext(i)[1] == ".rmvb":  # 筛选mp4文件
            print(i)
        if os.path.splitext(i)[1] == ".mov":  # 筛选mp4文
            print(i)
    return 1        


# 文本类型分类
def getWordFiles(request):
    path = "F:/Pycharm/PyCharm 2017.3.7/CookiesAndSessions/app/static/upfile"  # 设置路径
    dirs = os.listdir(path)  # 获取指定路径下的文件
    for i in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == ".txt":  # 筛选txt文件
            print(i)
        if os.path.splitext(i)[1] == ".doc":  # 筛选txt文件
            print(i)
        if os.path.splitext(i)[1] == ".docx":  # 筛选txt文件
            print(i)
        if os.path.splitext(i)[1] == ".xls":  # 筛选txt文件
            print(i)
    return 2

# 图片类型分类
def getPicFiles(request):
    path = "F:/Pycharm/PyCharm 2017.3.7/CookiesAndSessions/app/static/upfile"  # 设置路径
    dirs = os.listdir(path)  # 获取指定路径下的文件
    for i in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == ".jpg":  # 筛选csv文件
            print(i)
        if os.path.splitext(i)[1] == ".jpeg":  # 筛选csv文件
            print(i)
        if os.path.splitext(i)[1] == ".gif":  # 筛选csv文件
            print(i)
        if os.path.splitext(i)[1] == ".png":  # 筛选csv文件
            print(i)
        if os.path.splitext(i)[1] == ".bmp":  # 筛选csv文件
            print(i)
    return 3         



'''
def getFileName(path):   
    files = os.listdir(path)
    for i in files:
        if os.path.splitext(i)[1] == ".mp4":
            print i

int main()
    path2 = 'F:/Pycharm/PyCharm 2017.3.7/CookiesAndSessions/app/static/upfile'
    getFileName(path2)
'''
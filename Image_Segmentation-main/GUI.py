import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import huidufenge as h
from KMeans import K_means

image_path=None
answer_path=None

# 创建Tkinter主窗口
root = tk.Tk()
root.title("图像分割应用程序")
root.geometry('1400x750')

# 设置背景图片
bg_image_path = "B.jpg"
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# 创建一个Canvas组件
#canvas = tk.Canvas(root, bg="white", width=1000, height=1000)
#canvas.pack(pady=10)

# 函数：选择并展示图片
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        # 打开并显示图片
        global  image_path
        image_path=file_path
        image = Image.open(file_path)
        image.thumbnail((1000, 1000))  # 缩小图片以适应显示区域
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)

        #canvas.config(scrollregion=(0, 0, image.width(), image.height()))
        #canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        image_label.image = photo # 保持引用，避免垃圾回收

def zoom(event):
    scale = 1.0
    if event.delta > 0:
        scale = 1.1
    else:
        scale = 0.9
    #canvas.scale("all", event.x, event.y, scale, scale)

def show_image(process_time):
    global answer_path
    if answer_path:
        # 创建一个新的子窗口
        sub_window = tk.Toplevel(root)
        sub_window.title("分割后的图像")

        # 在子窗口中显示分割后的图像
        image = Image.open(answer_path)
        image.thumbnail((1000, 1000))
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(sub_window, image=photo)
        image_label.image = photo
        image_label.pack(pady=10)

        #显示时间
        time_label=tk.Label(sub_window,text=f"处理时间：{process_time:.2f}秒")
        time_label.pack(pady=5)

def process_image():
    global image_path,answer_path
    if image_path:
        src = cv2.imread(image_path)
        width = src.shape[1]
        height = src.shape[0]
        count=width*height
        s=time.time()
        # 打开并显示图片
        if count<1e6:
            answer = h.Graph(image_path=image_path)
            answer_path=image_path.split('.')[0]+'result.png'
            cv2.imwrite(answer_path,answer.segmented_image)
        else:
            answer_path = K_means(image_path)
        e=time.time()
        precess_time=e-s
        show_image(precess_time)

# 绑定鼠标滚轮事件到Canvas
#canvas.bind("<MouseWheel>", zoom)

# 创建标题标签
title_label = tk.Label(root, text="图像分割", font=("Helvetica", 20))
title_label.pack(pady=10)

# 创建展示图片的标签
image_label = tk.Label(root)
image_label.pack(pady=10)

# 创建导入图片按钮
import_button = tk.Button(root, text="导入图片", command=open_image)
import_button.pack(pady=5)

# 创建分割图片按钮
process_button= tk.Button(root,text='开始分析',command=process_image)
process_button.pack(pady=5)

# 启动Tkinter主循环
root.mainloop()

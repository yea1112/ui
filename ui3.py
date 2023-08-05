import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os

def load_image(image_path, width):
    img = Image.open(image_path)
    img.thumbnail((width, width))
    return ImageTk.PhotoImage(img)

def create_label(image, filename):
    label_frame = tk.Frame(frame_labels)
    label_frame.grid(padx=5, pady=5)

    label = tk.Label(label_frame, image=image)
    label.image = image
    label.pack()

    # 顯示檔名
    filename_label = tk.Label(label_frame, text=filename)
    filename_label.pack()

    # 添加對應的刪除按鈕，並綁定刪除函數
    delete_button = tk.Button(label_frame, text="刪除", command=lambda: delete_label(label_frame))
    delete_button.pack()

    return label_frame, label, delete_button

def generate_label(image_path):
    global image_width, image
    filename = os.path.basename(image_path)
    image = load_image(image_path, image_width)
    label_frame, _, _ = create_label(image, filename)
    labels.append((label_frame, image, filename))

def delete_all_labels():
    global labels
    for label_frame, _, _ in labels:
        label_frame.grid_forget()
    labels = []

def delete_label(label_frame):
    global labels
    for i, (frm, img, filename) in enumerate(labels):
        if frm == label_frame:
            frm.grid_forget()
            frm.destroy()  # 徹底刪除Label及其內容
            labels.pop(i)
            break

    # 重新排列剩餘的 Label
    for i, (frm, img) in enumerate(labels):
        row = i // 5
        col = i % 5
        frm.grid(row=row, column=col, padx=5, pady=5)

def drop(event):
    # 當檔案被拖放至視窗時，處理拖放的檔案
    files = event.data.split() 
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif')):
            generate_label(file)

# 創建 Tkinter 頂級視窗
win = TkinterDnD.Tk()
win.title("uPrint 影像產生器")
win.geometry("1000x700")  # 設定視窗大小

# 設定拖放區域
canvas = tk.Canvas(win, width=900, height=100, bg="#FFFFFF")
canvas.pack(pady=20)

# 在Canvas內顯示文字
canvas.create_text(450, 50, text="拖放影像檔案至此", font=('Arial', 16))


# 添加一個 Frame 用於放置 labels
frame_labels = tk.Frame(win)
frame_labels.pack()

# 加載預設影像
image_path = os.path.abspath("output/cmyk_noicc-srgb.tif")
image_width = 145
image = load_image(image_path, image_width)

# 初始化 labels 列表
labels = []

# 設定拖放區域接收檔案的事件
canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<Drop>>', drop)

def update_label_layout():
    global image_width, labels
    window_width = win.winfo_width()
    num_cols = window_width // (image_width + 10)  # 每個影像寬度+間距
    num_labels = len(labels)
    #print(f"Number of labels is {num_labels}")
    for i, (frm, img, filename) in enumerate(labels):
        row = i // num_cols
        col = i % num_cols
        frm.grid(row=row, column=col, padx=5, pady=5)

# 監聽視窗大小變化，更新影像排列
win.bind('<Configure>', lambda event: update_label_layout())


win.mainloop()


#備份最終穩定版
#穩定版1
#穩定版1.1 加上調整視窗大小會row col會跟著改變
#穩定版1.2 加上顯示檔名
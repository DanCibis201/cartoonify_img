import numpy as np
import tkinter as tk 
from tkinter import *
import easygui  
import cv2  
import matplotlib.pyplot as plt
import os  
import sys  


top = tk.Tk()
top.geometry('400x300')
top.title('Cartoonify Image Application!')
top.configure(background='#856ff8')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))


def upload():
    image_path = easygui.fileopenbox()
    cartoonify(image_path)

def close():
    top.destroy()


def cartoonify(image_path):

    imaginea1 = cv2.imread(image_path)
    imaginea1 = cv2.cvtColor(imaginea1, cv2.COLOR_BGR2RGB)

    imaginea2 = imaginea1.reshape((-1, 3))
    imaginea2 = np.float32(imaginea2)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 10
    attempts = 10
    ret, label, center = cv2.kmeans(imaginea2, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((imaginea1.shape)) 
    

    if imaginea1 is None:
        print("Error! Couldn't read from the image path!")
        sys.exit()
    resize_img1 = cv2.resize(imaginea1, (960, 540))
    # plt.imshow(resize_img1, cmap='gray')

    grayscale_img = cv2.cvtColor(imaginea1, cv2.COLOR_BGR2GRAY)
    resize_img2 = cv2.resize(grayscale_img, (960, 540))
    # plt.imshow(resize_img2, cmap="gray")

    smooth_grayscale_image = cv2.medianBlur(grayscale_img, 5)
    resize_img3 = cv2.resize(smooth_grayscale_image, (960, 540))
    #  plt.imshow(resize_img3, cmap='gray')


    get_edge = cv2.adaptiveThreshold(smooth_grayscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    resize_img4 = cv2.resize(get_edge, (960, 540))
    #plt.imshow(resize_img4, cmap='gray')

    color_image = cv2.bilateralFilter(imaginea1, 9, 300, 300)
    resize_img5 = cv2.resize(color_image, (960, 540))
    # plt.imshow(resize_img5, cmap="gray")


    cartoon_image = cv2.bitwise_and(color_image, color_image, mask = get_edge)
    resize_img6 = cv2.resize(cartoon_image, (960, 540))
    # plt.imshow(resize_img6, cmap='gray')

    images = [resize_img1, resize_img2, resize_img3, resize_img4, resize_img5, resize_img6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                            gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    savel = Button(top, text="Press to Save", command= save(resize_img6, image_path), padx=30, pady=5)
    savel.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    savel.pack(side=TOP, pady=50)


    plt.show()


def save(resize_img6, image_path):
    new_name = "Cartoonified_Image"
    path1 = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(resize_img6, cv2.COLOR_RGB2BGR))
    I = "Imaginea a fost salvată cu numele " + new_name + " în " + path
    tk.messagebox.showinfo(title=None, message=I)

upload = Button(top, text="Press to Cartoonify", command = upload, padx=10, pady=5)
upload.configure(background="#374256", foreground="wheat", font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=20)

close = Button(top, text ="Press to Close", command = close, padx = 10, pady = 5 )
close.configure(background="#374256", foreground="wheat", font=('calibri', 10, 'bold'))
close.pack(side=TOP, pady=60)

top.mainloop()
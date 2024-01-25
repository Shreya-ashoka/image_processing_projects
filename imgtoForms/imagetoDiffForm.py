import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import tkinter as tk
from tkinter import messagebox, Button, filedialog

root = tk.Tk()
root.geometry('950x700')
root.title('Choose to convert!')
root.configure(background='light green')
label = tk.Label(root, background="black", font=("arial", 30, "bold"))


def u():
    Imagepath = filedialog.askopenfilename()
    if Imagepath:
        C(Imagepath)


def C(Imagepath):
    originalImage = cv2.imread(Imagepath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

    if originalImage is None:
        print("Could not open or find the image.")
        sys.exit()

    R_1 = cv2.resize(originalImage, (930, 510))
    greyscale = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
    R_2 = cv2.resize(originalImage, (930, 510))
    smoothgray = cv2.medianBlur(greyscale, 5)
    R_3 = cv2.resize(smoothgray, (930, 510))

    # Convert smoothgray to grayscale (CV_8UC1)
    smoothgray = cv2.cvtColor(smoothgray, cv2.COLOR_RGB2GRAY)

    getedge = cv2.adaptiveThreshold(smoothgray, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    R_4 = cv2.resize(getedge, (930, 510))

    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)
    R_5 = cv2.resize(colorImage, (930, 510))

    cartoonImage = cv2.bitwise_and(colorImage, colorImage,
                                   mask=getedge)
    R_6 = cv2.resize(cartoonImage, (930, 510))

    images = [R_1, R_2, R_3, R_4, R_5, R_6]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw=
                             {'xticks': [], 'yticks': []}, gridspec_kw=dict(
        hspace=0.1, wspace=0.1
    ))

    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    save1 = Button(root, text="Save cartoon image", command=lambda: save(R_6, Imagepath))
    save1.configure(background="red", foreground="yellow", font=('arial', 20, "bold"))
    save1.pack(side=tk.TOP, pady=20)


def save(Resized6, Imagepath):
    newname = "converted Image"
    path1 = os.path.dirname(Imagepath)
    extension = os.path.splitext(Imagepath)[1]
    path = os.path.join(path1, newname + extension)

    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_RGB2BGR))

    I = "SAVED IMAGE is " + newname + " at " + path
    messagebox.showinfo(title=None, message=I)


a = Button(root, text="Conversion of image", command=u, padx=15, pady=10)
a.configure(background="black", foreground="white", font=("arial", 30, "bold"))
a.pack(side=tk.TOP, pady=20)

root.mainloop()

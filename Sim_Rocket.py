# GUI
# Author : Henri Faure
# Date : 4 April 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import keyboard
import numpy as np

# Ouvre une fenetre
fenetre = Tk()
fenetre.grid()
fenetre.title('Simulator EPFL_Rocket')
fenetre.call('wm', 'iconphoto', fenetre._w, PhotoImage(file='ERT_logo.png'))
fenetre.configure(bg="light goldenrod yellow")
Logo_tmp = Image.open('ERT_logo.png')
Logo_tmp = Logo_tmp.resize((100, 70), Image.ANTIALIAS)
Logo = ImageTk.PhotoImage(Logo_tmp)
Canvas1 = Canvas(fenetre)
Canvas1.create_image(100/2, 70/2, image=Logo)
Canvas1.config(bg="white", width=100, height=70)
Canvas1.pack(side=TOP, expand=False, fill=NONE)

class make_list(Listbox):

    def click_button(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        return value

    def build_main_window(self, liste):
        self.build_listbox(liste)

    def build_listbox(self, liste):
        scrollbar = Scrollbar(fenetre)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(fenetre, width=5, height=2, yscrollcommand=scrollbar.set)
        listbox.bind('<<ListboxSelect>>', self.click_button)
        for item in liste:
            listbox.insert(END, item)
        scrollbar.config(command=listbox.yview)
        listbox.pack(side=LEFT, fill=None, expand=True)
        return

def ChooseMotor():
    liste_m = np.array(["Solid", "Hybrid", "Liquid"])
    start = make_list(fenetre)
    start.build_main_window(liste_m)
    print()

def ChooseEnvironment():
    Liste_e = np.array(["Cernier", "Zurich", "Mexique"])
    start = make_list(fenetre)
    start.build_main_window(Liste_e)

def ChooseFins():
    Liste_f = np.array(["Small", "Medium", "Large"])
    start = make_list(fenetre)
    start.build_main_window(Liste_f)

def Motor1():
    # create_arc()        :  arc de cercle
    # create_bitmap()     :  bitmap
    # create_image()      :  image
    # create_line()       :  ligne
    # create_oval()       :  ovale
    # create_polygon()    :  polygone
    # create_rectangle()  :  rectangle
    # create_text()       :  texte
    # create_window()     :  fenetre
    canvas = Canvas(fenetre, width=500, height=80, background='yellow')
    ligne1 = canvas.create_line(25, 0, 25, 120)
    ligne2 = canvas.create_line(0, 80, 250, 80)
    txt = canvas.create_text(125, 60, text="ERT 2019", font="Arial 34 bold", fill="green")
    canvas.pack()

# Menu
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Create", command=Tk)
menu1.add_command(label="Edit")
menu1.add_separator()
menu1.add_command(label="Quit", command=fenetre.quit)
menubar.add_cascade(label="File", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Cut")
menu2.add_command(label="Copy")
menu2.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Zoom")
menubar.add_cascade(label="Tools", menu=menu3)

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="About")
menubar.add_cascade(label="Help", menu=menu4)

fenetre.config(menu=menubar)

Motor_Type = Button(fenetre, text ="Motor Type", cursor="man", bd=3, bg="dark blue", fg="yellow", relief=GROOVE,
                    command=ChooseMotor).pack(side=LEFT, padx=5, pady=20)


Environment_Type = Button(fenetre, text ="Environment Type", cursor="target", bd=3, bg="dark green", fg="white", relief=GROOVE,
                          command=ChooseEnvironment).pack(side=LEFT, padx=5, pady=20)

Fins_Type = Button(fenetre, text = "Fins_type?", cursor="mouse", bd=3, bg="red", fg="black", relief=GROOVE,
                   command=ChooseFins).pack(side=LEFT, padx=5, pady=20)


# fenetre.resizable(False,False)

# Affiche la fenetre
fenetre.mainloop()
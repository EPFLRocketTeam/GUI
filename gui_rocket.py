# GUI
# Author : Henri Faure
# Date : 7 April 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import keyboard
import numpy as np
import matplotlib.pyplot as plt

# Ouvre une fenetre
fenetre = Tk()
fenetre.geometry("640x480")
fenetre.grid()
fenetre.title('Simulator EPFL_Rocket')
fenetre.call('wm', 'iconphoto', fenetre._w, PhotoImage(file='ERT_logo.png'))
fenetre.configure(bg="light goldenrod yellow")

def TextLabel(type1, type2):
    label = Label(fenetre, text='The %s %s is selected' %(type2, type1), bg='white')
    label.place(x=20, y=40, anchor=NW)

def ThrustGraph():
    graph = Canvas(fenetre, width=190, height=150, background='white')
    graph.create_text(75, 15, text="Thrust Graph", font="Arial 8 italic", fill="black")
    graph.pack()
    graph.place(x=425, y=50)

# Choose motor parameters
motor_choice = Menubutton(fenetre, text="Choose Motor", bg='red', fg='black', cursor='hand2', relief=RAISED)
motor_choice.grid()
motor_choice.menu = Menu(motor_choice, tearoff=0)
motor_choice["menu"] = motor_choice.menu

motor_choice.menu.add_checkbutton(label="Solid", command=lambda: TextLabel('motor ', 'solid '))
motor_choice.menu.add_checkbutton(label="Hybrid", command=lambda: TextLabel('motor ', 'hybrid '))
motor_choice.menu.add_checkbutton(label="Liquid", command=lambda: TextLabel('motor ', 'liquid '))

motor_choice.pack()
motor_choice.place(x=10, y=10, anchor=NW)

# Choose Environment parameters
env_choice = Menubutton(fenetre, text="Choose Environment", bg='dark green', fg='yellow', cursor='hand2', relief=RAISED)
env_choice.grid()
env_choice.menu = Menu(env_choice, tearoff=0)
env_choice["menu"] = env_choice.menu

env_choice.menu.add_checkbutton(label="Cernier", command=lambda: TextLabel('environment ', 'Cernier '))
env_choice.menu.add_checkbutton(label="Zurich", command=lambda: TextLabel('environment ', 'Zurich '))
env_choice.menu.add_checkbutton(label="Mexique", command=lambda: TextLabel('environment ', 'Mexique '))

env_choice.pack()
env_choice.place(x=100, y=10, anchor=NW)

# Choose Fins parameters
fins_choice = Menubutton(fenetre, text="Choose Fins", bg='dark blue', fg='white', cursor='hand2', relief=RAISED)
fins_choice.grid()
fins_choice.menu = Menu(fins_choice, tearoff=0)
fins_choice["menu"] = fins_choice.menu

fins_choice.menu.add_checkbutton(label="Small", command=lambda: TextLabel('fins ', 'small '))
fins_choice.menu.add_checkbutton(label="Medium", command=lambda: TextLabel('fins ', 'medium '))
fins_choice.menu.add_checkbutton(label="Large", command=lambda: TextLabel('fins ', 'large '))

fins_choice.pack()
fins_choice.place(x=225, y=10, anchor=NW)


# Design rocket
canvas = Canvas(fenetre, width=500, height=250, background='white')
txt = canvas.create_text(115, 30, text="ERT 2019", font="Arial 34 bold", fill="green")
Logo_tmp = Image.open('ERT_logo.png')
Logo_tmp = Logo_tmp.resize((100, 70), Image.ANTIALIAS)
Logo = ImageTk.PhotoImage(Logo_tmp)
canvas.create_image(400, 2, anchor=NW, image=Logo)
canvas.pack()
canvas.place(x=131, y=220)

# Displays graph
# Thrust graph
thrust_button = Button(fenetre, text="Get Thrust", bg='yellow', fg='black', command=ThrustGraph)
thrust_button.pack()
thrust_button.place(x=485, y=20, anchor=NW)

# Bouton de sortie
bouton=Button(fenetre, text="END", bg='red', fg='black', command=fenetre.quit)
bouton.pack()
bouton.place(x=2, y=450, anchor=NW)

# Disp window
fenetre.mainloop()
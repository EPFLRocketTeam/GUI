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
    label.after(1500, lambda: label.destroy())

def Simu(Motor, Environment, Fins):
    graph = Canvas(fenetre, width=450, height=25, background='white')
    graph.create_text(225, 12.5, text='Simulation done with %s, %s, %s' %(Motor, Environment, Fins), font="Arial 8 italic", fill="black")
    graph.pack()
    graph.place(x=200, y=50)

# Choose motor parameters
motor_choice = Menubutton(fenetre, text='Choose Motor', bg='red', fg='black', cursor='hand2', relief=RAISED)
motor_choice.grid()
motor_choice.menu = Menu(motor_choice, tearoff=0)
motor_choice["menu"] = motor_choice.menu

mtr = StringVar()
motor_choice.menu.add_radiobutton(label='Solid', value='Solid motor', variable=mtr, command=lambda: TextLabel('motor ', 'solid '))
motor_choice.menu.add_radiobutton(label='Hybrid', value='Hybrid motor', variable=mtr, command=lambda: TextLabel('motor ', 'hybrid '))
motor_choice.menu.add_radiobutton(label='Liquid', value='Liquid motor', variable=mtr, command=lambda: TextLabel('motor ', 'liquid '))

motor_choice.pack()
motor_choice.place(x=10, y=10, anchor=NW)

# Choose Environment parameters
env_choice = Menubutton(fenetre, text="Choose Environment", bg='dark green', fg='yellow', cursor='hand2', relief=RAISED)
env_choice.grid()
env_choice.menu = Menu(env_choice, tearoff=0)
env_choice["menu"] = env_choice.menu

env = StringVar()
env_choice.menu.add_radiobutton(label='Cernier', variable=env, value='Cernier environment',
                                command=lambda: TextLabel('environment ', 'Cernier '))
env_choice.menu.add_radiobutton(label='Zurich', variable=env, value='Zurich environment',
                                command=lambda: TextLabel('environment ', 'Zurich '))
env_choice.menu.add_radiobutton(label='Mexique', variable=env, value='Mexique environment',
                                command=lambda: TextLabel('environment ', 'Mexique '))

env_choice.pack()
env_choice.place(x=100, y=10, anchor=NW)

# Choose Fins parameters
fins_choice = Menubutton(fenetre, text="Choose Fins", bg='dark blue', fg='white', cursor='hand2', relief=RAISED)
fins_choice.grid()
fins_choice.menu = Menu(fins_choice, tearoff=0)
fins_choice["menu"] = fins_choice.menu

fns = StringVar()
fins_choice.menu.add_radiobutton(label='Small', value='small fins', variable=fns, command=lambda: TextLabel('fins ', 'small '))
fins_choice.menu.add_radiobutton(label='Medium', value='Medium fins', variable=fns, command=lambda: TextLabel('fins ', 'medium '))
fins_choice.menu.add_radiobutton(label='Large', value='Large fins', variable=fns, command=lambda: TextLabel('fins ', 'large '))

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

# Launch simulation
simu_button = Button(fenetre, text="Launch simulation", bg='yellow', fg='black',
                     command=lambda : Simu(mtr.get(), env.get(), fns.get()))
simu_button.pack()
simu_button.place(x=471, y=20, anchor=NW)

# Bouton de sortie
bouton=Button(fenetre, text="END", bg='red', fg='black', command=fenetre.quit)
bouton.pack()
bouton.place(x=2, y=450, anchor=NW)

# Disp window
fenetre.mainloop()
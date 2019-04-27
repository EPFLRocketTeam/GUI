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
from matplotlib.figure import Figure

# Ouvre une fenetre
fenetre = Tk()
fenetre.geometry("640x480")
fenetre.grid()
fenetre.title('Simulator EPFL_Rocket')
fenetre.call('wm', 'iconphoto', fenetre._w, PhotoImage(file='ERT_logo.png'))
fenetre.configure(bg="light goldenrod yellow")

# Menu
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Create", command=fenetre)
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

def TextLabel(type1, type2):
    label = Label(fenetre, text='The %s %s is selected' %(type2, type1), bg='white')
    label.place(x=315, y=13, anchor=NW)
    label.after(2000, lambda: label.destroy())

def Simu(Motor, Environment, Fins):
    graph = Canvas(fenetre, width=370, height=25, background='white')
    graph.create_text(185, 12.5, text='Simulation done with %s, %s, %s' %(Motor, Environment, Fins), font="Arial 8 italic", fill="black")
    graph.pack()
    graph.place(x=600, y=238)
    graph.after(5000, lambda: graph.destroy())
    canvas.create_text(130, 30, text='Rocket Design', font='Arial 22 bold', fill='firebrick3')

# Choose motor parameters
motor_choice = Menubutton(fenetre, text='Choose Motor', bg='grey', fg='black', cursor='hand2', relief=RAISED)
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
env_choice = Menubutton(fenetre, text="Choose Environment", bg='grey', fg='black', cursor='hand2', relief=RAISED)
env_choice.grid()
env_choice.menu = Menu(env_choice, tearoff=0)
env_choice["menu"] = env_choice.menu

env = StringVar()
env_choice.menu.add_radiobutton(label='Cernier', variable=env, value='Cernier environment',
                                command=lambda: TextLabel('environment ', 'Cernier '))
env_choice.menu.add_radiobutton(label='Zurich', variable=env, value='Zurich environment',
                                command=lambda: TextLabel('environment ', 'Zurich '))
env_choice.menu.add_radiobutton(label='Mexico', variable=env, value='Mexico environment',
                                command=lambda: TextLabel('environment ', 'Mexico '))

env_choice.pack()
env_choice.place(x=100, y=10, anchor=NW)

# Choose Fins parameters
fins_choice = Menubutton(fenetre, text='Choose Fins', bg='grey', fg='black', cursor='hand2', relief=RAISED)
fins_choice.grid()
fins_choice.menu = Menu(fins_choice, tearoff=0)
fins_choice["menu"] = fins_choice.menu

fns = StringVar()
fins_choice.menu.add_radiobutton(label='Trapezoïdal', value='trapezoïdal fins', variable=fns, command=lambda: TextLabel(
    'fins ', 'trapezoïdal '))

fins_choice.pack()
fins_choice.place(x=225, y=10, anchor=NW)

# Design rocket
canvas = Canvas(fenetre, width=850, height=350, background='white')
Logo_tmp = Image.open('ERT_logo.png')
Logo_tmp = Logo_tmp.resize((100, 70), Image.ANTIALIAS)
Logo = ImageTk.PhotoImage(Logo_tmp)
canvas.create_image(750, 2, anchor=NW, image=Logo)
canvas.pack()
canvas.place(x=420, y=270)

# Create canvas
canvas1 = Canvas(fenetre, width=90, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas1.create_arc(-31, 119, 205, 0, width=1, outline='blue', style=ARC, start=90, extent=90)
canvas1.create_arc(-31, 39, 205, -80, width=1, outline='blue', style=ARC, start=-90, extent=-90)
canvas1.create_line(88, 0, 88, 40, width=1, fill='blue')
canvas.create_window(110, 200, window=canvas1)

canvas2 = Canvas(fenetre, width=300, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas2.create_rectangle(0, 0, 299, 39, width=1, outline='blue')
canvas.create_window(305, 200, window=canvas2)

canvas8 = Canvas(fenetre, width=10, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas8.create_rectangle(1, 0, 9, 39, width=1, outline='blue')
canvas.create_window(460, 200, window=canvas8)

canvas3 = Canvas(fenetre, width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas3.create_rectangle(1, 0, 199, 39, width=1, outline='blue')
canvas.create_window(565, 200, window=canvas3)

canvas4 = Canvas(fenetre, width=80, height=55, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas4.create_rectangle(1, 6.5, 79, 45.5, width=1, outline='blue')
canvas4.create_polygon(1, 32.5, 79, 32.5, 65, 54, 50, 54, width=1, outline='blue', fill='')
canvas.create_window(705, 200, window=canvas4)

canvas5 = Canvas(fenetre, width=10, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas5.create_polygon(1, 1, 9, 5, 9, 35, 1, 39, width=1, outline='blue', fill='')
canvas.create_window(750, 200, window=canvas5)

canvas6 = Canvas(fenetre, width=80, height=30, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas6.create_polygon(1, 29, 50, 1, 65, 1, 79, 29, width=1, outline='blue', fill='')
canvas.create_window(705, 164, window=canvas6)

canvas7 = Canvas(fenetre, width=10, height=10, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas7.create_oval(0, 0, 9, 9, width=1, fill='red', outline='red')
canvas.create_window(550, 200, window=canvas7)

canvas7 = Canvas(fenetre, width=10, height=10, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas7.create_oval(0, 0, 9, 9, width=1, fill='blue', outline='blue')
canvas.create_window(450, 200, window=canvas7)

# Join variables with file path
motor_file_path = '%s.txt' % (mtr.get())
environment_file_path = '%s.txt' % (env.get())
fins_file_path = '%s.txt' % (fns.get())

# Launch simulation
simu_button = Button(fenetre, text='Launch simulation', bg='yellow', fg='black',
                     command=lambda : Simu(mtr.get(), env.get(), fns.get()))
simu_button.pack()
simu_button.place(x=420, y=240, anchor=NW)

# Bouton de sortie
bouton = Button(fenetre, text="END", bg='red', fg='black', command=fenetre.quit)
bouton.pack()
bouton.place(x=2, y=610, anchor=NW)

# Disp window
fenetre.mainloop()
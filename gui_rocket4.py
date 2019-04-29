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
menu3.add_command(label="Launch")
menubar.add_cascade(label="Analyse", menu=menu3)


fenetre.config(menu=menubar)

for r in range(20):
    fenetre.rowconfigure(r, weight=1)
for c in range(20):
    fenetre.columnconfigure(c, weight=1)

def TextLabel(type1, type2):
    label = Label(fenetre, text='The %s %s is selected' %(type2, type1), bg='white')
    label.place(x=315, y=13, anchor=NW)
    label.after(2000, lambda: label.destroy())

def Simu(Motor, Environment, Fins):
    graph = Canvas(fenetre, background='white')
    graph.create_text(185, 12.5, text='Simulation done with %s, %s, %s' %(Motor, Environment, Fins), font="Arial 8 italic", fill="black")
    graph.place(x=600, y=238)
    graph.after(5000, lambda: graph.destroy())

# Choose motor parameters
motor_choice = Menubutton(fenetre, text='Choose Motor', bg='white', fg='black', cursor='hand2', relief=RAISED)
motor_choice.grid()
motor_choice.menu = Menu(motor_choice, tearoff=0)
motor_choice["menu"] = motor_choice.menu

mtr = StringVar()
motor_choice.menu.add_radiobutton(label='Solid', value='Solid motor', variable=mtr, command=lambda: TextLabel('motor ', 'solid '))
motor_choice.menu.add_radiobutton(label='Hybrid', value='Hybrid motor', variable=mtr, command=lambda: TextLabel('motor ', 'hybrid '))
motor_choice.menu.add_radiobutton(label='Liquid', value='Liquid motor', variable=mtr, command=lambda: TextLabel('motor ', 'liquid '))

motor_choice.place(x=10, y=10, anchor=NW)

# Choose Environment parameters
env_choice = Menubutton(fenetre, text="Choose Environment", bg='white', fg='black', cursor='hand2', relief=RAISED)
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
env_choice.place(x=100, y=10, anchor=NW)

# Choose Fins parameters
fins_choice = Menubutton(fenetre, text='Choose Fins', bg='white', fg='black', cursor='hand2', relief=RAISED)
fins_choice.grid()
fins_choice.menu = Menu(fins_choice, tearoff=0)
fins_choice["menu"] = fins_choice.menu

fns = StringVar()
fins_choice.menu.add_radiobutton(label='Trapezoïdal', value='trapezoïdal fins', variable=fns, command=lambda: TextLabel(
    'fins ', 'trapezoïdal '))

fins_choice.place(x=225, y=10, anchor=NW)

# Design rocket
canvas = Canvas(fenetre, width=800, height=300, bg='gray95')
canvas.place(x=335, y=370, anchor=NW)

canvas0 = Canvas(fenetre, width=850, height=350, background='white')
canvas0.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='se', padx=10, pady=10, in_=canvas)

# Create canvas
canvas1 = Canvas(fenetre, width=90, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas1.create_arc(-31, 119, 205, 0, width=1, outline='blue', style=ARC, start=90, extent=90)
canvas1.create_arc(-31, 39, 205, -80, width=1, outline='blue', style=ARC, start=-90, extent=-90)
canvas1.create_line(88, 0, 88, 40, width=1, fill='blue')
canvas1.grid(row=3, column=2, sticky='ne', ipady=20, in_=canvas0)

canvas2 = Canvas(fenetre, width=300, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas2.create_rectangle(0, 0, 299, 39, width=1, outline='blue')
canvas2.grid(row=3, column=3, sticky='nw', in_=canvas0)

canvas3 = Canvas(fenetre, width=10, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas3.create_rectangle(1, 0, 9, 39, width=1, outline='blue')
canvas3.grid(row=3, column=4, sticky='nw', in_=canvas0)

canvas4 = Canvas(fenetre, width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas4.create_rectangle(1, 0, 199, 39, width=1, outline='blue')
canvas4.grid(row=3, column=5, sticky='nw', in_=canvas0)

canvas5 = Canvas(fenetre, width=80, height=45, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas5.create_rectangle(1, 0, 79, 39, width=1, outline='blue')
canvas5.create_polygon(1, 26, 79, 26, 65, 44, 50, 44, width=1, outline='blue', fill='')
canvas5.grid(row=3, column=6, rowspan=2, sticky='nw', in_=canvas0)

canvas6 = Canvas(fenetre, width=10, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas6.create_polygon(1, 1, 9, 5, 9, 35, 1, 39, width=1, outline='blue', fill='')
canvas6.grid(row=3, column=7, sticky='nw', ipadx=50, in_=canvas0)

canvas7 = Canvas(fenetre, width=80, height=30, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas7.create_polygon(1, 28, 50, 0, 65, 0, 79, 28, width=1, outline='blue', fill='')
canvas7.grid(row=2, column=6, sticky='sw', in_=canvas0)

Name = 'Eiger'
Mass = 3832
Length = 189
Max_Diameter = 10.2

canvas8 = Canvas(fenetre, width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas8.create_text(100, 20, text='%s \nLength %d cm, max.diameter %d cm \nMass with motors %d g' %
                            (Name, Length, Max_Diameter, Mass), fill='black', font='Arial 8 italic', justify='left')
canvas8.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='nw', in_=canvas0)

Stability = 2.28
CG = 114
CP = 137
Mach = 0.30

canvas9 = Canvas(fenetre, width=100, height=50, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas9.create_text(50, 25, text='Stability : %s cal \nCG : %d cm \nCP %d cm \nat M=%d' % (Stability, CG, CP, Mach),
                    fill='black', font='Arial 8 italic', justify='left')
canvas9.grid(row=0, column=5, columnspan=3, padx=10, pady=10, sticky='ne', in_=canvas0)

Apogee = 3040
max_v = 107
max_a = 49.8
Mach_v = 0.32

canvas10 = Canvas(fenetre, width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas10.create_text(100, 20, text='Apogee : %d m \nMax. velocity : %d m.s-1   (Mach %d) \nMax. acceleration : '
                      '%d m.s-2' % (Apogee, max_v, Mach_v, max_a), font='Arial 8 italic', fill='blue', justify='left')
canvas10.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nw', in_=canvas0)


# Join variables with file path
motor_file_path = '%s.txt' % (mtr.get())
environment_file_path = '%s.txt' % (env.get())
fins_file_path = '%s.txt' % (fns.get())

# Launch simulation
simu_button = Button(fenetre, text='Launch simulation', bg='white', fg='black',
                     command=lambda : Simu(mtr.get(), env.get(), fns.get()))
# simu_button.grid(row=10, column=10, rowspan=1, columnspan=2, sticky='sw')

# Bouton de sortie
bouton = Button(fenetre, text="END", bg='black', fg='white', command=fenetre.quit)
bouton.grid(row=20, column=0, rowspan=1, columnspan=1, sticky='nswe', padx=10, pady=10)

# Disp window
fenetre.mainloop()
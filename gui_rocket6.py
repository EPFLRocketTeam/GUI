# GUI
# Author : Henri Faure
# Date : 7 April 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from tkinter import *
from math import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import keyboard
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# Displays in a label the selected rocket part
def TextLabel(type1, type2):
    label = Label(fenetre, text='The %s %s is selected' %(type2, type1), bg='DarkOrange1')
    label.grid(row=3, column=0, columnspan=3, in_=canvasAB)
    label.after(4000, lambda: label.destroy())

# Function which permits entry value manually
def EntryButton(canvasACN, name, rnum, cnum):

    # Check all values are mathematical values
    def TestFunction(value):
        if value in '0123456789-+*/.':
            return True
        else:
            return False

    # print entered value in command window
    def getvalue(event):
        val=eval(entry.get())  #do calculation on entered values if necessary
        print(val)

    Label(fenetre, text='%s' % name, bg='gray85', anchor=NW).grid(row=rnum, column=cnum, padx=10, pady=2, in_=canvasACN)
    entry = Entry(fenetre, validate='key', validatecommand=(fenetre.register(TestFunction), '%S'))
    entry.bind('<Return>', getvalue)
    entry.grid(row=rnum+1, column=cnum, padx=10, pady=10, in_=canvasACN)

# Displays canvas in which are the nosecone's parameters
def DispNoseCone():
    NoseCone_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC1.grid_remove()
    canvasAC3.grid_remove()
    canvasAC2.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical nosecone in drawing
def DisplayNose():
    canvasX = Canvas(fenetre, width=75, height=50, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvasX.grid(row=3, column=0, sticky='nsew', in_=canvas0)
    canvas1.grid(row=3, column=1, sticky='nw', in_=canvas0)

# Displays canvas in which are the tube's parameters
def DispTube():
    Tube_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC1.grid_remove()
    canvasAC2.grid_remove()
    canvasAC3.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical tube in drawing
def DisplayTube():
    canvas2.grid(row=3, column=2, sticky='nw', in_=canvas0)

# Displays canvas in which are the fins's parameters
def DispFins():
    Fins_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC2.grid_remove()
    canvasAC3.grid_remove()
    canvasAC1.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical fins in drawing
def DisplayFins():
    canvas3A.grid(row=3, column=7, rowspan=2, sticky='nw', in_=canvas0)
    canvas3B.grid(row=1, column=7, rowspan=2, sticky='sw', in_=canvas0)
    canvas3C.grid(row=3, column=8, sticky='nw', ipadx=70, in_=canvas0)

# Ouvre une fenetre with title and icon
fenetre = Tk()
fenetre.geometry("640x480")
fenetre.grid()
fenetre.title('Simulator EPFL_Rocket')
fenetre.call('wm', 'iconphoto', fenetre._w, PhotoImage(file='ERT_logo.png'))
fenetre.configure(bg="light goldenrod yellow")

fenetre.rowconfigure(0, weight=1)
fenetre.rowconfigure(1, weight=50)  #give a weight more important to the second row
fenetre.columnconfigure(0, weight=1)

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

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="Launch")
menubar.add_cascade(label="Help", menu=menu4)

fenetre.config(menu=menubar)

# First row in window
canvasA = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasA.grid(row=0, column=0, sticky='nswe')

# Arborescence, Left part of first row
canvasAA = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasAA.grid(row=0, column=0, sticky='nswe', in_=canvasA)

# Add new part, Center part of first row
canvasAB = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasAB.grid(row=0, column=1, sticky='nswe', in_=canvasA)

# Parameters, Right part of first row
canvasAC = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasAC.grid(row=0, column=2, sticky='nswe', in_=canvasA)
canvasAC1 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')
canvasAC2 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')
canvasAC3 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')

# Choose NoseCone
NoseCone_choice = Menubutton(fenetre, text='Nosecone', bg='white', fg='black', cursor='hand2', relief=RAISED)
NoseCone_choice.grid()
NoseCone_choice.menu = Menu(NoseCone_choice, tearoff=0)
NoseCone_choice["menu"] = NoseCone_choice.menu

nsc = StringVar()
NoseCone_choice.menu.add_radiobutton(label='Ogive', value='Ogive nosecone', variable=nsc, command=lambda:
    TextLabel('nosecone ', 'ogive '))

NoseCone_choice.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky='nswe', in_=canvasAB)

Inertia=Label(canvasAC2, text='Inertia Matrix of Nosecone', bg='gray85', fg='blue')
Inertia.grid(row=0, column=0, columnspan=3, padx=10, pady=2, in_=canvasAC2)

EntryButton(canvasAC2, '1', 1, 0)
EntryButton(canvasAC2, '2', 1, 1)
EntryButton(canvasAC2, '3', 1, 2)
EntryButton(canvasAC2, '4', 3, 0)
EntryButton(canvasAC2, '5', 3, 1)
EntryButton(canvasAC2, '6', 3, 2)
EntryButton(canvasAC2, '7', 5, 0)
EntryButton(canvasAC2, '8', 5, 1)
EntryButton(canvasAC2, '9', 5, 2)

DispN = Button(fenetre, text='Displays', command=lambda: DisplayNose())
DispN.grid(row=7, column=2, sticky='se', padx=10, pady=10, in_=canvasAC2)

NoseCone_choice.bind("<Button-1>", lambda event: DispNoseCone())

# Choose Tube
Tube_choice = Menubutton(fenetre, text='Tube', bg='white', fg='black', cursor='hand2', relief=RAISED)
Tube_choice.grid()
Tube_choice.menu = Menu(Tube_choice, tearoff=0)
Tube_choice["menu"] = Tube_choice.menu

tb = StringVar()
Tube_choice.menu.add_radiobutton(label='cylinder', value='cylinder tube', variable=tb, command=lambda:
    TextLabel('Tube ', 'cylinder '))

Tube_choice.grid(row=0, column=1, padx=10, pady=10, ipadx=25, ipady=10, sticky='nswe', in_=canvasAB)

InertiaTube=Label(canvasAC3, text='Inertia Matrix of Tube', bg='gray85', fg='blue')
InertiaTube.grid(row=0, column=0, columnspan=3, padx=10, pady=2, in_=canvasAC3)

EntryButton(canvasAC3, '1', 1, 0)
EntryButton(canvasAC3, '2', 1, 1)
EntryButton(canvasAC3, '3', 1, 2)
EntryButton(canvasAC3, '4', 3, 0)
EntryButton(canvasAC3, '5', 3, 1)
EntryButton(canvasAC3, '6', 3, 2)
EntryButton(canvasAC3, '7', 5, 0)
EntryButton(canvasAC3, '8', 5, 1)
EntryButton(canvasAC3, '9', 5, 2)

DispT = Button(fenetre, text='Displays', command=lambda: DisplayTube())
DispT.grid(row=7, column=2, sticky='se', padx=10, pady=10, in_=canvasAC3)

Tube_choice.bind("<Button-1>", lambda event: DispTube())

# Choose Fins
Fins_choice = Menubutton(fenetre, text='Fins', bg='white', fg='black', cursor='hand2', relief=RAISED)
Fins_choice.grid()
Fins_choice.menu = Menu(Fins_choice, tearoff=0)
Fins_choice["menu"] = Fins_choice.menu

fns = StringVar()
Fins_choice.menu.add_radiobutton(label='Trapezoïdal', value='trapezoïdal fins', variable=fns, command=lambda:
    TextLabel('fins ', 'trapezoïdal '))

Fins_choice.grid(row=0, column=2, padx=10, pady=10, ipadx=27, ipady=10, sticky='nswe', in_=canvasAB)

EntryButton(canvasAC1, 'Number', 0, 0)
EntryButton(canvasAC1, 'Root chord', 0, 1)
EntryButton(canvasAC1, 'Tip chord', 0, 2)
EntryButton(canvasAC1, 'Span', 2, 0)
EntryButton(canvasAC1, 'Sweep', 2, 1)
EntryButton(canvasAC1, 'Thickness', 2, 2)
EntryButton(canvasAC1, 'Phase', 4, 0)
EntryButton(canvasAC1, 'Body top offset', 4, 1)

DispF = Button(fenetre, text='Displays', command=lambda: DisplayFins())
DispF.grid(row=6, column=2, sticky='se', padx=10, pady=10, in_=canvasAC1)

Fins_choice.bind("<Button-1>", lambda event: DispFins())

# Choose motor
motor_choice = Menubutton(fenetre, text='Motor', bg='white', fg='black', cursor='hand2', relief=RAISED)
motor_choice.grid()
motor_choice.menu = Menu(motor_choice, tearoff=0)
motor_choice["menu"] = motor_choice.menu

mtr = StringVar()
motor_choice.menu.add_radiobutton(label='Solid', value='Solid motor', variable=mtr, command=lambda:
    TextLabel('motor ', 'solid '))
motor_choice.menu.add_radiobutton(label='Hybrid', value='Hybrid motor', variable=mtr, command=lambda:
    TextLabel('motor ', 'hybrid '))
motor_choice.menu.add_radiobutton(label='Liquid', value='Liquid motor', variable=mtr, command=lambda:
    TextLabel('motor ', 'liquid '))

motor_choice.grid(row=1, column=0, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe', in_=canvasAB)

# Choose Environment
env_choice = Menubutton(fenetre, text="Environment", bg='white', fg='black', cursor='hand2', relief='raised')
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
env_choice.grid(row=1, column=1, padx=10, pady=10, ipadx=2, ipady=10, sticky='nswe', in_=canvasAB)

# Design rocket, Second row of window
# scale : 1 pixel <-> 3 millimeters
# length : 3010 mm
# diameter : 155.6 mm
canvasB = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasB.grid(row=1, column=0, sticky='nswe')
canvasB.rowconfigure(0, weight=1)
canvasB.columnconfigure(0, weight=1)

# Quite superficial
canvas0 = Canvas(fenetre, bg='white')
canvas0.grid(row=0, column=0, sticky='nsew', padx=10, pady=10, in_=canvasB)
canvas0.rowconfigure(0, weight=1)
canvas0.rowconfigure(1, weight=5)
canvas0.rowconfigure(2, weight=1)
canvas0.rowconfigure(3, weight=5)
canvas0.rowconfigure(4, weight=1)

# Scrollbar
hbar=Scrollbar(canvasB, orient=HORIZONTAL)
hbar.grid(row=1, column=0, sticky='ew', in_=canvasB)
hbar.config(command=canvas0.xview)
vbar=Scrollbar(canvasB, orient=VERTICAL)
vbar.grid(row=0, column=1, sticky='ns', in_=canvasB)
vbar.config(command=canvas0.yview)
canvas0.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# Create canvas
# Nosecone
canvas1 = Canvas(fenetre, width=217, height=52, bg='white', highlightthickness=0, bd=0, relief='ridge')  # 300 mm + 350 mm
canvas1.create_arc(-34, 149, 240, 0, width=1, outline='blue', style=ARC, start=90, extent=90)
canvas1.create_arc(-34, 51, 240, -100, width=1, outline='blue', style=ARC, start=-90, extent=-90)
canvas1.create_line(100, 0, 216, 0, width=1, fill='blue')
canvas1.create_line(100, 51, 216, 51, width=1, fill='blue')
canvas1.create_line(216, 0, 216, 51, width=1, fill='blue')

# Tube
canvas2 = Canvas(fenetre, width=670, height=52, bg='white', highlightthickness=0, bd=0, relief='ridge')  # 2010 mm
canvas2.create_rectangle(1, 0, 669, 51, width=1, outline='blue')

# Fins
canvas3A = Canvas(fenetre, width=100, height=77, bg='white', highlightthickness=0, bd=0, relief='ridge')  # 350 mm
canvas3A.create_rectangle(1, 0, 99, 51, width=1, outline='blue')
canvas3A.create_polygon(4, 35, 97, 35, 81, 76, 40, 76, width=1, outline='blue', fill='')

canvas3B = Canvas(fenetre, width=100, height=73, bg='white', highlightthickness=0, bd=0, relief='ridge')  # 215 mm (height fins), 280 mm (length fins)
canvas3B.create_polygon(4, 71, 97, 71, 81, 0, 40, 0, width=1, outline='blue', fill='')

canvas3C = Canvas(fenetre, width=17, height=52, bg='white', highlightthickness=0, bd=0, relief='ridge')  # 50 mm
canvas3C.create_polygon(1, 1, 16, 5, 16, 47, 1, 51, width=1, outline='blue', fill='')

# Characteristics of rocket
Name = 'Eiger'
Mass = 3832
Length = 189
Max_Diameter = 10.2

canvas6 = Canvas(fenetre, width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas6.create_text(100, 20, text='%s \nLength %d cm, max.diameter %d cm \nMass with motors %d g' %
                            (Name, Length, Max_Diameter, Mass), fill='black', font='Arial 8 italic', justify='left')
canvas6.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nw', in_=canvas0)

Stability = 2.28
CG = 114
CP = 137
Mach = 0.30

canvas7 = Canvas(fenetre, width=100, height=50, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas7.create_text(50, 25, text='Stability : %s cal \nCG : %d cm \nCP %d cm \nat M=%d' % (Stability, CG, CP, Mach),
                    fill='black', font='Arial 8 italic', justify='left')
canvas7.grid(row=0, column=6, columnspan=3, padx=10, pady=10, sticky='ne', in_=canvas0)

Apogee = 3040
max_v = 107
max_a = 49.8
Mach_v = 0.32

canvas8 = Canvas(fenetre, width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
canvas8.create_text(100, 20, text='Apogee : %d m \nMax. velocity : %d m.s-1   (Mach %d) \nMax. acceleration : '
                      '%d m.s-2' % (Apogee, max_v, Mach_v, max_a), font='Arial 8 italic', fill='blue', justify='left')
canvas8.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nw', in_=canvas0)

# Bouton de sortie
# stop = Button(fenetre, text="x", bg='RED', fg='white', command=fenetre.quit)
# stop.grid(row=1, column=1, sticky='nswe', in_=canvasB)

# Disp window
fenetre.mainloop()
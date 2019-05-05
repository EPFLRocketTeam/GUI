# GUI
# Author : Henri Faure
# Last update : 5 May 2019
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
def EntryButton(canvasACN, name, rnum, cnum, entries):

    # Check all values are mathematical values
    def TestFunction(value):
        if value in '0123456789-+*/.':
            return True
        else:
            return False

    Label(fenetre, text='%s' % name, bg='gray85', anchor=NW).grid(row=rnum, column=cnum, padx=10, pady=2, in_=canvasACN)
    entry = Entry(fenetre, validate='key', validatecommand=(fenetre.register(TestFunction), '%S'))
    entry.insert(0, 0)
    entry.grid(row=rnum+1, column=cnum, padx=10, pady=10, in_=canvasACN)
    entries.append(entry)

# Function wich geta values from entries
def hallo(entries):
    Array_Value = []
    for entry in entries:
        Array_Value = np.append(Array_Value, eval(entry.get()))
    return Array_Value

# Displays canvas in which are the diameter parameter
def DispDiameter():
    Diameter_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC1.grid_remove()
    canvasAC2.grid_remove()
    canvasAC3.grid_remove()
    canvasAC0.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Get Max Diameter
def GetMaxDiameter():
    VALUES_D = hallo(entries0)
    Max_Diameter = VALUES_D[0]
    return Max_Diameter

# Displays canvas in which are the nosecone's parameters
def DispNoseCone():
    NoseCone_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC0.grid_remove()
    canvasAC1.grid_remove()
    canvasAC3.grid_remove()
    canvasAC2.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical nosecone in drawing
def DisplayNose():
    DispData()
    canvas1.delete('all')
    VALUES_N = hallo(entries1)
    VALUES_D = hallo(entries0)

    canvas1.configure(width=VALUES_N[0]/3, height=VALUES_D[0]/3, bg='white', highlightthickness=0, bd=0,
                     relief='ridge')  # 300 mm + 350 mm
    canvas1.create_arc(2/3*(1-VALUES_D[0]/3), 3.2*VALUES_D[0]/3, 4*VALUES_D[0]/3, 0, width=1, outline='blue', style=ARC,
                       start=90, extent=90)
    canvas1.create_arc(2/3*(1-VALUES_D[0]/3), VALUES_D[0]/3-1, 4*VALUES_D[0]/3, -2.2*VALUES_D[0]/3, width=1,
                       outline='blue', style=ARC, start=-90, extent=-90)
    canvas1.create_line(3/2*VALUES_D[0]/3, 0, VALUES_N[0]/3-1, 0, width=1, fill='blue')
    canvas1.create_line(3/2*VALUES_D[0]/3, VALUES_D[0]/3-1, VALUES_N[0]/3-1, VALUES_D[0]/3-1, width=1, fill='blue')
    canvas1.create_line(VALUES_N[0]/3-1, 0, VALUES_N[0]/3-1, VALUES_D[0]/3-1, width=1, fill='blue')
    canvas1.grid(row=3, column=1, sticky='nw', in_=canvas0)

# Get NoseCone length
def GetLenNose():
    VALUES_N = hallo(entries1)
    Len_Nose = VALUES_N[0]
    return Len_Nose

# Displays canvas in which are the tube's parameters
def DispTube():
    Tube_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC0.grid_remove()
    canvasAC1.grid_remove()
    canvasAC2.grid_remove()
    canvasAC3.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical tube in drawing
def DisplayTube():
    DispData()
    canvas2.delete('all')
    VALUES_T = hallo(entries2)
    VALUES_D = hallo(entries0)
    canvas2.configure(width=VALUES_T[0]/3, height=VALUES_D[0]/3, bg='white', highlightthickness=0, bd=0, relief='ridge')  # 2010 mm
    canvas2.create_rectangle(1, 0, VALUES_T[0]/3-1, VALUES_D[0]/3-1, width=1, outline='blue')
    canvas2.grid(row=3, column=2, sticky='nw', in_=canvas0)

# Get Tube length
def GetLenTube():
    VALUES_T = hallo(entries2)
    Len_Tube = VALUES_T[0]
    return Len_Tube

# Displays canvas in which are the fins's parameters
def DispFins():
    Fins_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC0.grid_remove()
    canvasAC2.grid_remove()
    canvasAC3.grid_remove()
    canvasAC1.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical fins in drawing
def DisplayFins():
    DispData()
    canvas3A.delete('all')
    canvas3B.delete('all')
    canvas3C.delete('all')

    VALUES_F = hallo(entries3)
    VALUES_D = hallo(entries0)

    if VALUES_F[0] == 3:
        canvas3A.configure(width=VALUES_F[1]/3+7, height=VALUES_D[0]/3+VALUES_F[3]/5, bg='white', highlightthickness=0,
                           bd=0, relief='ridge')  # 350 mm
        canvas3A.create_rectangle(1, 0, VALUES_F[1]/3+6, VALUES_D[0]/3-1, width=1, outline='blue')
        canvas3A.create_polygon(4, 2/3*VALUES_D[0]/3, VALUES_F[1]/3+4, 2/3*VALUES_D[0]/3, 7/8*VALUES_F[1]/3,
                                2/3*VALUES_D[0]/3+2/3*VALUES_F[3]/3, 7/8*VALUES_F[1]/3-VALUES_F[2]/3,
                                2/3*VALUES_D[0]/3+2/3*VALUES_F[3]/3, width=1, outline='blue', fill='')
        canvas3A.grid(row=3, column=7, rowspan=2, sticky='nw', in_=canvas0)

        canvas3B.configure(width=VALUES_F[1]/3+7, height=VALUES_F[3]/3+1, bg='white', highlightthickness=0, bd=0,
                           relief='ridge')  # 215 mm (height fins), 280 mm (length fins)
        canvas3B.create_polygon(4, VALUES_F[3]/3-1, VALUES_F[1]/3+4, VALUES_F[3]/3-1, 7/8*VALUES_F[1]/3, 0,
                                7/8*VALUES_F[1]/3-VALUES_F[2]/3, 0, width=1, outline='blue', fill='')
        canvas3B.grid(row=1, column=7, rowspan=2, sticky='sw', in_=canvas0)

        canvas3C.configure(width=1/3*VALUES_D[0]/3, height=VALUES_D[0]/3, bg='white', highlightthickness=0, bd=0,
                           relief='ridge')  # 50 mm
        canvas3C.create_polygon(1, 1, 1/3*VALUES_D[0]/3-1, 1/10*VALUES_D[0]/3, 1/3*VALUES_D[0]/3-1,
                                VALUES_D[0]/3-1/10*VALUES_D[0]/3+1, 1, VALUES_D[0]/3-1, width=1, outline='blue', fill='')
        canvas3C.grid(row=3, column=8, sticky='nw', ipadx=70, in_=canvas0)

# Get Fins length
def GetLenFins():
    VALUES_F = hallo(entries3)
    Len_Fins = VALUES_F[1]
    if Len_Fins != 0:
        return Len_Fins + 71
    else:
        return 0

# Displays Data
def DispData():

    # Name, Mass, Length, Max Diameter
    Name = 'Eiger'
    Mass = 3832
    Length = GetLenNose() + GetLenTube() + GetLenFins()
    Max_Diameter = GetMaxDiameter()

    canvas6.delete('all')
    canvas6.configure(width=250, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas6.create_text(125, 20, text='%s \nLength %.2f mm, max.diameter %.2f mm \nMass with motors %.2f g' % (Name,
                             Length, Max_Diameter, Mass), fill='black', font='Arial 8 italic',justify='left')
    canvas6.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='nw', in_=canvas0)

    # Stability, Centre de masse, Centre de pression, nombre de Mach
    Stability = 2.28
    CG = 114
    CP = 137
    Mach = 0.30

    canvas7.delete('all')
    canvas7.configure(width=100, height=50, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas7.create_text(50, 25, text='Stability : %s cal \nCG : %d cm \nCP %d cm \nat M=%d' % (Stability, CG, CP, Mach),
                        fill='black', font='Arial 8 italic', justify='left')
    canvas7.grid(row=0, column=6, columnspan=3, padx=10, pady=10, sticky='ne', in_=canvas0)

    # Apogee, Max velocity, Max acceleration, Nombre de Mach
    Apogee = 3040
    max_v = 107
    max_a = 49.8
    Mach_v = 0.32

    canvas8.delete('all')
    canvas8.configure(width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas8.create_text(100, 20, text='Apogee : %d m \nMax. velocity : %d m.s-1   (Mach %d) \nMax. acceleration : %d m.s-2'
                                      % (Apogee, max_v, Mach_v, max_a), font='Arial 8 italic', fill='blue', justify='left')
    canvas8.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='nw', in_=canvas0)

    # Put the rocket in middle of the canvas
    VALUES_D = hallo(entries0)
    canvasX.delete('all')
    canvasX.configure(width=250000/Length, height=VALUES_D[0] / 3, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvasX.grid(row=3, column=0, sticky='nsew', in_=canvas0)

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
#canvasA.grid_propagate('False')
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

canvasAC0 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')

canvasAC1 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')

canvasAC2 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')
# vbar2 = Scrollbar(canvasAC2, orient=VERTICAL)
# vbar2.grid(row=0, column=3, rowspan=10, sticky='ns', in_=canvasAC2)
# vbar2.config(command=canvasAC2.yview)
# canvasAC.configure(yscrollcommand=vbar2.set)

canvasAC3 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')
# vbar3 = Scrollbar(canvasAC3, orient=VERTICAL)
# vbar3.grid(row=0, column=3, rowspan=10, sticky='ns', in_=canvasAC3)
# vbar3.config(command=canvasAC3.yview)
# canvasAC.configure(yscrollcommand=vbar3.set)


# Choose Diameter
Diameter_choice = Button(fenetre, text='Diameter', bg='white', fg='black', cursor='hand2', relief=RAISED)
Diameter_choice.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky='nswe', in_=canvasAB)

entries0 = []
EntryButton(canvasAC0, 'Diameter', 0, 0, entries0)

Diameter_choice.bind("<Button-1>", lambda event: DispDiameter())

# Choose NoseCone
NoseCone_choice = Button(fenetre, text='Nosecone', bg='white', fg='black', cursor='hand2', relief=RAISED)
NoseCone_choice.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky='nswe', in_=canvasAB)

Inertia=Label(canvasAC2, text='Inertia Matrix of Nosecone', bg='gray85', fg='blue')
Inertia.grid(row=0, column=0, columnspan=3, padx=10, pady=2, in_=canvasAC2)

Len_Nose = 0
entries1 = []
EntryButton(canvasAC2, 'Length', 7, 0, entries1)
EntryButton(canvasAC2, '1', 1, 0, entries1)
EntryButton(canvasAC2, '2', 1, 1, entries1)
EntryButton(canvasAC2, '3', 1, 2, entries1)
EntryButton(canvasAC2, '4', 3, 0, entries1)
EntryButton(canvasAC2, '5', 3, 1, entries1)
EntryButton(canvasAC2, '6', 3, 2, entries1)
EntryButton(canvasAC2, '7', 5, 0, entries1)
EntryButton(canvasAC2, '8', 5, 1, entries1)
EntryButton(canvasAC2, '9', 5, 2, entries1)

DispN = Button(fenetre, text='Displays', command=lambda: DisplayNose())
DispN.grid(row=9, column=2, sticky='se', padx=10, pady=10, in_=canvasAC2)

NoseCone_choice.bind("<Button-1>", lambda event: DispNoseCone())

# Choose Tube
Tube_choice = Button(fenetre, text='Tube', bg='white', fg='black', cursor='hand2', relief=RAISED)
Tube_choice.grid(row=1, column=1, padx=10, pady=10, ipadx=25, ipady=10, sticky='nswe', in_=canvasAB)

InertiaTube=Label(canvasAC3, text='Inertia Matrix of Tube', bg='gray85', fg='blue')
InertiaTube.grid(row=0, column=0, columnspan=3, padx=10, pady=2, in_=canvasAC3)

entries2 = []
EntryButton(canvasAC3, 'Length', 7, 0, entries2)
EntryButton(canvasAC3, '1', 1, 0, entries2)
EntryButton(canvasAC3, '2', 1, 1, entries2)
EntryButton(canvasAC3, '3', 1, 2, entries2)
EntryButton(canvasAC3, '4', 3, 0, entries2)
EntryButton(canvasAC3, '5', 3, 1, entries2)
EntryButton(canvasAC3, '6', 3, 2, entries2)
EntryButton(canvasAC3, '7', 5, 0, entries2)
EntryButton(canvasAC3, '8', 5, 1, entries2)
EntryButton(canvasAC3, '9', 5, 2, entries2)

DispT = Button(fenetre, text='Displays', command=lambda: DisplayTube())
DispT.grid(row=9, column=2, sticky='se', padx=10, pady=10, in_=canvasAC3)

Tube_choice.bind("<Button-1>", lambda event: DispTube())

# Choose Fins
Fins_choice = Button(fenetre, text='Fins', bg='white', fg='black', cursor='hand2', relief=RAISED)
Fins_choice.grid(row=1, column=2, padx=10, pady=10, ipadx=27, ipady=10, sticky='nswe', in_=canvasAB)

entries3=[]
EntryButton(canvasAC1, 'Number', 0, 0, entries3)
EntryButton(canvasAC1, 'Root chord', 0, 1, entries3)
EntryButton(canvasAC1, 'Tip chord', 0, 2, entries3)
EntryButton(canvasAC1, 'Span', 2, 0, entries3)
EntryButton(canvasAC1, 'Sweep', 2, 1, entries3)
EntryButton(canvasAC1, 'Thickness', 2, 2, entries3)
EntryButton(canvasAC1, 'Phase', 4, 0, entries3)
EntryButton(canvasAC1, 'Body top offset', 4, 1, entries3)

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

motor_choice.grid(row=2, column=0, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe', in_=canvasAB)

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
env_choice.grid(row=2, column=1, padx=10, pady=10, ipadx=2, ipady=10, sticky='nswe', in_=canvasAB)

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

# Draw rocket
canvas1 = Canvas(fenetre)
canvas2 = Canvas(fenetre)
canvas3A = Canvas(fenetre)
canvas3B = Canvas(fenetre)
canvas3C = Canvas(fenetre)

# Update data
canvas6 = Canvas(fenetre)
canvas7 = Canvas(fenetre)
canvas8 = Canvas(fenetre)
canvasX = Canvas(fenetre)
# canvasY = Canvas(fenetre, width=830, height=20, bg='white', highlightthickness=0, bd=0, relief='ridge')
# canvasY.grid(row=0, column=1, columnspan=3, sticky='nsew', in_=canvas0)

# Bouton de sortie
# stop = Button(fenetre, text="x", bg='RED', fg='white', command=fenetre.quit)
# stop.grid(row=1, column=1, sticky='nswe', in_=canvasB)

# Disp window
fenetre.mainloop()
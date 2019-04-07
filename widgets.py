# GUI
# Author : Henri Faure
# Date : 4 April 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from tkinter import *

# Ouvre une fenetre
fenetre = Tk()

# Button(fenetre, text ="watch", relief=RAISED, cursor="watch").pack()
#
# label = Label(fenetre, text="Is your favorite color in the list? If yes which one?", bg='red')
# label.pack(side=TOP, padx=5, pady=5)
#
# # photo = PhotoImage(file="ERT_logo.png")
#
# b1 = Button(fenetre, text ="FLAT", relief=FLAT).pack()
# b2 = Button(fenetre, text ="RAISED", relief=RAISED).pack()
# b3 = Button(fenetre, text ="SUNKEN", relief=SUNKEN).pack()
# b4 = Button(fenetre, text ="GROOVE", relief=GROOVE).pack()
# b5 = Button(fenetre, text ="RIDGE", relief=RIDGE).pack()
#
# # Entrée
# value = StringVar()
# value.set("texte par défaut")
# entree = Entry(fenetre, textvariable=str, width=10)
# entree.pack()
#
# # Checkbutton
# bouton = Checkbutton(fenetre, text="Nouveau?")
# bouton.pack()

# # radiobutton
# value = StringVar()
# bouton1 = Radiobutton(fenetre, text="Oui", variable=value, value=1)
# bouton2 = Radiobutton(fenetre, text="Non", variable=value, value=2)
# bouton3 = Radiobutton(fenetre, text="Peu être", variable=value, value=3)
# bouton1.pack()
# bouton2.pack()
# bouton3.pack()

# liste
liste = Listbox(fenetre)
# liste.yscroll = Scrollbar(liste, orient=VERTICAL)
# liste.yscroll.pack(side=RIGHT, fill=Y)
#
# liste.list = Listbox(liste, yscrollcommand=liste.yscroll.set)
#
#
# liste.yscroll.config(command=liste.list.yview)
liste.insert(1, "red")
liste.insert(2, "green")
liste.insert(3, "blue")
liste.insert(4, "yellow")
liste.insert(5, "black")
liste.pack()



# canvas
# create_arc()        :  arc de cercle
# create_bitmap()     :  bitmap
# create_image()      :  image
# create_line()       :  ligne
# create_oval()       :  ovale
# create_polygon()    :  polygone
# create_rectangle()  :  rectangle
# create_text()       :  texte
# create_window()     :  fenetre
# canvas = Canvas(fenetre, width=250, height=120, background='yellow')
# ligne1 = canvas.create_line(25, 0, 25, 120)
# ligne2 = canvas.create_line(0, 80, 250, 80)
# txt = canvas.create_text(125, 60, text="ERT 2019", font="Arial 34 bold", fill="green")
# canvas.pack()

# Change coordinates of ligne1
# canvas.coords(ligne1, 15, 0, 15, 120)
#
# value = DoubleVar()
# scale = Scale(fenetre, variable=value)
# scale.pack()

fenetre['bg']='green'
#
# # frame 1
# Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
# Frame1.pack(side=LEFT, padx=30, pady=30)
#
# # frame 2
# Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
# Frame2.pack(side=LEFT, padx=10, pady=10)
#
# # frame 3 dans frame 2
# Frame3 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
# Frame3.pack(side=RIGHT, padx=5, pady=5)
#
# # Ajout de labels
# Label(Frame1, text="Frame 1").pack(padx=10, pady=10)
# Label(Frame2, text="Frame 2").pack(padx=10, pady=10)
# Label(Frame3, text="Frame 3", bg="white").pack(padx=10, pady=10)
#
# p = PanedWindow(fenetre, orient=HORIZONTAL)
# p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
# p.add(Label(p, text='Volet 1', background='blue', anchor=CENTER))
# p.add(Label(p, text='Volet 2', background='white', anchor=CENTER) )
# p.add(Label(p, text='Volet 3', background='red', anchor=CENTER) )
# p.pack()
#
# s = Spinbox(fenetre, from_=0, to=10)
# s.pack()
#
# l = LabelFrame(fenetre, text="Motor", padx=10, pady=10)
# l.pack(fill="both", expand="yes")
#
# Label(l, text="Choose motor").pack()

# Bouton de sortie
# bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
# bouton.pack(side=RIGHT, padx=5, pady=5)

# Affiche la fenetre
fenetre.mainloop()
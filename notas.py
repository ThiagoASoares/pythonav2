from sqlite3.dbapi2 import Cursor, Error
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from tkinter import StringVar
import sqlite3
from typing import TypeVar



app = tk.Tk()
app.geometry("800x500+500+130")
app.title("NOTAS DA FACULDADE")

materia=StringVar()
av1=StringVar()
av2=StringVar()
av3=StringVar()
avd=StringVar()
avds=StringVar()
media=StringVar()
result=StringVar()
professor=StringVar()
curso=StringVar()
newWindow = None
upWindows = None
telaPesquisar= None


def getConnection():
    try:
        conn = sqlite3.connect("faculdade.db")
    except sqlite3.Error as e:
        print("ERRO, Não foi possivel abrir uma conexão com o banco de Dados ", e)
    else:
        return conn
def createTable():
    query_notas = """CREATE TABLE IF NOT EXISTS notas( materia NOT NULL UNIQUE PRIMARY KEY,
                        av1 DOUBLE,
                        av2 DOUBLE,
                        av3 DOUBLE,
                        avd DOUBLE, 
                        avds DOUBLE,
                        media DOUBLE,
                        resultado TEXT,
                        FOREIGN KEY (materia) REFERENCES materias(materia))"""
    
    query_materias = """CREATE TABLE IF NOT EXISTS materias(
                    materia TEXT NOT NULL UNIQUE PRIMARY KEY, 
                    professor TEXT,
                    curso TEXT)"""
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query_notas)
    cursor.execute(query_materias)
    conn.commit()
    
    cursor.execute("SELECT * FROM 'notas' ORDER BY  materia")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    materia.set("")
    av1.set("")
    av2.set("")
    av3.set("")
    avd.set("")
    avds.set("")
    



def cadastrarMateria():
    if materia.get() == "" or professor.get() == "" or curso.get() == '' :
        resultado = tk.showwarning("", "Por favor, digite todos os  campos.", icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = getConnection()
        cursor = conn.cursor()
        query = """INSERT INTO 'materias' (materia, professor, curso) VALUES (?, ?, ?)"""
        cursor.execute(query, (str(materia.get()), str(professor.get()), str(curso.get())))
        conn.commit()
        cursor.execute("SELECT * FROM 'notas' ORDER BY materia")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        materia.set("")
        professor.set("")
        curso.set("")
        upWindows.destroy()
def calcularMedia():
    av1p = float(av1.get())
    av2p = float(av2.get())
    avdp = float(avd.get())
    if av1.get() < av2.get() and av3.get() > av1.get() :
        av1p= float(av3.get())
    elif av1.get() > av2.get() and av3.get() > av2.get() :
        av2p=float(av3.get())
    elif avd.get() < avds.get():
        avdp= float(avds.get())
    media1 = (av1p + av2p + avdp)/3
    media.set(str(media1))
    if media1 >= 6:
        result.set("APROVADO")
    elif media1 < 6:
        result.set("REPROVADO")

def incluirNotas():
    if materia.get() == "" or av1.get() == "" or av2.get() == '' or avd.get() == '':
        resultado = tk.showwarning("", "Por favor, digite todos os  campos.", icon="warning")
    else:
        calcularMedia()
        tree.delete(*tree.get_children())
        conn = getConnection()
        cursor = conn.cursor()
        query = """INSERT INTO 'notas' (materia, av1, av2, av3, avd , avds , media, resultado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(query,(str(materia.get()), str(av1.get()), str(av2.get()), str(av3.get()), str(avd.get()),str(avds.get()),str(media.get()),str(result.get())))
                    
        conn.commit()
        cursor.execute("SELECT * FROM 'notas' ORDER BY materia")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        materia.set("")
        av1.set("")
        av2.set("")
        av3.set("")
        avd.set("")
        avds.set("")
        newWindow.destroy()



def telaIncluirNotas():
    if  tree.selection():
        resultado = msb.showwarning(
            "", "Por favor, selecione a Materia que deseja incluir as notas.", icon="warning")
    else:
        global newWindow
        newWindow = Toplevel()
        newWindow.title("Incluir Notas")
        formTitle = Frame(newWindow)
        formTitle.pack(side=TOP)
        formContact = Frame(newWindow)
        formContact.pack(side=TOP, pady=10)
        width = 400
        height = 400
        screen_width = newWindow.winfo_screenwidth()
        screen_height = newWindow.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
        newWindow.resizable(0, 0)
               
        lbl_title = Label(formTitle, text="Incluindo notas",
                        font=('arial', 18), bg='blue', width=300)
        lbl_title.pack(fill=X)
        lbl_materia = Label(formContact, text='Matéria', font=('arial', 12))
        lbl_materia.grid(row=0, sticky=W)
        lbl_av1 = Label(formContact, text='Av1', font=('arial', 12))
        lbl_av1.grid(row=1, sticky=W)
        lbl_av2 = Label(formContact, text='Av2', font=('arial', 12))
        lbl_av2.grid(row=2, sticky=W)
        lbl_av3 = Label(formContact, text='Av3', font=('arial', 12))
        lbl_av3.grid(row=3, sticky=W)
        lbl_avd = Label(formContact, text='Avd', font=('arial', 12))
        lbl_avd.grid(row=4, sticky=W)
        lbl_avds = Label(formContact, text='Avds', font=('arial', 12))
        lbl_avds.grid(row=5, sticky=W)

        materiaEntry = Entry(formContact, textvariable=materia, font=('arial', 12))
        materiaEntry.grid(row=0, column=1)
        av1Entry = Entry(formContact, textvariable=av1, font=('arial', 12))
        av1Entry.grid(row=1, column=1)
        av2Entry = Entry(formContact, textvariable=av2, font=('arial', 12))
        av2Entry.grid(row=2, column=1)
        av3Entry = Entry(formContact, textvariable=av3, font=('arial', 12))
        av3Entry.grid(row=3, column=1)
        avdEntry = Entry(formContact, textvariable=avd, font=('arial', 12))
        avdEntry.grid(row=4, column=1)
        avdsEntry = Entry(formContact, textvariable=avds, font=('arial', 12))
        avdsEntry.grid(row=5, column=1)

        btn_include = Button(formContact, text="Incluir",
                           width=50, command=incluirNotas)
        btn_include.grid(row=6, columnspan=2, pady=10)


        
def telaIncluirMaterias():
    global upWindows
    upWindows = Toplevel()
    upWindows.title("Matérias")
    formTitle = Frame(upWindows)
    formTitle.pack(side=TOP)
    formContact = Frame(upWindows)
    formContact.pack(side=TOP, pady=10)
    width = 500
    height = 300
    screen_width = upWindows.winfo_screenwidth()
    screen_height = upWindows.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    upWindows.geometry("%dx%d+%d+%d" % (width, height, x, y))
    upWindows.resizable(0, 0)

    lbl_title = Label(formTitle, text="MATÉRIAS",font=('arial', 18), bg='blue', width=300)
    lbl_title.pack(fill=X)
    lbl_materia = Label(formContact, text='MATÉRIA', font=('arial', 12))
    lbl_materia.grid(row=0, sticky=W)
    lbl_professor = Label(formContact, text='PROFESSOR', font=('arial', 12))
    lbl_professor.grid(row=1, sticky=W)
    lbl_curso = Label(formContact, text='CURSO', font=('arial', 12))
    lbl_curso.grid(row=2, sticky=W)
    
    materiaEntry = Entry(formContact, textvariable=materia , font=('arial', 12))
    materiaEntry.grid(row=0, column=1)
    professorEntry = Entry(formContact, textvariable=professor , font=('arial', 12))
    professorEntry.grid(row=1, column=1)
    cursoEntry = Entry(formContact, textvariable=curso , font=('arial', 12))
    cursoEntry.grid(row=2, column=1)
    
    btn_incluir = Button(formContact, text="Incluir",width=20, bg= 'green', command=cadastrarMateria)
    btn_incluir.grid(row=6, column=0, pady=10, padx=5)
    btn_pesquisar = Button(formContact, text="Pesquisar",width=20, bg='yellow', command=telaPesquisarMateria)
    btn_pesquisar.grid(row=6, column=3, pady=10)
    
def telaPesquisarMateria():
    telaPequisar = Toplevel()
    telaPequisar.geometry("800x300+500+150")
    top = Frame(telaPequisar, width=500, bd=1, relief=SOLID)
    top.pack(side=TOP)
    mid = Frame(telaPequisar, width=500)
    mid.pack(side=TOP)
    midleft = Frame(mid, width=100)
    midleft.pack(side=LEFT, pady=10)
    midright = Frame(mid, width=100)
    midright.pack(side=RIGHT, pady=10)
    midleftPadding = Frame(mid, width=350)
    midleftPadding.pack(side=LEFT)
    midright = Frame(mid, width=100)
    midright.pack(side=RIGHT, pady=10)     
    bottom = Frame(telaPequisar, width=200)
    bottom.pack(side=BOTTOM) 
    tableMargin = Frame(telaPequisar, width=300)
    tableMargin.pack() 
    
    btn_Alterar = Button(midleft, text="Alterar",bg="yellow")# command=telaIncluirMaterias)
    btn_Excluir = Button(midright,text="Excluir",bg= "red")#command=telaIncluirNotas)

    scrollbarY = Scrollbar(tableMargin, orient=VERTICAL)
    tree1 = ttk.Treeview(tableMargin,columns=('materia','professor','curso'), height=400, selectmode="extended", yscrollcommand=scrollbarY.set)
    scrollbarY.config(command=tree1.yview)
    scrollbarY.pack(side=RIGHT, fill=Y)
    tree1.column('#0', stretch=NO, minwidth=0, width=1)
    tree1.column('materia',minwidth=0,width=250)
    tree1.column('professor',minwidth=0,width=160)
    tree1.column('curso',minwidth=0,width=160)
    tree1.heading('materia',text='MATÉRIA')
    tree1.heading('professor',text='PROFESSOR')
    tree1.heading('curso',text='CURSO')
    btn_Alterar.pack()
    btn_Excluir.pack()
    tree1.pack()
    lbl_notas = Label(bottom, text="Para Alterar ou Excluir selecione a matéria na lista", font=('arial', 12), width=200)
    lbl_notas.pack(fill=X)
    



     


top = Frame(app, width=500, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Frame(app, width=500)
mid.pack(side=TOP)
midleft = Frame(mid, width=100)
midleft.pack(side=LEFT, pady=10)
midright = Frame(mid, width=100)
midright.pack(side=RIGHT, pady=10)
midleftPadding = Frame(mid, width=350)
midleftPadding.pack(side=LEFT)
midright = Frame(mid, width=100)
midright.pack(side=RIGHT, pady=10)     
bottom = Frame(app, width=200)
bottom.pack(side=BOTTOM) 
tableMargin = Frame(app, width=300)
tableMargin.pack() 
   
btn_Materia = Button(midleft, text="CADASTRAR MATERIA",
                  bg="cornflower blue", command=telaIncluirMaterias)
btn_Notas = Button(midright,text="INCLUIR NOTAS",bg= "yellow",command=telaIncluirNotas)



scrollbarY = Scrollbar(tableMargin, orient=VERTICAL)
tree = ttk.Treeview(tableMargin,columns=('materia','av1','av2','av3','avd','avds','media','situacao'), height=400, selectmode="extended", yscrollcommand=scrollbarY.set)
scrollbarY.config(command=tree.yview)
scrollbarY.pack(side=RIGHT, fill=Y)
tree.column('#0', stretch=NO, minwidth=0, width=1)
tree.column('materia',minwidth=0,width=250)
tree.column('av1',minwidth=0,width=60)
tree.column('av2',minwidth=0,width=60)
tree.column('av3',minwidth=0,width=60)
tree.column('avd',minwidth=0,width=60)
tree.column('avds',minwidth=0,width=60)
tree.column('media',minwidth=0,width=60)
tree.column('situacao',minwidth=0,width=80)
tree.heading('materia',text='MATERIA')
tree.heading('av1',text='AV1')
tree.heading('av2',text='AV2')
tree.heading('av3',text='AV3')
tree.heading('avd',text='AVD')
tree.heading('avds',text='AVDS')
tree.heading('media',text='MÉDIA')
tree.heading('situacao',text='SITUAÇÃO')
btn_Materia.pack()
btn_Notas.pack()

tree.pack()

  
if __name__ == '__main__':
    createTable()
    app.mainloop()


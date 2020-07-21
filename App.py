from tkinter import *
from tkinter import ttk,filedialog,messagebox
import tkinter as tk
import speech_recognition as sr
import os,time

filePath = ''

def addTab():
    vc = sr.Recognizer()
    def convert(audio):
        try:
            say = vc.recognize_google(audio,language="th-TH")
            print(say)
            if choice.get() == 0:
                Eappname.delete(0,END)
                Eappname.insert(0,say)
            else:
                Ewebname.delete(0,END)
                Ewebname.insert(0,say)
        except sr.UnknownValueError:
            print("ไม่เข้าใจ")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def listen():
        with sr.Microphone() as source: #เปิดไมค์
            vc.adjust_for_ambient_noise(source)
            print('เริ่มพูด')
            audio = vc.listen(source,timeout=5)
            convert(audio)


    def add():
        direct = (os.getcwd() + '\\Open.txt')
        openFile = open(direct,'a')
        openFile.write('\n')
        if choice.get() == 0:
            sentence = ('app '  + filePath  + ' '+ (Eappname.get()).lower() )
            print(sentence)
        elif choice.get() == 1:
            sentence = ('website '  + Eweburl.get()  + ' ' + (Ewebname.get()).lower() ) 
            print(sentence)
        openFile.write(sentence)
        openFile.close()
        
        
    def getPath():
        global filePath
        filePath = filedialog.askopenfilename(initialdir =  "/", title = "Select A File")
        filePath = filePath.replace(' ','?').lower()
        print(filePath)


    def ShowChoice():

        print(choice.get())
        if choice.get() == 0:
            try:
                Lwebname.grid_forget()
                Ewebname.grid_forget()
                Bapppath.grid_forget()
                Lweburl.grid_forget()
                Eweburl.grid_forget()
                Badd.grid_forget()
            except:
                pass
            Lappname.grid(row=2,column=0,pady=5)
            Eappname.grid(row=2,column=1)
            Lapppath.grid(row=3,column=0,pady=5)
            Bapppath.grid(row=3,column=1)
            Bappname.grid(row=4,column=0)
            Badd.grid(row=4,column=1)
        elif choice.get() == 1:
            try:
                Lappname.grid_forget()
                Eappname.grid_forget()
                Bwebname.grid_forget()
                Lapppath.grid_forget()
                Bapppath.grid_forget()
                Badd.grid_forget()
            except:
                pass
            Lwebname.grid(row=2,column=0,pady=5)
            Ewebname.grid(row=2,column=1)
            Lweburl.grid(row=3,column=0,pady=5)
            Eweburl.grid(row=3,column=1)
            Bwebname.grid(row=4,column=0)
            Badd.grid(row=4,column=1)
            
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            addTab.destroy()
            root.destroy()


    def getback():
        addTab.destroy()
        root.deiconify()


    root.withdraw()
    addTab = Toplevel()
    addTab.title("Add menu")
    addTab.geometry("300x200")
    addTab.resizable(0,0)

            
    choice = tk.IntVar()
    choice.set(2)  # initializing the choice, i.e. Python

    webOrApp = [("Application"),("Website")]
    Badd = ttk.Button(addTab,text='เพิ่มข้อมูล',command=add)

    Lappname = ttk.Label(addTab,text='Application  : ')
    Eappname = ttk.Entry(addTab,width=20)
    Lapppath = ttk.Label(addTab,text='Path  : ')
    Bapppath = ttk.Button(addTab,text='Path',command=getPath)
    Bappname = ttk.Button(addTab,text='พูดชื่อเเอป',command=listen)

    Lwebname = ttk.Label(addTab,text='Website  : ')
    Ewebname = ttk.Entry(addTab,width=20)
    Lweburl = ttk.Label(addTab,text='URL  :')
    Eweburl = ttk.Entry(addTab,width=20)
    Bwebname = ttk.Button(addTab,text='พูดชื่อเว็ป',command=listen)

    Bclose = ttk.Button(addTab,text='Back',command=getback)
    Bclose.grid(row=0,column=0,pady=10)


    for val, webOrApp in enumerate(webOrApp):
        tk.Radiobutton(addTab, 
                    text=webOrApp,
                    padx = 20, 
                    variable=choice, 
                    command=ShowChoice,
                    value=val).grid(row=1,column=val)

    addTab.protocol("WM_DELETE_WINDOW", on_closing)
    addTab.mainloop()

    
def delTab():
    
    def createList():
        frame = Frame(delTab)
        frame.pack()

        listNodes = Listbox(frame, width=20, height=20, font=("Helvetica", 12))
        listNodes.pack(side="left", fill="y")

        scrollbar = Scrollbar(frame, orient="vertical")
        scrollbar.config(command=listNodes.yview)
        scrollbar.pack(side="right", fill="y")

        listNodes.config(yscrollcommand=scrollbar.set)
        for x in range(100):
            listNodes.insert(END, str(x))

        

    def getback():
        delTab.destroy()
        root.deiconify()


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            delTab.destroy()
            root.destroy()


    root.withdraw()
    delTab = Toplevel()
    delTab.title('delete menu')
    delTab.geometry("300x200")
    delTab.resizable(0,0)

    Bback = ttk.Button(delTab,text='Back',command=getback)
    Bback.grid(row=0,column=0,padx=10,pady=10)

    ttk.Label(delTab,text='Type').grid(row=1,column=0)
    ttk.Label(delTab,text='Name').grid(row=1,column=1)

    delTab.protocol("WM_DELETE_WINDOW", on_closing)

    createList()

    delTab.mainloop()

root = Tk()
root.title("Voice recognization")
root.geometry("300x200")
root.resizable(0,0)

ttk.Label(root,text='Voice recognization').pack(anchor=N,pady=15)
ttk.Button(root,text='Add list',command=addTab).pack(anchor=N,pady=10)
ttk.Button(root,text='delete list',command=delTab).pack(anchor=N)
ttk.Button(root,text='Start').pack(anchor=N,pady=10)

root.mainloop()
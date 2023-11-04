from tkinter import *
from tkinter import ttk,filedialog,messagebox
import tkinter as tk
import threading
import speech_recognition as sr
import os,time

def voice_Input():
    vc = sr.Recognizer()
    def main(audio):#รับฟัง
        try:
            say = vc.recognize_google(audio,language="th-TH")
            print(say)
            text.config(text = say)
        except sr.UnknownValueError:
            print("ไม่เข้าใจ")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        status.config(text = "Status : Stand By")
        button.config(text = "Start")
        button["state"] = NORMAL

    def listening():
        
        with sr.Microphone() as source: #เปิดไมค์
            
            print('พูดไรหน่อย')
            audio = vc.listen(source)
            main(audio)

    status.config(text = "Status : Listening")
    button.config(text = "Listening")
    button["state"] = DISABLED
    threading.Thread(target=listening).start()
    






root = Tk()
root.title("SMART FARM")
root.geometry("300x200")
root.resizable(0,0)


status = ttk.Label(root,text='Status : Stand By')
status.pack(anchor=N,pady=15)
button = ttk.Button(root,text='Start',command = voice_Input)
button.pack(anchor=N,pady=10)
text = ttk.Label(root,text='')
text.pack(anchor=N,pady=5)

root.mainloop()


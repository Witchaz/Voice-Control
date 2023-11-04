import speech_recognition as sr
from gtts import gTTS
import os,subprocess,webbrowser,playsound,pathlib,time



def main(audio):#รับฟัง
    try:
        say = vc.recognize_google(audio,language="th-TH")
        print(say)
        
    except sr.UnknownValueError:
        print("ไม่เข้าใจ")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


vc = sr.Recognizer()

with sr.Microphone() as source: #เปิดไมค์
    vc.adjust_for_ambient_noise(source)
    while True:
            print('พูดไรหน่อย')
            audio = vc.listen(source)
            main(audio)
  
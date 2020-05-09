import speech_recognition as sr
from gtts import gTTS
import os,subprocess,webbrowser,playsound,pathlib,time
import AudioController as ac
import Searching

def command(say): #รับคำสั่ง
    sentence = say.split()
    if 'เปิด' in say:
        for i in range(len(open_list)): ##ไล่เเถวลงมาเพื่อตรวจสอบว่ามีชื่อในนั้นไหม
            if any(word in say for word in Appname):
                if Appdata[i][0] == 'website':
                    print(Appname[i])
                    #webbrowser.get(using='windows-default').open(Appdata[i][1])
                elif Appdata[i][0] == 'app':
                    subprocess.Popen([Appdata[i][1]],shell=True)
    elif 'ค้นหา' in say:
        find = say.replace('ค้นหา','')
        search = Searching(find)
        search.fill()
    elif 'ปรับเสียง' in say :
        print()
def feedback(say): ## ตอบกลับด้วยเสียง
    tts = gTTS(say,lang='th')
    tts.save('Speak.mp3')
    playsound.playsound('Speak.mp3')
    os.remove('Speak.mp3')


def check(audio):#รับฟัง
    try:
        #r.adjust_for_ambient_noise()
        say = r.recognize_google(audio,language="th-TH")
        print(say)
        feedback(say)
        command(say)
        
        
    except sr.UnknownValueError:
        print("ไม่เข้าใจ")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()

with open('Open.txt') as op: #โหลดไฟล์ 
    open_list = op.read().splitlines()
    Appdata = [i.split() for i in open_list]
    Appname = []
    for i in range(len(open_list)):
        try:
            App = (Appdata[i][2:])
            Appname.append(' '.join(App))
        except:
            pass
    
    
    

with sr.Microphone() as source: #เปิดไมค์
    r.adjust_for_ambient_noise(source)
    while True:
            print('พูดไรหน่อย')
            audio = r.listen(source)
            check(audio)
 
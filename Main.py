import speech_recognition as sr
from gtts import gTTS
import os,subprocess,webbrowser,playsound,pathlib,time
#import AudioController as ac

ppmode = 0
class Searching:
    def __init__(self,Search):
        self.search = Search
        self.url = "https://www.google.com.tr/search?q={}".format(self.search)
        webbrowser.get('windows-default').open(url=self.url) 

def command(say): #รับคำสั่ง
    if 'เปิด' in say:
        say = say.lower()
        print(say)
        if any(word in say for word in Appname):
            print('work here!')
            for i in range(len(Appname)):
                if Appname[i].upper() in say.upper():
                    AppOp = Appname[i]
                    break
            lines = Appname.index(AppOp)
            if Appdata[lines][0] == 'website':
                print('web work!!')
                webbrowser.get(using='windows-default').open(Appdata[lines][1])
            elif Appdata[lines][0] == 'app':
                print('app work!!')
                app_path = (Appdata[lines][1])
                app_path = app_path.replace('?',' ')
                subprocess.Popen(app_path,shell=True,)
                #subprocess.Popen([Appdata[lines][1]],shell=True)
            mustSay = "เปิด {} เเล้ว".format(AppOp)
            return mustSay
        else :  
            return say
        
    elif 'ค้นหา' in say:
        find = say.replace('ค้นหา','')
        search = Searching(find)
        mustSay = "ค้นหา {} เเล้ว".format(find)
        return mustSay
    else :
        return say

def feedback(mustSay): ## ตอบกลับด้วยเสียง
    tts = gTTS(mustSay,lang='th')
    tts.save('Speak.mp3')
    playsound.playsound('Speak.mp3')
    os.remove('Speak.mp3')


def main(audio):#รับฟัง
    try:
        
        say = vc.recognize_google(audio,language="th-TH")
        print(say)
        mustSay = command(say)
        #feedback(mustSay)
        
        
    except sr.UnknownValueError:
        print("ไม่เข้าใจ")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


vc = sr.Recognizer()

with open('Open.txt') as op: #โหลดไฟล์ 
    open_list = op.read().splitlines()
    Appdata = [i.split() for i in open_list]
    Appdata.sort(key=len,reverse=True)
    Appname = []
    for i in range(len(open_list)):
        try:
            App = (Appdata[i][2:])
            Appname.append(' '.join(App))
        except:
            pass
    
    print(Appname)

with sr.Microphone() as source: #เปิดไมค์
    vc.adjust_for_ambient_noise(source)
    while True:
            print('พูดไรหน่อย')
            audio = vc.listen(source)
            main(audio)
 
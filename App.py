from tkinter import *
from gtts import gTTS
from tkinter import ttk,filedialog,messagebox
import tkinter as tk
import threading,playsound
import speech_recognition as sr
import os,time,json
from google.cloud import dialogflow
import constants
from io import BytesIO
def voice_Input():
    def tts(text):
        # mp3_fp = BytesIO()
        tts = gTTS(text,lang='th')
       # tts.write_to_fp(mp3_fp)
        try:
            tts.save('Speak.mp3')
            playsound.playsound('Speak.mp3')
            os.remove('Speak.mp3')
        except:
            pass
        
            

    def detect_intent_texts(project_id, session_id, text, language_code):
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        print("Session path: {}\n".format(session))

    
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        s = (format((response.query_result.fulfillment_messages[0].text)))
        s.replace('\\','\\\\')
        decoded_text = bytes(s, 'utf-8').decode('unicode-escape').encode('latin1').decode('utf-8')
        print(decoded_text)
        first = decoded_text.find('"')
        respond_text.config(text=decoded_text[first+1:-2])
        return decoded_text


    vc = sr.Recognizer()
    def main(audio):#รับฟัง
        try:
            say = vc.recognize_google(audio,language="th-TH")
            print(say + "\n\n")
            send_text.config(text = say)
            respond = detect_intent_texts(constants.PROJECT_ID,constants.SESSION_ID,say,constants.LANGUAGE_CODE)
            tts(respond)
            

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
send_text = ttk.Label(root,text='')
send_text.pack(anchor=N,pady=5)
respond_text = ttk.Label(root,text='')
respond_text.pack(anchor=N,pady=0)

root.mainloop()


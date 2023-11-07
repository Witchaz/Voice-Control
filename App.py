from tkinter import *
from tkinter import ttk,filedialog,messagebox
import tkinter as tk
import threading,playsound
import speech_recognition as sr
import os,time
from google.cloud import dialogflow
import constants

def voice_Input():
    def tts(text):
        from google.cloud import texttospeech

        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="th-Thai", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )


        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )


        with open("speak.mp3", "wb") as out:
            out.write(response.audio_content)
            print('Audio content written to file "speak.mp3"')
            out.close()
        
        try:
            playsound.playsound('speak.mp3')
        except FileNotFoundError:
            print("File not found")
            
        os.remove("speak.mp3")    
        
        
            

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
        return format(response.query_result.fulfillment_text);


    vc = sr.Recognizer()
    def main(audio):#รับฟัง
        try:
            say = vc.recognize_google(audio,language="th-TH")
            print(say + "\n\n")
            text.config(text = say)
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
text = ttk.Label(root,text='')
text.pack(anchor=N,pady=5)

root.mainloop()


# -*- coding: utf-8 -*-
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import sys
import os
import random
from tkinter import *
from tkinter import ttk
import threading

imgname="image.png"
output_mp3 = "./mp3_dir/speech.mp3"

repeat_list = ["いただきます",
               "ごちそうさまでした",
               "ごちそうさま",
               "こんにちは",
               "おはよう",
               "おはようございます",
               "こんばんは",
               "さようなら",
               "さよなら",
               "またね",
               "お疲れ",
               "おつかれ",
               "おやすみ"
               ]

aizuchi_list = ["わかる",
                "それな",
                "うける",
                "わかりみが深み",
                "いやまじでそれ",
                "それはやばい",
                "ははは",
                "あーね"
                ]
                
finish_list = ["ごちそうさま",
                "ごちそうさまでした",
                "おわり",
                "さようなら",
                "さよなら",
                "終わり",
                "またね",
                "おやすみ"
                ]



def meshitomo_message(phrase):
    print("メシ友さん:" + phrase)
    tts=gTTS(text=phrase, lang="ja")
    tts.save(output_mp3)
    playsound(output_mp3)

def get_audio():
    r = sr.Recognizer()
    mic = sr.Microphone()
    phrase = ""
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=6)
            phrase = r.recognize_google(audio, language='ja-JP')
    except sr.WaitTimeoutError:
        meshitomo_message("もう一度お願いします")
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        meshitomo("インターネットの接続状況の調子が悪いかも{0}".format(e))
    return phrase

def main1():
    loop = False
    while(True):
        if os.path.exists(output_mp3):
            os.remove(output_mp3)
        phrase = get_audio()
        if phrase == "":
            continue
        if phrase in repeat_list:
            loop = True
        if(loop):
            print("あなた：" + phrase)
            if phrase in repeat_list:
                meshitomo_message(phrase)
                if phrase in finish_list:
                    sys.exit()
                    break
            else:
                if phrase in finish_list:
                    sys.exit()
                    break
                meshitomo_message(random.choice(aizuchi_list))

def main2():
    win = Tk()
    win.title('メシ友さん')
    pngfile=PhotoImage(file=imgname)
    cv=Canvas(bg="white",width=800-1,height=768-1)
    cv.create_image(1,1,image=pngfile,anchor=NW)
    cv.grid(row=1, column=1)
    win.mainloop()

thread_2 = threading.Thread(target=main2)
if __name__ == "__main__":

    thread_2.setDaemon(True)
    thread_2.start()
    main1()
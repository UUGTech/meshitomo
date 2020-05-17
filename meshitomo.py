# -*- coding: utf-8 -*-
'''
* @author UUGTech
* @copyright 2020 by UUGTech
'''
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

# 同じ言葉を返すリスト
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

# テキトーに相槌
aizuchi_list = [
                "わかりみが深み",
                "いやまじでそれ",
                "本当にそれな",
                "おっしゃる通り",
                "わかるわー"
                ]

# 終了コマンド
finish_list = ["ごちそうさま",
                "ごちそうさまでした",
                "おわり",
                "さようなら",
                "さよなら",
                "終わり",
                "またね",
                "おやすみ"
                ]

# メシ友さんに喋らせる
def meshitomo_message(phrase):
    if os.path.exists(output_mp3):
            os.remove(output_mp3)
    print("メシ友さん:" + phrase)
    tts=gTTS(text=phrase, lang="ja")
    tts.save(output_mp3)
    playsound(output_mp3)

# 音声を聞きとる
def get_audio():
    r = sr.Recognizer()
    mic = sr.Microphone()
    phrase = ""
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            phrase = r.recognize_google(audio, language='ja-JP')
    except sr.WaitTimeoutError:
        meshitomo_message("もう一度お願いします")
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        meshitomo("インターネットの接続状況の調子が悪いかも{0}".format(e))
    return phrase

# 会話ループ
def main1():
    loop = False
    meshitomo_message("メシ友さん起動しました。一緒にご飯を食べましょう")
    while(True):
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

# ウィンドウ描画（メシ友さん誕生）
def main2():
    win = Tk()
    win.title('メシ友さん')
    pngfile=PhotoImage(file=imgname)
    cv=Canvas(bg="white",width=800-1,height=768-1)
    cv.create_image(1,1,image=pngfile,anchor=NW)
    cv.grid(row=1, column=1)
    win.mainloop()


#--------------------Main--------------------#
if __name__ == "__main__":
    # ウィンドウ描画と会話ループは別スレッド
    thread_2 = threading.Thread(target=main2)
    thread_2.setDaemon(True)
    thread_2.start()
    main1()
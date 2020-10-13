import pyttsx3
import datetime
import speech_recognition as sr
import os
import wikipedia
import webbrowser
import random
import time
import requests
import json
from dadjokes import Dadjoke
import reverse_geocoder as rg

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

from youtubesearchpython import SearchVideos

# speaking function
def speak(str):

    converter = pyttsx3.init()
    converter.setProperty('rate',150)

    converter.setProperty('volume',1)
    voice=converter.getProperty('voices')
    converter.setProperty('voice',voice[1].id)
    converter.say(str)
    converter.runAndWait()

def wishme():
    list=['hey  let\'s get start','I have been waiting for you so badly','let\'s blast today']
    greet=random.choice(list)
    x=datetime.datetime.now()
    day=x.strftime("%A")
    hour=int(x.hour)
    if hour in range(0,13):
        speak(f"Good morning sir what is your plan for{day} {greet}")
        # speak(greet)
    elif hour in range(13,19):
        speak(f"Good afternoon BUDDY {greet}")
        # speak(greet)
    else:
        speak(f"good evening buddy {greet}")
        # speak(greet)
def listening():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening......")
        r.pause_threshold=1.2
        audio=r.listen(source)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"user said {query}")
    except Exception as e:
        print("say that again plz")
        return "none"
    return query

# open browser
def opentask(url):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))
    webbrowser.get('chrome').open_new_tab(url)


def closetask():
    os.system("taskkill /im chrome.exe /f")


def msg(message,number):

    url='https://www.fast2sms.com/dev/bulk'
    params={
        'authorization':'RBkqGN1o3zrV6YD5bKFWlTnQyIe8i02CE7LjwU9AsvuagdXcfx9nLNBDwVhGK10PJI24f68je5ryMavg',
        'sender_id':'FSTSMS',
        'message':message,
        'language':'english',
        'route':'p',
        'numbers':number
    }
    response = requests.get(url,params=params)
    val=response.json()
    speak(f"message has been sent")
#    space information
def space1():
    url = 'https://api.nasa.gov/planetary/apod?api_key=5zIdEfvez6tXFKS1v90e88PhEwFOsDSfgcw5UX8m'
    params = {
        'concept_tags': 'True'
    }
    response = requests.get(url, params=params)
    x = response.json()
    print(x)
    try:
        opentask(x['hdurl'])
    except :
        opentask(x['url'])
    speak(f"you are going to {x['title']}")
    speak(f"today\'s picture is about {x['explanation']}")

def space2():
    now=datetime.datetime.now()

    url = 'https://epic.gsfc.nasa.gov/api/images.php?date=2015-10-31'
    response = requests.get(url)
    x = response.json()

    link = 'http://epic.gsfc.nasa.gov/epic-archive/jpg/' + x[1]['image'] + '.jpg'
    opentask(link)
    speak(f"{x[1]['caption']}")

# jokes

def joke():
    dadjoke = Dadjoke()
    print(dadjoke.joke)
    speak(dadjoke.joke)
#     Iss currrent location showing
def ISS():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    val = json.loads(response.text)
    # print(val)
    lat =float((val['iss_position']['latitude']))
    lon = float((val['iss_position']['longitude']))

    coordinates = (lat,lon)

    results = rg.search(coordinates)  # default mode = 2

    print(results)
    val1=results[0]['name']
    speak(f"currently ISS is passing from {results[0]['name']} {results[0]['admin1']}{results[0]['admin2']} and country is{results[0]['cc']}")
    speak(" i am opening google map for ISS passing place")
    opentask(f"https://www.google.com/maps/search/{lat},{lon}/@{lat},{lon},13z")
    speak("ISS moving speed is 7.66 km per second")

if __name__ == '__main__':
    wishme()

    while 1:

        query = listening().lower()
        path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

        if 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query,sentences=1)
            speak(f"according to wikipedia f{result}")

        elif 'search youtube' in query:
            # opentask("youtube.com")
            num=["first","second","third","fourth","fifth"]

            speak("what you want to search ")
            query=listening().lower()
            search = SearchVideos(query, offset=1, mode="json", max_results=5)
            obj=json.loads(search.result())
            lis=[]
            for i in range(5):
               lis.append(obj['search_result'][i]['link'])
            speak("top 5 result have been found")
            dic = {
                num[0]: lis[0], num[1]: lis[1], num[2]: lis[2], num[3]: lis[3], num[4]: lis[4]
            }
            speak("which result you want to execute")
            query=listening().lower()

            for i in range(5):
                if num[i] in query:
                    speak(f"opening {num[i]} result in the youtube")
                    if num[i] in dic:
                        opentask(dic[num[i]])
                    else:
                        speak("sorry invalid result ")

        elif 'open google' in query:
            # wb.get('chrome %s').open_new_tab('google.com')
            opentask("google.com")
        elif 'close google' in query:
            speak("closing google")
            closetask()
        elif 'close youtube' in query:
            speak("closing youtube")
            closetask()
        elif 'play music' in query:
            time.sleep(3)
            speak("for music i am opening spotify web")
            opentask("https://open.spotify.com/")
            time.sleep(2)
            speak("play whatever song you like ")
            time.sleep(2)
            speak("enjoy your music world")
        elif 'stop music' in query:
            speak("stoping music")
            closetask()


        elif 'the time' in query:
            stre = datetime.datetime.now().strftime("%H:%M:%S")
            x = datetime.datetime.now()
            day = x.strftime("%A")
            speak(f"it is {day} and time is {stre}")
        elif 'shutdown computer' in query:
            speak("do you really want to shutdown")
            query=listening().lower()


            if 'yes'in query:
                speak("say password to execute process")
                query = listening().lower()
                trail = 3
                while trail!=0:
                    with open("PASSWORD.txt","r") as f:
                        pwd=f.readline()

                    if query==pwd:
                        os.system("shutdown /s /t 1")
                    else:
                        speak("sorry say true password")
                        query=listening().lower()
                        trail-=1
                        speak(f"you have {trail} attempt remained")
                speak("you have attempted three wrong password please try again after while")
        elif  'change the password' in query:
            while 1:
                speak("tell me old password to change the password")
                query=listening().lower()
                f=open("PASSWORD.txt","r")
                pwd=f.readline()
                f.close()
                if query==pwd:
                    speak("say your new password")
                    query=listening().lower()
                    speak("repeat your password")
                    query1=listening().lower()
                    if query==query1:
                        f1=open("PASSWORD.txt","w+")
                        al=f1.write(query)
                        f1.close()
                        speak("your password has been changed")
                        break
                    else:
                        speak("your new password is not same")

                elif 'exit process' in query:
                    break
                elif query!=pwd:
                    speak("sorry you have said wrong password try again")

                else:
                    speak("sorry can not recognize ")
        elif 'put the computer sleep mode' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'start notepad'in query:

            os.system("%windir%\\system32\\notepad.exe")
        elif 'start sublime' in query:

            os.startfile("C:\\Program Files\\Sublime Text 3\\sublime_text.exe")
        elif 'start code' in query:
            os.startfile("C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        elif 'close notepad' in query:
            os.system("taskkill /im notepad.exe /f")
        elif 'close sublime' in query:
            os.system("taskkill /im sublime_text.exe /f")
        elif 'close code' in query:
            os.system("taskkill /im Code.exe /f")
        elif 'search in google' in query:
            speak("what you want to search")
            try:
                from googlesearch import search
            except ImportError:
                print("No module named 'google' found")


            query = listening().lower()
            num=["first","second","third","fourth","fifth"]

            list=[]
            for j in (search(query, tld="co.in", num=5, stop=5, pause=2)):
                """stop= none"""
                list.append(j)
            speak("top 5 result have been found")
            time.sleep(3)
            speak("which result you want to open")

            dic={
                 num[0]:list[0],num[1]:list[1],num[2]:list[2],num[3]:list[3],num[4]:list[4]

                 }
            query = listening().lower()
            choice=[]
            for x in dic:
                choice.append(x)
            for i in range(0,5):
                if choice[i] in query:
                    speak(f"opening {choice[i]} result in the google")
                    if choice[i] in dic:
                        opentask(dic[choice[i]])
                    else:
                        speak("sorry invalid result ")
        elif 'today news' in query:
            url = "https://bing-news-search1.p.rapidapi.com/news"

            querystring = {"safeSearch": "Off", "textFormat": "Raw"}

            headers = {
                'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
                'x-rapidapi-key': "658da30fc0msh85323d8216370c9p1e2d28jsnc1ad07e340e8",
                'x-bingapis-sdk': "true"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            val = json.loads(response.text)
            list = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth"]
            for i in range(1, 11):
                speak(f"{list[i - 1]} news is {val['value'][i]['name']}")
                query = listening().lower()

                if 'exit news' in query:
                    break
        elif 'weather information' in query:
            api_key = '5fa1a0255ce3c1760e68638a52de83df'
            url = 'http://api.openweathermap.org/data/2.5/weather?&q=Ahmedabad&appid=5fa1a0255ce3c1760e68638a52de83df'
            response = requests.get(url)
            x = response.json()
            speak(f"ahmedabad\'s temperature is {(x['main']['temp']-273.15)} celsius ")
            time.sleep(0.5)
            speak(f"the atmoshpheric pressure is {x['main']['pressure']} pascal")
            time.sleep(0.5)
            speak(f"humidity is {x['main']['humidity']} percent ")
            time.sleep(0.5)
            speak(f" wind speed is {x['wind']['speed']} meter per second")
            time.sleep(0.5)
            speak(f"the weather is {x['weather'][0]['description']}")
        elif 'send message' in query:
            lnum={'aditya':'xxxxxxxxxx','smith':'xxxxxxxxxx','sahil':'xxxxxxxxxx','harsh':'xxxxxxxxxx','gathiyo':'xxxxxxxxxx','bhargav':'xxxxxxxxxx'}

            choice=[]
            for x in lnum:
                choice.append(x)

            for i in range(0,len(lnum)):


                try:
                    if choice[i] in query:
                        speak("say your message")
                        query=listening().lower()
                        speak(f"sending message to f{choice[i]}")
                        if choice[i] in lnum:
                            msg(query,lnum[choice[i]])
                        else:
                            speak("something went wrong")
                except Exception as e:

                    speak("person contact is not listed in my dictionary")
        elif 'space information' in query:
            speak("there are two choice first one is  astrony picture of the day and second is earth view what would you like choose")
            query=listening().lower()
            if 'first one' in query:
                space1()
            if 'earch view' in query:
                space2()
        elif 'i want to laugh' in query:
            speak("this joke surely make you laugh")
            time.sleep(0.5)
            speak("oka listen carefully")
            joke()
        elif 'international space station' in query:
            ISS()
        elif 'GO AI' in query:

            my_bot = ChatBot(name='stuart', read_only=True, logic_adapters=[
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.BestMatch'
            ])

            trainer = ListTrainer(my_bot)

            trainer_corpus = ChatterBotCorpusTrainer(my_bot)
            trainer_corpus.train(
            'chatterbot.corpus.english'
            )
            while True:
                query = listening().lower()
                speak(my_bot.get_response(query))
                if 'exit' in query:
                    break
        else:
            speak('Sorry sir i am not programmed for this task')




import speech_recognition as sr
import os
from youtubesearchpython import VideosSearch
from gtts import gTTS
from playsound import playsound
import datetime
import time
import warnings
import calendar
import random
import wikipedia
import requests
from googlesearch import search
import json

warnings.filterwarnings('ignore')

def recordAudio():

    #record do audio
    r = sr.Recognizer() #Criação do objeto de reconhecimento

    #Uso do Microphone
    with sr.Microphone() as source:
        print('Diz Algo: ')
        audio = r.listen(source)

    #Usa o Speech do Google
    data = ''
    try:
        data = r.recognize_google(audio)
        data = data +'.'
        print('Saida: '+data)
    except sr.UnknownValueError: #Vê se á erros
        print('Google Speech Recognition could not understand the audio,unknow error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error '+e)
    
    return data

#recordAudio()

def assistantResponse(text):

    print(text)

    #Converte o texto para audio
    myobj = gTTS(text = text,lang='en',slow=False)

    #Guarda a Saida de audio
    myobj.save('assistant_record.mp3')

    #Reproduz o audio

    playsound('assistant_record.mp3')
    os.system('del assistant_record.mp3')

def wakeWord(text):
    WAKE_WORDS = ['hey peter','okay peter','peter']

    text = text.lower()

    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    return False

def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day
    
    month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
    ordNum = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th','25th','26th','27th','28th','29th','30th','31st']
    
    return 'Today is '+weekday+' '+ month_names[monthNum - 1]+' the '+ ordNum[dayNum - 1]+'.'

def greeting(text):

    GREETING_INPUTS = ['hi','hey','hola','greetings','wassup','hello']

    GREETING_RESPONSES = ['howdy', 'whats good', 'hello','hi','hello there']
    
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) +'.'
    
    return ''
def getPerson(text):

    wordList = text.split()

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' '+wordList[i+3]


def getWeather(text):

    #API:1e6c5de544e6038e4922f9426e2c77b8
    api_key = "1e6c5de544e6038e4922f9426e2c77b8"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name=text.split()
    city_name=city_name[-1]
    city_name=city_name.replace(".","")
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name +"&units=metric"

    response = requests.get(complete_url)
    print(city_name)
    x = response.json()

    if x["cod"] != "404": 
        y = x["main"] 

        current_temperature = y["temp"] 

        current_humidiy = y["humidity"] 

        current_temp_min = y["temp_min"]

        current_temp_max = y["temp_max"]

        z = x["weather"] 

        weather_description = z[0]["description"] 
  
        print("The Weather in "+ city_name + " :\nTemperature = " +
                    str(current_temperature) + "º" +
          "\n Min. Temperature = "+ str(current_temp_min) +"º"+

          "\n Max. Temperature = "+ str(current_temp_max)+ "º"+

          "\n Humidity = " +
                    str(current_humidiy) +" %" +
          "\n Description = " +
                    str(weather_description)) 
        return "The Weather in "+ city_name + " :\nTemperature = " + str(current_temperature) + "º" + "\n Min. Temperature = "+ str(current_temp_min) +"º"+ "\n Max. Temperature = "+ str(current_temp_max)+ "º"+"\n Humidity = " +str(current_humidiy) +" %" +"\n Description = " +str(weather_description) 
        
  
    else: 
        print(" City Not Found ")
while True:

    text = recordAudio()
    response = ''

    if(wakeWord(text) == True):

        response = response + greeting(text)
        if('date' in text):
            get_date = getDate()
            response = response + ' ' +get_date
        
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response +' '+wiki

        if('weather' in text):
            get_Weather = getWeather(text)
            response = response +' '+get_Weather

        if('time' in text):
            now = datetime.datetime.now()
            mer=''
            if now.hour >=12:
                mer = 'p.m'
                hour = now.hour -12
            else:
                mer = 'a.m'
                hour = now.hour

            if now.minute < 10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)
            
            response = response +' '+'It is  '+str(hour)+':'+minute+' '+mer+'.'
        if('open' in text):
            if('Google' in text):
                if('search' in text):
                    searchName = text
                    indexOfsearchName = text.find('search')
                    os.system("start "+ search(searchName[indexOfsearchName + 6: -1],num_results=10,lang="en")[0])
                    response = response + 'Searching for '+searchName[indexOfsearchName + 6: -1]+' on Google.'
                else:
                    os.system('start www.google.pt')
                    response= response +'Opening Google.'
            if('YouTube' in text):
                if('play' in text):
                    videoName = text
                    indexOfVideoName = text.find('play')
                    videosSearch = VideosSearch(videoName[indexOfVideoName + 5: -1], limit = 2, region='pt-pt')
                    print(videoName[indexOfVideoName + 5: -1])
                    os.system('start ' + videosSearch.result()['result'][0]['link'])
                    response = response + 'Playing ' + videoName[indexOfVideoName + 5: -1] + ' on Youtube.'
                else:
                    os.system('start www.youtube.com')
                    response = response +'Opening Youtube.'              
              
        if('close' in text):
            assistantResponse('Hope you Enjoyed.')
            time.sleep(3)
            exit()

        assistantResponse(response)
            
import pygame
import numpy as np
import spotipy
import sys
import pprint
import os
import urllib.request
import time
import requests
import json
import threading
import googlemaps
import datetime
import random
from datetime import datetime
from colorthief import ColorThief
from PIL import Image, ImageTk
from spotipy.oauth2 import SpotifyOAuth
from time import strftime
import tkinter as tk
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = 'portsmouth,gb'
WEATHER_API_KEY = ''
GOOGLE_API_KEY = ''
URL = ''
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast?"
FORECAST_URL = ''
isTravel = False
home_coord = '50.81447735115325, -1.0844253635578485'
work_coord = '50.8760800950388, -1.2417771713491559'
os.environ["SPOTIPY_CLIENT_ID"] = "8a3551ed1c614b1fa92aa297c1a6d226"
os.environ["SPOTIPY_CLIENT_SECRET"] = "0e0563dcee50459192f7243139cb7205"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"
scope = 'user-read-private user-read-playback-state user-library-modify user-read-playback-position app-remote-control user-read-currently-playing user-library-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), requests_timeout=10, retries=10)
pygame.init()
root = tk.Tk()

backgroundR = 0
backgroundG = 0
backgroundB = 0
changed = 0
fontColour = (255, 255, 255)
songName = ''
songArtist = ''
isNewSong = True
spotifyTimestamp = time.gmtime()[4]
print(spotifyTimestamp)
dominant_color = (0, 0, 0)
spotPlaying = False
journeyLength = ''
sync = 5
temperature = 0
currWeather = ''
forecast = []
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

pygame.font.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

pygame.display.init()
# background = pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, 0, screen_width, screen_height))

myfontArtist = pygame.font.SysFont('Roboto', 52, bold=True)
myfontSong = pygame.font.SysFont('Roboto', 32)
myfontWeekday = pygame.font.SysFont('Roboto', 62, bold=False)
myfontTime = pygame.font.SysFont('Roboto', 94, bold=True)
myfontForecast = pygame.font.SysFont('Roboto', 44, bold=False)
def getAPIKEYS():
    global WEATHER_API_KEY
    global GOOGLE_API_KEY
    global BASE_URL
    global BASE_URL_FORECAST
    global FORECAST_URL
    global URL
    apiFile = open('keys.txt', 'r')
    apiLines = apiFile.readlines()
    count = 0
    for line in apiLines:
        if 'Weather=' in line.strip():
            print('Weather')
            WEATHER_API_KEY = line.strip().replace('Weather=', '')
        if 'Google=' in line.strip():
            print('Google')
            GOOGLE_API_KEY = line.strip().replace('Google=', '')
        count += 1
    return


def getWeather():
    global URL
    global temperature
    global currWeather
    response = requests.get(URL)
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data['main']
        # getting temperature
        temperature = main['feels_like']
        # weather report
        report = data['weather'][0]['description']
        currWeather = report.title()

def refreshJourney():
    global GOOGLE_API_KEY
    global journeyLength
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    now = datetime.now()
    directions_result = gmaps.directions(home_coord, work_coord, mode="driving", departure_time=now, avoid='tolls')
    legs = directions_result[0].get("legs")
    for leg in legs:
        journeyLength = leg.get('duration_in_traffic').get('text')



def forecastDay(dateIn):
    datetime_object = datetime.strptime(dateIn, '%Y-%m-%d')
    date = datetime_object.weekday()
    if date == 0:
        return 'Mon'
    if date == 1:
        return 'Tue'
    if date == 2:
        return 'Wed'
    if date == 3:
        return 'Thu'
    if date == 4:
        return 'Fri'
    if date == 5:
        return 'Sat'
    if date == 6:
        return 'Sun'

def getForecast():
    global FORECAST_URL
    global temperature
    global currWeather
    global forecast
    forecast = []
    response = requests.get(FORECAST_URL)
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        for i in range(1, len(data['list'])):
            time = data['list'][i]['dt_txt']
            if(time[-8:] == '15:00:00'):
                strDate = (data['list'][i]['dt_txt'])[:10]
                strDate = forecastDay(strDate)
                strWeat = data['list'][i]['weather'][0]['main']
                strTemp = (str(int(data['list'][i]['main']['feels_like'])) + '°' )
                strText = (strDate + ' | ' + strTemp + ' | ' + strWeat)
                forecast.append(strText)
        print(forecast)


def drawWeather():
    global temperature
    global currWeather
    if int(temperature) < 10:
        textLen = 100
    tempText = str(int(temperature)) + '°'
    textsurfaceTemp = myfontTime.render(tempText, True, fontColour)
    textsurfaceCurr = myfontWeekday.render(currWeather, True, fontColour)
    screen.blit(textsurfaceTemp,(((screen_width - (textsurfaceTemp.get_width() + 10) ), 0)))
    screen.blit(textsurfaceCurr,(((screen_width - (textsurfaceCurr.get_width() + 10) ), (textsurfaceTemp.get_height() - 14))))

    for i in range(len(forecast)):
        textSurfaceForecast = myfontForecast.render(forecast[i], True, fontColour)
        screen.blit(textSurfaceForecast,(((screen_width - (textSurfaceForecast.get_width() + 10) ), (textsurfaceTemp.get_height() + textsurfaceCurr.get_height() - 20 + (i * 48)))))


def getCurrentlyPlaying():
    global spotifyTimestamp
    global songName
    global songArtist
    global isNewSong
    global spotPlaying
    prevSong = songName
    playing = sp.current_user_playing_track()
    if playing == None:
        spotPlaying = False
        print('No song playing')
    if playing != None:
        spotPlaying = True
        print('found song')
        try:
            songArtist = playing['item']['artists'][0]['name']
            songName = playing['item']['name']
            isNewSong = True
        except:
            print('Spotify error')
        if prevSong != songName:
            urllib.request.urlretrieve(playing['item']['album']['images'][0]['url'], 'spotify.jpeg')
            print('new song')
            isNewSong = True

def fadeInImg(img, x, y):
    inc = 0
    for i in range (30):
        pygame.event.get()
        inc = (i // 11) + 1
        img.set_alpha(i * inc)
        screen.blit(img, (x, y))
        pygame.display.update()
        pygame.time.wait(10)
    img.set_alpha(225)
    draw()



def placeSpotifyImage(change):
    global isNewSong
    spotifyImg = pygame.image.load('spotify.jpeg').convert()
    spotifyImg = pygame.transform.smoothscale(spotifyImg, (700, 700))
    placex = (screen_width / 2) - (spotifyImg.get_width() / 2)
    placey = (screen_height / 2) - (spotifyImg.get_width() / 2)
    if isNewSong and change:
        fadeInImg(spotifyImg, placex, placey)
    else:
        screen.blit(spotifyImg, (placex, placey))

def spotifyDeets(update):
    global isNewSong
    global dominant_color
    global spotPlaying
    global backgroundR
    global backgroundG
    global backgroundB
    if update:
        getCurrentlyPlaying()
        if spotPlaying:
            placeSpotifyImage(True)
            draw()

def weekday():
    date = datetime.today().weekday()
    if date == 0:
        return 'Monday'
    if date == 1:
        return 'Tuesday'
    if date == 2:
        return 'Wednesday'
    if date == 3:
        return 'Thursday'
    if date == 4:
        return 'Friday'
    if date == 5:
        return 'Saturday'
    if date == 6:
        return 'Sunday'

def clock():
    global backgroundR
    global backgroundG
    global backgroundB
    now = datetime.now()
    block = pygame.draw.rect(screen, (backgroundR, backgroundG, backgroundB), pygame.Rect(0, 0, 300, 150))
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%d %B")
    date = weekday()
    textSurfaceWeekDay = myfontWeekday.render(date, True, fontColour)
    textSurfaceDate = myfontWeekday.render(current_date, True, fontColour)
    textSurfaceTime = myfontTime.render(current_time, True, fontColour)
    screen.blit(textSurfaceTime, (10, 0))
    screen.blit(textSurfaceWeekDay, (12, (textSurfaceTime.get_height() - 14)))
    screen.blit(textSurfaceDate, (12, (textSurfaceTime.get_height() + textSurfaceDate.get_height() - 20)))

def spotifyText():
    global songName
    global songArtist
    textsurfaceArtist = myfontArtist.render(songArtist, True, fontColour)
    textsurfaceSong = myfontSong.render(songName, True, fontColour)
    screen.blit(textsurfaceArtist,(((screen_width / 2) - 350 ),((screen_height / 2 ) + 350)))
    screen.blit(textsurfaceSong,(((screen_width / 2) - 350 ),((screen_height / 2 ) + 410)))

def changeBackground():
    global backgroundR
    global backgroundG
    global backgroundB
    global songName
    global songArtist
    global myFont
    global fontColour
    if abs((backgroundR + backgroundG + backgroundB) - (dominant_color[0] + dominant_color[1] + dominant_color[2])) < 15:
        print('Background is the same')
        return
    stepsR = backgroundR - dominant_color[0]
    stepsG = backgroundG - dominant_color[1]
    stepsB = backgroundB - dominant_color[2]
    currentR = backgroundR
    currentG = backgroundG
    currentB = backgroundB
    rUp = False
    gUp = False
    bUp = False
    print('looping')
    if stepsR < 0: #Negative number
        stepsR = abs(stepsR)
        rUp = True
    if stepsG < 0: #Negative number
        stepsG = abs(stepsG)
        gUp = True
    if stepsB < 0: #Negative number
        stepsB = abs(stepsB)
        bUp = True
    for i in range(0, 120):
        pygame.event.get()
        if stepsR > 5:
            if rUp:
                currentR = currentR + 4
                stepsR = stepsR - 4
            elif not rUp:
                currentR = currentR - 4
                stepsR = stepsR - 4
        if stepsG > 5:
            if gUp:
                currentG = currentG + 4
                stepsG = stepsG - 4
            elif not gUp:
                currentG = currentG - 4
                stepsG = stepsG - 4
        if stepsB > 5:
            if bUp:
                currentB = currentB + 4
                stepsB = stepsB - 4
            elif not bUp:
                currentB = currentB - 4
                stepsB = stepsB - 4
        backgroundR = currentR
        backgroundG = currentG
        backgroundB = currentB
        if(backgroundR + backgroundG + backgroundB) > 540:
            fontColour = (0, 0, 0)
        if(backgroundR + backgroundG + backgroundB) < 540:
            fontColour = (255, 255, 255)
        draw()

def drawTravel():
    global journeyLength
    global screen_width
    global screen_height
    journeyText = journeyLength + ' to work'
    textsurfaceJourney = myfontWeekday.render(journeyText, True, fontColour)
    screen.blit(textsurfaceJourney,((screen_width / 2 - (textsurfaceJourney.get_rect().width / 2)),(screen_height - 80)))

def draw():
    global backgroundR
    global backgroundG
    global backgroundB
    global spotPlaying
    global isTravel
    screen.fill((backgroundR, backgroundG, backgroundB))
    clock()
    if spotPlaying:
        placeSpotifyImage(False)
        spotifyText()
    drawWeather()
    if isTravel:
        drawTravel()
    pygame.display.update()
    pygame.event.get()


def Travelling():
    global isTravel
    current_time = datetime.now().strftime("%H:%M:%S")
    start = '07:00:00'
    end = '09:00:00'
    if weekday() not in ['Saturday', 'Sunday']:
        if current_time > start and current_time < end:
            isTravel = True
            print('Work time')
    if weekday() in ['Saturday', 'Sunday']:
        isTravel = False


getAPIKEYS()
# Set API URLs from grabbed keys
FORECAST_URL = BASE_URL_FORECAST + "q=" + CITY + "&units=metric&appid=" + WEATHER_API_KEY
URL = BASE_URL + "q=" + CITY + "&units=metric&appid=" + WEATHER_API_KEY
threading.Thread(getWeather())
threading.Thread(getForecast())
threading.Thread(refreshJourney())
pygame.mouse.set_visible(False)
while True:
    Travelling()
    if (sync % 5) == 0:
        spotifyDeets(True)
    if isNewSong and spotPlaying:
        print('changing background')
        color_thief = ColorThief('spotify.jpeg')
        dominant_color = color_thief.get_color(quality=1)
        changeBackground()
        changed = 0
        isNewSong = False
    if not spotPlaying:
        if changed != 1:
            dominant_color = (0, 0, 0)
            changeBackground()
            changed = 1
    if (sync % 20) == 0:
        if not spotPlaying:
            dominant_color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
            changeBackground()
    if (sync % 140) == 0:
        if isTravel:
            print('Refreshing Journey Time')
            threading.Thread(refreshJourney())
    if sync == 240:
        threading.Thread(getWeather())
        threading.Thread(getForecast())
    if sync > 240:
        sync = 0
    draw()
    print(sync)
    pygame.time.wait(1000)
    sync = sync + 1
    pygame.event.get()


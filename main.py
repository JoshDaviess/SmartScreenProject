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
from datetime import datetime
from colorthief import ColorThief
from PIL import Image, ImageTk
from spotipy.oauth2 import SpotifyOAuth
from time import strftime
import tkinter as tk
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = 'portsmouth,gb'
API_KEY = 'ad8ae6c5543cfeb83b3e084515554caf'
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
os.environ["SPOTIPY_CLIENT_ID"] = "8a3551ed1c614b1fa92aa297c1a6d226"
os.environ["SPOTIPY_CLIENT_SECRET"] = "0e0563dcee50459192f7243139cb7205"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"
scope = 'user-read-private user-read-playback-state user-library-modify user-read-playback-position app-remote-control user-read-currently-playing user-library-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
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
sync = 4
temperature = 0
currWeather = ''

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

pygame.font.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

pygame.display.init()
# background = pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, 0, screen_width, screen_height))

myfontArtist = pygame.font.SysFont('Roboto', 44, bold=True)
myfontSong = pygame.font.SysFont('Roboto', 28)
myfontWeekday = pygame.font.SysFont('Roboto', 58, bold=False)
myfontTime = pygame.font.SysFont('Roboto', 86, bold=True)


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
        temperature = main['temp'] - 273.15
        # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']
        # weather report
        report = data['weather'][0]['description']
        currWeather = report
        print(int(temperature))
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
    print(URL)

def drawWeather():
    global temperature
    global currWeather
    if int(temperature) < 10:
        textLen = 100
    tempText = str(int(temperature)) + '°'
    textsurfaceTemp = myfontTime.render(tempText, True, fontColour)
    textsurfaceCurr = myfontWeekday.render(currWeather, True, fontColour)
    screen.blit(textsurfaceTemp,(((screen_width - (textsurfaceTemp.get_width() + 10) ), 10)))
    screen.blit(textsurfaceCurr,(((screen_width - (textsurfaceCurr.get_width() + 10) ), (textsurfaceTemp.get_height() - 10))))


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
        songArtist = playing['item']['artists'][0]['name']
        songName = playing['item']['name']
        isNewSong = True
        if prevSong != songName:
            urllib.request.urlretrieve(playing['item']['album']['images'][0]['url'], 'spotify.jpeg')
            print('new song')
            isNewSong = True
        spotifyTimestamp = time.gmtime()[4]

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
    spotifyImg = pygame.transform.smoothscale(spotifyImg, (500, 500))
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
    screen.blit(textSurfaceTime, (10, 10))
    screen.blit(textSurfaceWeekDay, (12, 88))
    screen.blit(textSurfaceDate, (12, 148))

def spotifyText():
    global songName
    global songArtist
    textsurfaceArtist = myfontArtist.render(songArtist, True, fontColour)
    textsurfaceSong = myfontSong.render(songName, True, fontColour)
    screen.blit(textsurfaceArtist,(((screen_width / 2) - 250 ),((screen_height / 2 ) + 250)))
    screen.blit(textsurfaceSong,(((screen_width / 2) - 250 ),((screen_height / 2 ) + 294)))

def changeBackground():
    global backgroundR
    global backgroundG
    global backgroundB
    global songName
    global songArtist
    global myFont
    global fontColour
    if abs((backgroundR + backgroundG + backgroundB) - (dominant_color[0] + dominant_color[1] + dominant_color[2])) < 35:
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
    for i in range(0, 150):
        pygame.event.get()
        if stepsR > 10:
            if rUp:
                currentR = currentR + 2
                stepsR = stepsR - 2
            elif not rUp:
                currentR = currentR - 2
                stepsR = stepsR - 2
        if stepsG > 10:
            if gUp:
                currentG = currentG + 2
                stepsG = stepsG - 2
            elif not gUp:
                currentG = currentG - 2
                stepsG = stepsG - 2
        if stepsB > 10:
            if bUp:
                currentB = currentB + 2
                stepsB = stepsB - 2
            elif not bUp:
                currentB = currentB - 2
                stepsB = stepsB - 2
        backgroundR = currentR
        backgroundG = currentG
        backgroundB = currentB
        if(backgroundR + backgroundG + backgroundB) > 550:
            fontColour = (0, 0, 0)
        if(backgroundR + backgroundG + backgroundB) < 550:
            fontColour = (255, 255, 255)
        draw()


def draw():
    global backgroundR
    global backgroundG
    global backgroundB
    global spotPlaying
    screen.fill((backgroundR, backgroundG, backgroundB))
    clock()
    if spotPlaying:
        placeSpotifyImage(False)
        spotifyText()
    drawWeather()
    pygame.display.update()
    pygame.event.get()




threading.Thread(getWeather())
while True:
    if (sync % 4) == 0:
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
    if sync == 60:
        threading.Thread(getWeather())
    if sync > 60:
        sync = 0
    draw()
    print(sync)
    pygame.time.wait(1000)
    sync = sync + 1
    pygame.event.get()


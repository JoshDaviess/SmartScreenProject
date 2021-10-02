import pygame
import numpy as np
import spotipy
import sys
import pprint
import os
import urllib.request
import time
from datetime import datetime
from colorthief import ColorThief
from PIL import Image, ImageTk
from spotipy.oauth2 import SpotifyOAuth
from time import strftime
import tkinter as tk
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
fontColour = (255, 255, 255)
songName = ''
songArtist = ''
isNewSong = True
spotifyTimestamp = time.gmtime()[4]
print(spotifyTimestamp)
dominant_color = (0, 0, 0)
spotPlaying = False
sync = 6

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

pygame.font.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

pygame.display.init()
# background = pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, 0, screen_width, screen_height))

myfontArtist = pygame.font.SysFont('Roboto', 36, bold=True)
myfontSong = pygame.font.SysFont('Roboto', 32)
myfontWeekday = pygame.font.SysFont('Roboto', 52, bold=True)
myfontTime = pygame.font.SysFont('Roboto', 42, bold=True)





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
        songArtist = playing['item']['artists'][0]['name']
        songName = playing['item']['name']
        if prevSong != songName:
            urllib.request.urlretrieve(playing['item']['album']['images'][0]['url'], 'spotify.jpeg')
            print('new song')
            isNewSong = True
        spotifyTimestamp = time.gmtime()[4]

def fadeInImg(img, x, y):
    for i in range (50):
        pygame.event.get()
        img.set_alpha(i * 3)
        screen.blit(img, (x, y))
        pygame.display.update()
        pygame.time.wait(10)
    img.set_alpha(225)


def minute_passed(oldepoch):
    return time.time() - oldepoch >= 60

def placeSpotifyImage(img, placex, placey, change):
    global isNewSong
    if isNewSong and change:
        fadeInImg(img, placex, placey)
    else:
        screen.blit(img, (placex, placey))

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
            spotifyImg = pygame.image.load('spotify.jpeg').convert()
            spotifyImg = pygame.transform.smoothscale(spotifyImg, (400, 400))
            placex = (screen_width / 2) - (spotifyImg.get_width() / 2)
            placey = (screen_height / 2) - (spotifyImg.get_width() / 2)
            placeSpotifyImage(spotifyImg, placex, placey, True)
            screen.fill((backgroundR, backgroundG, backgroundB))
            clock()
            spotifyText()
            placeSpotifyImage(spotifyImg, placex, placey, False)
            pygame.display.update()
    pygame.event.get()
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
    print(current_time)
    date = weekday()
    textSurfaceWeekDay = myfontWeekday.render(date, True, fontColour)
    textSurfaceTime = myfontTime.render(current_time, True, fontColour)
    screen.blit(textSurfaceWeekDay, (10, 10))
    screen.blit(textSurfaceTime, (10, 60))

def spotifyText():
    global songName
    global songArtist
    textsurfaceArtist = myfontArtist.render(songArtist, True, fontColour)
    textsurfaceSong = myfontSong.render(songName, True, fontColour)
    screen.blit(textsurfaceArtist,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 200)))
    screen.blit(textsurfaceSong,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 236)))

def changeBackground():
    global backgroundR
    global backgroundG
    global backgroundB
    global songName
    global songArtist
    global myFont
    global fontColour

    color_thief = ColorThief('spotify.jpeg')
    dominant_color = color_thief.get_color(quality=1)
    spotifyImg = pygame.image.load('spotify.jpeg').convert()
    spotifyImg = pygame.transform.smoothscale(spotifyImg, (400, 400))
    placex = (screen_width / 2) - (spotifyImg.get_width() / 2)
    placey = (screen_height / 2) - (spotifyImg.get_width() / 2)

    #screen.fill((backgroundR, backgroundG, backgroundB))
    # placeSpotifyImage(spotifyImg, placex, placey, False)
    # textsurfaceArtist = myfontArtist.render(songArtist, True, fontColour)
    # textsurfaceSong = myfontSong.render(songName, True, fontColour)
    # screen.blit(textsurfaceArtist,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 200)))
    # screen.blit(textsurfaceSong,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 236)))
    # clock()
    #pygame.display.update()

    stepsR = backgroundR - dominant_color[0]
    stepsG = backgroundG - dominant_color[1]
    stepsB = backgroundB - dominant_color[2]
    currentR = backgroundR
    currentG = backgroundG
    currentB = backgroundB
    rUp = False
    gUp = False
    bUp = False
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
        screen.fill((currentR, currentG, currentB))
        backgroundR = currentR
        backgroundG = currentG
        backgroundB = currentB
        if(backgroundR + backgroundG + backgroundB) > 600:
            fontColour = (0, 0, 0)
        if(backgroundR + backgroundG + backgroundB) < 600:
            fontColour = (255, 255, 255)
        placeSpotifyImage(spotifyImg, placex, placey, False)
        textsurfaceArtist = myfontArtist.render(songArtist, True, fontColour)
        textsurfaceSong = myfontSong.render(songName, True, fontColour)
        screen.blit(textsurfaceArtist,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 200)))
        screen.blit(textsurfaceSong,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 236)))
        clock()
        pygame.display.update()

while True:
    if sync > 5:
        spotifyDeets(True)
        sync = 0

    if isNewSong and spotPlaying:
        print('changing background')
        changeBackground()
        isNewSong = False
        clock()
    if not spotPlaying:
        screen.fill((0, 0, 0))
        clock()
        pygame.display.update()
    pygame.time.wait(1000)
    print(sync)
    sync = sync + 1
    clock()
    pygame.display.update()
    pygame.event.get()


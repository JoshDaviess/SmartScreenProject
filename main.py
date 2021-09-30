import pygame
import numpy as np
import spotipy
import sys
import pprint
import os
import urllib.request
import time
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
isNewSong = True
spotifyTimestamp = time.gmtime()[4]
print(spotifyTimestamp)
dominant_color = ''

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

pygame.font.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

pygame.display.init()
# background = pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, 0, screen_width, screen_height))

myfont = pygame.font.SysFont('Roboto', 30)
textsurface = myfont.render('Some Text', True, (255, 255, 255))
screen.blit(textsurface,(0,0))




def getCurrentlyPlaying(songName, songArtist):
    global spotifyTimestamp
    playing = sp.current_user_playing_track()
    if playing != None:
        songArtist = playing['item']['album']['artists'][0]['name']
        songName = playing['item']['name']
        urllib.request.urlretrieve(playing['item']['album']['images'][0]['url'], 'spotify.jpeg')
        spotifyTimestamp = time.gmtime()[4]

def fadeInImg(img, x, y):
    for i in range (100):
        pygame.event.get()
        img.set_alpha(i)
        pygame.display.update()
        rect = img.get_rect()
        screen.blit(img, (x, y))
        pygame.display.update()
        pygame.time.wait(10)
    img.set_alpha(225)

def minute_passed(oldepoch):
    return time.time() - oldepoch >= 60

def placeSpotifyImage(img, placex, placey):
    global isNewSong
    if isNewSong:
        fadeInImg(img, placex, placey)
        isNewSong = False
    elif not isNewSong:
        screen.blit(img, (placex, placey))
        pygame.display.update()

def spotifyDeets(update):
    global isNewSong
    global dominant_color
    songName = ''
    songArtist = ''
    if update:
        getCurrentlyPlaying(songName, songArtist)
    spotifyImg = pygame.image.load('spotify.jpeg').convert()
    spotifyImg = pygame.transform.smoothscale(spotifyImg, (400, 400))
    placex = (screen_width / 2) - (spotifyImg.get_width() / 2)
    placey = (screen_height / 2) - (spotifyImg.get_width() / 2)
    placeSpotifyImage(spotifyImg, placex, placey)
    if update:
        color_thief = ColorThief('spotify.jpeg')
        dominant_color = color_thief.get_color(quality=1)
    pygame.event.get()


def changeBackground(newColour):
    global backgroundR
    global backgroundG
    global backgroundB
    stepsR = backgroundR - newColour[0]
    stepsG = backgroundG - newColour[1]
    stepsB = backgroundB - newColour[2]
    currentR = backgroundR
    currentG = backgroundG
    currentB = backgroundB
    rUp = False
    gUp = False
    bUp = False
    print(stepsR)
    print(stepsG)
    print(stepsB)
    if stepsR < 0: #Negative number
        stepsR = abs(stepsR)
        rUp = True
    if stepsG < 0: #Negative number
        stepsG = abs(stepsG)
        gUp = True
    if stepsB < 0: #Negative number
        stepsB = abs(stepsB)
        bUp = True

    totalSteps = max(stepsR,stepsG,stepsB)
    print(totalSteps)

    for i in range(0, 255):
        pygame.event.get()
        if stepsR != 0:
            if rUp:
                currentR = currentR + 1
                stepsR = stepsR - 1
            elif not rUp:
                currentR = currentR - 1
                stepsR = stepsR - 1
        if stepsG != 0:
            if gUp:
                currentG = currentG + 1
                stepsG = stepsG - 1
            elif not gUp:
                currentG = currentG - 1
                stepsG = stepsG - 1
        if stepsB != 0:
            if bUp:
                currentB = currentB + 1
                stepsB = stepsB - 1
            elif not bUp:
                currentB = currentB - 1
                stepsB = stepsB - 1
        screen.fill((currentR, currentG, currentB))
        backgroundR = currentR
        backgroundG = currentG
        backgroundB = currentB
        spotifyDeets(False)
        pygame.display.flip()
        # screen.fill((i + 1, backgroundG, backgroundB))
        # pygame.display.flip()
        # backgroundR = i
while True:
    spotifyDeets(True)
    changeBackground(dominant_color)
    pygame.time.wait(5000)
    pygame.event.get()
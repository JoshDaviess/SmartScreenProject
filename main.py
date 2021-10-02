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
songName = ''
songArtist = ''
isNewSong = True
spotifyTimestamp = time.gmtime()[4]
print(spotifyTimestamp)
dominant_color = (0, 0, 0)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

pygame.font.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

pygame.display.init()
# background = pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, 0, screen_width, screen_height))

myfontArtist = pygame.font.SysFont('Roboto', 36, bold=True)
myfontSong = pygame.font.SysFont('Roboto', 32)





def getCurrentlyPlaying():
    global spotifyTimestamp
    global songName
    global songArtist
    global isNewSong
    prevSong = songName
    playing = sp.current_user_playing_track()
    if playing != None:
        songArtist = playing['item']['artists'][0]['name']
        songName = playing['item']['name']
        if prevSong != songName:
            urllib.request.urlretrieve(playing['item']['album']['images'][0]['url'], 'spotify.jpeg')
            print('new song')
            isNewSong = True

        spotifyTimestamp = time.gmtime()[4]

def fadeInImg(img, x, y):
    for i in range (100):
        pygame.event.get()
        img.set_alpha(i)
        pygame.display.update()
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
    if update:
        getCurrentlyPlaying()
        spotifyImg = pygame.image.load('spotify.jpeg').convert()
        spotifyImg = pygame.transform.smoothscale(spotifyImg, (400, 400))
        placex = (screen_width / 2) - (spotifyImg.get_width() / 2)
        placey = (screen_height / 2) - (spotifyImg.get_width() / 2)
        placeSpotifyImage(spotifyImg, placex, placey, True)
    pygame.event.get()


def changeBackground():
    global backgroundR
    global backgroundG
    global backgroundB
    global songName
    global songArtist
    global myFont
    spotifyImg = pygame.image.load('spotify.jpeg').convert()
    spotifyImg = pygame.transform.smoothscale(spotifyImg, (400, 400))
    placex = (screen_width / 2) - (spotifyImg.get_width() / 2)
    placey = (screen_height / 2) - (spotifyImg.get_width() / 2)
    screen.fill((backgroundR, backgroundG, backgroundB))
    placeSpotifyImage(spotifyImg, placex, placey, False)
    textsurfaceArtist = myfontArtist.render(songArtist, True, (255, 255, 255))
    textsurfaceSong = myfontSong.render(songName, True, (255, 255, 255))
    screen.blit(textsurfaceArtist,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 200)))
    screen.blit(textsurfaceSong,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 236)))
    pygame.display.update()
    color_thief = ColorThief('spotify.jpeg')
    dominant_color = color_thief.get_color(quality=1)
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
    for i in range(0, 255):
        pygame.event.get()
        if stepsR > 10:
            if rUp:
                currentR = currentR + 1
                stepsR = stepsR - 1
            elif not rUp:
                currentR = currentR - 1
                stepsR = stepsR - 1
        if stepsG > 10:
            if gUp:
                currentG = currentG + 1
                stepsG = stepsG - 1
            elif not gUp:
                currentG = currentG - 1
                stepsG = stepsG - 1
        if stepsB > 10:
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
        placeSpotifyImage(spotifyImg, placex, placey, False)
        screen.blit(textsurfaceArtist,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 200)))
        screen.blit(textsurfaceSong,(((screen_width / 2) - 200 ),((screen_height / 2 )+ 236)))
        pygame.display.update()
        # screen.fill((i + 1, backgroundG, backgroundB))
        # pygame.display.flip()
        # backgroundR = i
while True:
    spotifyDeets(True)
    if isNewSong:
        changeBackground()
        isNewSong = False
    pygame.time.wait(1500)
    pygame.event.get()
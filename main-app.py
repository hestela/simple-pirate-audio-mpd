#!/usr/bin/env python3

import signal

import RPi.GPIO as GPIO
from mpd import MPDClient

BUTTONS = [5, 6, 16, 24]
LABELS = ["A", "B", "X", "Y"]

# Some simple m3u playlists
WHITE_NOISE = 'white_noise'
CLASSIC = 'classic'
STATE = 'PLAY'

client = MPDClient()
# Default playlist
curr_playlist = CLASSIC


def test_mpd_con():
    try:
        client.ping()
    # Cheap way to refresh connection
    except Exception as e:
        client.connect("localhost", 6600)

def check_playlist():
    status = client.status()
    num_songs = int(status['playlistlength'])

    # Assume we got paused for some reason
    if num_songs > 0:
        client.play()
        return

    # Queue is empty, reload playlist and start
    client.load(curr_playlist)
    client.play()

def load_start_playlist(playlist):
    global curr_playlist
    # Clear in case we are playing something
    client.clear()
    curr_playlist = playlist
    client.load(curr_playlist)
    client.play()

def try_next():
    try:
        client.next()
    # Playlist got cleared or was stopped on a side channel
    except Exception as e:
        pass


def handle_button(pin):
    global STATE
    test_mpd_con()

    label = LABELS[BUTTONS.index(pin)]

    # White Noise
    if label == "X":
        if curr_playlist != WHITE_NOISE: 
            load_start_playlist(WHITE_NOISE)
            print('switch to white noise')
        else:
            try_next()
            print('next white noise')

    if label == "Y":
        print("Y RemoteControl: VolumeUp")

    # Classic Music
    if label == "A":
        if curr_playlist != CLASSIC:
            load_start_playlist(CLASSIC)
            print('switch to classic')
        else:
            try_next()
            print('next classic')

    # Pause
    if label == "B":
        if STATE == 'PLAY':
            STATE = 'PAUSE'
            print("PAUSE")
            client.pause()
        else:
            STATE = 'PLAY'
            print("PLAY")
            client.play()

    # Check if playlist got emptied
    if STATE == 'PLAY':
        check_playlist()


GPIO.setmode(GPIO.BCM)

for pin in BUTTONS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)


# MPD init and hard reset
test_mpd_con()
client.random(1)
# Repeat makes playlist repeat. Should help avoid having to poll for an empty queue
client.repeat(1)
client.clear()
check_playlist()

# No code below this will execute
signal.pause()

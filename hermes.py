# Standard Libraries
import atexit
import calendar
import csv
import datetime
import locale
import math
import os
import random
import smtplib
import ssl
import sys
import threading
import time
from email.message import EmailMessage
import socket
import webbrowser

# Third-Party Libraries
import clipboard
import folium
import keyboard
import numpy as np
import pygame
import pygame.gfxdraw
from pygame.locals import QUIT
import pyautogui
import requests
import serial
import serial.tools.list_ports
import cv2
import xml.etree.ElementTree as ET

# Ground Position
TrackerLatD = 0
TrackerLonD = 0
TrackerAltF = 0

# Balloon Position
PayloadLatD = 0
PayloadLonD = 0
PayloadAltF = 0

# Landing Location
TargetLatD = 0
TargetLonD = 0
TargetAltF = 0

# Flight Conditions
AscentRate = 0

# Radio Positions
LatRFD = 0
LonRFD = 0
AltRFD = 0

LatIridium = 0
LonIridium = 0
AltIridium = 0

LatAPRS = 0
LonAPRS = 0
AltAPRS = 0

TimestampRFD = ''
TimestampIridium = ''
TimestampAPRS = ''

# Distances
Distance2DPayload = 0
Distance3DPayload = 0

Distance2DTarget = 0
Distance3DTarget = 0

# Pointing Angles (Deg)
SigmaPayload = 0
GammaPayload = 0

SigmaTarget = 0
GammaTarget = 0

# Tweak Offset (Deg)
SigmaTweak = 0
GammaTweak = 0

# API Information
Mun = ''
Cou = ''
Sub = ''
Position = ''
Location = ''

# Last Ping Position
PrevLatD = None
PrevLonD = None
PrevAltF = None

# Time
MET = ''
UTC = ''

# Communication
RFD = False
RFDConditional = False

Iridium = False
IridiumConditional = False
IridiumActive = True

APRS = False
APRSConditional = False

Ubiquiti = False
UbiquitiConditional = False

Arduino = False
ArduinoConditional = False

DataList = ''

# Comms Input
IMEI = 0
Callsign = ''
IP = ''

# Data Logging
FileWrite = True

# Flight Events
Tracking = False
Launched = False
Vented = False
Cut = False
Descent = False
Landed = False

# Button Guards
GuardVent = True

# Timing Bools
LaunchTime = None
StartTime = None
Time = 0

# Settings Menu
Settings = False

# Video Fullscreen
Fullscreen = False

# Manual Functions
ManualTracking = False
ManualVenting = True

# Peripherals
DispAltitude = True
DispCompass = True
DispLocation = True
DispTime = True

# Peripheral Settings
CompassSetting = 1

# Map Writing
Map = None
MapFile = None

# Screen Capture
Recording = False
Capture = None

# Launch Logic
Launch1 = False
Launch2 = False
Reset1 = False
Reset2 = False
Reset3 = False
Reset4 = False
Countdown1 = False
Countdown2 = False
Countdown3 = False
PrevTime = None

# Vent Logic
AltVentOpen = None
AltVentClose = None
VelVentClose = None

# Tracker-Target Equivalency
ReturnToSender = False

# Messaging and Input
OutputMessage = ''
InputText = ''
InputWindowW = False
InputWindowH = False
InputTrackerLat = False
InputTrackerLon = False
InputTrackerAlt = False
InputPayloadLat = False
InputPayloadLon = False
InputPayloadAlt = False
InputAltVentOpen = False
InputAltVentClose = False
InputVelVentClose = False
InputRFD = False
InputIridium = False
InputAPRS = False
InputUbiquiti = False
InputArduino = False

# Video Stream Logging
FPS = 30
Cap = None
PrevFrameSize = None
PrevFrameTime = None

# Serial Ports
COMRFD = ''
COMArduino = ''
SerialRFD = None
SerialArduino = None

# HTTP Session
Session = requests.Session()

# Program Clock
Clock = pygame.time.Clock()

# Program Running
Running = True

# Motor Controls
ControlX = 0
ControlY = 0
ControlR = 0

# Countdown Command
CountdownX = 0
CountdownY = 0
CountdownW = 0
CountdownH = 0

# Fullscreen Button
FullscreenX = 0
FullscreenY = 0
FullscreenR = 0

# Help Button
HelpX = 0
HelpY = 0
HelpR = 0

# Launch Command
LaunchX = 0
LaunchY = 0
LaunchW = 0
LaunchH = 0
LaunchS = 0

# Settings Menu
MenuX = 0
MenuY = 0
MenuW = 0
MenuH = 0

# Power Button
PowerX = 0
PowerY = 0
PowerR = 0

# Radio Display
RadioX = 0
RadioY = 0
RadioW = 0
RadioH = 0
RadioS = 0

# Launch Reset Command
ResetX = 0
ResetY = 0
ResetW = 0
ResetH = 0
ResetR = 0

# Settings Button
SettingsX = 0
SettingsY = 0
SettingsR = 0

# D-Pad Controls
TriangleHeight = 0
TriangleShapes = 0

# Vent Command
VentX = 0
VentY = 0
VentW = 0
VentH = 0

# Initialize Pygame
pygame.font.init()
pygame.mixer.init()
pygame.joystick.init()
pygame.init()

# Display
WindowW = pygame.display.Info().current_w
WindowH = WindowW * (9/16)

# Define Scale Factor
SF = min(WindowW / 1920, WindowH / 1080)

# Video Display
VideoW = 800 * SF
VideoH = 600 * SF
VideoX = (WindowW - VideoW) // 2
VideoY = (WindowH - VideoH) // 2

# Create Window
Window = pygame.display.set_mode((WindowW, WindowH))

# Window Title
pygame.display.set_caption("HERMES Telemetry GUI")

# Set Cursor
pygame.mouse.set_pos((WindowW, WindowH))

# Locale
locale.setlocale(locale.LC_ALL, '')

# Threading Lock
Lock = threading.Lock()

# Directory
Directory = os.getcwd()

# Resources
Resources = os.path.join(Directory, "Resources")
Videos = os.path.join(Directory, "Videos")
print(Resources)

# Load Resources
ButtonHelp = pygame.image.load(os.path.join(Resources, "ButtonHelp.png"))
ButtonPower = pygame.image.load(os.path.join(Resources, "ButtonPower.png"))
ButtonSettings = pygame.image.load(
    os.path.join(Resources, "ButtonSettings.png"))
ButtonFullscreenA = pygame.image.load(
    os.path.join(Resources, "ButtonFullscreenA.png"))
ButtonFullscreenB = pygame.image.load(
    os.path.join(Resources, "ButtonFullscreenB.png"))
LogoMNSGC = pygame.image.load(os.path.join(Resources, "LogoMNSGC.png"))
LogoNASA = pygame.image.load(os.path.join(Resources, "LogoNASA.png"))
LogoNEBP = pygame.image.load(os.path.join(Resources, "LogoNEBP.png"))
WifiOn = pygame.image.load(os.path.join(Resources, "WifiOn.png"))
WifiOff = pygame.image.load(os.path.join(Resources, "WifiOff.png"))
TrackingOn = pygame.image.load(os.path.join(Resources, "TrackingOn.png"))
TrackingOff = pygame.image.load(os.path.join(Resources, "TrackingOff.png"))
CaptureOn = pygame.image.load(os.path.join(Resources, "CaptureOn.png"))
CaptureOff = pygame.image.load(os.path.join(Resources, "CaptureOff.png"))
DPad = pygame.image.load(os.path.join(Resources, "DPad.png"))
DPadDown = pygame.image.load(os.path.join(Resources, "DPadDown.png"))
DPadLeft = pygame.image.load(os.path.join(Resources, "DPadLeft.png"))
DPadRight = pygame.image.load(os.path.join(Resources, "DPadRight.png"))
DPadUp = pygame.image.load(os.path.join(Resources, "DPadUp.png"))
DPadCenter = pygame.image.load(os.path.join(Resources, "DPadCenter.png"))
CircleBlack = pygame.image.load(os.path.join(Resources, "CircleBlack.png"))
CircleWhite = pygame.image.load(os.path.join(Resources, "CircleWhite.png"))

Beep = os.path.join(Resources, "Beep.mp3")
Blop = os.path.join(Resources, "Blop.mp3")
Buzz = os.path.join(Resources, "Buzz.mp3")
Launch00 = os.path.join(Resources, "Launch00.mp3")
Launch10 = os.path.join(Resources, "Launch10.mp3")
Launch30 = os.path.join(Resources, "Launch30.mp3")
Launch60 = os.path.join(Resources, "Launch60.mp3")
Static = os.path.join(Resources, "Static.mp3")
Switch = os.path.join(Resources, "Switch.mp3")
Tap = os.path.join(Resources, "Tap.mp3")

# Reconfigure Resources
LogoMNSGC = pygame.transform.smoothscale(
    LogoMNSGC, (int(800 * SF), int(800 * SF)))
LogoNASA = pygame.transform.smoothscale(
    LogoNASA, (int(230 * SF), int(200 * SF)))
LogoNEBP = pygame.transform.smoothscale(
    LogoNEBP, (int(200 * SF), int(200 * SF)))
DPad = pygame.transform.smoothscale(DPad, (int(170 * SF), int(170 * SF)))
DPadDown = pygame.transform.smoothscale(
    DPadDown, (int(170 * SF), int(170 * SF)))
DPadLeft = pygame.transform.smoothscale(
    DPadLeft, (int(170 * SF), int(170 * SF)))
DPadRight = pygame.transform.smoothscale(
    DPadRight, (int(170 * SF), int(170 * SF)))
DPadUp = pygame.transform.smoothscale(DPadUp, (int(170 * SF), int(170 * SF)))
DPadCenter = pygame.transform.smoothscale(
    DPadCenter, (int(100 * SF), int(100 * SF)))

Icons = {
    "WifiOn": "WifiOn.png",
    "WifiOff": "WifiOff.png",
    "TrackingOn": "TrackingOn.png",
    "TrackingOff": "TrackingOff.png",
    "CaptureOn": "CaptureOn.png",
    "CaptureOff": "CaptureOff.png",
    "ButtonHelp": "ButtonHelp.png",
    "ButtonPower": "ButtonPower.png",
    "ButtonSettings": "ButtonSettings.png",
    "ButtonFullscreenA": "ButtonFullscreenA.png",
    "ButtonFullscreenB": "ButtonFullscreenB.png"
}

Indicators = {}
Buttons = {}

for Name, Path in Icons.items():
    Indicator = pygame.image.load(os.path.join(Resources, Path))
    Indicator = pygame.transform.smoothscale(
        Indicator, (int(60 * SF), int(60 * SF)))
    Indicators[Name] = Indicator

    if Name.startswith("Button"):
        Button = pygame.image.load(os.path.join(Resources, Path))
        Button = pygame.transform.smoothscale(
            Button, (int(45 * SF), int(45 * SF)))
        Buttons[Name] = Button


def Startup():
    # Logo Placement
    LogoW = LogoMNSGC.get_width()
    LogoH = LogoMNSGC.get_height()

    LogoSurface = pygame.Surface((LogoW, LogoH))
    LogoSurface.blit(LogoMNSGC, (0, 0))

    # Startup Animation
    FadeDuration = 1000
    FadeSteps = 50
    StepDelay = FadeDuration / FadeSteps

    Particles = []
    NumParticles = 30

    for _ in range(NumParticles):
        Particle = {
            'x': random.randint(0, WindowW),
            'y': random.randint(0, WindowH),
            'size': random.randint(1, 2),
            'speed': random.uniform(0.01, 0.05),
            'fade': random.uniform(0.1, 1) * FadeSteps
        }

        Particles.append(Particle)

    # Fade Effect
    for Step in range(FadeSteps + 1):
        Alpha = int(Step / FadeSteps * 255)
        LogoSurface.set_alpha(Alpha)

        Window.fill((0, 0, 0))

        for Particle in Particles:
            Particle['x'] += Particle['speed']

            LogoRect = pygame.Rect((WindowW - LogoW) //
                                   2, (WindowH - LogoH) // 2, LogoW, LogoH)
            ParticleRect = pygame.Rect(
                Particle['x'], Particle['y'], Particle['size'], Particle['size'])
            ParticleAlpha = int(Particle['fade'] / FadeSteps * 255)

            if not LogoRect.colliderect(ParticleRect):
                pygame.draw.circle(Window, (255, 255, 255, ParticleAlpha), (int(
                    Particle['x']), int(Particle['y'])), Particle['size'])

            if Particle['x'] > WindowW:
                Particle['x'] = 0
                Particle['y'] = random.randint(0, WindowH)

        Window.blit(LogoSurface, ((WindowW - LogoW) //
                    2, (WindowH - LogoH) // 2))

        pygame.display.flip()
        pygame.time.delay(int(StepDelay))

    pygame.time.delay(1000)


def SetupRFD():
    global RFD, RFDConditional, COMRFD, SerialRFD, OutputMessage

    RFDConditional = True

    try:
        Expected = "COM4"

        Ports = serial.tools.list_ports.comports()

        for Port in Ports:
            if Expected in Port.device:
                with Lock:
                    SerialRFD = serial.Serial(
                        port=Port.device,
                        baudrate=57600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=None
                    )

                pygame.mixer.music.load(Blop)
                pygame.mixer.music.play()

                OutputMessage = 'RFD Connection Established'

                RFDConditional = False
                RFD = True

                DisplayRadios()
                DisplayOutput()

                break
        else:
            raise ValueError('RFD Port Not Found')

    except (OSError, serial.SerialException, ValueError, Exception):
        with Lock:
            if SerialRFD:
                SerialRFD.close()
            SerialRFD = None

        OutputMessage = 'RFD Unavailable'

        RFDConditional = False
        RFD = False


def SetupIridium():
    global Iridium, IridiumConditional, OutputMessage

    IridiumConditional = True

    try:
        req = requests.get(
            "https://borealis.rci.montana.edu/meta/flights?imei={}".format(IMEI))
        req.raise_for_status()

        LatestFlight = req.json()[-1]

        pygame.mixer.music.load(Blop)
        pygame.mixer.music.play()

        OutputMessage = 'Iridium Connection Established'

        IridiumConditional = False
        Iridium = True

        DisplayRadios()
        DisplayOutput()

    except (requests.exceptions.RequestException, IndexError, KeyError, Exception):
        OutputMessage = 'Iridium Unavailable'

        IridiumConditional = False
        Iridium = False


def SetupAPRS():
    global APRS, APRSConditional
    global OutputMessage

    APRSConditional = True

    try:
        URL = "https://api.aprs.fi/api/get"

        Params = {
            'name': Callsign,
            'what': 'loc',
            'apikey': '186239.PvPtIQBgYaOM92d',
            'format': 'xml'
        }

        Response = requests.get(URL, params=Params)
        Response.raise_for_status()

        if Response.status_code == 200:
            root = ET.fromstring(Response.text)

            entry = root.find('entries/entry')
            name = entry.find('name').text
            lat = entry.find('lat').text
            lng = entry.find('lng').text
            alt = entry.find('altitude').text
            symbol = entry.find('symbol').text
            comment = entry.find('comment').text

        pygame.mixer.music.load(Blop)
        pygame.mixer.music.play()

        OutputMessage = 'APRS Connection Established'

        APRSConditional = False
        APRS = True

        DisplayRadios()
        DisplayOutput()

    except (requests.exceptions.RequestException, IndexError, KeyError, Exception):
        OutputMessage = 'APRS Unavailable'

        APRSConditional = False
        APRS = False


def SetupUbiquiti():
    global Ubiquiti, UbiquitiConditional, Cap, OutputMessage

    UbiquitiConditional = True

    Port = 8554

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((IP, Port))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    except (socket.timeout, socket.gaierror, ConnectionRefusedError, Exception):
        OutputMessage = 'Ubiquiti Unavailable'
        Ubiquiti = False
        UbiquitiConditional = False
        return

    RTSP = "rtsp://{}:{}/payload".format(IP, Port)

    try:
        Cap = cv2.VideoCapture(RTSP)
        if not Cap.isOpened():
            OutputMessage = 'Ubiquiti Unavailable'
            Ubiquiti = False
        else:
            OutputMessage = 'Ubiquiti Connection Established'
            Ubiquiti = True
    except (cv2.error, Exception):
        OutputMessage = 'Ubiquiti Unavailable'
        Ubiquiti = False

    UbiquitiConditional = False


def SetupArduino():
    global Arduino, ArduinoConditional, COMArduino, SerialArduino, OutputMessage

    ArduinoConditional = True

    try:
        Expected = "COM3"

        Ports = list(serial.tools.list_ports.comports())

        for Port in Ports:
            if Expected in Port.device:
                SerialArduino = serial.Serial(Port.device, 9600)
                SerialArduino.close()

                COMArduino = Port.device
                break
        else:
            OutputMessage = 'Arduino Unavailable'
            ArduinoConditional = False
            Arduino = False
            return

        time.sleep(2)

        SerialArduino = serial.Serial(COMArduino, 9600)
        pygame.mixer.music.load(Blop)
        pygame.mixer.music.play()

        OutputMessage = 'Arduino Connection Established'
        ArduinoConditional = False
        Arduino = True

        DisplayRadios()
        DisplayOutput()

    except (serial.SerialException, Exception):
        if 'SerialArduino' in locals():
            SerialArduino.close()
        SerialArduino = None

        OutputMessage = 'Arduino Unavailable'
        ArduinoConditional = False
        Arduino = False


def UpdateRFD():
    global RFD, SerialRFD, DataList, LatRFD, LonRFD, AltRFD, TimestampRFD, OutputMessage

    if SerialRFD:
        try:
            SerialRFD.timeout = 0.1
            RawData = SerialRFD.readline()

            if RawData:
                DecodedData = RawData.decode("utf-8")
                DataList = DecodedData.split(",")

                if len(DataList) >= 30:
                    packet, siv, fix, lat, lon, alt, year, month, day, hour, minute, sec, nedN, nedE, nedD, \
                        bat, bat33, bat51, bat52, aint, aext, ptemp, dint, dent, pres, ax, ay, az, pitch, roll, \
                        yaw = DataList[:31]

                    if lat != 0:
                        LatRFD = round(float(lat) * .0000001, 6)
                    if lon != 0:
                        LonRFD = round(float(lon) * .0000001, 6)
                    if alt != 0:
                        AltRFD = float(alt) / 1000 * 3.28084

                    TimestampRFD = ''.join(
                        [year, month, day, hour, minute, sec])

                    DataRow = [packet, siv, fix, lat, lon, alt, year, month, day, hour, minute, sec, nedN, nedE, nedD,
                               bat, bat33, bat51, bat52, aint, aext, ptemp, dint, dent, pres, ax, ay, az, pitch, roll, yaw]

                    if FileWrite:
                        Directory = os.path.join(os.getcwd(), "Data", "LogRFD")
                        os.makedirs(Directory, exist_ok=True)

                        DateString = datetime.datetime.now().strftime("%Y%m%d")
                        FileName = f"RFD_{DateString}.csv"
                        FilePath = os.path.join(Directory, FileName)

                        with open(FilePath, "a", newline='\n') as f:
                            writer = csv.writer(f, delimiter=',')
                            writer.writerow(DataRow)

        except (serial.SerialTimeoutException, Exception):
            pygame.mixer.music.load(Static)
            pygame.mixer.music.play()

            OutputMessage = 'RFD Downlink Failed'

            SerialRFD.close()
            SerialRFD = None

            RFD = False

    else:
        DataList = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                    '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'END\r\n']


def UpdateIridium():
    global Iridium, LatIridium, LonIridium, AltIridium, AscentRate, TimestampIridium, OutputMessage

    if Iridium:
        try:
            BaseURL = "https://borealis.rci.montana.edu"

            URL = "{}/meta/flights?imei={}".format(BaseURL, IMEI)
            Req = Session.get(URL)
            Req.raise_for_status()
            LatestFlight = Req.json()[-1]

            FlightTime = calendar.timegm(time.strptime(
                LatestFlight, "%Y-%m-%d")) - 1357023600

            UID = (int(FlightTime) << 24) | int(IMEI[8:])

            URL = "{}/flight?uid={}".format(BaseURL, UID)
            Req = Session.get(URL)
            Req.raise_for_status()
            Data = Req.json()

            if 'data' in Data and Data['data']:
                DataRow = Data['data'][-1]

                if DataRow[3] != 0:
                    LatIridium = DataRow[3]
                if DataRow[4] != 0:
                    LonIridium = DataRow[4]
                if DataRow[5] != 0:
                    AltIridium = DataRow[5] * 3.28084
                if DataRow[6] != 0:
                    AscentRate = DataRow[6] * 3.28084

                TimestampIridium = datetime.datetime.utcfromtimestamp(
                    DataRow[2]).strftime("%Y%m%d%H%M%S")

                if FileWrite:
                    Directory = os.path.join(os.getcwd(), "Data", "LogIridium")
                    os.makedirs(Directory, exist_ok=True)

                    DateString = datetime.datetime.now().strftime("%Y%m%d")
                    FileName = f"Iridium_{DateString}.csv"
                    FilePath = os.path.join(Directory, FileName)

                    with open(FilePath, "a", newline='\n') as f:
                        Writer = csv.writer(f, delimiter=',')
                        Writer.writerow(DataRow)

        except (requests.exceptions.RequestException, ValueError, IndexError, KeyError, TypeError, AttributeError, Exception):
            pygame.mixer.music.load(Static)
            pygame.mixer.music.play()

            OutputMessage = 'Iridium Downlink Failed'
            Iridium = False


def UpdateAPRS():
    global APRS, LatAPRS, LonAPRS, AltAPRS, TimestampAPRS, OutputMessage

    if APRS:
        try:
            URL = "https://api.aprs.fi/api/get"
            Params = {
                'name': Callsign,
                'what': 'loc',
                'apikey': '186239.PvPtIQBgYaOM92d',
                'format': 'xml'
            }

            Response = Session.get(URL, params=Params)
            Response.raise_for_status()

            if Response.status_code == 200:
                root = ET.fromstring(Response.text)
                entry = root.find('entries/entry')
                name = entry.find('name').text
                lat = entry.find('lat').text
                lon = entry.find('lng').text
                alt = entry.find('altitude').text
                symbol = entry.find('symbol').text
                comment = entry.find('comment').text

                if lat != 0:
                    LatAPRS = round(float(lat), 6)
                if lon != 0:
                    LonAPRS = round(float(lon), 6)
                if alt != 0:
                    AltAPRS = round(float(alt), 6)

                TimestampAPRS = datetime.datetime.fromtimestamp(
                    int(entry.find('time').text)).strftime("%Y%m%d%H%M%S")

                DataRow = [name, lat, lon, alt, symbol, comment]

                if FileWrite:
                    Directory = os.path.join(os.getcwd(), "Data", "LogAPRS")
                    os.makedirs(Directory, exist_ok=True)

                    DateString = datetime.datetime.now().strftime("%Y%m%d")
                    FileName = f"APRS_{DateString}.csv"
                    FilePath = os.path.join(Directory, FileName)

                    with open(FilePath, "a", newline='\n') as f:
                        Writer = csv.writer(f, delimiter=',')
                        Writer.writerow(DataRow)

            else:
                raise requests.exceptions.RequestException

        except (requests.exceptions.RequestException, ValueError, AttributeError, ET.ParseError, IndexError, Exception):
            pygame.mixer.music.load(Static)
            pygame.mixer.music.play()

            OutputMessage = 'APRS Downlink Failed'

            APRS = False


def UpdateUbiquiti():
    global Ubiquiti, VideoX, VideoY, VideoW, VideoH, Cap, OutputMessage, PrevFrameSize, PrevFrameTime

    if Fullscreen:
        VideoW = int(WindowW)
        VideoH = int(WindowH)
        VideoX = 0
        VideoY = 0
        ScreenX = 0
        ScreenY = 0
    else:
        VideoW = int(800 * SF)
        VideoH = int(600 * SF)
        VideoX = (WindowW - VideoW) // 2
        VideoY = (WindowH - VideoH) // 2
        ScreenX = int(WindowW / 2 - 400 * SF)
        ScreenY = int(WindowH / 2 - 250 * SF)

    ScreenOutline = (255, 255, 255)
    ScreenOutlineWidth = int(6 * SF)
    ScreenDimensions = (ScreenX, ScreenY, VideoW, VideoH)

    if Ubiquiti:
        CurrentTime = pygame.time.get_ticks()
        if PrevFrameTime is not None and CurrentTime - PrevFrameTime < 1000 // FPS:
            return
        PrevFrameTime = CurrentTime

        Ret, Frame = Cap.read()

        if not Ret:
            Cap.release()
            Ubiquiti = False
            OutputMessage = 'Ubiquiti Downlink Failed'
            return

        Frame = cv2.resize(Frame, (VideoW, VideoH))

        Frame = np.rot90(Frame, k=3)

        if PrevFrameSize != (VideoW, VideoH):
            Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
            PrevFrameSize = (VideoW, VideoH)

        Frame = pygame.surfarray.make_surface(Frame)
        Window.blit(Frame, (VideoX, VideoY + 50))
    else:
        Thumb = pygame.image.load(os.path.join(Resources, "Thumb.png"))
        Thumb = pygame.transform.scale(Thumb, (VideoW, VideoH))
        Window.blit(Thumb, ScreenDimensions)

    pygame.draw.rect(Window, ScreenOutline, ScreenDimensions,
                     ScreenOutlineWidth, border_radius=ScreenOutlineWidth)


def UpdateArduino():
    global Arduino, SerialArduino, Tracking, OutputMessage

    if Arduino:
        try:
            if Tracking:
                Command = '{:.2f}'.format(
                    SigmaPayload + SigmaTweak) + "," + '{:.2f}'.format(GammaPayload + GammaTweak)
            else:
                Command = '{:.2f}'.format(
                    SigmaTweak) + "," + '{:.2f}'.format(GammaTweak)

            SerialArduino.write(Command.encode())

        except (AttributeError, OSError, serial.SerialException, Exception):
            if SerialArduino:
                SerialArduino.close()
            SerialArduino = None

            pygame.mixer.music.load(Static)
            pygame.mixer.music.play()

            OutputMessage = 'Arduino Uplink Failed'

            Arduino = False
            Tracking = False


def Calculations():
    global PayloadLatD, PayloadLonD, PayloadAltF, TargetLatD, TargetLonD, TargetAltF, Distance2DPayload, Distance3DPayload, Distance2DTarget, Distance3DTarget, SigmaPayload, GammaPayload, SigmaTarget, GammaTarget, SigmaTweak, GammaTweak

    # Weighted Data Consolidation
    if not ManualTracking:
        WeightedRFD = 0.5
        WeightedAPRS = 0.5

        if Iridium and LatIridium != 0 and LonIridium != 0 and AltIridium != 0:
            PayloadLatD = LatIridium
            PayloadLonD = LonIridium
            PayloadAltF = AltIridium

            if RFD and APRS:
                if abs(LatIridium - LatRFD) < 0.1 and abs(LatIridium - LatRFD) < 0.1:
                    CorrectedLatRFD = LatRFD - LatIridium
                    CorrectedLonRFD = LonRFD - LonIridium
                    CorrectedRFDAlt = AltRFD - AltIridium

                    CorrectedAPRSLat = LatAPRS - LatIridium
                    CorrectedAPRSLon = LonAPRS - LonIridium
                    CorrectedAPRSAlt = AltAPRS - AltIridium

                    if LatRFD != 0 and LonRFD != 0 and AltRFD != 0 and LatAPRS != 0 and LonAPRS != 0 and AltAPRS != 0:
                        PayloadLatD = (WeightedRFD * CorrectedLatRFD + WeightedAPRS *
                                       CorrectedAPRSLat) / (WeightedRFD + WeightedAPRS)
                        PayloadLonD = (WeightedRFD * CorrectedLonRFD + WeightedAPRS *
                                       CorrectedAPRSLon) / (WeightedRFD + WeightedAPRS)
                        PayloadAltF = (WeightedRFD * CorrectedRFDAlt + WeightedAPRS *
                                       CorrectedAPRSAlt) / (WeightedRFD + WeightedAPRS)
                elif abs(LatIridium - LatRFD) >= 0.1 and abs(LatIridium - LatAPRS) < 0.1:
                    PayloadLatD = (LatAPRS + LatIridium) / 2
                    PayloadLonD = (LonAPRS + LonIridium) / 2
                    PayloadAltF = (AltAPRS + AltIridium) / 2
                elif abs(LatIridium - LatRFD) < 0.1 and abs(LatIridium - LatAPRS) >= 0.1:
                    PayloadLatD = (LatRFD + LatIridium) / 2
                    PayloadLonD = (LonRFD + LonIridium) / 2
                    PayloadAltF = (AltRFD + AltIridium) / 2
            elif RFD and not APRS:
                if LatRFD != 0 and LonRFD != 0 and AltRFD != 0 and abs(LatIridium - LatRFD) < 0.1:
                    PayloadLatD = (LatRFD + LatIridium) / 2
                    PayloadLonD = (LonRFD + LonIridium) / 2
                    PayloadAltF = (AltRFD + AltIridium) / 2
            elif not RFD and APRS:
                if LatAPRS != 0 and LonAPRS != 0 and AltAPRS != 0 and abs(LatIridium - LatAPRS) < 0.1:
                    PayloadLatD = (LatAPRS + LatIridium) / 2
                    PayloadLonD = (LonAPRS + LonIridium) / 2
                    PayloadAltF = (AltAPRS + AltIridium) / 2

        if not Iridium:
            if RFD and not APRS and LatRFD != 0 and LonRFD != 0 and AltRFD != 0:
                PayloadLatD = LatRFD
                PayloadLonD = LonRFD
                PayloadAltF = AltRFD
            if not RFD and APRS and LatAPRS != 0 and LonAPRS != 0 and AltAPRS != 0:
                PayloadLatD = LatAPRS
                PayloadLonD = LonAPRS
                PayloadAltF = AltAPRS
            if RFD and APRS and LatRFD != 0 and LonRFD != 0 and AltRFD != 0:
                if LatAPRS != 0 and LonAPRS != 0 and AltAPRS != 0:
                    PayloadLatD = (LatRFD + LatAPRS) / 2
                    PayloadLonD = (LonRFD + LonAPRS) / 2
                    PayloadAltF = (AltRFD + AltAPRS) / 2
                elif LatAPRS == 0 and LonAPRS == 0 and AltAPRS == 0:
                    PayloadLatD = LatRFD
                    PayloadLonD = LonRFD
                    PayloadAltF = AltRFD
                elif LatRFD == 0 and LonRFD == 0 and AltRFD == 0:
                    PayloadLatD = LatAPRS
                    PayloadLonD = LonAPRS
                    PayloadAltF = AltAPRS

    # Set Target to Tracker
    if ReturnToSender:
        TargetLatD = TrackerLatD
        TargetLonD = TrackerLonD
        TargetAltF = TrackerAltF

    DataRow = [PayloadLatD, PayloadLonD, PayloadAltF]

    # Aggregate Data File
    if FileWrite:
        Directory = os.path.join(os.getcwd(), "Data", "Aggregate")
        os.makedirs(Directory, exist_ok=True)

        DateString = datetime.datetime.now().strftime("%Y%m%d")
        FileName = f"Aggregate_{DateString}.csv"
        FilePath = os.path.join(Directory, FileName)

        with open(FilePath, "a", newline='\n') as f:
            Writer = csv.writer(f, delimiter=',')
            Writer.writerow(DataRow)

    # Constants
    R = 6371000.0
    a = 6378137.0

    # Distance Calculation (Tracker to Payload)
    dLat = math.radians(PayloadLatD - TrackerLatD)
    dLon = math.radians(PayloadLonD - TrackerLonD)
    dAlt = (PayloadAltF - TrackerAltF) * 0.3048

    Pos1 = [TrackerLatD, TrackerLonD, TrackerAltF / 5280]
    Pos2 = [PayloadLatD, PayloadLonD, PayloadAltF / 5280]

    Lat1, Lon1, Lat2, Lon2 = map(
        math.radians, [Pos1[0], Pos1[1], Pos2[0], Pos2[1]])

    dLon = Lon2 - Lon1
    dLat = Lat2 - Lat1

    a = math.sin(dLat / 2) ** 2 + math.cos(Lat1) * \
        math.cos(Lat2) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Downrange Distance (mi)
    Distance2DPayload = 3958.8 * c

    # Line-of-Sight Distance (mi)
    Distance3DPayload = math.sqrt(
        Distance2DPayload ** 2 + (Pos2[2] - Pos1[2]) ** 2)

    # Intermediary CalcuLations
    p = (math.sin(dLat / 2)) ** 2 + math.cos(Lat1) * \
        math.cos(Lat2) * (math.sin(dLon / 2)) ** 2
    q = 2 * math.atan2(math.sqrt(p), math.sqrt(1 - p))
    d = R * q

    # Azimuth
    y = math.sin(dLon) * math.cos(Lat2)
    x = math.cos(Lat1) * math.sin(Lat2) - math.sin(Lat1) * \
        math.cos(Lat2) * math.cos(dLon)
    Alpha = math.atan2(y, x)

    # Heading
    if Alpha < 0:
        Alpha += 2 * math.pi

    Azimuth = (3 * math.pi / 2 - Alpha) % (2 * math.pi)
    if Azimuth >= math.pi:
        Azimuth -= 2 * math.pi

    if Alpha < 0:
        Alpha += 2 * math.pi

    Azimuth = (3 * math.pi / 2 - Alpha) % (2 * math.pi)

    if Azimuth >= math.pi and Azimuth < 2 * math.pi:
        Azimuth -= 2 * math.pi

    # Pan Angle (Deg)
    SigmaPayload = (270) - math.degrees(Azimuth)

    if SigmaPayload >= 360:
        SigmaPayload -= 360

    # Tilt Angle (Deg)
    GammaPayload = math.degrees(math.atan2(dAlt, d))

    # Tweak Correction
    if SigmaTweak >= 360:
        SigmaTweak -= 360
    if GammaTweak >= 360:
        GammaTweak -= 360

    if SigmaTweak <= -360:
        SigmaTweak += 360
    if GammaTweak <= -360:
        GammaTweak += 360

    # Distance Calculation (Payload to Target)
    dLat = math.radians(TargetLatD - PayloadLatD)
    dLon = math.radians(TargetLonD - PayloadLonD)
    dAlt = (TargetAltF - PayloadAltF) * 0.3048

    Pos1 = [PayloadLatD, PayloadLonD, PayloadAltF / 5280]
    Pos2 = [TargetLatD, TargetLonD, TargetAltF / 5280]

    Lat1, Lon1, Lat2, Lon2 = map(
        math.radians, [Pos1[0], Pos1[1], Pos2[0], Pos2[1]])

    dLon = Lon2 - Lon1
    dLat = Lat2 - Lat1

    a = math.sin(dLat / 2) ** 2 + math.cos(Lat1) * \
        math.cos(Lat2) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Downrange Distance (mi)
    Distance2DTarget = 3958.8 * c

    # Line-of-Sight Distance (mi)
    Distance3DTarget = math.sqrt(
        Distance2DTarget ** 2 + (Pos2[2] - Pos1[2]) ** 2)

    # Intermediary Calculations
    p = (math.sin(dLat / 2)) ** 2 + math.cos(Lat1) * \
        math.cos(Lat2) * (math.sin(dLon / 2)) ** 2
    q = 2 * math.atan2(math.sqrt(p), math.sqrt(1 - p))
    d = R * q

    # Azimuth
    y = math.sin(dLon) * math.cos(Lat2)
    x = math.cos(Lat1) * math.sin(Lat2) - math.sin(Lat1) * \
        math.cos(Lat2) * math.cos(dLon)
    Alpha = math.atan2(y, x)

    # Heading
    if Alpha < 0:
        Alpha += 2 * math.pi

    Azimuth = (3 * math.pi / 2 - Alpha) % (2 * math.pi)
    if Azimuth >= math.pi:
        Azimuth -= 2 * math.pi

    if Alpha < 0:
        Alpha += 2 * math.pi

    Azimuth = (3 * math.pi / 2 - Alpha) % (2 * math.pi)

    if Azimuth >= math.pi and Azimuth < 2 * math.pi:
        Azimuth -= 2 * math.pi

    # Pan Angle (Deg)
    SigmaTarget = (270) - math.degrees(Azimuth)

    if SigmaTarget >= 360:
        SigmaTarget -= 360

    # Tilt Angle (Deg)
    GammaTarget = math.degrees(math.atan2(dAlt, d))


def DisplayTitle():
    if not Fullscreen:
        # Draw Logos
        Window.blit(LogoNASA, (int(530 * SF), int(60 * SF)))
        Window.blit(LogoNEBP, (int(1180 * SF), int(60 * SF)))

        # Title
        Font = pygame.font.SysFont("Impact", int(120 * SF))
        Title = Font.render("HERMES", True, (255, 255, 255))
        TitleRect = Title.get_rect(center=(int(960 * SF), int(135 * SF)))
        Window.blit(Title, TitleRect)

        # Subtitle
        Font = pygame.font.SysFont("Bahnschrift", int(40 * SF))
        Subtitle = Font.render("Video Telemetry GUI", True, (255, 255, 255))
        SubtitleRect = Subtitle.get_rect(
            center=(int(WindowW / 2), int(220 * SF)))
        Window.blit(Subtitle, SubtitleRect)


def DisplayAltitude():
    # Altimeter Placement
    AltimeterX = int(1420 * SF)
    AltimeterY = int(300 * SF)

    if not Fullscreen and DispAltitude:
        # Altitude Bar
        pygame.draw.rect(Window, (0, 0, 0), (AltimeterX,
                         AltimeterY, int(55 * SF), int(600 * SF)))

        # Indicator Marks
        for i in range(0, 120001, 1000):
            IndicatorY = int(AltimeterY + (600 * SF) - (i * 0.005 * SF))
            if i % 5000 == 0:
                pygame.draw.line(Window, (255, 255, 255), (AltimeterX + int(22 * SF),
                                 IndicatorY), (AltimeterX + int(37 * SF), IndicatorY), int(1 * SF))
            else:
                pygame.draw.line(Window, (255, 255, 255), (AltimeterX + int(25 * SF),
                                 IndicatorY), (AltimeterX + int(35 * SF), IndicatorY), int(1 * SF))

        # Altitude Indicator
        IndicatorY = int(AltimeterY + (600 * SF) - (PayloadAltF * 0.005 * SF))
        pygame.draw.line(Window, (255, 255, 255), (AltimeterX, IndicatorY),
                         (AltimeterX + int(60 * SF), IndicatorY), int(4 * SF))

        # Divider
        pygame.draw.line(Window, (255, 255, 255), (AltimeterX + int(160 * SF), AltimeterY - int(
            20 * SF)), (AltimeterX + int(160 * SF), AltimeterY + int(620 * SF)), int(4 * SF))

        # Text Markings
        Altitude = [
            (pygame.font.SysFont("Bahnschrift", int(20 * SF)), "0 ft", 595),
            (pygame.font.SysFont("Bahnschrift", int(20 * SF)), "15,000 ft", 517.5),
            (pygame.font.SysFont("Bahnschrift", int(20 * SF)), "50,000 ft", 342.5),
            (pygame.font.SysFont("Bahnschrift", int(20 * SF)), "80,000 ft", 192.5),
            (pygame.font.SysFont("Bahnschrift", int(20 * SF)), "110,000 ft", 42.5),
        ]

        for Font, Text, Offset in Altitude:
            TextSurface = Font.render(Text, True, (255, 255, 255))
            TextRect = TextSurface.get_rect(
                topleft=(AltimeterX + int(65 * SF), AltimeterY + int(Offset * SF)))
            Window.blit(TextSurface, TextRect)

        # Altitude Markers
        Altitude = [
            (pygame.font.SysFont("Impact", int(20 * SF)), "SEA LEVEL", 595),
            (pygame.font.SysFont("Impact", int(20 * SF)), "HIGH CLOUDS", 512.5),
            (pygame.font.SysFont("Impact", int(20 * SF)), "STRATOSPHERE", 337.5),
            (pygame.font.SysFont("Impact", int(20 * SF)), "FLOAT ALTITUDE", 187.5),
            (pygame.font.SysFont("Impact", int(20 * SF)), "BURST ALTITUDE", 37.5),
        ]

        for Font, Text, Offset in Altitude:
            TextSurface = Font.render(Text, True, (255, 255, 255))
            TextRect = TextSurface.get_rect(
                topleft=(AltimeterX + int(180 * SF), AltimeterY + int(Offset * SF)))
            Window.blit(TextSurface, TextRect)

        # Triangle Markers
        TriangleSize = int(10 * SF)
        TriangleColor = (255, 255, 255)
        TriangleY = [AltimeterY + int(597.5 * SF), AltimeterY + int(520 * SF), AltimeterY + int(
            345 * SF), AltimeterY + int(195 * SF), AltimeterY + int(45 * SF)]
        TriangleX = AltimeterX - TriangleSize + int(65 * SF)

        for Y, X in zip(TriangleY, [TriangleX] * len(TriangleY)):
            pygame.draw.polygon(Window, TriangleColor, [
                                (X, Y), (X - TriangleSize, Y + TriangleSize / 2), (X, Y + TriangleSize)], 0)

        # Divider
        pygame.draw.line(Window, (255, 255, 255), (int(
            1380 * SF), int(950 * SF)), (int(1780 * SF), int(950 * SF)), 1)

        # Ascent Information
        Font = pygame.font.SysFont("Bahnschrift", int(25 * SF))

        Text = Font.render("ALTITUDE", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1380 * SF), int(965 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render("DISTANCE", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1600 * SF), int(965 * SF)))
        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(15 * SF))

        Text = Font.render("ASCENT RATE", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1380 * SF), int(1005 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render("DOWNRANGE", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1600 * SF), int(1005 * SF)))
        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))

        Text = Font.render(
            str("{:.0f}".format(PayloadAltF)) + " ft", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1505 * SF), int(970 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render(
            str("{:.1f}".format(Distance3DPayload)) + " mi", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1725 * SF), int(970 * SF)))
        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(15 * SF))

        Text = Font.render(str("{:.1f}".format(AscentRate)) + " ft/s", True, (255, 255, 255)
                           ) if not ManualTracking else Font.render("0 ft/s", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1505 * SF), int(1005 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render(
            str("{:.1f}".format(Distance2DPayload)) + " mi", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(1725 * SF), int(1005 * SF)))
        Window.blit(Text, TextRect)


def DisplayLocation():
    global Mun, Cou, Sub, Position, Location, PrevLatD, PrevLonD, PrevAltF

    if not Fullscreen and DispLocation:
        # Updated Payload Position
        if (
            PrevLatD is None
            or PrevLonD is None
            or PrevAltF is None
            or abs(PayloadLatD - PrevLatD) >= 0.1
            or abs(PayloadLonD - PrevLonD) >= 0.1
            or abs(PayloadAltF - PrevAltF) >= 100
        ):
            # OpenStreetMap API
            URL = "https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}".format(
                PayloadLatD, PayloadLonD)

            try:
                Response = requests.get(URL)
                Response.raise_for_status()
                Data = Response.json()

                if Data is not None:
                    # Geographic Information
                    Address = Data.get("address", {})
                    Mun = Address.get("town") or Address.get("city") or Address.get(
                        "nearest_town") or Address.get("nearest_city") or "Unknown"
                    Cou = Address.get("county")
                    Sub = Address.get("ISO3166-2-lvl4",
                                      "").split("-")[-1].strip()

                    # Cardinal Directions
                    if PayloadLatD >= 0:
                        LatDirection = "N"
                    else:
                        LatDirection = "S"

                    if PayloadLonD >= 0:
                        LonDirection = "E"
                    else:
                        LonDirection = "W"

                    # Coordinate String
                    Position = "{:.2f}°{}, {:.2f}°{}".format(
                        abs(PayloadLatD), LatDirection, abs(PayloadLonD), LonDirection)

                    # Location String
                    if Mun != "Unknown":
                        if Sub:
                            Location = "{}, {}".format(Mun, Sub)
                        else:
                            Location = Mun
                    else:
                        if Sub:
                            if Cou:
                                Location = "{}, {}".format(Cou, Sub)
                            else:
                                Location = "Rural {}".format(Sub)
                        else:
                            Location = "International Waters"

                    # Abbreviate Long Strings
                    if len(Location) > 20:
                        Location = Location[:20] + "..."

                    # Reset Payload Position
                    PrevLatD = PayloadLatD
                    PrevLonD = PayloadLonD
                    PrevAltF = PayloadAltF

            except requests.exceptions.RequestException:
                Position = "0.00°N, 0.00°E"
                Location = "Location Unavailable"

        # Coordinate and Altitude Display
        Font = pygame.font.SysFont("Bahnschrift", int(25 * SF))
        Text = Font.render(Position, True, (255, 255, 255))
        TextRect = Text.get_rect(midright=(int(1372.5 * SF), int(842.5 * SF)))
        TextWidth = Text.get_width()

        RightEdge = int(1180 * SF) + 200 * SF
        RectWidth = TextWidth + int(20 * SF)
        LeftEdge = RightEdge - RectWidth

        pygame.draw.rect(Window, (0, 0, 0), (600 * SF,
                         860 * SF, 780 * SF, 60 * SF))
        pygame.draw.rect(Window, (255, 255, 255), (600 * SF,
                         860 * SF, 780 * SF, 60 * SF), int(2 * SF))

        pygame.draw.rect(Window, (0, 0, 0), (LeftEdge,
                         820 * SF, RectWidth, 40 * SF))
        pygame.draw.rect(Window, (255, 255, 255), (LeftEdge,
                         820 * SF, RectWidth, 40 * SF), int(2 * SF))

        pygame.draw.rect(Window, (0, 0, 0), (LeftEdge + 2 * SF,
                         840 * SF, RectWidth - 4 * SF, 50 * SF))

        Window.blit(Text, TextRect)

        # Geographic Location Display
        if Location != '':
            Font = pygame.font.SysFont("Bahnschrift", int(40 * SF))
            Text = Font.render(Location, True, (255, 255, 255))
        else:
            Font = pygame.font.SysFont("Bahnschrift", int(30 * SF))
            Text = Font.render("Location Unavailable", True, (255, 255, 255))

        TextRect = Text.get_rect(midright=(int(1372.5 * SF), int(892.5 * SF)))
        Window.blit(Text, TextRect)


def DisplayCompass():
    global CompassX, CompassY, CircleBlack, CircleWhite

    # Compass Placement
    CompassX = int(560 * SF)
    CompassY = int(890 * SF)

    if not Fullscreen and DispCompass:
        LargeTicks = 24
        SmallTicks = 3

        LargeAngle = 2 * math.pi / LargeTicks
        SmallAngle = LargeAngle / SmallTicks

        NeedleLength = int(60 * SF)

        # Compass Outline
        CircleWhite = pygame.transform.smoothscale(
            CircleWhite, (int(160 * SF), int(160 * SF)))
        CircleBlack = pygame.transform.smoothscale(
            CircleBlack, (int(155 * SF), int(155 * SF)))
        Window.blit(CircleWhite, (int(CompassX - 80 * SF),
                    int(CompassX + 250 * SF)))
        Window.blit(CircleBlack, (int(CompassX - 77.5 * SF),
                    int(CompassX + 252.5 * SF)))

        # Large Radial Ticks
        for i in range(LargeTicks):
            Angle = LargeAngle * i
            X1 = CompassX + math.cos(Angle) * int(60 * SF)
            Y1 = CompassY + math.sin(Angle) * int(60 * SF)
            X2 = CompassX + math.cos(Angle) * int(70 * SF)
            Y2 = CompassY + math.sin(Angle) * int(70 * SF)

            pygame.draw.line(Window, (255, 255, 255),
                             (int(X1), int(Y1)), (int(X2), int(Y2)), 1)

        # Small Radial Ticks
        for i in range(LargeTicks * SmallTicks):
            X1 = CompassX + math.cos(SmallAngle * i) * int(70 * SF)
            Y1 = CompassY + math.sin(SmallAngle * i) * int(70 * SF)
            X2 = CompassX + math.cos(SmallAngle * i) * int(72 * SF)
            Y2 = CompassY + math.sin(SmallAngle * i) * int(72 * SF)

            pygame.draw.line(Window, (255, 255, 255),
                             (int(X1), int(Y1)), (int(X2), int(Y2)), 1)

        # Cardinal Directions
        Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))

        Directions = [
            ("N", (CompassX, CompassY - int(40 * SF))),
            ("E", (CompassX + int(40 * SF), CompassY)),
            ("S", (CompassX, CompassY + int(40 * SF))),
            ("W", (CompassX - int(40 * SF), CompassY)),
        ]

        for Dir, Pos in Directions:
            Text = Font.render(Dir, True, (255, 255, 255))
            TextRect = Text.get_rect(center=Pos)
            Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(25 * SF))

        # Compass Needle
        CompassNeedleX = 0
        CompassNeedleY = 0
        CompassBaseX = 0
        CompassBaseY = 0

        # Point from Tracker to Payload
        if CompassSetting == 1:
            Text = Font.render("Tracker > Payload", True, (255, 255, 255))
            CompassNeedleX = CompassX + \
                math.cos(math.radians(SigmaPayload) -
                         math.pi / 2) * NeedleLength
            CompassNeedleY = CompassY + \
                math.sin(math.radians(SigmaPayload) -
                         math.pi / 2) * NeedleLength
            CompassBaseX = CompassX - \
                math.cos(math.radians(SigmaPayload) - math.pi / 2) * 10 * SF
            CompassBaseY = CompassY - \
                math.sin(math.radians(SigmaPayload) - math.pi / 2) * 10 * SF

        # Point from Payload to Target
        if CompassSetting == 2:
            Text = Font.render("Payload > Target", True, (255, 255, 255))
            CompassNeedleX = CompassX + \
                math.cos(math.radians(SigmaTarget) -
                         math.pi / 2) * NeedleLength
            CompassNeedleY = CompassY + \
                math.sin(math.radians(SigmaTarget) -
                         math.pi / 2) * NeedleLength
            CompassBaseX = CompassX - \
                math.cos(math.radians(SigmaTarget) - math.pi / 2) * 10 * SF
            CompassBaseY = CompassY - \
                math.sin(math.radians(SigmaTarget) - math.pi / 2) * 10 * SF

        TextRect = Text.get_rect(topleft=(int(650 * SF), int(867.5 * SF)))
        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(15 * SF))

        Text = Font.render("Click Compass to Change", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(650 * SF), int(897.5 * SF)))
        Window.blit(Text, TextRect)

        for Offset in range(-(int(3 * SF) // 2), int(3 * SF) // 2 + 1):
            pygame.draw.line(Window, (255, 0, 0), (int(CompassBaseX), int(
                CompassBaseY) + Offset), (int(CompassNeedleX), int(CompassNeedleY) + Offset))

        # Compass Center
        pygame.gfxdraw.filled_circle(
            Window, CompassX, CompassY, int(10 * SF), (255, 255, 255))


def DisplayTime():
    global Capture, Countdown1, Countdown2, Countdown3, LaunchTime, Launched, Map, MapFile, MET, OutputMessage, Recording, StartTime, Time, UTC, PrevTime

    try:
        # Launch Timer Start
        if Launched and LaunchTime is None:
            LaunchTime = datetime.datetime.utcnow().strftime("%H:%M:%S")
            StartTime = datetime.datetime.now()

            OutputMessage = "Launch Timer Commenced"

            # Ten-Second Countdown
            if Countdown1:
                pygame.mixer.music.load(Launch10)
                pygame.mixer.music.play()
                MET = "T  - 00:00:10"

            # Thirty-Second Countdown
            elif Countdown2:
                pygame.mixer.music.load(Launch30)
                pygame.mixer.music.play()
                MET = "T  - 00:00:30"

            # Sixty-Second Countdown
            elif Countdown3:
                pygame.mixer.music.load(Launch60)
                pygame.mixer.music.play()
                MET = "T  - 00:01:00"

            # Zero-Second Countdown
            else:
                pygame.mixer.music.load(Launch00)
                pygame.mixer.music.play()
                MET = "T  - 00:00:00"

            # Create Map File
            if Map is None:
                Map = folium.Map()
                Count = 1

                if not os.path.exists("Maps"):
                    os.makedirs("Maps")

                while os.path.exists(f"Maps/Map{Count}.html"):
                    Count += 1

                MapFile = f"Maps/Map{Count}.html"

            # Create Video File
            Count = 1

            if not os.path.exists("Videos"):
                os.makedirs("Videos")

            while os.path.exists(f"Videos/Video{Count}.mp4"):
                Count += 1

            Timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            Filename = f"Video{Timestamp}_{Count}.mp4"

            FourCC = cv2.VideoWriter_fourcc(*"mp4v")
            Capture = cv2.VideoWriter(os.path.join(
                "Videos", Filename), FourCC, 20.0, (int(WindowW), int(WindowH)), isColor=True)
            Recording = True

        # Launch Timer Halt
        if not Launched:
            LaunchTime = None
            StartTime = None

            MET = "T  - 00:00:00"

            # Save Map File
            if Map is not None:
                Map.save(MapFile)
                Map = None
                MapFile = None

            # Save Video File
            if Recording:
                Recording = False
                Capture.release()
                Capture = None

        # Update MET and UTC
        CurrentUTC = datetime.datetime.utcnow()

        if PrevTime is None or CurrentUTC.second != PrevTime:
            PrevTime = CurrentUTC.second

            if Launched:
                Elapsed = datetime.datetime.now() - StartTime
                S = Elapsed.total_seconds()

                if Countdown1:
                    CountdownTime = 10
                elif Countdown2:
                    CountdownTime = 30
                elif Countdown3:
                    CountdownTime = 60
                else:
                    CountdownTime = 0

                # Count Down
                if S < CountdownTime:
                    S = CountdownTime - S
                    H = int(S / 3600)
                    M = int((S % 3600) / 60)
                    S = int(S % 60)
                    MET = "T  - {:02d}:{:02d}:{:02d}".format(H, M, S)

                # Count Up
                else:
                    S -= CountdownTime - 1
                    H = int(S / 3600)
                    M = int((S % 3600) / 60)
                    S = int(S % 60)
                    MET = "T + {:02d}:{:02d}:{:02d}".format(H, M, S)

        UTC = CurrentUTC.strftime("%H:%M:%S")

        if Recording:
            # Capture Frame
            Frame = pyautogui.screenshot(region=(0, 0, WindowW, WindowH))
            Frame = cv2.cvtColor(np.array(Frame), cv2.COLOR_RGB2BGR)
            Capture.write(Frame)

        if not Fullscreen and DispTime:
            # Text Background
            pygame.draw.rect(Window, (0, 0, 0), (int(810 * SF),
                             int(270 * SF), int(300 * SF), int(95 * SF)))
            pygame.draw.rect(Window, (255, 255, 255), (int(
                810 * SF), int(270 * SF), int(300 * SF), int(95 * SF)), 2)

            # Text Boxes
            Font = pygame.font.SysFont("Calibri", int(50 * SF))

            if Launched:
                Text = Font.render(MET, True, (255, 255, 255))
            else:
                if not Countdown1 and not Countdown2 and not Countdown3:
                    Text = Font.render("T  - 00:00:00", True, (255, 255, 255))
                elif Countdown1:
                    Text = Font.render("T  - 00:00:10", True, (255, 255, 255))
                elif Countdown2:
                    Text = Font.render("T  - 00:00:30", True, (255, 255, 255))
                elif Countdown3:
                    Text = Font.render("T  - 00:01:00", True, (255, 255, 255))

            TextRect = Text.get_rect()
            TextRect.center = (int(960 * SF), int(300 * SF))
            Window.blit(Text, TextRect)

            Font = pygame.font.SysFont("Calibri", int(30 * SF))
            Text = Font.render("UTC " + UTC, True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.center = (int(960 * SF), int(345 * SF))
            Window.blit(Text, TextRect)

        # Update Map
        if Launched and Map is not None:
            if PayloadLatD != 0 and PayloadLonD != 0:
                folium.CircleMarker([PayloadLatD, PayloadLonD], radius=2, fill=True, color='black',
                                    fill_color='black', popup=f"{int(PayloadAltF)}⠀ft").add_to(Map)

    except Exception:
        OutputMessage = 'Launch Timer Error'

        if Recording:
            # Append Final Frame
            Frame = pyautogui.screenshot(region=(0, 0, WindowW, WindowH))
            Frame = cv2.cvtColor(np.array(Frame), cv2.COLOR_RGB2BGR)
            Capture.write(Frame)

            # Save Video File
            if not Launched:
                Recording = False
                Capture.release()
                Capture = None


def DisplayRadios():
    global RadioX, RadioY, RadioW, RadioH, RadioS

    # Radio Placement
    RadioX = int(200 * SF)
    RadioY = int(350 * SF)
    RadioW = int(60 * SF)
    RadioH = int(30 * SF)
    RadioS = int(70 * SF)

    if not Fullscreen:
        # Header Text
        Font = pygame.font.SysFont("Bahnschrift", int(24 * SF))
        Text = Font.render("RADIO/SERIAL CONNECTIVITY", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (RadioX + 105 * SF, 320 * SF)
        Window.blit(Text, TextRect)

        # Radio Labels
        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Names = ["RFD", "Iridium", "APRS", "Ubiquiti", "Arduino"]
        Colors = [(0, 200, 0, 0.8), (120, 0, 0, 0.2)]
        Connections = [RFD, Iridium, APRS, Ubiquiti, Arduino]
        Conditionals = [RFDConditional, IridiumConditional,
                        APRSConditional, UbiquitiConditional, ArduinoConditional]

        # Radio Buttons
        for i in range(5):
            ButtonX = int((i + 0.5) * RadioS + RadioX - 100 * SF)
            Color = (120, 0, 0, 0.6) if Conditionals[i] else (
                Colors[0] if Connections[i] else Colors[1])

            pygame.draw.rect(Window, Color, (ButtonX, RadioY, RadioW, RadioH))
            pygame.draw.rect(Window, (50, 50, 50, 0.8),
                             (ButtonX, RadioY, RadioW, RadioH), int(3 * SF))
            pygame.draw.rect(Window, (50, 50, 50, 0.8), (ButtonX, int(
                RadioY + 1.5 * RadioH), RadioW, RadioH // 1.5))

            Text = Font.render(Names[i], True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.center = (ButtonX + int(RadioW / 2),
                               RadioY + int(1.8 * RadioH))
            Window.blit(Text, TextRect)

        # Dividers
        pygame.draw.line(Window, (255, 255, 255), (RadioX - int(65 * SF), RadioY - int(
            12.5 * SF)), (RadioX + int(275 * SF), RadioY - int(12.5 * SF)), int(3 * SF))
        pygame.draw.line(Window, (255, 255, 255), (RadioX - int(65 * SF), RadioY + int(
            80 * SF)), (RadioX + int(275 * SF), RadioY + int(80 * SF)), int(3 * SF))


def DisplayOutput():
    global OutputMessage

    # Output Placement
    OutputX = int(135 * SF)
    OutputY = int(450 * SF)
    OutputW = int(340 * SF)
    OutputH = int(30 * SF)

    if not Fullscreen:
        # Output Bos
        pygame.draw.rect(Window, (0, 0, 0),
                         (OutputX, OutputY, OutputW, OutputH))
        pygame.draw.rect(Window, (255, 255, 255),
                         (OutputX, OutputY, OutputW, OutputH), 1)

        # Output Dialogue
        Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
        OutputText = Font.render(OutputMessage, True, (255, 255, 255))
        TextRect = OutputText.get_rect(
            center=(OutputX + OutputW / 2, OutputY + OutputH / 2))
        Window.blit(OutputText, TextRect)


def DisplayControls():
    global ControlX, ControlY, ControlR, TriangleHeight, TriangleShapes

    # Control Placement
    ControlX = int(300 * SF)
    ControlY = int(600 * SF)
    ControlR = int(50 * SF)

    if not Fullscreen:

        # D-Pad Arrows
        TriangleHeight = int(math.sqrt(3) * ControlR / 2)
        TriangleShapes = [
            [(ControlX, ControlY - 2 * TriangleHeight), (ControlX - 0.75 * ControlR, ControlY - TriangleHeight),
             (ControlX + 0.75 * ControlR, ControlY - TriangleHeight)],
            [(ControlX, ControlY + 2 * TriangleHeight), (ControlX - 0.75 * ControlR, ControlY + TriangleHeight),
             (ControlX + 0.75 * ControlR, ControlY + TriangleHeight)],
            [(ControlX + 2 * TriangleHeight, ControlY), (ControlX + TriangleHeight, ControlY - 0.75 * ControlR),
             (ControlX + TriangleHeight, ControlY + 0.75 * ControlR)],
            [(ControlX - 2 * TriangleHeight, ControlY), (ControlX - TriangleHeight, ControlY - 0.75 * ControlR),
             (ControlX - TriangleHeight, ControlY + 0.75 * ControlR)]
        ]

        # Display D-Pad
        Window.blit(DPad, (int(ControlX - 85 * SF), int(ControlY - 85 * SF)))

        # Angle Displays
        FontBahnschrift28 = pygame.font.SysFont("Bahnschrift", int(28 * SF))
        FontBahnschrift20 = pygame.font.SysFont("Bahnschrift", int(20 * SF))
        FontBahnschrift25 = pygame.font.SysFont("Bahnschrift", int(25 * SF))
        FontCalibri = pygame.font.SysFont("Calibri", int(18 * SF))
        FontImpact = pygame.font.SysFont("Impact", int(32 * SF))

        Labels = [
            ("Pan: ", (ControlX - 120 * SF, ControlY + 150 * SF)),
            ("Tilt: ", (ControlX + 45 * SF, ControlY + 150 * SF))
        ]

        for Label, Pos in Labels:
            Text = FontBahnschrift28.render(Label, True, (255, 255, 255))
            TextRect = Text.get_rect(midleft=(int(Pos[0]), int(Pos[1])))
            Window.blit(Text, TextRect)

        Angles = [
            (str("{:.0f}°".format(int(SigmaPayload))),
             (ControlX - 60 * SF, ControlY + 145 * SF)),
            (str("{:.0f}°".format(int(GammaPayload))),
             (ControlX + 95 * SF, ControlY + 145 * SF))
        ]

        for Angle, Pos in Angles:
            Text = FontImpact.render(Angle, True, (255, 255, 255))
            TextRect = Text.get_rect(midleft=(int(Pos[0]), int(Pos[1])))
            Window.blit(Text, TextRect)

        Tweaks = [
            ("Tweak: {:.0f}°".format(int(SigmaTweak)),
             (ControlX - 120 * SF, ControlY + 180 * SF)),
            ("Tweak: {:.0f}°".format(int(GammaTweak)),
             (ControlX + 45 * SF, ControlY + 180 * SF))
        ]

        for Tweak, Pos in Tweaks:
            Text = FontCalibri.render(Tweak, True, (255, 255, 255))
            TextRect = Text.get_rect(midleft=(int(Pos[0]), int(Pos[1])))
            Window.blit(Text, TextRect)

        # Tracking Label
        pygame.draw.line(Window, (255, 255, 255), (ControlX - 20 * SF,
                         ControlY - 20 * SF), (ControlX - 70 * SF, ControlY - 70 * SF))
        pygame.draw.line(Window, (255, 255, 255), (ControlX - 160 * SF,
                         ControlY - 70 * SF), (ControlX - 60 * SF, ControlY - 70 * SF))

        Text = FontBahnschrift20.render("TRACKING", True, (255, 255, 255))
        TextRect = Text.get_rect(
            midleft=(int(ControlX - 160 * SF), int(ControlY - (80 * SF))))
        Window.blit(Text, TextRect)

        # Tweak Offset Label
        pygame.draw.line(Window, (255, 255, 255), (ControlX - 70 *
                         SF, ControlY), (ControlX - 120 * SF, ControlY + 50 * SF))
        pygame.draw.line(Window, (255, 255, 255), (ControlX - 260 * SF,
                         ControlY + 50 * SF), (ControlX - 110 * SF, ControlY + 50 * SF))

        Text = FontBahnschrift20.render("TWEAK OFFSET", True, (255, 255, 255))
        TextRect = Text.get_rect(
            midleft=(int(ControlX - 260 * SF), int(ControlY + 40 * SF)))
        Window.blit(Text, TextRect)

        # Brackets
        pygame.draw.line(Window, (255, 255, 255), (ControlX - 150 * SF,
                         ControlY + 140 * SF), (ControlX - 150 * SF, ControlY + 180 * SF))
        pygame.draw.line(Window, (255, 255, 255), (ControlX + 150 * SF,
                         ControlY + 140 * SF), (ControlX + 150 * SF, ControlY + 180 * SF))

        pygame.draw.line(Window, (255, 255, 255), (ControlX - 155 * SF,
                         ControlY + 160 * SF), (ControlX - 150 * SF, ControlY + 160 * SF))
        pygame.draw.line(Window, (255, 255, 255), (ControlX + 150 * SF,
                         ControlY + 160 * SF), (ControlX + 155 * SF, ControlY + 160 * SF))

        Text = FontBahnschrift25.render("{:.0f}°".format(
            SigmaPayload + SigmaTweak), True, (255, 255, 255))
        TextRect = Text.get_rect(
            midright=(int(ControlX - 165 * SF), int(ControlY + 160 * SF)))
        Window.blit(Text, TextRect)

        Text = FontBahnschrift25.render("{:.0f}°".format(
            GammaPayload + GammaTweak), True, (255, 255, 255))
        TextRect = Text.get_rect(
            midleft=(int(ControlX + 165 * SF), int(ControlY + 160 * SF)))
        Window.blit(Text, TextRect)

        pygame.draw.line(Window, (255, 255, 255), (ControlX - 150 * SF,
                         ControlY + 200 * SF), (ControlX + 150 * SF, ControlY + 200 * SF))
        pygame.draw.line(Window, (255, 255, 255), (ControlX,
                         ControlY + 200 * SF), (ControlX, ControlY + 210 * SF))

        Text = FontBahnschrift20.render(
            "POINTING ANGLES", True, (255, 255, 255))
        TextRect = Text.get_rect(
            center=(int(ControlX), int(ControlY + 230 * SF)))
        Window.blit(Text, TextRect)


def DisplayLaunch():
    global Launch1, Launch2, Launched
    global LaunchX, LaunchY, LaunchW, LaunchH, LaunchS
    global ResetX, ResetY, ResetW, ResetH, ResetR
    global CountdownX, CountdownY, CountdownW, CountdownH
    global Countdown1, Countdown2, Countdown3

    # Launch Button Values
    LaunchX = int(960 * SF)
    LaunchY = int(1020 * SF)
    LaunchW = int(30 * SF)
    LaunchH = int(30 * SF)
    LaunchS = int(40 * SF)

    # Reset Button Values
    ResetX = int(LaunchX + (140 * SF))
    ResetY = int(LaunchY)
    ResetW = int(20 * SF)
    ResetH = int(20 * SF)
    ResetR = int(8 * SF)

    # Countdown Button Values
    CountdownX = 710 * SF
    CountdownY = 1005 * SF
    CountdownW = 50 * SF
    CountdownH = 30 * SF

    if not Fullscreen:
        BackgroundShapes = [
            ((LaunchX - LaunchS - LaunchW / 2, LaunchY - 60 * SF),
             (LaunchW + 80 * SF, LaunchH + 10 * SF)),
            ((LaunchX - 55 * SF, LaunchY + 20 * SF),
             (LaunchW + 80 * SF, LaunchH + 10 * SF)),
            ((LaunchX + 170 * SF, LaunchY - 60 * SF),
             (LaunchW + 130 * SF, LaunchH + 90 * SF)),
            ((LaunchX - 250 * SF, LaunchY - 60 * SF),
             (LaunchW + 130 * SF, LaunchH + 10 * SF)),
            ((LaunchX - 250 * SF, LaunchY + 20 * SF),
             (LaunchW + 130 * SF, LaunchH + 10 * SF))
        ]

        for Rect in BackgroundShapes:
            pygame.draw.rect(Window, (50, 50, 50, 0.80), Rect)
            pygame.draw.rect(Window, (255, 255, 255, 1), Rect, int(1 * SF))

        Lines = [
            ((LaunchX - 60 * SF, LaunchY - 60 * SF),
             (LaunchX - 60 * SF, 1080 * SF)),
            ((LaunchX + 60 * SF, LaunchY - 60 * SF),
             (LaunchX + 60 * SF, 1080 * SF)),
            ((LaunchX + 65 * SF, LaunchY), (LaunchX + 130 * SF, LaunchY)),
            ((LaunchX + 135 * SF, LaunchY - 60 * SF),
             (LaunchX + 135 * SF, LaunchY + 60 * SF)),
            ((LaunchX + 165 * SF, LaunchY - 60 * SF),
             (LaunchX + 165 * SF, LaunchY + 60 * SF)),
            ((LaunchX - 85 * SF, LaunchY - 60 * SF),
             (LaunchX - 85 * SF, LaunchY + 60 * SF)),
            ((LaunchX - 255 * SF, LaunchY - 60 * SF),
             (LaunchX - 255 * SF, LaunchY + 60 * SF))
        ]

        for Line in Lines:
            pygame.draw.line(Window, (255, 255, 255), Line[0], Line[1])

        # Labels
        Font = pygame.font.SysFont("Bahnschrift", int(25 * SF))

        Text = Font.render("LAUNCH", True, (255, 255, 255))
        TextRect = Text.get_rect(center=(LaunchX, LaunchY - int(40 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render("TIMER RESET", True, (255, 255, 255))
        TextRect = Text.get_rect(
            center=(LaunchX + int(250 * SF), LaunchY - int(40 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render("SET CLOCK", True, (255, 255, 255))
        TextRect = Text.get_rect(
            center=(LaunchX - int(170 * SF), LaunchY - int(40 * SF)))
        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))

        Text = Font.render("L1", True, (255, 255, 255))
        TextRect = Text.get_rect(
            center=(LaunchX - LaunchS, LaunchY + int(40 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render("L2", True, (255, 255, 255))
        TextRect = Text.get_rect(
            center=(LaunchX + LaunchS, LaunchY + int(40 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render("PRESS ALL FOUR", True, (255, 255, 255))
        TextRect = Text.get_rect(
            center=(LaunchX + int(250 * SF), LaunchY + int(10 * SF)))
        Window.blit(Text, TextRect)

        Text = Font.render("TO HALT THE CLOCK", True, (255, 255, 255))
        TextRect = Text.get_rect(
            center=(LaunchX + int(250 * SF), LaunchY + int(30 * SF)))
        Window.blit(Text, TextRect)

        # Launch Buttons
        if Launch1:
            Color = (0, 200, 0, 0.8)
        else:
            Color = (120, 0, 0, 0.2)

        pygame.draw.rect(Window, Color, (LaunchX - LaunchS -
                         LaunchW / 2, LaunchY - LaunchH / 2, LaunchW, LaunchH))

        if Launch2:
            Color = (0, 200, 0, 0.8)
        else:
            Color = (120, 0, 0, 0.2)

        pygame.draw.rect(Window, Color, (LaunchX + LaunchS -
                         LaunchW / 2, LaunchY - LaunchH / 2, LaunchW, LaunchH))

        Color = (255, 255, 255)

        pygame.draw.rect(Window, Color, (LaunchX - LaunchS - LaunchW / 2,
                         LaunchY - LaunchH / 2, LaunchW, LaunchH), int(1 * SF))
        pygame.draw.rect(Window, Color, (LaunchX + LaunchS - LaunchW / 2,
                         LaunchY - LaunchH / 2, LaunchW, LaunchH), int(1 * SF))

        Launched = Launch1 and Launch2

        # Reset Buttons
        Reset = [
            (ResetX, ResetY - (-35) * SF),
            (ResetX, ResetY - (-5) * SF),
            (ResetX, ResetY - (25) * SF),
            (ResetX, ResetY - (55) * SF)
        ]

        for i in range(4):
            if [Reset1, Reset2, Reset3, Reset4][i]:
                Color = (0, 200, 0, 0.8)
            else:
                Color = (120, 0, 0, 0.2)

            pygame.draw.rect(Window, Color, (*Reset[i], ResetW, ResetH))

            Color = (255, 255, 255)

            pygame.draw.rect(
                Window, Color, (*Reset[i], ResetW, ResetH), int(1 * SF))

        Countdown = [
            (CountdownX, CountdownY),
            (CountdownX + 55 * SF, CountdownY),
            (CountdownX + 110 * SF, CountdownY)
        ]

        for i in range(3):
            if [Countdown1, Countdown2, Countdown3][i]:
                Color = (0, 200, 0, 0.8)
            else:
                Color = (120, 0, 0, 0.2)

            pygame.draw.rect(
                Window, Color, (*Countdown[i], CountdownW, CountdownH))

            Color = (255, 255, 255)

            pygame.draw.rect(
                Window, Color, (*Countdown[i], CountdownW, CountdownH), int(1 * SF))

        Text = Font.render("T-10", True, (255, 255, 255))
        TextRect = Text.get_rect(center=(735 * SF, 1020 * SF))
        Window.blit(Text, TextRect)

        Text = Font.render("T-30", True, (255, 255, 255))
        TextRect = Text.get_rect(center=(790 * SF, 1020 * SF))
        Window.blit(Text, TextRect)

        Text = Font.render("T-60", True, (255, 255, 255))
        TextRect = Text.get_rect(center=(845 * SF, 1020 * SF))
        Window.blit(Text, TextRect)


def DisplayVent():
    global VentX, VentY, VentW, VentH, OutputMessage

    # Vent Placement
    VentX = int(150 * SF)
    VentY = int(940 * SF)
    VentW = int(100 * SF)
    VentH = int(30 * SF)

    if not Fullscreen:
        # Header Text
        Font = pygame.font.SysFont("Bahnschrift", int(24 * SF))
        Text = Font.render("VENT COMMANDS", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.topleft = (155 * SF, 890 * SF)
        Window.blit(Text, TextRect)

        # Divider
        pygame.draw.line(Window, (255, 255, 255), (int(
            150 * SF), int(920 * SF)), (int(355 * SF), int(920 * SF)), int(3 * SF))

        # Guard On
        if GuardVent:
            pygame.draw.rect(Window, (50, 50, 50, 0.8),
                             (VentX, VentY - 5 * SF, 205 * SF, VentH + 10 * SF))
            pygame.draw.rect(Window, (255, 255, 255), (VentX, VentY -
                             5 * SF, 205 * SF, VentH + 10 * SF), int(1 * SF))

            Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
            Text = Font.render("REMOVE GUARD", True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.center = (VentX + 105 * SF, VentY + 15 * SF)
            Window.blit(Text, TextRect)

        # Guard Off
        else:
            pygame.draw.rect(Window, (50, 50, 50, 0.8),
                             (VentX, VentY + 40 * SF, 205 * SF, 40 + SF))
            pygame.draw.rect(Window, (255, 255, 255), (VentX,
                             VentY + 40 * SF, 205 * SF, 40 * SF), int(1 * SF))

            Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
            Text = Font.render("REPLACE GUARD", True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.center = (VentX + 105 * SF, VentY + 60 * SF)
            Window.blit(Text, TextRect)

            # Vent Open
            if Vented:
                pygame.draw.rect(Window, (0, 120, 0, 0.8),
                                 (VentX, VentY, VentW, VentH))
                pygame.draw.rect(Window, (255, 255, 255),
                                 (VentX, VentY, VentW, VentH), int(1 * SF))

            # Vent Not Open
            else:
                pygame.draw.rect(Window, (120, 0, 0, 0.8),
                                 (VentX, VentY, VentW, VentH))
                pygame.draw.rect(Window, (255, 255, 255),
                                 (VentX, VentY, VentW, VentH), int(1 * SF))

            # Cut Issued
            if Cut:
                pygame.draw.rect(Window, (0, 120, 0, 0.8),
                                 (VentX + 105 * SF, VentY, VentW, VentH))
                pygame.draw.rect(
                    Window, (255, 255, 255), (VentX + 105 * SF, VentY, VentW, VentH), int(1 * SF))

            # Cut Not Issued
            else:
                pygame.draw.rect(Window, (120, 0, 0, 0.8),
                                 (VentX + 105 * SF, VentY, VentW, VentH))
                pygame.draw.rect(
                    Window, (255, 255, 255), (VentX + 105 * SF, VentY, VentW, VentH), int(1 * SF))

            # Vent Button
            Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
            Text = Font.render("VENT", True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.topleft = (VentX + 27.5 * SF, VentY + 5 * SF)
            Window.blit(Text, TextRect)

            # Cut Button
            Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
            Text = Font.render("CUT", True, (255, 255, 255))
            TextRect = Text.get_rect()
            TextRect.topleft = (VentX + 137.5 * SF, VentY + 5 * SF)
            Window.blit(Text, TextRect)

    # Vent Alarm
    if Vented:
        if OutputMessage == "-- VENTING --":
            OutputMessage = ""
        else:
            OutputMessage = "-- VENTING --"
            pygame.mixer.music.load(Buzz)
            pygame.mixer.music.play()

    # Automatic Float Logic
    EmailSender = "nebpiridiumcommand@gmail.com"
    EmailPassword = "lfscbpdqtwcepffm"
    EmailReceiver = "data@sbd.iridium.com"
    EmailSubject = str(IMEI)
    EmailBody = ""

    em = EmailMessage()
    em['From'] = EmailSender
    em['To'] = EmailReceiver
    em['Subject'] = EmailSubject
    em.set_content(EmailBody)

    if not ManualVenting:
        # Payload Reaches Vent Altitude
        if not Vented and AltVentOpen is not None and PayloadAltF >= AltVentOpen - 100:
            try:
                if os.path.exists("Resources/Commands/011.sbd"):
                    with open("Resources/Commands/011.sbd", "rb") as file:
                        FileData = file.read()

                em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                  filename=os.path.basename("Resources/Commands/011.sbd"))
                Context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                    smtp.login(EmailSender, EmailPassword)
                    smtp.sendmail(EmailSender, EmailReceiver, em.as_string())

                OutputMessage = "Vent Opened"
            except Exception:
                OutputMessage = "Failed to Send Command"

        # Payload Reaches Float Altitude or Float Ascent Rate
        if (Vented and AltVentClose is not None and PayloadAltF >= AltVentClose - 100) or (Vented and VelVentClose is not None and AscentRate <= VelVentClose + 0.5):
            try:
                if os.path.exists("Resources/Commands/100.sbd"):
                    with open("Resources/Commands/100.sbd", "rb") as file:
                        FileData = file.read()

                em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                  filename=os.path.basename("Resources/Commands/100.sbd"))
                Context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                    smtp.login(EmailSender, EmailPassword)
                    smtp.sendmail(EmailSender, EmailReceiver, em.as_string())

                if os.path.exists("Resources/Commands/000.sbd"):
                    with open("Resources/Commands/000.sbd", "rb") as file:
                        FileData = file.read()

                em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                  filename=os.path.basename("Resources/Commands/000.sbd"))
                Context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                    smtp.login(EmailSender, EmailPassword)
                    smtp.sendmail(EmailSender, EmailReceiver, em.as_string())

                OutputMessage = "Vent Closed"
            except Exception:
                OutputMessage = "Failed to Send Command"


def DisplayButtons():
    global PowerX, PowerY, PowerR
    global HelpX, HelpY, HelpR
    global SettingsX, SettingsY, SettingsR
    global FullscreenX, FullscreenY, FullscreenR
    global MenuX, MenuY, MenuW, MenuH
    global ReturnToSender

    # Internet Indicator
    try:
        socket.create_connection(("www.google.com", 80))
        Window.blit(Indicators["WifiOn"], (int(30 * SF), int(30 * SF)))
    except Exception:
        Window.blit(Indicators["WifiOff"], (int(30 * SF), int(30 * SF)))

    # Tracker Indicator
    if Tracking:
        Window.blit(Indicators["TrackingOn"], (int(120 * SF), int(30 * SF)))
    else:
        Window.blit(Indicators["TrackingOff"], (int(120 * SF), int(30 * SF)))

    # Recording Indicator
    if Launched:
        Window.blit(Indicators["CaptureOn"], (int(210 * SF), int(30 * SF)))
    else:
        Window.blit(Indicators["CaptureOff"], (int(210 * SF), int(30 * SF)))

    # Button Placement
    Coordinates = {
        "Power": {
            "x": int(1860 * SF),
            "y": int(60 * SF),
            "r": int(20 * SF)
        },
        "Help": {
            "x": int(1740 * SF),
            "y": int(60 * SF),
            "r": int(20 * SF)
        },
        "Settings": {
            "x": int(1800 * SF),
            "y": int(60 * SF),
            "r": int(20 * SF)
        },
        "Fullscreen": {
            "x": int(1300 * SF),
            "y": int(330 * SF),
            "r": int(30 * SF)
        },
        "Menu": {
            "x": int((WindowW - MenuW) // 2),
            "y": int((WindowH - MenuH) // 2),
            "w": int(WindowW // 1.5),
            "h": int(WindowH // 1.5)
        }
    }

    # Power Button Placement
    PowerX = Coordinates["Power"]["x"]
    PowerY = Coordinates["Power"]["y"]
    PowerR = Coordinates["Power"]["r"]
    Window.blit(Buttons["ButtonPower"],
                (int(PowerX - 20 * SF), int(PowerY - 20 * SF)))

    # Help Button Placement
    HelpX = Coordinates["Help"]["x"]
    HelpY = Coordinates["Help"]["y"]
    HelpR = Coordinates["Help"]["r"]
    Window.blit(Buttons["ButtonHelp"],
                (int(HelpX - 20 * SF), int(HelpY - 20 * SF)))

    # Settings Button Placement
    SettingsX = Coordinates["Settings"]["x"]
    SettingsY = Coordinates["Settings"]["y"]
    SettingsR = Coordinates["Settings"]["r"]
    Window.blit(Buttons["ButtonSettings"],
                (int(SettingsX - 20 * SF), int(SettingsY - 20 * SF)))

    # Fullscreen Button Placement
    if Fullscreen:
        FullscreenX = int(1840 * SF)
        FullscreenY = int(130 * SF)
        FullscreenR = int(20 * SF)

        Window.blit(Indicators["ButtonFullscreenB"], (int(
            FullscreenX - 20 * SF), int(FullscreenY - 20 * SF)))
    else:
        FullscreenX = Coordinates["Fullscreen"]["x"]
        FullscreenY = Coordinates["Fullscreen"]["y"]
        FullscreenR = Coordinates["Fullscreen"]["r"]

        Window.blit(Indicators["ButtonFullscreenA"], (int(
            FullscreenX - 20 * SF), int(FullscreenY - 20 * SF)))

    # Settings Menu Placement
    MenuX = Coordinates["Menu"]["x"]
    MenuY = Coordinates["Menu"]["y"]
    MenuW = Coordinates["Menu"]["w"]
    MenuH = Coordinates["Menu"]["h"]

    if Settings:
        # Display Settings Menu
        pygame.draw.rect(Window, (0, 0, 0), (MenuX, MenuY, MenuW, MenuH))
        pygame.draw.rect(Window, (255, 255, 255),
                         (MenuX, MenuY, MenuW, MenuH), 2)

        # Settings Menu Title
        Font = pygame.font.SysFont("Impact", int(80 * SF))
        Text = Font.render("SETTINGS", True, (255, 255, 255))
        TextRect = Text.get_rect(center=(MenuX + MenuW // 2, MenuY))

        HeaderW = TextRect.width + int(15 * SF)
        HeaderH = TextRect.height + int(5 * SF)
        HeaderX = MenuX + (MenuW - HeaderW) // 2
        HeaderY = TextRect.centery - HeaderH // 2

        # Header Background
        pygame.draw.rect(Window, (0, 0, 0),
                         (HeaderX, HeaderY, HeaderW, HeaderH))
        pygame.draw.rect(Window, (255, 255, 255),
                         (HeaderX, HeaderY, HeaderW, HeaderH), int(2 * SF))

        Window.blit(Text, (TextRect.left, TextRect.top))

        # Header Text
        Font = pygame.font.SysFont("Bahnschrift", int(30 * SF))
        Text = Font.render("UI SCALE", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(360 * SF), int(265 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        # UI Width Input
        pygame.draw.rect(Window, (0, 0, 0), (int(360 * SF),
                         int(300 * SF), int(120 * SF), int(30 * SF)))
        pygame.draw.rect(Window, (255, 255, 255), (int(
            360 * SF), int(300 * SF), int(120 * SF), int(30 * SF)), int(1 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("UI WIDTH", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(420 * SF), int(315 * SF))

        Window.blit(Text, TextRect)

        # UI Height Input
        pygame.draw.rect(Window, (0, 0, 0), (int(490 * SF),
                         int(300 * SF), int(120 * SF), int(30 * SF)))
        pygame.draw.rect(Window, (255, 255, 255), (int(
            490 * SF), int(300 * SF), int(120 * SF), int(30 * SF)), int(1 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("UI HEIGHT", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(550 * SF), int(315 * SF))

        Window.blit(Text, TextRect)

        # Peripheral Toggle Buttons
        Font = pygame.font.SysFont("Bahnschrift", int(30 * SF))
        Text = Font.render("PERIPHERALS", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(360 * SF), int(380 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        Font = pygame.font.SysFont("Bahnschrift", int(25 * SF))

        Text = Font.render("Altimeter", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(390 * SF), int(420 * SF)))
        Window.blit(Text, (TextRect.left, TextRect.top))

        Text = Font.render("Navigator", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(390 * SF), int(460 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        Text = Font.render("Compass", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(390 * SF), int(500 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        Text = Font.render("Clock", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(390 * SF), int(540 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        if DispAltitude:
            Color = (0, 200, 0, 0.8)
        else:
            Color = (120, 0, 0, 0.2)

        pygame.draw.rect(Window, Color, (int(360 * SF),
                         int(420 * SF), int(20 * SF), int(20 * SF)))

        if DispLocation:
            Color = (0, 200, 0, 0.8)
        else:
            Color = (120, 0, 0, 0.2)

        pygame.draw.rect(Window, Color, (int(360 * SF),
                         int(460 * SF), int(20 * SF), int(20 * SF)))

        if DispCompass:
            Color = (0, 200, 0, 0.8)
        else:
            Color = (120, 0, 0, 0.2)

        pygame.draw.rect(Window, Color, (int(360 * SF),
                         int(500 * SF), int(20 * SF), int(20 * SF)))

        if DispTime:
            Color = (0, 200, 0, 0.8)
        else:
            Color = (120, 0, 0, 0.2)

        pygame.draw.rect(Window, Color, (int(360 * SF),
                         int(540 * SF), int(20 * SF), int(20 * SF)))

        pygame.draw.rect(Window, (255, 255, 255), (int(
            360 * SF), int(420 * SF), int(20 * SF), int(20 * SF)), 1)
        pygame.draw.rect(Window, (255, 255, 255), (int(
            360 * SF), int(460 * SF), int(20 * SF), int(20 * SF)), 1)
        pygame.draw.rect(Window, (255, 255, 255), (int(
            360 * SF), int(500 * SF), int(20 * SF), int(20 * SF)), 1)
        pygame.draw.rect(Window, (255, 255, 255), (int(
            360 * SF), int(540 * SF), int(20 * SF), int(20 * SF)), 1)

        # Automatic Tracking Button
        Font = pygame.font.SysFont("Bahnschrift", int(30 * SF))
        Text = Font.render("AUTOMATIC RADIO TRACKING", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(360 * SF), int(620 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        Font = pygame.font.SysFont("Bahnschrift", int(25 * SF))
        Text = Font.render("Disable for Manual Entry", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(410 * SF), int(663 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        if not ManualTracking:
            Color = (0, 200, 0)
        else:
            Color = (120, 0, 0)

        pygame.gfxdraw.filled_circle(Window, int(
            375 * SF), int(675 * SF), int(15 * SF), Color)
        pygame.gfxdraw.aacircle(Window, int(375 * SF),
                                int(675 * SF), int(15 * SF), (255, 255, 255))

        # Automatic Venting
        Font = pygame.font.SysFont("Bahnschrift", int(30 * SF))
        Text = Font.render("AUTOMATIC VENT COMMANDING", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(845 * SF), int(620 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        Font = pygame.font.SysFont("Bahnschrift", int(25 * SF))
        Text = Font.render("Enable for Automatic Float", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(895 * SF), int(663 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        if not ManualVenting:
            Color = (0, 200, 0)
        else:
            Color = (120, 0, 0)

        pygame.gfxdraw.filled_circle(Window, int(
            860 * SF), int(675 * SF), int(15 * SF), Color)
        pygame.gfxdraw.aacircle(Window, int(860 * SF),
                                int(675 * SF), int(15 * SF), (255, 255, 255))

        # Coordinate Input
        if not ManualTracking:
            Color = (150, 150, 150, 0.2)
        else:
            Color = (255, 255, 255)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("PAYLOAD LAT", True, Color)
        TextRect = Text.get_rect()
        TextRect.center = (int(420 * SF), int(725 * SF))

        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("PAYLOAD LON", True, Color)
        TextRect = Text.get_rect()
        TextRect.center = (int(550 * SF), int(725 * SF))

        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("PAYLOAD ALT", True, Color)
        TextRect = Text.get_rect()
        TextRect.center = (int(680 * SF), int(725 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, Color, (int(360 * SF),
                         int(710 * SF), int(120 * SF), int(30 * SF)), 1)
        pygame.draw.rect(Window, Color, (int(490 * SF),
                         int(710 * SF), int(120 * SF), int(30 * SF)), 1)
        pygame.draw.rect(Window, Color, (int(620 * SF),
                         int(710 * SF), int(120 * SF), int(30 * SF)), 1)

        pygame.draw.line(Window, (255, 255, 255), (int(
            360 * SF), int(750 * SF)), (int(740 * SF), int(750 * SF)), int(4 * SF))

        Color = (255, 255, 255)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("TRACKER LAT", True, Color)
        TextRect = Text.get_rect()
        TextRect.center = (int(420 * SF), int(780 * SF))

        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("TRACKER LON", True, Color)
        TextRect = Text.get_rect()
        TextRect.center = (int(550 * SF), int(780 * SF))

        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("TRACKER ALT", True, Color)
        TextRect = Text.get_rect()
        TextRect.center = (int(680 * SF), int(780 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, Color, (int(360 * SF),
                         int(765 * SF), int(120 * SF), int(30 * SF)), 1)
        pygame.draw.rect(Window, Color, (int(490 * SF),
                         int(765 * SF), int(120 * SF), int(30 * SF)), 1)
        pygame.draw.rect(Window, Color, (int(620 * SF),
                         int(765 * SF), int(120 * SF), int(30 * SF)), 1)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("Payload: ({:.2f}°, {:.2f}°) {:.0f} ft  |  Tracker: ({:.2f}°, {:.2f}°) {:.0f} ft".format(
            PayloadLatD, PayloadLonD, PayloadAltF, TrackerLatD, TrackerLonD, TrackerAltF), True, Color)
        TextRect = Text.get_rect()
        TextRect.center = (int(550 * SF), int(820 * SF))

        Window.blit(Text, TextRect)

        # Float Input
        Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
        Text = Font.render("BEGIN VENTING AT", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(930 * SF), int(725 * SF))

        Window.blit(Text, TextRect)

        if ManualVenting:
            Color = (150, 150, 150, 0.2)
        else:
            Color = (255, 255, 255)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("ALTITUDE (FT)", True, Color)
        TextRect = Text.get_rect()
        TextRect.topleft = (int(1040 * SF), int(717.5 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, Color, (int(1030 * SF),
                         int(710 * SF), int(240 * SF), int(30 * SF)), 1)

        pygame.draw.line(Window, (255, 255, 255), (int(
            840 * SF), int(750 * SF)), (int(1275 * SF), int(750 * SF)), int(4 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
        Text = Font.render("CLOSE AT            OR", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.topleft = (int(845 * SF), int(770 * SF))

        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("ft/s", True, Color)
        TextRect = Text.get_rect()
        TextRect.topleft = (int(947.5 * SF), int(772.5 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, Color, (int(940 * SF),
                         int(765 * SF), int(40 * SF), int(30 * SF)), 1)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("ALTITUDE (FT)", True, Color)
        TextRect = Text.get_rect()
        TextRect.topleft = (int(1040 * SF), int(772.5 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, Color, (int(1030 * SF),
                         int(765 * SF), int(240 * SF), int(30 * SF)), 1)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))

        if AltVentOpen is None and AltVentClose is None and VelVentClose is None:
            Text = Font.render(
                "Vent Alt: None  |  Float Alt: None  |  Float Vel: None", True, Color)
        if AltVentOpen is not None and AltVentClose is None and VelVentClose is None:
            Text = Font.render("Vent Alt: {:.0f} ft  |  Float Alt: None  |  Float Vel: None".format(
                AltVentOpen), True, Color)
        if AltVentOpen is None and AltVentClose is not None and VelVentClose is None:
            Text = Font.render("Vent Alt: None  |  Float Alt: {:.0f} ft  |  Float Vel: None".format(
                AltVentClose), True, Color)
        if AltVentOpen is None and AltVentClose is None and VelVentClose is not None:
            Text = Font.render(
                "Vent Alt: None  |  Float Alt: None  |  Float Vel: {:.1f} ft/s".format(VelVentClose), True, Color)
        if AltVentOpen is not None and AltVentClose is not None and VelVentClose is None:
            Text = Font.render("Vent Alt: {:.0f} ft  |  Float Alt: {:.0f} ft  |  Float Vel: None".format(
                AltVentOpen, AltVentClose), True, Color)
        if AltVentOpen is None and AltVentClose is not None and VelVentClose is not None:
            Text = Font.render("Vent Alt: None  |  Float Alt: {:.0f} ft  |  Float Vel: {:.1f} ft/s".format(
                AltVentClose, VelVentClose), True, Color)
        if AltVentOpen is not None and AltVentClose is None and VelVentClose is not None:
            Text = Font.render("Vent Alt: {:.0f} ft  |  Float Alt: None  |  Float Vel: {:.1f} ft/s".format(
                AltVentOpen, VelVentClose), True, Color)
        if AltVentOpen is not None and AltVentClose is not None and VelVentClose is not None:
            Text = Font.render("Vent Alt: {:.0f} ft  |  Float Alt: {:.0f} ft  |  Float Vel: {:.1f} ft/s".format(
                AltVentOpen, AltVentClose, VelVentClose), True, Color)

        TextRect = Text.get_rect()
        TextRect.center = (int(1060 * SF), int(820 * SF))

        Window.blit(Text, TextRect)

        # Connection Input
        Font = pygame.font.SysFont("Bahnschrift", int(30 * SF))
        Text = Font.render("CONNECTIONS", True, (255, 255, 255))
        TextRect = Text.get_rect(topright=(int(1560 * SF), int(265 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        pygame.draw.rect(Window, (255, 255, 255), (int(
            1365 * SF), int(300 * SF), int(200 * SF), int(30 * SF)), int(1 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("IRIDIUM IMEI", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(1465 * SF), int(315 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, (255, 255, 255), (int(
            1365 * SF), int(345 * SF), int(200 * SF), int(30 * SF)), int(1 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("APRS CALLSIGN", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(1465 * SF), int(360 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, (255, 255, 255), (int(
            1365 * SF), int(390 * SF), int(200 * SF), int(30 * SF)), int(1 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("STREAM IP", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(1465 * SF), int(405 * SF))

        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
        Text = Font.render("RFD Data", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(1470 * SF), int(450 * SF))

        Window.blit(Text, TextRect)

        # Guided Descent System
        Font = pygame.font.SysFont("Bahnschrift", int(30 * SF))
        Text = Font.render("GUIDED DESCENT", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(845 * SF), int(265 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        pygame.draw.rect(Window, (255, 255, 255), (int(
            845 * SF), int(300 * SF), int(115 * SF), int(30 * SF)), int(1 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("TARGET LAT", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(902.5 * SF), int(315 * SF))

        Window.blit(Text, TextRect)

        pygame.draw.rect(Window, (255, 255, 255), (int(
            970 * SF), int(300 * SF), int(115 * SF), int(30 * SF)), int(1 * SF))

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("TARGET LON", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(1027.5 * SF), int(315 * SF))

        Window.blit(Text, TextRect)

        Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))
        Text = Font.render("SAME AS TRACKER", True, (255, 255, 255))
        TextRect = Text.get_rect(topleft=(int(870 * SF), int(340 * SF)))

        Window.blit(Text, (TextRect.left, TextRect.top))

        if ReturnToSender:
            Color = (0, 200, 0, 0.8)
        else:
            Color = (120, 0, 0, 0.2)

        pygame.draw.rect(Window, Color, (int(845 * SF),
                         int(340 * SF), int(15 * SF), int(15 * SF)))
        pygame.draw.rect(Window, (255, 255, 255), (int(
            845 * SF), int(340 * SF), int(15 * SF), int(15 * SF)), int(1 * SF))

        # RFD Data Display
        Font = pygame.font.SysFont("Bahnschrift", int(12 * SF))

        TextX = int(1400 * SF)
        TextY = int(470 * SF)

        Labels = ['Packet', 'Siv', 'Fix', 'Lat', 'Lon', 'Alt', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Sec', 'NED - N',
                  'NED - E', 'NED - D', 'Battery', 'Battery (33)', 'Battery (51)', 'Battery (52)', 'A (Internal)',
                  'A (External)', 'Temperature', 'D (Internal)', 'D (External)', 'Pressure', 'Acceleration (x)',
                  'Acceleration (y)', 'Acceleration (z)', 'Pitch', 'Roll', 'Yaw']

        LabelW = max(Font.render(Label, True, (255, 255, 255)).get_width()
                     for Label in Labels)

        for i, Item in enumerate(zip(DataList[:-1], Labels)):
            Value, Label = Item

            LabelText = f"{Label}: "
            LabelSurface = Font.render(LabelText, True, (255, 255, 255))
            LabelRect = LabelSurface.get_rect(top=TextY, right=TextX + LabelW)
            Window.blit(LabelSurface, LabelRect)

            ValueText = str(Value)
            ValueSurface = Font.render(ValueText, True, (255, 255, 255))
            ValueRect = ValueSurface.get_rect(top=TextY, left=TextX + LabelW)
            Window.blit(ValueSurface, ValueRect)

            TextY += max(LabelRect.height, ValueRect.height)

        Font = pygame.font.SysFont("Bahnschrift", int(14 * SF))
        Text = Font.render(
            "HERMES RELEASE VERSION 1.9 | PRODUCED AND TESTED BY NASA'S MINNESOTA SPACE GRANT CONSORTIUM (MnSGC) AT THE UNIVERSITY OF MINNESOTA TWIN CITIES", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (int(960 * SF), int(880 * SF))

        Window.blit(Text, TextRect)


def Input():
    global SF, SerialRFD, SerialArduino
    global OutputMessage
    global SigmaTweak, GammaTweak
    global RFD, Iridium, APRS, Ubiquiti, Arduino
    global RFDConditional, IridiumConditional, APRSConditional, UbiquitiConditional, ArduinoConditional
    global COMRFD, COMArduino, InputRFD, InputIridium, InputAPRS, InputUbiquiti, InputArduino
    global CompassSetting, InputText
    global TrackerLatD, TrackerLonD, TrackerAltF, PayloadLatD, PayloadLonD, PayloadAltF
    global InputTrackerLat, InputTrackerLon, InputTrackerAlt, InputPayloadLat, InputPayloadLon, InputPayloadAlt, InputAltVentOpen, InputAltVentClose, InputVelVentClose
    global Recording, Capture, Running, Launch1, Launch2, Reset1, Reset2, Reset3, Reset4, Countdown1, Countdown2, Countdown3, GuardVent, Vented, Cut
    global AltVentOpen, AltVentClose, VelVentClose
    global IMEI, Callsign, IP
    global Fullscreen, Settings, ReturnToSender
    global JoystickX, JoystickY, WindowW, WindowH, InputWindowW, InputWindowH
    global DispAltitude, DispCompass, DispLocation, DispTime
    global Tracking, ManualTracking, ManualVenting

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Shutdown()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            MouseX, MouseY = pygame.mouse.get_pos()
            MousePos = pygame.mouse.get_pos()

            pygame.mixer.music.load(Tap)
            pygame.mixer.music.play()

            # Power Button
            if (MouseX - PowerX) ** 2 + (MouseY - PowerY) ** 2 <= PowerR ** 2:
                Shutdown()

            # Help Button
            if (MouseX - HelpX) ** 2 + (MouseY - HelpY) ** 2 <= HelpR ** 2:
                URL = 'https://docs.google.com/document/d/1PRoLkXaMrUWXbg3vbNBbG_Q1igPCRx8imRnfndy7S-0/edit?usp=sharing'
                webbrowser.open(URL)

            # Fullscreen Button
            if (MouseX - FullscreenX) ** 2 + (MouseY - FullscreenY) ** 2 <= FullscreenR ** 2:
                if Fullscreen:
                    Fullscreen = False
                else:
                    Fullscreen = True

            # Compass Button
            if (MouseX - CompassX) ** 2 + (MouseY - CompassY) ** 2 <= int(4000 * SF):
                if CompassSetting < 2:
                    CompassSetting += 1
                else:
                    CompassSetting = 1

            # Launch 1 Button
            Button = pygame.Rect(LaunchX - LaunchS - LaunchW/2,
                                 LaunchY - LaunchH/2, LaunchW, LaunchH)
            if Button.collidepoint(MousePos):
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Launch1 = True

            # Launch 2 Button
            Button = pygame.Rect(LaunchX + LaunchS - LaunchW/2,
                                 LaunchY - LaunchH/2, LaunchW, LaunchH)
            if Button.collidepoint(MousePos):
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Launch2 = True

            # Reset 1 Button
            Button = pygame.Rect(ResetX, ResetY + 35 * SF, ResetW, ResetH)
            if Button.collidepoint(MousePos):
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Reset1 = True

            # Reset 2 Button
            Button = pygame.Rect(ResetX, ResetY + 5 * SF, ResetW, ResetH)
            if Button.collidepoint(MousePos):
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Reset2 = True

            # Reset 3 Button
            Button = pygame.Rect(ResetX, ResetY - 25 * SF, ResetW, ResetH)
            if Button.collidepoint(MousePos):
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Reset3 = True

            # Reset 4 Button
            Button = pygame.Rect(ResetX, ResetY - 55 * SF, ResetW, ResetH)
            if Button.collidepoint(MousePos):
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Reset4 = True

            if Reset1 and Reset2 and Reset3 and Reset4:
                Reset = [
                    (ResetX, ResetY - (-35) * SF),
                    (ResetX, ResetY - (-5) * SF),
                    (ResetX, ResetY - (25) * SF),
                    (ResetX, ResetY - (55) * SF)
                ]

                for i in range(4):
                    Color = (0, 200, 0, 0.8)
                    pygame.draw.rect(
                        Window, Color, (*Reset[i], ResetW, ResetH))
                    Color = (255, 255, 255)
                    pygame.draw.rect(
                        Window, Color, (*Reset[i], ResetW, ResetH), int(1 * SF))

                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                time.sleep(0.5)
                pygame.mixer.music.load(Beep)
                pygame.mixer.music.play()

                OutputMessage = "Launch Timer Halted"
                Launch1 = False
                Launch2 = False
                Reset1 = False
                Reset2 = False
                Reset3 = False
                Reset4 = False

            # Countdown 1 Button
            Button = pygame.Rect(CountdownX, CountdownY,
                                 CountdownW, CountdownH)
            if Button.collidepoint(MousePos) and Launched == False:
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Countdown2 = False
                Countdown3 = False
                Countdown1 = not Countdown1

            # Countdown 2 Button
            Button = pygame.Rect(CountdownX + 55 * SF,
                                 CountdownY, CountdownW, CountdownH)
            if Button.collidepoint(MousePos) and Launched == False:
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Countdown1 = False
                Countdown3 = False
                Countdown2 = not Countdown2

            # Countdown 3 Button
            Button = pygame.Rect(CountdownX + 110 * SF,
                                 CountdownY, CountdownW, CountdownH)
            if Button.collidepoint(MousePos) and Launched == False:
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()
                Countdown1 = False
                Countdown2 = False
                Countdown3 = not Countdown3

            # Radio Buttons
            Buttons = [
                pygame.Rect(int((i + 0.5) * RadioS + RadioX -
                            100 * SF), RadioY, RadioW, RadioH)
                for i in range(5)
            ]

            Actions = [
                (RFDConditional, RFD, SetupRFD, 'RFD Disconnected'),
                (IridiumConditional, Iridium, SetupIridium, 'Iridium Disconnected'),
                (APRSConditional, APRS, SetupAPRS, 'APRS Disconnected'),
                (UbiquitiConditional, Ubiquiti,
                 SetupUbiquiti, 'Ubiquiti Disconnected'),
                (ArduinoConditional, Arduino, SetupArduino, 'Arduino Disconnected')
            ]

            for i, Button in enumerate(Buttons):
                if Button.collidepoint(MousePos) and not Settings:
                    pygame.mixer.music.load(Switch)
                    pygame.mixer.music.play()

                    Conditional, Connection, SetupFunction, Message = Actions[i]

                    if not Conditional and not Connection:
                        ButtonX = int((i + 0.5) * RadioS + RadioX - 100 * SF)
                        pygame.draw.rect(Window, (80, 0, 0, 0.8),
                                         (ButtonX, RadioY, RadioW, RadioH))
                        pygame.draw.rect(
                            Window, (50, 50, 50, 0.8), (ButtonX, RadioY, RadioW, RadioH), int(3 * SF))

                        SetupFunction()
                    else:
                        if i == 0:
                            RFD = False

                            if SerialRFD:
                                SerialRFD.close()
                                SerialRFD = None
                        if i == 1:
                            Iridium = False
                        if i == 2:
                            APRS = False
                        if i == 3:
                            Ubiquiti = False
                        if i == 4:
                            Arduino = False
                            Tracking = False

                            if SerialArduino:
                                SerialArduino.close()
                                SerialArduino = None

                        DisplayRadios()
                        OutputMessage = Message

            # Tracking Arrows
            Button = [
                pygame.Rect(ControlX - 0.75 * ControlR, ControlY - 2 *
                            TriangleHeight, 1.5 * ControlR, 2 * TriangleHeight),
                pygame.Rect(ControlX - 0.75 * ControlR, ControlY +
                            TriangleHeight, 1.5 * ControlR, 2 * TriangleHeight),
                pygame.Rect(ControlX + TriangleHeight, ControlY -
                            0.75 * ControlR, 2 * TriangleHeight, 1.5 * ControlR),
                pygame.Rect(ControlX - 2 * TriangleHeight, ControlY -
                            0.75 * ControlR, 2 * TriangleHeight, 1.5 * ControlR)
            ]

            for i, Polygon in enumerate(TriangleShapes):
                Polygon = [(int(X), int(Y)) for X, Y in Polygon]

                if Button[i].collidepoint(pygame.mouse.get_pos()) and not (MouseX - ControlX) ** 2 + (MouseY - ControlY) ** 2 <= ControlR ** 2 and not Fullscreen:
                    if i == 0:
                        Window.blit(
                            DPadUp, (int(ControlX - 85 * SF), int(ControlY - 85 * SF)))
                        if Arduino:
                            GammaTweak += 1
                    if i == 1:
                        Window.blit(
                            DPadDown, (int(ControlX - 85 * SF), int(ControlY - 85 * SF)))
                        if Arduino:
                            GammaTweak -= 1
                    if i == 2:
                        Window.blit(
                            DPadRight, (int(ControlX - 85 * SF), int(ControlY - 85 * SF)))
                        if Arduino:
                            SigmaTweak += 1
                    if i == 3:
                        Window.blit(
                            DPadLeft, (int(ControlX - 85 * SF), int(ControlY - 85 * SF)))
                        if Arduino:
                            SigmaTweak -= 1

                    pygame.draw.line(Window, (255, 255, 255), (ControlX - 20 * SF,
                                     ControlY - 20 * SF), (ControlX - 70 * SF, ControlY - 70 * SF))

            # Tracking Button
            if (MouseX - ControlX) ** 2 + (MouseY - ControlY) ** 2 <= ControlR ** 2:
                Window.blit(DPadCenter, (int(ControlX - 50 * SF),
                            int(ControlY - 50 * SF)))
                pygame.draw.line(Window, (255, 255, 255), (ControlX - 20 * SF,
                                 ControlY - 20 * SF), (ControlX - 70 * SF, ControlY - 70 * SF))

                if not Tracking and Arduino:
                    OutputMessage = 'Tracking Commencing'

                    Tracking = True
                elif Tracking and Arduino:
                    OutputMessage = 'Tracking Terminating'

                    Tracking = False

            # Vent Guard
            Button = pygame.Rect(VentX, VentY - 5 * SF, 205 * SF, 40 + SF)
            if Button.collidepoint(MousePos) and GuardVent:
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()

                GuardVent = False

                break

            Button = pygame.Rect(VentX, VentY + 40 * SF, 205 * SF, 40 + SF)
            if Button.collidepoint(MousePos) and not GuardVent:
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()

                GuardVent = True

                break

            # Vent Button
            Button = pygame.Rect(VentX, VentY, VentW, VentH)
            if Button.collidepoint(MousePos) and not GuardVent:
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()

                if not Iridium:
                    OutputMessage = "No Active Iridium"
                else:
                    EmailSender = "nebpiridiumcommand@gmail.com"
                    EmailPassword = "lfscbpdqtwcepffm"
                    EmailReceiver = "data@sbd.iridium.com"
                    EmailSubject = str(IMEI)
                    EmailBody = ""

                    em = EmailMessage()
                    em['From'] = EmailSender
                    em['To'] = EmailReceiver
                    em['Subject'] = EmailSubject
                    em.set_content(EmailBody)

                    if Vented:
                        try:
                            if os.path.exists("Resources/Commands/100.sbd"):
                                with open("Resources/Commands/100.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/100.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            if os.path.exists("Resources/Commands/000.sbd"):
                                with open("Resources/Commands/000.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/000.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            Vented = False

                            OutputMessage = "Vent Closed"

                            break

                        except Exception as e:
                            print(e)

                    if not Vented:
                        try:
                            if os.path.exists("Resources/Commands/011.sbd"):
                                with open("Resources/Commands/011.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/011.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            Vented = True

                            OutputMessage = "Vent Opened"

                            break

                        except Exception:
                            OutputMessage = "Failed to Send Command"

            # Cut Button
            Button = pygame.Rect(VentX + 105 * SF, VentY, VentW, VentH)
            if Button.collidepoint(MousePos) and not GuardVent:
                pygame.mixer.music.load(Switch)
                pygame.mixer.music.play()

                if not Iridium:
                    OutputMessage = "No Active Iridium"
                else:
                    EmailSender = "nebpiridiumcommand@gmail.com"
                    EmailPassword = "lfscbpdqtwcepffm"
                    EmailReceiver = "data@sbd.iridium.com"
                    EmailSubject = str(IMEI)
                    EmailBody = ""

                    em = EmailMessage()
                    em['From'] = EmailSender
                    em['To'] = EmailReceiver
                    em['Subject'] = EmailSubject
                    em.set_content(EmailBody)

                    try:
                        if not Cut:
                            if os.path.exists("Resources/Commands/001.sbd"):
                                with open("Resources/Commands/001.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/001.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            if os.path.exists("Resources/Commands/000.sbd"):
                                with open("Resources/Commands/000.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/000.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            Cut = True

                            OutputMessage = "Cutdown Initiated"

                            break

                        if Cut:
                            if os.path.exists("Resources/Commands/000.sbd"):
                                with open("Resources/Commands/000.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/000.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            OutputMessage = "Cutdown Reset"

                            time.sleep(1)

                            if os.path.exists("Resources/Commands/001.sbd"):
                                with open("Resources/Commands/001.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/001.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            if os.path.exists("Resources/Commands/000.sbd"):
                                with open("Resources/Commands/000.sbd", "rb") as file:
                                    FileData = file.read()

                            em.add_attachment(FileData, maintype="application", subtype="octet-stream",
                                              filename=os.path.basename("Resources/Commands/000.sbd"))
                            Context = ssl.create_default_context()

                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=Context) as smtp:
                                smtp.login(EmailSender, EmailPassword)
                                smtp.sendmail(
                                    EmailSender, EmailReceiver, em.as_string())

                            OutputMessage = "Cutdown Initiated"

                            break

                    except Exception:
                        OutputMessage = "Failed to Send Command"

            # Settings Button
            if (MouseX - SettingsX) ** 2 + (MouseY - SettingsY) ** 2 <= SettingsR ** 2:
                if Settings == False:
                    Settings = True
                else:
                    Settings = False

                    InputPayloadLat = False
                    InputPayloadLon = False
                    InputPayloadAlt = False

                    InputTrackerLat = False
                    InputTrackerLon = False
                    InputTrackerAlt = False

                    InputRFD = False
                    InputIridium = False
                    InputAPRS = False
                    InputUbiquiti = False
                    InputArduino = False

            # Settings Menu
            if Settings:
                global DispAltitude, DispCompass, DispLocation, DispTime

                Peripherals = [
                    (pygame.Rect(int(360 * SF), int(420 * SF),
                     int(20 * SF), int(20 * SF)), 'DispAltitude'),
                    (pygame.Rect(int(360 * SF), int(460 * SF),
                     int(20 * SF), int(20 * SF)), 'DispLocation'),
                    (pygame.Rect(int(360 * SF), int(500 * SF),
                     int(20 * SF), int(20 * SF)), 'DispCompass'),
                    (pygame.Rect(int(360 * SF), int(540 * SF),
                     int(20 * SF), int(20 * SF)), 'DispTime')
                ]

                for Button, Variable in Peripherals:
                    if Button.collidepoint(MousePos):
                        globals()[Variable] = not globals()[Variable]

                # Manual Tracking
                if ((MousePos[0] - int(375 * SF))**2 + (MousePos[1] - int(675 * SF))**2) <= (int(15 * SF)**2):
                    ManualTracking = not ManualTracking

                # Manual Venting
                if ((MousePos[0] - int(865 * SF))**2 + (MousePos[1] - int(675 * SF))**2) <= (int(15 * SF)**2):
                    ManualVenting = not ManualVenting

                # Guided Descent
                Button = pygame.Rect(
                    int(845 * SF), int(340 * SF), int(15 * SF), int(15 * SF))
                if Button.collidepoint(MousePos):
                    ReturnToSender = not ReturnToSender

                Fields = [
                    (pygame.Rect(int(360 * SF), int(300 * SF),
                     int(120 * SF), int(30 * SF)), 'InputWindowW'),
                    (pygame.Rect(int(490 * SF), int(300 * SF),
                     int(120 * SF), int(30 * SF)), 'InputWindowH'),
                    (pygame.Rect(int(360 * SF), int(710 * SF),
                     int(120 * SF), int(30 * SF)), 'InputPayloadLat'),
                    (pygame.Rect(int(490 * SF), int(710 * SF),
                     int(120 * SF), int(30 * SF)), 'InputPayloadLon'),
                    (pygame.Rect(int(620 * SF), int(710 * SF),
                     int(120 * SF), int(30 * SF)), 'InputPayloadAlt'),
                    (pygame.Rect(int(360 * SF), int(765 * SF),
                     int(120 * SF), int(30 * SF)), 'InputTrackerLat'),
                    (pygame.Rect(int(490 * SF), int(765 * SF),
                     int(120 * SF), int(30 * SF)), 'InputTrackerLon'),
                    (pygame.Rect(int(620 * SF), int(765 * SF),
                     int(120 * SF), int(30 * SF)), 'InputTrackerAlt'),
                    (pygame.Rect(int(1365 * SF), int(300 * SF),
                     int(200 * SF), int(30 * SF)), 'InputIridium'),
                    (pygame.Rect(int(1365 * SF), int(345 * SF),
                     int(200 * SF), int(30 * SF)), 'InputAPRS'),
                    (pygame.Rect(int(1365 * SF), int(390 * SF),
                     int(200 * SF), int(30 * SF)), 'InputUbiquiti'),
                    (pygame.Rect(int(1030 * SF), int(710 * SF),
                     int(240 * SF), int(30 * SF)), 'InputAltVentOpen'),
                    (pygame.Rect(int(1030 * SF), int(765 * SF),
                     int(240 * SF), int(30 * SF)), 'InputAltVentClose'),
                    (pygame.Rect(int(940 * SF), int(765 * SF),
                     int(40 * SF), int(30 * SF)), 'InputVelVentClose')
                ]

                for Field, Flag in Fields:
                    if Field.collidepoint(MousePos):
                        if 'InputPayload' in Flag and not ManualVenting:
                            globals()[Flag] = True
                        if 'Vent' in Flag and not ManualVenting:
                            globals()[Flag] = True
                        if not 'Payload' in Flag and not 'Vent' in Flag:
                            globals()[Flag] = True

        if event.type == pygame.KEYDOWN:
            if keyboard.is_pressed('w') and Arduino:
                GammaTweak += 1
            if keyboard.is_pressed('a') and Arduino:
                SigmaTweak -= 1
            if keyboard.is_pressed('s') and Arduino:
                GammaTweak -= 1
            if keyboard.is_pressed('d') and Arduino:
                SigmaTweak += 1

            if InputPayloadLat or InputPayloadLon or InputPayloadAlt or InputTrackerLat or InputTrackerLon or InputTrackerAlt or InputAltVentOpen or InputAltVentClose or InputVelVentClose or InputWindowW or InputWindowH or InputRFD or InputIridium or InputAPRS or InputUbiquiti or InputArduino:
                if event.key == pygame.K_ESCAPE:
                    InputWindowW = False
                    InputWindowH = False
                    InputPayloadLat = False
                    InputPayloadLon = False
                    InputPayloadAlt = False
                    InputTrackerLat = False
                    InputTrackerLon = False
                    InputTrackerAlt = False
                    InputAltVentOpen = False
                    InputAltVentClose = False
                    InputVelVentClose = False
                    InputRFD = False
                    InputIridium = False
                    InputAPRS = False
                    InputUbiquiti = False
                    InputArduino = False

                    InputText = ""
                elif event.key == pygame.K_RETURN:
                    try:
                        if InputWindowW:
                            if float(InputText) <= 1920 and float(InputText) >= 512:
                                WindowW = float(InputText)
                                WindowH = WindowW * (9/16)
                                SF = min(WindowW / 1920, WindowH / 1080)
                                InputWindowW = False
                        if InputWindowH:
                            if float(InputText) <= 1080 and float(InputText) >= 288:
                                WindowH = float(InputText)
                                WindowW = WindowH * (16/9)
                                SF = min(WindowW / 1920, WindowH / 1080)
                                InputWindowH = False
                        if InputPayloadLat:
                            PayloadLatD = float(InputText)
                            InputPayloadLat = False
                        if InputPayloadLon:
                            PayloadLonD = float(InputText)
                            InputPayloadLon = False
                        if InputPayloadAlt:
                            PayloadAltF = float(InputText)
                            InputPayloadAlt = False
                        if InputTrackerLat:
                            TrackerLatD = float(InputText)
                            InputTrackerLat = False
                        if InputTrackerLon:
                            TrackerLonD = float(InputText)
                            InputTrackerLon = False
                        if InputTrackerAlt:
                            TrackerAltF = float(InputText)
                            InputTrackerAlt = False
                        if InputAltVentOpen:
                            AltVentOpen = float(InputText)
                            InputAltVentOpen = False
                        if InputAltVentClose:
                            VelVentClose = None
                            AltVentClose = float(InputText)
                            InputAltVentClose = False
                        if InputVelVentClose:
                            AltVentClose = None
                            VelVentClose = float(InputText)
                            InputVelVentClose = False
                        if InputIridium:
                            IMEI = str(InputText)
                            InputIridium = False
                        if InputAPRS:
                            Callsign = str(InputText)
                            InputAPRS = False
                        if InputUbiquiti:
                            IP = str(InputText)
                            InputUbiquiti = False

                        InputText = ""
                    except ValueError:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    InputText = InputText[:-1]
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    Clipboard = clipboard.paste()
                    Inputs = [InputWindowW, InputWindowH, InputPayloadLat, InputPayloadLon, InputPayloadAlt, InputTrackerLat, InputTrackerLon,
                              InputTrackerAlt, InputAltVentOpen, InputAltVentClose, InputVelVentClose, InputIridium, InputAPRS, InputUbiquiti]

                    while '\0' in Clipboard:
                        Clipboard = Clipboard.replace('\0', '')

                    for Condition in Inputs:
                        if Condition:
                            InputText += Clipboard
                            break
                    else:
                        InputText += event.unicode.replace('\0', '')
                else:
                    InputText += event.unicode.replace('\0', '')

        try:
            if event.type == pygame.JOYDEVICEADDED:
                try:
                    if pygame.joystick.get_count() > 0:
                        joystick = pygame.joystick.Joystick(0)
                        joystick.init()
                except pygame.error:
                    OutputMessage = 'Controller Error'

            if event.type == pygame.JOYAXISMOTION:
                if event.axis == JoystickX:
                    if event.value < -0.5:
                        SigmaTweak -= 1
                    elif event.value > 0.5:
                        SigmaTweak += 1
                elif event.axis == JoystickY:
                    if event.value < -0.5:
                        GammaTweak += 1
                    elif event.value > 0.5:
                        GammaTweak -= 1
        except KeyError as e:
            if str(e) != '5':
                raise

    Inputs = [
        (InputWindowW, (360, 300), (120, 30)),
        (InputWindowH, (490, 300), (120, 30)),
        (InputPayloadLat, (360, 710), (120, 30)),
        (InputPayloadLon, (490, 710), (120, 30)),
        (InputPayloadAlt, (620, 710), (120, 30)),
        (InputTrackerLat, (360, 765), (120, 30)),
        (InputTrackerLon, (490, 765), (120, 30)),
        (InputTrackerAlt, (620, 765), (120, 30)),
        (InputIridium, (1365, 300), (200, 30)),
        (InputAPRS, (1365, 345), (200, 30)),
        (InputUbiquiti, (1365, 390), (200, 30)),
        (InputAltVentOpen, (1030, 710), (240, 30)),
        (InputAltVentClose, (1030, 765), (240, 30)),
        (InputVelVentClose, (940, 765), (40, 30))
    ]

    for Condition, Pos, Size in Inputs:
        if Condition:
            pygame.draw.rect(Window, (0, 0, 0), (int(
                Pos[0] * SF), int(Pos[1] * SF), int(Size[0] * SF), int(Size[1] * SF)))
            pygame.draw.rect(Window, (255, 255, 255), (int(
                Pos[0] * SF), int(Pos[1] * SF), int(Size[0] * SF), int(Size[1] * SF)), int(2 * SF))

            Font = pygame.font.SysFont("Bahnschrift", int(20 * SF))
            InputTextLim = ''

            if len(InputText) > 8 and (InputTrackerLat or InputTrackerLon or InputTrackerAlt or InputPayloadLat or InputPayloadLon or InputPayloadAlt):
                InputTextLim = InputText[:8] + "..."

            InputSurface = Font.render(
                InputTextLim if InputTextLim else InputText, True, (255, 255, 255))
            InputRect = InputSurface.get_rect()
            InputRect.topleft = (
                int((Pos[0] + 5) * SF), int((Pos[1] + 5) * SF))
            Window.blit(InputSurface, InputRect)

            if InputText == '':
                Prompt = ''
                Font = pygame.font.SysFont("Bahnschrift", int(16 * SF))

                if Pos == (1365, 300):
                    Prompt = "ex: 300234064901600"
                elif Pos == (1365, 345):
                    Prompt = "ex: KD0AWK-3"
                elif Pos == (1365, 390):
                    Prompt = "ex: 192.168.2.101"

                if Prompt:
                    InputSurface = Font.render(
                        Prompt, True, (100, 100, 100, 0.8))
                    InputRect = InputSurface.get_rect()
                    InputRect.topleft = (int(
                        (Pos[0] + 25 if Pos[0] == 1365 else Pos[0] + 45) * SF), int((Pos[1] + 7.5) * SF))
                    Window.blit(InputSurface, InputRect)


def Shutdown():
    global Map, MapFile, Recording, Capture, SerialRFD, SerialArduino

    # Save Map File
    if Map:
        Map.save(MapFile)
        Map = None
    MapFile = None

    # Save Video File
    if Recording:
        Recording = False
        Capture.release()
    Capture = None

    # Close RFD Serial Port
    if SerialRFD:
        SerialRFD.close()
    SerialRFD = None

    # Close Arduino Serial Port
    if SerialArduino:
        SerialArduino.close()
    SerialArduino = None

    # Close GUI
    pygame.quit()
    sys.exit()


def Cleanup():
    Shutdown()


atexit.register(Cleanup)

Startup()

while Running:
    # Handle Quit Events
    for event in pygame.event.get():
        if event.type == QUIT:
            Shutdown()

    # Initialize Joystick
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        JoystickX, JoystickY = 0, 1

    # Clear Window
    Window.fill((0, 0, 0))

    # Initialize Threads
    ThreadRFD = threading.Thread(target=UpdateRFD)
    ThreadIridium = threading.Thread(target=UpdateIridium)
    ThreadAPRS = threading.Thread(target=UpdateAPRS)
    ThreadUbiquiti = threading.Thread(target=UpdateUbiquiti)
    ThreadArduino = threading.Thread(target=UpdateArduino)
    ThreadCalculations = threading.Thread(target=Calculations)

    # Start Threads
    ThreadRFD.start()
    ThreadIridium.start()
    ThreadAPRS.start()
    ThreadUbiquiti.start()
    ThreadArduino.start()
    ThreadCalculations.start()

    # Join Threads
    ThreadRFD.join()
    ThreadIridium.join()
    ThreadAPRS.join()
    ThreadUbiquiti.join()
    ThreadArduino.join()
    ThreadCalculations.join()

    DisplayAltitude()
    DisplayLocation()
    DisplayCompass()
    DisplayTime()

    DisplayTitle()
    DisplayRadios()
    DisplayOutput()
    DisplayControls()
    DisplayLaunch()
    DisplayVent()

    DisplayButtons()

    # User Input
    Input()

    # Window Background
    pygame.draw.rect(Window, (255, 255, 255),
                     (0, 0, WindowW, WindowH), int(3 * SF))

    # Refresh Display
    pygame.display.update()

    # Loop Frequency
    Clock.tick(30)

# Close GUI
Shutdown()

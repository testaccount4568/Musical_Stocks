import requests
import pygame
from pygame import mixer
import time
import requests
from playsound import playsound
import numpy

Piano_Sound_Files = {"A3-[AudioTrimmer.com].mp3","A4-[AudioTrimmer.com].mp3","A5-[AudioTrimmer.com].mp3","B3-[AudioTrimmer.com].mp3","B4-[AudioTrimmer.com].mp3","B5-[AudioTrimmer.com].mp3","C3-[AudioTrimmer.com].mp3","C4-[AudioTrimmer.com].mp3","C5-[AudioTrimmer.com].mp3","D3-[AudioTrimmer.com].mp3","D4-[AudioTrimmer.com].mp3","D5-[AudioTrimmer.com].mp3","E3-[AudioTrimmer.com].mp3","E4-[AudioTrimmer.com].mp3","E5-[AudioTrimmer.com].mp3","F3-[AudioTrimmer.com].mp3","F4-[AudioTrimmer.com].mp3","F5-[AudioTrimmer.com].mp3","G3-[AudioTrimmer.com].mp3","G4-[AudioTrimmer.com].mp3","G5-[AudioTrimmer.com].mp3"}
Drum_sounf_files = {"Bass-Drum-Hit-Level-5a.mp3","Drum-Sticks-Hit-A.mp3","Drum-Sticks-Hit-B.mp3", "Hi-Hat-Closed-Hit-A1.mp3", "Hi-Hat-Closed-Hit-A2.mp3", "Hi-Hat-Open-Hit-A1.mp3","Splash-Cymbal-Hit-Short.mp3"}


def get_data_from_Alpha_Vantage_API():
    #replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=demo'
    r = requests.get(url)
    data_from_Alpha_Vantage = r.json()
    return data_from_Alpha_Vantage


def softmax(z):
    e = numpy.exp(z-numpy.max(z))
    s = numpy.sum(e, axis=1, keepdims=True)
    return (e/s).reshape(1,4)

def put_prices_data_into_Array(data_from_Alpha_Vantage):
    Price_Array = []
    Volume_Array = []
    for each_result in data_from_Alpha_Vantage["Time Series (1min)"]:
        Price_Array.append(data_from_Alpha_Vantage["Time Series (1min)"][each_result]["1. open"])
        Volume_Array.append(data_from_Alpha_Vantage["Time Series (1min)"][each_result]["5. volume"])
    return Price_Array, Volume_Array
   
Charecteristics = [["PianoSmash", "trumpet", "trombone", "EGuitarStrum"],
                   ["Minor","NoBeat","Violin"],
                     ["Soft","Piano", "slow"],
                       ["Major", "fast","good beat", "electricGuitar", "Drums", "Trumpet"],
                         ["mediumVol", "Piano"],
                           ["midTempo", "SoftBeat", "Keyborad" ],
                             ["Maj/Min", "slow", "Piano"]]
#Spike, Bear_Main, Bear_Minor, Bull_Main, bull minor, plateau major, plateau minor.
Spike_Transition_To = {""}


data_from_Alpha_Vantage = get_data_from_Alpha_Vantage_API()
Price_Array, Volume_Array = put_prices_data_into_Array(data_from_Alpha_Vantage)
TrendParameters = numpy.array({2,0.5, 1.5, 0.05})
Weights = numpy.array({5, 1, 3, 1})


def get_Trend(Array_of_10_min, TrendParameters):
    diff_array = ""
    ret_Array = {0}*4 # {Spike, Bull, Plat, Bear}
    for i in range(9):
        x = (Array_of_10_min[i+1] - Array_of_10_min[i])
        if( x > TrendParameters[0] or x <-1*TrendParameters[0] ):
            ret_Array[0] += 1
            continue
        elif(x > TrendParameters[1] or x < TrendParameters[2]):
            ret_Array[1] += 1
            continue
        elif(x > -1*TrendParameters[2] or x < -1*TrendParameters[1]):
            ret_Array[2] += 1
            continue
        ret_Array[3] +=1
    ret_Array = numpy.ndarray(ret_Array)
    ret_Array = ret_Array * Weights
    ret_Array = softmax(ret_Array)
    return ret_Array
Spiked = False
def makeMusic_with_trends(Trends_Percentage):
    totalCharecteristics = {}
    i = numpy.argmax(Trends_Percentage)
    match i:
        case 0:
            return Charecteristics[0]
        case 1:
            totalCharecteristics+= Charecteristics[3]
        case 2:
            totalCharecteristics+= Charecteristics[5]
        case 3:
            totalCharecteristics += Charecteristics[1]
    Trends_Percentage[i] = 0
   
    i = numpy.argmax(Trends_Percentage)
    match i:
        case 1:
            totalCharecteristics+= Charecteristics[2]
        case 2:
            totalCharecteristics+= Charecteristics[4]
        case 3:
            totalCharecteristics+= Charecteristics[6]
    return totalCharecteristics


def turn_Prices_into_Music(Price_Array):
    Note = 67
    Octave = 3
    print(Price_Array)
    for index in range(200):
        if(index == 0):
            print(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/c3.mp3")
            playsound(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/A3-[AudioTrimmer.com].mp3")

            continue
        if(Price_Array[index] > Price_Array[index-1]):
            Note+=1
            if(Note > 71):
                Octave+=1
                Note = 65
            if(Octave > 7):
                Octave = 7
            print(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/"+ chr(Note) + '{}'.format(Octave) + ".mp3")
            playsound(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/"+ chr(Note) + '{}'.format(Octave) + "-[AudioTrimmer.com].mp3")
            continue
        elif(Price_Array[index] < Price_Array[index-1]):
            Note -= 1
            if(Note<65):
                Octave -= 1
                Note = 71
            if(Octave < 0):
                Octave=0
            print(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/"+ chr(Note) + '{}'.format(Octave) + ".mp3")
            playsound(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/"+ chr(Note) + '{}'.format(Octave) + "-[AudioTrimmer.com].mp3")
            continue
        print(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/"+ chr(Note) + '{}'.format(Octave) + ".mp3")
        playsound(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/" + chr(Note) + '{}'.format(Octave) + "-[AudioTrimmer.com].mp3")


data_from_Alpha_Vantage = get_data_from_Alpha_Vantage_API()
Price_Array = put_prices_data_into_Array(data_from_Alpha_Vantage)
# turn_Prices_into_Music(Price_Array)

playsound(r"C:\Users\Aguilar\Desktop\Muscial_Stocks\Get_Data\CMajor/A3-[AudioTrimmer.com].mp3")



def playDrums():

def get_data_from_YFinance_API():
     #replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=demo'
    r = requests.get(url)
    data = r.json()
    print(data)
    
    pygame.mixer.load("")
    mixer.music.play(-1)
data_from_Alpha_Vantage = get_data_from_Alpha_Vantage_API()
def Final(Attributes):
    i=9
    while i<data_from_Alpha_Vantage:
        data_10 = {data_from_Alpha_Vantage[i],data_from_Alpha_Vantage[i-1],data_from_Alpha_Vantage[i-2],data_from_Alpha_Vantage[i-3],data_from_Alpha_Vantage[i-4],data_from_Alpha_Vantage[i-5],data_from_Alpha_Vantage[i-6],data_from_Alpha_Vantage[i-7],data_from_Alpha_Vantage[i-8],data_from_Alpha_Vantage[i-9]}
        trendPercent = get_Trend(data_10)
        temporary = makeMusic_with_trends(trendPercent)
        
        i+=6

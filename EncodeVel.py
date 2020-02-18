import numpy as np
import pretty_midi
import glob

def get_piano_roll(midifile):
	#midi_data = pretty_midi.PrettyMIDI('test.midi')
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=25)
	print(piano_roll.shape)
	return piano_roll


def encode(arr):
    timeinc=0
    outString=""
    for _ in arr: #looping through piano roll array
        for vel in arr[timeinc]: #loops through an increment in time (sample in the song and gets velocity values)
            if vel != 0:
                noteRep=str(vel) + " " #adding velocity figures to encoding string
                outString=outString+noteRep #outString is the string which will contain all encoded data
        outString=outString+"\n"
        timeinc = timeinc+1 #updating loop
    return outString


files=glob.glob(r".\dataset\train\*.midi") #getting training MIDI files
print(files)
for f in files[0:1]:
    #some path manipulation to get files
    x= f.split("\\")[-1]
    print(x)
    fileName=f+"\\"+x
    #converting midi to piano roll array
    pr = get_piano_roll(fileName)
    #transpose so you loop through columns when iterating later
    arr = pr.T
    outString= encode(arr)
    file1 = open("dataVel.txt","a")
    file1.write(outString)

file1.close()
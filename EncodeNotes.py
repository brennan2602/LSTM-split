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

#encoding note values from training MIDI files into a text file
def encode(arr):
    timeinc=0
    outString=""
    for time in arr: #looping through increments in time in a song (columns of piano roll array)
        notesinc = -1
        if np.all(time==0): # if all values in this column are 0 nothing is being played so write # to file
            outString=outString+"#"
        for vel in arr[timeinc]:
            notesinc=notesinc+1 #associating note with velocity figure in column
            if vel != 0:
                noteRep=str(notesinc) + " " #writing only the note to the training file
                outString=outString+noteRep #adding note to the encoded string
        outString=outString+"\n" #new line for new time increment (sample)
        timeinc = timeinc+1
    return outString


files=glob.glob(r".\dataset\train\*.midi") #getting training MIDI files to encode into text file
for f in files[0:1]:
    #some manipulation of path to file
    x= f.split("\\")[-1]
    print(x)
    fileName=f+"\\"+x
    #converting MIDI file to piano roll array
    pr = get_piano_roll(fileName)
    #transpose so later we are iterating through columns not rows
    arr = pr.T
    #encoding piano roll in text format
    outString= encode(arr)
    file1 = open("dataNotes.txt","a")
    file1.write(outString)

file1.close()
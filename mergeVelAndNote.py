import numpy as np
with open('generatedNotes.txt') as f: #reading in the generated note values
    lines = f.readlines()
outString=""

for l in lines:
    if len(l.strip()) != 0: #removing blank lines
        outString=outString+l

with open('generatedVel.txt') as f: #reading in the generated velocity values
    lines = f.readlines()
outString2=""
for l in lines:
    if len(l.strip()) != 0:#removing blank lines
        outString2=outString2+l


output=outString.split("\n") #splitting generated notes by lines (samples)
arr=np.zeros((128,len(output))) #creating a numpy array of zeros size 128 x number of samples
print(arr.shape)

j=0
for i in arr.T: #looping through columns of the array (i.e. time samples)
    if output[j].find("#") <0: # when the generated line of text isn't "#" i.e. nothing playing enter this block
        val=output[j] # these are the notes being played at a particular time
        #print(val)
        #print(output[j].find("#") )
        internal=val.split(" ") #if a group of notes are being played they are seperated by " " this splits
                                #this sample into an array of the notes being played
                                #e.g val ="30 37 43 " internal will be ["30","37","43"," "]
        #print(internal)
        while '' in internal:#removes last element from array (always blank)
            internal.remove('')
        for v in internal:#loops through array of note numbers
            index= float(v) #cast to float fixed some errors I ran into directly casting to Int
            index=int(index)#casting the note number to an int so I can index the piano roll array
            if index>127 or index<1: #checking for error cases
                index=0
            i[index]=-1 #changing value at this index of current column of piano roll array to -1 this is a flag to
                        #populate this part of the piano roll array with a velocity later
    j=j+1

output=outString2.split("\n") #splitting velocity file on new lines

#this could possibly be simplified (as discussed in report)
l=[] # 1D list (array) to store velocity values
for i in output:
    val=i.split(" ") #splitting array of velocity values on current line where " " occurs
    clipped=val[0:-1] #getting rid of last element (always blank)
    vels= np.array(clipped) #converting from list to np array
    for v in vels: #looping through velocities
        try:
            v=float(v) #casting velocity strings to float
        except:
            v=0

        v=int(v) #then casting to int

        if v> 127 or v < 1: #checking for error cases
            v= 0
        l.append(v)
#print(l)

index=0 #used to loop through array of velocity figures
for i in arr.T: #looping through columns of piano roll array
    #print(len(i))
    for j in range(len(i)): #essentially looping from 0-127 but not hard coded
        if i[j] ==-1: #if element j of column i is "-1" it is flagged that a note should be being played
            i[j]=l[index] #setting element j of column i to the velocity value stored at current index in array l
            index+=1 #incrementing pointer for velocity values which populate array
            if index>=len(l): #if less velocity values have been generated then notes this resets index so it circles
                              #back through velocity array again
                index=0
np.savetxt("arrayafter.txt", arr, fmt="%s")
#used with help from Gemibni
#Liam Pratt, 12/18/2025
#Accomplay

from music21 import *
#Define root of note as a string
root_note_name = 'C4'
#Create a music21 Note object for the root note
root_note = note.Note(root_note_name)
print(f"Root Note Name: {root_note_name}")
print(f"Music21 Root Note Object: {root_note}")

#Define the scale type(major, minor, possibly add dorian and mixolydian)
scale_type = ('major')

#Create a music21 Scale object based on the root note and scale type
if scale_type == 'major':
    accompaniment_scale = scale.MajorScale(root_note)
elif scale_type == 'minor':
        scale.MinorScale(root_note)
else:
    print(f"Unsupported scale type: {scale_type}. Defaulting to Major.")
    accompaniment_scale = scale.MajorScale(root_note)

#Debug Print
print(f"Scale Type: {scale_type}")
print(f"Accompaniment Scale: {accompaniment_scale}")
print(f"Notes in Scale: {[str(p) for p in accompaniment_scale.pitches]}")



#==========TEMPO========TEMPO============
#Define the tempo in beats per minute (BPM)

tempo_bpm = 120
#Define a default duration for notes, e.g. a quarter note (0.5 for half notes)
default_duration = 0.5 #quarter note duration in music21

print(f"Tempo (BPM): {tempo_bpm}")
print(f"Default Duration (music21): {default_duration}")


#============PLAYING AUDIO=============

#Create an empty stream
s = stream.Stream()

#Add each pitch from the accompaniment scale to the stream
for p in accompaniment_scale.pitches:
    n = note.Note(p)
    n.quarterLength = 0.5 #Give each note a quarter note duration for playing
    s.append(n)

#Display the stream (this will often generate a midi file and/or player
s.show('midi')
print("Attempted to play the scale. If a player does not appear, check file directory.")

# Save the stream to a MIDI file
midi_file_path = 'my_scale.mid'
s.write('midi', fp=midi_file_path)

print(f"Scale saved to {midi_file_path}. You can download this file and play it locally.")




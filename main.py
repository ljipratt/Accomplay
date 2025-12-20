#used with help from Gemibni
#Liam Pratt, 12/18/2025
#Accomplay

from music21 import *
#Define root of note as a string

root_note_name = input("Enter root note name: ")
#Create a music21 Note object for the root note
root_note = note.Note(root_note_name)
print(f"Root Note Name: {root_note_name}")
print(f"Music21 Root Note Object: {root_note}")

#Define the scale type(major, minor, possibly add dorian and mixolydian)
scale_type = input("Enter Scale type(major/minor")

#Create a music21 Scale object based on the root note and scale type
if scale_type == 'major':
    accompaniment_scale = scale.MajorScale(root_note)
elif scale_type == 'minor':
    accompaniment_scale =  scale.MinorScale(root_note)
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


# Save the stream to a MIDI file
midi_file_path = 'my_scale.mid'
s.write('midi', fp=midi_file_path)

print(f"Scale saved to {midi_file_path}. You can download this file and play it locally.")



#=====================CHORD SCALES==========================
#Get pitches for the root, third, fifth, and seventh degrees from the tonic from acccompaniment scale

#use .pitch to get the raw pitch object
root_pitch = root_note.pitch

# Get the chord tones in the root's octave
pitches_root_octave = {
    accompaniment_scale.pitchFromDegree(1, root_pitch),  #Root
    accompaniment_scale.pitchFromDegree(3, root_pitch), #third
    accompaniment_scale.pitchFromDegree(5, root_pitch), #fifth
    accompaniment_scale.pitchFromDegree(7, root_pitch) #seventh
}

# Generate pitches for one octave lower and one octave higher
pitches_lower_octave = [p.transpose('-P8') for p in pitches_root_octave]
pitches_higher_octave = [p.transpose('P8') for p in pitches_root_octave]

#Combine all pitches and sort them to ensure ascending order
#chord_scale_pitches = sorted([*pitches_lower_octave, *pitches_root_octave, *pitches_higher_octave])
ascending_chord_scale_pitches = sorted([*pitches_lower_octave, *pitches_root_octave, *pitches_higher_octave])
descending_chord_scale_pitches = list(reversed(ascending_chord_scale_pitches[:-1]))
chord_scale_pitches = ascending_chord_scale_pitches + descending_chord_scale_pitches



#combine all pitches and sort them to ensure ascending order
print(f"Chord Scale Pitches ({scale_type} 7th, 3 octaves): {[str(p) for p in chord_scale_pitches]}")

#=======print test==========

s_chord_scale = stream.Stream()

#add each pitch from the chord scale to the stream
for p in chord_scale_pitches:
    n = note.Note(p)
    n.quarterLength = 0.5
    s_chord_scale.append(n)

#Save the stream to a MIDI file
chord_scale_midi_file_path = 'Chord_Scale.mid'
s_chord_scale.write('midi', fp=chord_scale_midi_file_path)
print(f"Saved chord scale to {chord_scale_midi_file_path}")
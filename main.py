#used with help from Gemibni
#Liam Pratt, 12/18/2025
#Accomplay

from music21 import *
from music_generator import MusicGenerator
# Instantiate the MusicGenerator class with default values
# You can change these values as needed
root_note_name = "C"
scale_type = "major"
beats_per_measure = 4 # e.g., 4 for 4/4 time
beat_duration = 4     # e.g., 4 for quarter note

# If you want to use interactive input, uncomment the lines below and comment out the default values above
# root_note_name = input("Enter root note name: ")
# scale_type = input("Enter Scale type (major/minor): ")
# beats_per_measure = int(input("Enter beats per measure (e.g., 4): "))
# beat_duration = int(input("Enter beat duration (2 for half, 4 for quarter, 8 for eighth): "))

music_gen = MusicGenerator(root_note_name, scale_type, beats_per_measure, beat_duration)

# Print information about the generated scale and settings
music_gen.print_info()

# Generate and save the scale MIDI file
music_gen.generate_scale_midi('my_scale.mid')

# Generate and save the chord scale MIDI file
music_gen.generate_chord_scale_midi('Chord_Scale.mid')

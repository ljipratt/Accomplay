#used with help from Gemibni
#Liam Pratt, 12/18/2025
#Accomplay

import sys
import importlib
from music21 import *

# Force reload of music_generator module if it's already loaded
if 'music_generator' in sys.modules:
    del sys.modules['music_generator']
    importlib.invalidate_caches()

from music_generator import MusicGenerator, ChordObject

# Instantiate the MusicGenerator class with default values
# You can change these values as needed
root_note_name = "C"
scale_type = "major"
beats_per_measure = 4 # e.g., 4 for 4/4 time
beat_duration = 4     # e.g., 4 for quarter note
seventh_type = "major" # e.g., 'minor', 'major', 'augmented'
play_seventh = True    # New: Whether to include the seventh degree in the chord

# If you want to use interactive input, uncomment the lines below and comment out the default values above
# root_note_name = input("Enter root note name: ")
# scale_type = input("Enter Scale type (major/minor): ")
# beats_per_measure = int(input("Enter beats per measure (e.g., 4): "))
# beat_duration = int(input("Enter beat duration (2 for half, 4 for quarter, 8 for eighth): "))

music_gen = MusicGenerator(root_note_name, scale_type, beats_per_measure, beat_duration, seventh_type, play_seventh)

# Define the first chord using ChordObject and add it to the progression
first_chord = ChordObject(
    root_note_name,
    scale_type,
    seventh_type,
    play_seventh,
    music_gen.chord_duration_beats # Use the default chord duration
)
music_gen.add_chord_to_progression(first_chord)

# Define the second chord here in the main script
second_chord = ChordObject(
    "D", # A different root note
    "minor", # A different scale type
    "minor", # Minor seventh
    True, # Play the seventh
    0.5 # Play for 0.5 beats (eighth note)
)
music_gen.add_chord_to_progression(second_chord)

# Print information about the generated scale and settings
music_gen.print_sheet_info()
music_gen.print_chord_info()

# Generate and save the scale MIDI file with metronome
music_gen.generate_scale_midi('my_scale_with_metronome.mid', include_metronome=True)

# Generate and save the chord scale MIDI file with metronome
music_gen.generate_chord_scale_midi('Chord_Scale_with_metronome.mid', include_metronome=True)

# The standalone metronome generation is removed as it's now integrated into scale and chord scale generation.

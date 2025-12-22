# music_generator.py (conceptual file)
# used with help from Gemini

from music21 import *

class MusicGenerator:
    """Encapsulates logic for generating musical scales and chords, and outputting MIDI."""

    def __init__(self, root_note_name, scale_type, beats_per_measure=4, beat_duration=4):
        self.root_note_name = root_note_name
        self.scale_type = scale_type
        self.root_note = note.Note(root_note_name)
        self.accompaniment_scale = self._create_scale()
        self.tempo_bpm = 120  # Default tempo
        self.default_duration = 0.5  # Quarter note duration in music21
        self.beats_per_measure = beats_per_measure # New: Number of beats per measure
        self.beat_duration = beat_duration     # New: Duration of a beat (e.g., 4 for quarter note)

    def _create_scale(self):
        """Helper to create the music21 Scale object based on type."""
        if self.scale_type.lower() == 'major':
            return scale.MajorScale(self.root_note)
        elif self.scale_type.lower() == 'minor':
            return scale.MinorScale(self.root_note)
        else:
            print(f"Unsupported scale type: {self.scale_type}. Defaulting to Major.")
            return scale.MajorScale(self.root_note)

    def print_info(self):
        """Prints information about the generated scale and settings."""
        print(f"Root Note Name: {self.root_note_name}")
        print(f"Music21 Root Note Object: {self.root_note}")
        print(f"Scale Type: {self.scale_type}")
        print(f"Accompaniment Scale: {self.accompaniment_scale}")
        print(f"Notes in Scale: {[str(p) for p in self.accompaniment_scale.pitches]}")
        print(f"Tempo (BPM): {self.tempo_bpm}")
        print(f"Default Duration (music21): {self.default_duration}")
        print(f"Time Signature: {self.beats_per_measure}/{self.beat_duration}")

    def generate_scale_midi(self, file_path='my_scale.mid'):
        """Generates and saves a MIDI file for the defined scale."""
        s = stream.Stream()
        # Add time signature to the stream
        s.append(meter.TimeSignature(f'{self.beats_per_measure}/{self.beat_duration}'))
        for p in self.accompaniment_scale.pitches:
            n = note.Note(p)
            n.quarterLength = self.default_duration
            s.append(n)
        s.write('midi', fp=file_path)
        print(f"Scale saved to {file_path}. You can download this file and play it locally.")

    def _generate_chord_scale_pattern1(self):
        """Generates the first chord scale pattern (ascending then descending 7ths)."""
        root_pitch = self.root_note.pitch

        # Get the chord tones in the root's octave (1st, 3rd, 5th, 7th degrees)
        pitches_root_octave = {
            self.accompaniment_scale.pitchFromDegree(1, root_pitch),
            self.accompaniment_scale.pitchFromDegree(3, root_pitch),
            self.accompaniment_scale.pitchFromDegree(5, root_pitch),
            self.accompaniment_scale.pitchFromDegree(7, root_pitch)
        }

        # Generate pitches for one octave lower and one octave higher
        pitches_lower_octave = [p.transpose('-P8') for p in pitches_root_octave]
        pitches_higher_octave = [p.transpose('P8') for p in pitches_root_octave]

        # Combine all pitches and sort them to ensure ascending order
        ascending_chord_scale_pitches = sorted([*pitches_lower_octave, *pitches_root_octave, *pitches_higher_octave])
        descending_chord_scale_pitches = list(reversed(ascending_chord_scale_pitches[:-1]))

        chord_scale_pattern1 = ascending_chord_scale_pitches + descending_chord_scale_pitches
        return chord_scale_pattern1

    def generate_chord_scale_midi(self, file_path='Chord_Scale.mid'):
        """Generates and saves a MIDI file for a 7th chord scale (3 octaves)."""
        chord_scale_pitches = self._generate_chord_scale_pattern1()

        print(f"Chord Scale Pitches ({self.scale_type} 7th, 3 octaves): {[str(p) for p in chord_scale_pitches]}")

        s_chord_scale = stream.Stream()
        # Add time signature to the stream
        s_chord_scale.append(meter.TimeSignature(f'{self.beats_per_measure}/{self.beat_duration}'))
        for p in chord_scale_pitches:
            n = note.Note(p)
            n.quarterLength = self.default_duration
            s_chord_scale.append(n)

        s_chord_scale.write('midi', fp=file_path)
        print(f"Saved chord scale to {file_path}")

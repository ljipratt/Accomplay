# music_generator.py (conceptual file)
# used with help from Gemini

from music21 import *
import math


class ChordObject:
    """Encapsulates the properties of a single chord."""

    def __init__(self, root_note_name, scale_type, seventh_type, play_seventh, duration_beats):
        self.root_note_name = root_note_name
        self.scale_type = scale_type
        self.seventh_type = seventh_type
        self.play_seventh = play_seventh
        self.duration_beats = duration_beats

    def _get_chord_symbol(self):
        """Generates the chord symbol string based on musical conventions."""
        chord_symbol = self.root_note_name
        if self.play_seventh:
            if self.scale_type.lower() == 'major':
                if self.seventh_type.lower() == 'major':
                    chord_symbol += 'maj7'
                elif self.seventh_type.lower() == 'minor':
                    chord_symbol += '7'
                else:
                    chord_symbol += '7'
            elif self.scale_type.lower() == 'minor':
                if self.seventh_type.lower() == 'major':
                    chord_symbol += 'm(maj7)'
                elif self.seventh_type.lower() == 'minor':
                    chord_symbol += 'm7'
                else:
                    chord_symbol += 'm7'
            elif self.seventh_type.lower() == 'augmented':
                chord_symbol += 'aug7'
            else:
                chord_symbol += '7'
        else:
            if self.scale_type.lower() == 'minor':
                chord_symbol += 'm'
        return chord_symbol

    def __repr__(self):
        return f"{self._get_chord_symbol()}({self.duration_beats} beats)"


class MusicGenerator:
    """Encapsulates logic for generating musical scales and chords, and outputting MIDI."""

    def __init__(self, root_note_name, scale_type, beats_per_measure=4, beat_duration=4, seventh_type='major',
                 play_seventh=True):
        self.root_note_name = root_note_name
        self.scale_type = scale_type
        self.root_note = note.Note(root_note_name)
        self.accompaniment_scale = self._create_scale()
        self.tempo_bpm = 120  # Default tempo
        self.default_duration = 0.5  # Quarter note duration in music21 (used for scales)
        self.beats_per_measure = beats_per_measure  # New: Number of beats per measure
        self.beat_duration = beat_duration  # New: Duration of a beat (e.g., 4 for quarter note)
        self.seventh_type = seventh_type  # New: Type of seventh degree ('minor', 'major', 'augmented')
        self.play_seventh = play_seventh  # New: Whether to include the seventh degree in the chord
        self.chord_duration_beats = 0.5  # Changed: Set to 0.5 beats for eighth notes (assuming 4/4 time)

        # New: Chord Progression initialization
        self.currentChordProg = []
        self.total_progression_beats = 0

    def add_chord_to_progression(self, chord_obj):
        """Adds a ChordObject to the current progression and updates total beats."""
        if not isinstance(chord_obj, ChordObject):
            raise TypeError("Only ChordObject instances can be added to the progression.")
        self.currentChordProg.append(chord_obj)
        self.total_progression_beats += chord_obj.duration_beats

    def _create_scale(self):
        """Helper to create the music21 Scale object based on type."""
        if self.scale_type.lower() == 'major':
            return scale.MajorScale(self.root_note)
        elif self.scale_type.lower() == 'minor':
            return scale.MinorScale(self.root_note)
        else:
            print(f"Unsupported scale type: {self.scale_type}. Defaulting to Major.")
            return scale.MajorScale(self.root_note)

    def print_sheet_info(self):
        """Prints information about the general sheet music settings."""
        print(f"Root Note Name: {self.root_note_name}")
        print(f"Music21 Root Note Object: {self.root_note}")
        print(f"Scale Type: {self.scale_type}")
        print(f"Accompaniment Scale: {self.accompaniment_scale}")
        print(f"Notes in Scale: {[str(p) for p in self.accompaniment_scale.pitches]}")
        print(f"Tempo (BPM): {self.tempo_bpm}")
        print(f"Default Duration (music21): {self.default_duration}")
        print(f"Time Signature: {self.beats_per_measure}/{self.beat_duration}")

    def print_chord_info(self):
        """Prints information relevant to the current chord and progression."""
        print(f"Seventh Type: {self.seventh_type}")
        print(f"Play Seventh: {self.play_seventh}")
        print(f"Chord Duration (beats): {self.chord_duration_beats}")
        # Display chord progression info
        print(f"Current Chord Progression: {self.currentChordProg}")
        print(f"Total Progression Beats: {self.total_progression_beats}")

    def generate_scale_midi(self, file_path='my_scale_with_metronome.mid', include_metronome=False,
                            num_measures_metronome=None):
        """Generates and saves a MIDI file for the defined scale.

        Args:
            file_path (str): The path to save the MIDI file.
            include_metronome (bool): Whether to include a metronome track.
            num_measures_metronome (int, optional): Number of measures for the metronome. Defaults to None (uses metronome's default).
        """
        score = stream.Score()
        score.append(meter.TimeSignature(f'{self.beats_per_measure}/{self.beat_duration}'))
        score.append(tempo.MetronomeMark(number=self.tempo_bpm))

        # Create a part for the scale notes
        scale_part = stream.Part()
        scale_part.append(instrument.Piano())
        for p in self.accompaniment_scale.pitches:
            n = note.Note(p)
            n.quarterLength = self.default_duration
            scale_part.append(n)
        score.append(scale_part)

        # Add metronome part if requested
        if include_metronome:
            # Determine the length of the metronome part based on the scale part's duration
            # Each note in the scale part has duration self.default_duration.
            # The total duration of the scale part in quarter lengths is len(self.accompaniment_scale.pitches) * self.default_duration.
            # Total beats = (total quarter lengths) / (4 / self.beat_duration)
            # Total measures = total beats / self.beats_per_measure
            # We want the metronome to cover at least the duration of the scale, rounded up.
            scale_total_quarter_lengths = len(self.accompaniment_scale.pitches) * self.default_duration
            beat_quarter_length = 4.0 / self.beat_duration
            scale_total_beats = scale_total_quarter_lengths / beat_quarter_length
            estimated_measures = (scale_total_beats / self.beats_per_measure)

            metronome_part = self._create_metronome_part(
                num_measures=num_measures_metronome if num_measures_metronome is not None else math.ceil(
                    estimated_measures) + 2
            )
            metronome_part.insert(0, instrument.Woodblock())  # Changed to Woodblock
            score.append(metronome_part)
            # Adjust the start offset of the scale part to align with the metronome lead-in
            scale_part.offset = metronome_part.duration.quarterLength - score.duration.quarterLength if metronome_part.duration.quarterLength > score.duration.quarterLength else 0

        score.write('midi', fp=file_path)
        print(f"Scale saved to {file_path}. You can download this file and play it locally.")

    def _generate_single_chord_pattern(self, root_note_name, scale_type, seventh_type, play_seventh):
        """Generates the ascending/descending 7th chord pattern for a single chord.

        Args:
            root_note_name (str): The root note name of the chord.
            scale_type (str): The scale type ('major' or 'minor').
            seventh_type (str): The type of seventh degree ('minor', 'major', 'augmented').
            play_seventh (bool): Whether to include the seventh degree in the chord.

        Returns:
            list: A list of music21.pitch.Pitch objects forming the chord pattern.
        """
        root_note = note.Note(root_note_name)
        if scale_type.lower() == 'major':
            current_scale = scale.MajorScale(root_note)
        elif scale_type.lower() == 'minor':
            current_scale = scale.MinorScale(root_note)
        else:
            current_scale = scale.MajorScale(root_note)  # Default to Major if unknown

        root_pitch = root_note.pitch

        # Get the 1st, 3rd, 5th degrees from the accompaniment scale, in the root's octave
        pitch_1 = current_scale.pitchFromDegree(1, root_pitch)
        pitch_3 = current_scale.pitchFromDegree(3, root_pitch)
        pitch_5 = current_scale.pitchFromDegree(5, root_pitch)

        pitches_root_octave = {pitch_1, pitch_3, pitch_5}

        # Determine the 7th pitch based on the seventh_type parameter, if play_seventh is True
        if play_seventh:
            seventh_pitch_in_root_octave = None
            if seventh_type.lower() == 'minor':
                seventh_pitch_in_root_octave = root_pitch.transpose('m7')
            elif seventh_type.lower() == 'major':
                seventh_pitch_in_root_octave = root_pitch.transpose('M7')
            elif seventh_type.lower() == 'augmented':
                seventh_pitch_in_root_octave = root_pitch.transpose('A7')
            else:
                print(f"Unsupported seventh type: {seventh_type}. Defaulting to diatonic 7th.")
                seventh_pitch_in_root_octave = current_scale.pitchFromDegree(7, root_pitch)
            pitches_root_octave.add(seventh_pitch_in_root_octave)

        all_pitches = []
        for p in pitches_root_octave:
            all_pitches.append(p.transpose('-P8'))  # Lower octave
            all_pitches.append(p)  # Root octave
            all_pitches.append(p.transpose('P8'))  # Higher octave

        unique_sorted_ascending_pitches = sorted(list(set(all_pitches)))

        ascending_chord_scale_pitches = unique_sorted_ascending_pitches
        descending_chord_scale_pitches = list(
            reversed(ascending_chord_scale_pitches[:-1]))  # Avoid duplicating the peak note

        return ascending_chord_scale_pitches + descending_chord_scale_pitches

    def generate_chord_scale_midi(self, file_path='Chord_Scale_with_metronome.mid', include_metronome=False,
                                  num_measures_metronome=None):
        """Generates and saves a MIDI file for a 7th chord scale (3 octaves).

        Args:
            file_path (str): The path to save the MIDI file.
            include_metronome (bool): Whether to include a metronome track.
            num_measures_metronome (int, optional): Number of measures for the metronome. Defaults to None (uses metronome's default).
        """
        score = stream.Score()
        score.append(meter.TimeSignature(f'{self.beats_per_measure}/{self.beat_duration}'))
        score.append(tempo.MetronomeMark(number=self.tempo_bpm))

        chord_scale_part = stream.Part()
        chord_scale_part.append(instrument.Piano())

        total_chord_progression_quarter_lengths = 0

        for chord_obj in self.currentChordProg:
            chord_pitches = self._generate_single_chord_pattern(chord_obj.root_note_name, chord_obj.scale_type,
                                                                chord_obj.seventh_type, chord_obj.play_seventh)
            actual_quarter_length = chord_obj.duration_beats * (4 / self.beat_duration)

            for p in chord_pitches:
                n = note.Note(p)
                n.quarterLength = actual_quarter_length
                chord_scale_part.append(n)
            total_chord_progression_quarter_lengths += len(chord_pitches) * actual_quarter_length

        score.append(chord_scale_part)

        # Add metronome part if requested
        if include_metronome:
            # Determine the length of the metronome part based on the total progression duration
            beat_quarter_length = 4.0 / self.beat_duration
            total_progression_beats_in_quarter_lengths = self.total_progression_beats * (4 / self.beat_duration)
            estimated_measures = (
                        total_progression_beats_in_quarter_lengths / (self.beats_per_measure * beat_quarter_length))

            metronome_part = self._create_metronome_part(
                num_measures=num_measures_metronome if num_measures_metronome is not None else math.ceil(
                    estimated_measures) + 2
            )
            metronome_part.insert(0, instrument.Woodblock())
            score.append(metronome_part)
            # Adjust the start offset of the chord scale part to align with the metronome lead-in
            chord_scale_part.offset = metronome_part.duration.quarterLength - score.duration.quarterLength if metronome_part.duration.quarterLength > score.duration.quarterLength else 0

        score.write('midi', fp=file_path)
        print(
            f"Chord Scale Pitches for Progression ({', '.join([c._get_chord_symbol() for c in self.currentChordProg])}), Total Beats: {self.total_progression_beats}: Saved to {file_path}")

    def _create_metronome_part(self, num_measures=4, metronome_pitch='C5'):
        """Creates a music21.stream.Stream for a metronome click track.

        Args:
            num_measures (int): The number of measures for the metronome track.
            metronome_pitch (str): The pitch for the metronome click (e.g., 'C5').

        Returns:
            music21.stream.Stream: A stream containing the metronome clicks.
        """
        metronome_stream = stream.Part()
        metronome_stream.append(meter.TimeSignature(f'{self.beats_per_measure}/{self.beat_duration}'))
        metronome_stream.append(tempo.MetronomeMark(number=self.tempo_bpm))

        # Calculate the duration of a single beat in quarterLength
        beat_quarter_length = 4.0 / self.beat_duration

        for _ in range(num_measures):
            for beat in range(self.beats_per_measure):
                n = note.Note(metronome_pitch, quarterLength=beat_quarter_length)
                # Slightly different sound for the first beat of the measure
                if beat == 0:
                    n.volume.velocity = 50  # Reduced volume
                else:
                    n.volume.velocity = 35  # Reduced volume
                metronome_stream.append(n)
        return metronome_stream
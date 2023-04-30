import numpy as np
import math

names = ['A', 'A#/B♭', 'B', 'C', 'C#/D♭', 'D', 'D#/E♭', 'E', 'F', 'F#/G♭', 'G', 'G#/A♭']

def get_note(frequency):
    if frequency == None:
        return None
    distance_from_a = (math.log(frequency) - math.log(440)) / (math.log(2) / 12)
    num_semitones = math.floor(distance_from_a + 0.5)
    cents_off = round(distance_from_a - num_semitones, 6)

    letter_name = names[num_semitones % 12]
    octave = 4 + num_semitones // 12

    return (letter_name, octave, cents_off)

def print_note(frequency):
    note_data = get_note(frequency)
    if note_data == None:
        return None
    letter_name, octave, cents_off = note_data
    print(f"{letter_name}{octave} {'+' if cents_off > 0 else ''}{cents_off if cents_off != 0 else ''}")


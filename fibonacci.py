from miditoolkit.midi import parser, containers
import numpy as np

if __name__ == '__main__':
    print("Fibonacci MIDI sequence generator")
    has_rhythm = input("Fibonacci rhythm? [Y/N] ")
    has_rhythm = has_rhythm != "N" and has_rhythm != "n"
    base_duration = int(480 * 4 / int(input("Base note value? 1 for whole note, 2 for half note, etc. ")))
    has_pitch = input("Fibonacci pitch? [Y/N] ")
    has_pitch = has_pitch != "N" and has_pitch != "n"
    base_pitch = int(input("Base pitch? 60 is C4, 61 is C#4, etc. "))
    n_notes = int(input("How many notes does the sequence have? "))
    output_path = input("Path of result .mid file? ")

    alpha, beta = (1 + np.sqrt(5)) / 2, (1 - np.sqrt(5)) / 2
    integers = np.arange(1, n_notes + 1)
    fibonacci_sequence = np.array(np.rint(((alpha ** integers) - (beta ** integers)) / np.sqrt(5)), dtype=int)
    midi_obj = parser.MidiFile()
    midi_obj.instruments = [containers.Instrument(program=0)]
    current_duration = 0
    for fibonacci_number in fibonacci_sequence:
        pitch = base_pitch + (fibonacci_number - 1 if has_pitch else 0)
        duration = base_duration * (fibonacci_number if has_rhythm else 1)
        midi_obj.instruments[0].notes.append(
            containers.Note(velocity=64, pitch=pitch, start=current_duration, end=current_duration + duration))
        current_duration += duration
    midi_obj.dump(output_path)

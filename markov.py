from miditoolkit.midi import parser, containers
import numpy as np

if __name__ == '__main__':
    print("Markov chain MIDI sequence generator")
    markov_path = input("Path of .mid file for Markov chain construction? ")
    use_transpose = input("Use pitch as row and rhythm as column? If no, it will be vice versa. [Y/N] ")
    use_transpose = use_transpose != "N" and use_transpose != "n"
    scale_path = input("Path of .mid file for scale? ")
    change_pitch = input("Stochastic pitch? [Y/N] ")
    change_pitch = change_pitch != "N" and change_pitch != "n"
    change_duration = input("Stochastic duration? [Y/N] ")
    change_duration = change_duration != "N" and change_duration != "n"
    n_notes = int(input("How many notes does the sequence have? "))
    output_path = input("Path of result .mid file? ")

    markov_notes = parser.MidiFile(markov_path).instruments[0].notes
    scale_notes = parser.MidiFile(scale_path).instruments[0].notes
    scale_length = min(len(markov_notes), len(scale_notes))
    markov_pitches = np.array([note.pitch for note in markov_notes])[:scale_length]
    markov_durations = np.array([note.end - note.start for note in markov_notes])[:scale_length]
    markov_matrix = np.array(np.outer(markov_pitches, markov_durations), dtype=float)
    markov_matrix /= np.sum(markov_matrix, axis=0)

    midi_obj = parser.MidiFile()
    midi_obj.instruments = [containers.Instrument(program=0)]
    current_state = np.random.choice(scale_length)
    current_duration = 0
    for _ in range(n_notes):
        current_state = np.random.choice(scale_length, p=markov_matrix[:, current_state])
        pitch = scale_notes[current_state].pitch if change_pitch else 60
        duration = scale_notes[current_state].end - scale_notes[current_state].start if change_duration else 480
        midi_obj.instruments[0].notes.append(
            containers.Note(velocity=64, pitch=pitch, start=current_duration, end=current_duration + duration))
        current_duration += duration
    midi_obj.dump(output_path)

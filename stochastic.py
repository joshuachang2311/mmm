from miditoolkit.midi import parser, containers
import numpy as np

if __name__ == '__main__':
    print("Stochastic MIDI sequence generator")
    distribution_path = input("Path of .mid file for probability distribution? ")
    use_pitch_distribution = input("Use pitch distribution? [Y/N] ")
    use_pitch_distribution = use_pitch_distribution != "N" and use_pitch_distribution != "n"
    scale_path = input("Path of .mid file for scale? ")
    change_pitch = input("Stochastic pitch? [Y/N] ")
    change_pitch = change_pitch != "N" and change_pitch != "n"
    change_duration = input("Stochastic duration? [Y/N] ")
    change_duration = change_duration != "N" and change_duration != "n"
    n_notes = int(input("How many notes does the sequence have? "))
    output_path = input("Path of result .mid file? ")

    distribution_notes = parser.MidiFile(distribution_path).instruments[0].notes
    scale_notes = parser.MidiFile(scale_path).instruments[0].notes
    scale_length = min(len(distribution_notes), len(scale_notes))
    probability_distribution = np.array(
        [(note.pitch if use_pitch_distribution else note.end - note.start) for note in distribution_notes])
    probability_distribution = probability_distribution / np.sum(probability_distribution)

    midi_obj = parser.MidiFile()
    midi_obj.instruments = [containers.Instrument(program=0)]
    current_duration = 0
    for _ in range(n_notes):
        random_index = np.random.choice(scale_length, p=probability_distribution)
        pitch = scale_notes[random_index].pitch if change_pitch else 60
        random_index = np.random.choice(scale_length, p=probability_distribution)
        duration = scale_notes[random_index].end - scale_notes[random_index].start if change_duration else 480
        midi_obj.instruments[0].notes.append(
            containers.Note(velocity=64, pitch=pitch, start=current_duration, end=current_duration + duration))
        current_duration += duration
    midi_obj.dump(output_path)

from miditoolkit.midi import parser, containers

if __name__ == '__main__':
    print("Chromatic MIDI sequence generator")
    base_duration = int(480 * 4 / int(input("Note value? 1 for whole note, 2 for half note, etc. ")))
    base_pitch = int(input("Starting pitch? 60 is C4, 61 is C#4, etc. "))
    n_notes = int(input("How many of this note does the sequence have? "))
    output_path = input("Path of result .mid file? ")

    midi_obj = parser.MidiFile()
    midi_obj.instruments = [containers.Instrument(program=0)]
    current_duration = 0
    for i_semitone in range(n_notes):
        pitch = base_pitch + i_semitone
        midi_obj.instruments[0].notes.append(
            containers.Note(velocity=64, pitch=pitch, start=current_duration, end=current_duration + base_duration))
        current_duration += base_duration
    midi_obj.dump(output_path)

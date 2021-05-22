from skimage.transform import resize
from midiutil.MidiFile import MIDIFile
from skimage import io
import numpy as np

from processing import constants, types


def convert_image_to_midi(image: np.ndarray) -> MIDIFile:
    image = rescale(image)
    note_events = image_to_notes(image)
    midi = create_midi_file(note_events)
    return midi


def load_image(file_name: str) -> np.ndarray:
    image: np.ndarray = io.imread(file_name, as_gray=True)
    return image


def rescale(image: np.ndarray) -> np.ndarray:
    height, width = image.shape
    width_ratio = height / (width / constants.NO_PIANO_KEYS)
    image = resize(image, (int(width_ratio), constants.NO_PIANO_KEYS))
    return image


def image_to_notes(image: np.ndarray) -> list[types.NoteEventType]:
    height, width = image.shape
    note_events: list[types.NoteEventType] = []
    for i in range(width):
        note_on: None | int = None
        note_started: bool = False
        for j in range(height):
            x = i
            y = height - j - 1
            current_pixel = image[y][x]
            # print(current_pixel, x, y)
            if not note_started and current_pixel <= 0.7:
                note_started = True
                note_on = j
            elif note_started and current_pixel >= 0.95:
                note_events.append(types.NoteEventType(i, note_on, j))
                note_started = False
                note_on = None
        if note_started:
            note_events.append(types.NoteEventType(i, note_on, height))
    return note_events


def create_midi_file(note_events: list[types.NoteEventType]) -> MIDIFile:
    # create your MIDI object
    mf = MIDIFile(1)  # only 1 track
    track = 0  # the only track

    time = 0  # start at the beginning
    mf.addTrackName(track, time, "track_0")
    mf.addTempo(track, time, 1000)

    # add some notes
    channel = 0
    volume = 100

    note_events = sorted(note_events, key=lambda k: k.note_on)
    # print(note_events)
    for note_event in note_events:
        mf.addNote(
            track,
            channel,
            note_event.key + 21,
            int(note_event.note_on / 5),
            (note_event.note_off - note_event.note_on) / 5,
            volume
        )
    return mf


def main():
    file_name = 'ltypBIXdmfZAGGC-800x450-noPad.jpg'

    image = load_image(file_name)
    midi = convert_image_to_midi(image)

    # write it to disk
    save_file_name = ''.join(file_name.split('.')[:-1])
    with open(f'{save_file_name}.mid', 'wb') as f:
        midi.writeFile(f)


if __name__ == '__main__':
    main()

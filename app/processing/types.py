from typing import NamedTuple


class NoteEventType(NamedTuple):
    key: int
    note_on: int
    note_off: int

import logging
import os

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from midiutil.MidiFile import MIDIFile
from fastapi import FastAPI

from processing import convert_image_to_midi

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")

DEBUG = True if os.name == 'nt' else False  # assume windows is not server
app = FastAPI()

origins = [
    'http://localhost:5000',
    'https://hkportfolioanalysis.firebaseapp.com',
    'https://hkportfolioanalysis.firebaseapp.com/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get('/')
def check_status():
    return 'ok'


@app.post('/api/convert_image_to_midi')
async def run_convert_image_to_midi(image) -> MIDIFile:
    midi = convert_image_to_midi(image)
    return midi

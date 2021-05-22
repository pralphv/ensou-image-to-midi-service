import os
import tempfile

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTasks
from fastapi import FastAPI, File, UploadFile, Response, responses

from processing import convert_image_to_midi, load_image

DEBUG = True if os.name == 'nt' else False
app = FastAPI()

origins = [
    'https://ensou-d031f.web.app'
]

if DEBUG:
    origins.append('http://localhost:5000')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get('/')
def check_status():
    return 'ok'


def remove_file(path: str) -> None:
    os.unlink(path)


@app.post('/api/convert_image_to_midi')
async def run_convert_image_to_midi(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...)
) -> Response:
    image = load_image(file.file)
    midi = convert_image_to_midi(image)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        midi.writeFile(f)
        background_tasks.add_task(remove_file, f.name)
        return responses.FileResponse(f.name, media_type="audio/mid")

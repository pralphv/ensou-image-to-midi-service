import base64
import json
from io import BytesIO

from app.processing import convert_image_to_midi, load_image


def lambda_handler(event, context):
    image = base64.b64decode(event['encoded_image'])

    image = load_image(BytesIO(image))
    midi = convert_image_to_midi(image)
    buffered = BytesIO()
    midi.writeFile(buffered)
    encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://ensoumidi.com',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        },
        'body': json.dumps({'midi_file': encoded_string})
    }

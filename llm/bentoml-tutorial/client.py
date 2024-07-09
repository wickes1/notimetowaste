from pathlib import Path
import bentoml

with bentoml.SyncHTTPClient("http://localhost:3000") as client:
    audio_url = "./female.wav"
    response = client.transcribe(audio_file=audio_url)
    print(response)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import StreamingResponse
from io import BytesIO

from lib.audio_generator_old import AudioGenerator

audio_gen = AudioGenerator()

# Initialize the app
app = FastAPI(
    title="Simple API",
    description="A lightweight FastAPI example",
    version="0.1.0"
)


class TextInput(BaseModel):
    text: str


@app.post("/python/text-to-speech/generate-audio")
async def generate_audio(text: TextInput):
    try:
        tts = AudioGenerator(lang="en-uk", slow=False)
        audio_stream = tts.generate_to_stream(text.text)
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=generated_audio.mp3"}
        )
    except Exception as e:
        return {"error": str(e)}

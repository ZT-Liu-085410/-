import edge_tts
import asyncio
import os

async def speak(text, voice, rate, filename):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(filename)

def synthesize_by_voice(text, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    voices = [
        "en-US-JennyNeural",
        "en-US-GuyNeural",
        "en-GB-RyanNeural",
        "en-US-AriaNeural",
        "en-GB-SoniaNeural"
    ]
    tasks = []
    for voice in voices:
        filename = os.path.join(output_dir, f"{voice}_default.wav")
        tasks.append(speak(text, voice, "+0%", filename))
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

def synthesize_by_rate(text, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    voice = "en-US-JennyNeural"
    rates = ["-20%", "-10%", "+0%","+10%","+20%"]
    tasks = []
    for rate in rates:
        safe_rate = rate.replace("%", "pct")
        filename = os.path.join(output_dir, f"{voice}_{safe_rate}.wav")
        tasks.append(speak(text, voice, rate, filename))
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

def synthesize_combined(text, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    voices = [
        "en-US-JennyNeural",
        "en-US-GuyNeural",
        "en-GB-RyanNeural",
        "en-US-AriaNeural",
        "en-GB-SoniaNeural"
    ]
    rates = ["-20%", "+0%", "+20%"]
    tasks = []
    for voice in voices:
        for rate in rates:
            safe_rate = rate.replace("%", "pct")
            filename = os.path.join(output_dir, f"{voice}_{safe_rate}.wav")
            tasks.append(speak(text, voice, rate, filename))
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

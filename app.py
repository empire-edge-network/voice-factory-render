import io
import edge_tts
import asyncio
from flask import Flask, send_file, request

app = Flask(__name__)

async def generate_speech(text, voice):
    """Generates MP3 audio from text using Edge TTS."""
    communicate = edge_tts.Communicate(text, voice)
    # Use an in-memory buffer to avoid writing to disk
    audio_buffer = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
            
    audio_buffer.seek(0)
    return audio_buffer

@app.route('/speak', methods=['GET'])
def speak():
    # 1. Get text from the URL (n8n will send the script here)
    text = request.args.get('text')
    
    # 2. Set default voice and error checks
    voice = "en-US-JennyNeural"  # High-quality, professional voice
    if not text:
        return "Please provide 'text' parameter in the URL.", 400

    # 3. Generate the MP3
    try:
        audio_buffer = asyncio.run(generate_speech(text, voice))
        
        # 4. Return the MP3 file
        return send_file(
            audio_buffer,
            mimetype="audio/mp3",
            as_attachment=True,
            download_name="voiceover.mp3"
        )
    except Exception as e:
        return f"TTS Generation Error: {e}", 500

if __name__ == '__main__':
    # Use this for local testing only

    app.run(debug=True)
    
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

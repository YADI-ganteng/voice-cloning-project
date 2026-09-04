"""
🎤 Voice Cloning Script
Generate MP3 dari suara sample
"""

import os
from gtts import gTTS

def generate_mp3_from_text(text_file="cerita/cerita.txt", output="output/hasil.mp3"):
    """Generate MP3 dari cerita"""
    os.makedirs("output", exist_ok=True)
    
    # Baca cerita
    with open(text_file, "r", encoding="utf-8") as f:
        cerita = f.read()
    
    print(f"📝 Cerita: {len(cerita.split())} kata")
    
    # Generate MP3
    print("🎤 Generating MP3...")
    tts = gTTS(text=cerita, lang="id", slow=False)
    tts.save(output)
    
    print(f"✅ MP3: {output}")
    return output

if __name__ == "__main__":
    generate_mp3_from_text()

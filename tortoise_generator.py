"""
🐢 Tortoise TTS - Voice Cloning Generator
"""

import os
import sys
import torch
import torchaudio

print("=" * 60)
print("🐢 TORTOISE TTS - VOICE CLONING")
print("=" * 60)

# Install Tortoise
print("\n📦 Installing Tortoise...")
os.system("pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu")
os.system("pip install -q transformers scipy inflect progressbar")

if not os.path.exists("tortoise-tts"):
    os.system("git clone https://github.com/neonbjb/tortoise-tts.git")

os.chdir("tortoise-tts")
os.system("pip install -q -r requirements.txt")
os.system("python setup.py install")
os.chdir("..")

print("✅ Installed!")

# Load model
print("\n📥 Loading model...")
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio

tts = TextToSpeech()
print("✅ Model loaded!")

# Load sample
print("\n🎤 Loading sample...")
sample_files = [f for f in os.listdir("voice_sample") if f.endswith(('.mp3', '.wav'))]

if not sample_files:
    print("❌ No sample!")
    sys.exit(1)

sample_path = os.path.join("voice_sample", sample_files[0])
voice_samples = [load_audio(sample_path, 22050)]
print(f"✅ Sample: {sample_path}")

# Load cerita
print("\n📝 Loading cerita...")
cerita_files = [f for f in os.listdir("cerita") if f.endswith('.txt')]

cerita = "Di sebuah desa terpencil, terjadi kejadian aneh."
if cerita_files:
    with open(os.path.join("cerita", cerita_files[0]), "r") as f:
        cerita = f.read()

# Potong ke 100 kata untuk GitHub
words = cerita.split()
if len(words) > 100:
    cerita = ' '.join(words[:100])
    print(f"⚠️ Dipotong ke 100 kata")

print(f"✅ Cerita: {len(cerita.split())} kata")

# Generate
print("\n🐢 Cloning suara...")
print("⏳ 10-30 menit di CPU...")

gen = tts.tts_with_preset(
    cerita,
    voice_samples=voice_samples,
    preset="fast",
    num_autoregressive_samples=4,
    diffusion_iterations=30,
    cond_free=True,
)

# Save
os.makedirs("output", exist_ok=True)
output_wav = "output/hasil_clone.wav"
torchaudio.save(output_wav, gen.squeeze(0).cpu(), 24000)

# Convert MP3
os.system("ffmpeg -i output/hasil_clone.wav -codec:a libmp3lame -qscale:a 2 output/hasil_clone.mp3 -y")

print("\n✅ MP3 berhasil: output/hasil_clone.mp3")

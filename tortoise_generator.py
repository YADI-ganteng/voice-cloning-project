"""
🐢 Tortoise TTS - Voice Cloning Generator (FIXED)
"""

import os
import sys
import subprocess

print("=" * 60)
print("🐢 TORTOISE TTS - VOICE CLONING")
print("=" * 60)

# ============ INSTALL TORCH & DEPENDENCIES ============
print("\n📦 Installing torch & dependencies...")
os.system("pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu")
os.system("pip install -q transformers scipy inflect progressbar")
print("✅ Installed!")

# ============ IMPORT TORCH ============
import torch
import torchaudio
print(f"✅ Torch: {torch.__version__}")

# ============ INSTALL TORTOISE ============
print("\n📦 Installing Tortoise TTS...")

if not os.path.exists("tortoise-tts"):
    os.system("git clone https://github.com/neonbjb/tortoise-tts.git")

os.chdir("tortoise-tts")
os.system("pip install -q -r requirements.txt")
os.system("python setup.py install")
os.chdir("..")

print("✅ Tortoise installed!")

# ============ LOAD MODEL ============
print("\n📥 Loading Tortoise model...")
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio

tts = TextToSpeech()
print("✅ Model loaded!")

# ============ LOAD SAMPLE ============
print("\n🎤 Loading voice sample...")
sample_files = []
if os.path.exists("voice_sample"):
    sample_files = [f for f in os.listdir("voice_sample") if f.endswith(('.mp3', '.wav'))]

if not sample_files:
    print("❌ No sample!")
    sys.exit(1)

sample_path = os.path.join("voice_sample", sample_files[0])
voice_samples = [load_audio(sample_path, 22050)]
print(f"✅ Sample: {sample_path}")

# ============ LOAD CERITA ============
print("\n📝 Loading cerita...")
cerita_files = []
if os.path.exists("cerita"):
    cerita_files = [f for f in os.listdir("cerita") if f.endswith('.txt')]

cerita = "Di sebuah desa terpencil, terjadi kejadian aneh."
if cerita_files:
    with open(os.path.join("cerita", cerita_files[0]), "r", encoding="utf-8") as f:
        cerita = f.read()

# Potong ke 50 kata untuk GitHub (lebih cepat)
words = cerita.split()
if len(words) > 50:
    cerita = ' '.join(words[:50])
    print(f"⚠️ Dipotong ke 50 kata")

print(f"✅ Cerita: {len(cerita.split())} kata")

# ============ GENERATE ============
print("\n🐢 Cloning suara...")
print("⏳ 5-15 menit di CPU...")

try:
    gen = tts.tts_with_preset(
        cerita,
        voice_samples=voice_samples,
        preset="ultra_fast",  # Lebih cepat
        num_autoregressive_samples=2,
        diffusion_iterations=10,
    )
    
    # Save
    os.makedirs("output", exist_ok=True)
    output_wav = "output/hasil_clone.wav"
    torchaudio.save(output_wav, gen.squeeze(0).cpu(), 24000)
    
    # Convert ke MP3
    os.system("ffmpeg -i output/hasil_clone.wav -codec:a libmp3lame -qscale:a 2 output/hasil_clone.mp3 -y")
    
    print("\n✅ MP3 berhasil: output/hasil_clone.mp3")
    
except Exception as e:
    print(f"❌ Generate failed: {e}")
    sys.exit(1)

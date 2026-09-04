"""
🐢 Tortoise TTS - FIXED INSTALL
"""

import os
import sys
import subprocess

print("=" * 60)
print("🐢 TORTOISE TTS - FIXED")
print("=" * 60)

# ============ INSTALL DEPENDENCIES ============
print("\n📦 Installing dependencies...")

# Install torch
os.system("pip install -q torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu")

# Install transformers yang compatible
os.system("pip install -q transformers==4.30.0")

# Install dependencies lain
os.system("pip install -q scipy inflect progressbar")

print("✅ Dependencies installed!")

# ============ INSTALL TORTOISE ============
print("\n📦 Installing Tortoise TTS...")

# Clone Tortoise
if os.path.exists("tortoise-tts"):
    os.system("rm -rf tortoise-tts")

os.system("git clone https://github.com/neonbjb/tortoise-tts.git")

# Install dengan pip langsung
os.chdir("tortoise-tts")
os.system("pip install -q -e .")
os.chdir("..")

print("✅ Tortoise installed!")

# ============ VERIFIKASI ============
print("\n🔍 Verifikasi install...")

try:
    import torch
    print(f"✅ Torch: {torch.__version__}")
except:
    print("❌ Torch tidak terinstall")

try:
    from tortoise.api import TextToSpeech
    print("✅ Tortoise module loaded!")
except Exception as e:
    print(f"❌ Tortoise gagal: {e}")
    print("\n🔄 Mencoba alternatif install...")
    
    # Alternatif: Install dari source
    os.chdir("tortoise-tts")
    os.system("python setup.py build")
    os.system("python setup.py install")
    os.chdir("..")
    
    try:
        from tortoise.api import TextToSpeech
        print("✅ Tortoise loaded (alternatif)!")
    except Exception as e2:
        print(f"❌ Masih gagal: {e2}")
        print("\n📝 Menggunakan gTTS sebagai fallback...")
        
        # Fallback ke gTTS
        os.system("pip install -q gTTS")
        from gtts import gTTS
        
        # Load cerita
        cerita = "Di sebuah desa terpencil, terjadi kejadian aneh."
        if os.path.exists("cerita"):
            files = [f for f in os.listdir("cerita") if f.endswith('.txt')]
            if files:
                with open(os.path.join("cerita", files[0]), "r") as f:
                    cerita = f.read()
        
        # Generate
        tts = gTTS(text=cerita, lang="id", slow=False)
        os.makedirs("output", exist_ok=True)
        tts.save("output/hasil.mp3")
        print("✅ MP3 dibuat dengan gTTS (bukan cloning)")
        sys.exit(0)

# ============ LOAD MODEL ============
print("\n📥 Loading Tortoise model...")
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio

tts = TextToSpeech()
print("✅ Model loaded!")

# ============ LOAD SAMPLE ============
print("\n🎤 Loading sample...")
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

words = cerita.split()
if len(words) > 30:
    cerita = ' '.join(words[:30])
    print(f"⚠️ Dipotong ke 30 kata")

# ============ GENERATE ============
print("\n🐢 Cloning suara...")
print("⏳ 5-10 menit...")

import torch
import torchaudio

gen = tts.tts_with_preset(
    cerita,
    voice_samples=voice_samples,
    preset="ultra_fast",
    num_autoregressive_samples=2,
    diffusion_iterations=10,
)

os.makedirs("output", exist_ok=True)
torchaudio.save("output/hasil_clone.wav", gen.squeeze(0).cpu(), 24000)
os.system("ffmpeg -i output/hasil_clone.wav -codec:a libmp3lame -qscale:a 2 output/hasil_clone.mp3 -y")

print("\n✅ MP3: output/hasil_clone.mp3")

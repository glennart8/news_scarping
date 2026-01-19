import edge_tts
import asyncio
import pygame
import os

# "sv-SE-SofieNeural" (Kvinna) eller "sv-SE-MattiasNeural" (Man)
VOICE = "sv-SE-SofieNeural"
OUTPUT_FILE = "nyhetssändning.mp3"

async def _create_audio_file(text):
    """Hjälpfunktion som körs asynkront för att spara ljudfilen."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

def speak_text(text):
    """Genererar tal från text och spelar upp det."""
    print(f"Genererar ljud..")
    
    try:
        # 1. Skapa ljudfilen (kör async-kod synkront)
        asyncio.run(_create_audio_file(text))
        
        # 2. Spela upp med pygame
        print("Spelar upp sändningen...")
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()
        
        # Vänta tills det spelat klart
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        print("Uppspelning klar.")
        
    except Exception as e:
        print(f"Ljudfel: {e}")

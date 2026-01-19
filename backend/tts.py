import edge_tts
import asyncio
import pygame
from datetime import datetime

# "sv-SE-SofieNeural" (Kvinna) eller "sv-SE-MattiasNeural" (Man)
VOICE = "sv-SE-SofieNeural"

async def _create_audio_file(text, filename):
    """Hjälpfunktion som körs asynkront för att spara ljudfilen."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

def speak_text(text):
    """Genererar tal från text och spelar upp det."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = f"nyhetssändning-{date_str}.mp3"
    
    print(f"Genererar ljud till {output_file}..")
    
    try:
        # 1. Skapa ljudfilen (kör async-kod synkront)
        asyncio.run(_create_audio_file(text, output_file))
        
        # 2. Spela upp med pygame
        print("Spelar upp sändningen...")
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Vänta tills det spelat klart
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        print("Uppspelning klar.")
        
    except Exception as e:
        print(f"Ljudfel: {e}")

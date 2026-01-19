import requests
from bs4 import BeautifulSoup
import time


# --- Scraper-funktion ---
def scrape_articles(rss_url, max_articles=3, paragraph_class=None):
    print(f"Hämtar RSS från {rss_url}...")
    
    try:
        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, "xml") # Gör soppa
        items = soup.find_all("item") # Hämta alla ingredienser (artiklar)
    except Exception as e:
        print(f"Kunde inte hämta RSS: {e}")
        return []

    # Skapar en lista av dictionaries att appenda nyheter till
    raw_articles = []
    
    # Loopa igenom de senaste artiklarna
    for item in items[:max_articles]:
        url = item.link.text
        rss_title = item.title.text
        print(f"\nBearbetar: {rss_title}")

        try:
            # Gå in på artikeln
            article_resp = requests.get(url)
            if article_resp.status_code != 200:
                continue
            
            # Tolka HTML-koden
            article_soup = BeautifulSoup(article_resp.content, "html.parser")
            
            # --- Hämta texten ---
            paragraphs = []
            # Om vi har en specifik klass att leta efter (t.ex. för SVT)
            if paragraph_class:
                paragraphs = article_soup.find_all("p", class_=paragraph_class)
            
            # Fallback: Hämta alla p-taggar om ingen specifik klass hittades eller angavs
            if not paragraphs:
                paragraphs = article_soup.find_all("p")

            # Slå ihop texten
            full_text = " ".join([p.text for p in paragraphs])
            
            # Filtrera bort korta texter (t.ex. bara video-beskrivningar)
            if len(full_text) < 200:
                print("För lite text, hoppar över (förmodligen bara video).")
                continue

            # Spara rådata
            raw_articles.append({
                "rss_title": rss_title,
                "url": url,
                "text": full_text
            })
            
            # För att undvika krash eller ban
            time.sleep(1)

        except Exception as e:
            print(f"Fel vid hantering av {url}: {e}")

    return raw_articles
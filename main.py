from backend.scraper import scrape_svt_articles
from backend.agent import analyze_news, generate_radio_script
from backend.tts import speak_text

if __name__ == "__main__":
    print("Startar nyhetsprocessen...")
    
    # 1. Skrapa
    raw_articles = scrape_svt_articles(max_articles=3)
    print(f"\nHittade {len(raw_articles)} artiklar att analysera.\n")
    
    analyzed_articles = []

    # 2. Analysera
    for i, article_data in enumerate(raw_articles, 1):
        print(f"Analyserar: {article_data['rss_title']}...")
        
        analys = analyze_news(article_data['text'])
        
        if analys:
            analyzed_articles.append(analys)
            print(f"--- Resultat Artikel {i} ---")
            print(f"Rubrik:  {analys.title}")
            print(f"Land:    {analys.country}")
            print(f"Kategori:{analys.category}")
            print(f"Allvar:  {analys.severity}/10")
            print(f"Sammanfattning: {analys.summary}\n")
        else:
            print("Misslyckades med analysen.\n")

    # 3. Skapa radiomanus och läs upp
    if analyzed_articles:
        print("Skapar sammanfattning...")
        # Skapa ett manus med hgjälp av LLM som sammanfattar de skrapade artiklarna
        script = generate_radio_script(analyzed_articles)
        
        speak_text(script)

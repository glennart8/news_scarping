from backend.scraper import scrape_articles
from backend.agent import analyze_news, generate_radio_script
from backend.tts import speak_text
from backend.constants import RSS_FEEDS

if __name__ == "__main__":
    print("Startar...")
    
    # 1. Skrapa
    raw_articles = []
    
    for feed in RSS_FEEDS:
        print(f"\n--- Hämtar från {feed['source']} ---")
        articles = scrape_articles(feed['url'], max_articles=2, paragraph_class=feed['paragraph_class'])
        raw_articles.extend(articles)
    
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

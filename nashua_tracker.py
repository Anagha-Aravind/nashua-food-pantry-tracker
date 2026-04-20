import requests
from bs4 import BeautifulSoup

SOURCES = {
    "Nashua Soup Kitchen & Shelter (NSKS)": {
        "url": "https://nsks.org/donate-goods/",
        "keys": ['cereal', 'rice', 'pasta', 'shampoo', 'diapers', 'tuna', 'beans', 'mac', 'cheese', 'razor', 'shave', 'menstrual', 'toilet paper', 'formula', 'ensure']
    },
    "Corpus Christi Food Pantry": {
        "url": "https://corpuschristifoodpantry.org/?page_id=1888", 
        "keys": ['coffee', 'ketchup', 'spam', 'juice', 'tissues', 'detergent', 'flour', 'oil', 'ham', 'cracker', 'syrup', 'jelly', 'deodorant']
    }
}

def run_final_nashua_report():
    header = {'User-Agent': 'Mozilla/5.0'}
    urgent_triggers = ['urgent', 'emergency', 'shortage', 'critically', 'priority', 'high need']
    
    print("🚀 NASHUA COMMUNITY NEEDS: FINAL VERIFIED REPORT\n")

    for name, info in SOURCES.items():
        print(f"📡 SOURCE: {name}")
        try:
            res = requests.get(info['url'], headers=header, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            if "wishlist" in res.text.lower():
                print("  [INFO] 🛒 Active Amazon Wishlist detected on site.")

            unique_items = {}

            for tag in soup.find_all(['li', 'p', 'span', 'strong', 'td']):
                txt = tag.get_text().strip()
                
                if any(k in txt.lower() for k in info['keys']):
                    if 3 < len(txt) < 95:
                        # Normalization: Treat '1' and 'one' the same to prevent duplicates
                        norm_txt = txt.lower().replace("  ", " ").replace("1 pound", "one pound")
                        
                        if norm_txt not in unique_items:
                            label = "[URGENTLY NEED]" if any(u in norm_txt for u in urgent_triggers) else "[NEED]"
                            unique_items[norm_txt] = f"  {label} {txt}"
            
            if unique_items:
                for item_display in sorted(unique_items.values()):
                    print(item_display)
            else:
                print("  ⚠️ No items found.")
                
        except Exception as e:
            print(f"  ❌ Connection Error: {e}")
        print("-" * 55)

    print("\n✅ DATA AGGREGATION COMPLETE. READY FOR PUBLIC DISTRIBUTION.")

if __name__ == "__main__":
    run_final_nashua_report()
  

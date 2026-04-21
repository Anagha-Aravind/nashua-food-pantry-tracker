import asyncio
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# --- THE MASTER REGISTRY ---
RESOURCES = {
    "Nashua Soup Kitchen & Shelter": {
        "type": "static",
        "url": "https://nsks.org/donate-goods/",
        "keys": ['cereal', 'rice', 'pasta', 'shampoo', 'diapers', 'tuna', 'beans', 'mac', 'cheese', 'razor', 'menstrual', 'toilet paper']
    },
    "Corpus Christi Food Pantry": {
        "type": "static",
        "url": "https://corpuschristifoodpantry.org/?page_id=1888",
        "keys": ['coffee', 'ketchup', 'spam', 'juice', 'tissues', 'detergent', 'flour', 'oil', 'ham', 'cracker', 'jelly', 'syrup']
    },
    "End 68 Hours of Hunger (Nashua)": {
        "type": "static", # Switched to static for better stability
        "url": "https://www.end68hoursofhunger.org/find-your-chapter/new-hampshire/nashua/",
        "contact": "Nashua@end68hoursofhunger.org",
        "keys": ["peanut butter", "jelly", "fluff", "canned soup", "mac & cheese", "fruit cups", "granola bars", "oatmeal"]
    },
    "Salvation Army Nashua": {
        "type": "dynamic",
        "url": "https://easternusa.salvationarmy.org/northern-new-england/nashua/alleviate-hunger/",
        "contact": "Amarilis (amarilis.dejesus@use.salvationarmy.org)",
        "keys": ["peanut butter", "jelly", "canned meats", "tuna", "cereal", "pasta", "rice", "toilet paper", "diapers"]
    },
    "Hudson Community Food Pantry": {
        "type": "static",
        "url": "https://www.hudsonfoodpantry.org/need-help",
        "keys": ["nonperishable", "meat", "dairy", "paper goods", "cleaning supplies", "hygiene"]
    },
    "Litchfield Community Church Pantry": {
        "type": "static",
        "url": "https://www.litchfieldcommunitychurchnh.com/food-pantry/",
        "keys": ["spaghetti sauce", "peanut butter", "jelly", "cereal", "peas", "corn", "carrots", "spam", "tuna"]
    },
    "Pilgrim Congregational Church": {
        "type": "static",
        "url": "https://pilgrimchurch.us/2024/04/09/food-pantry-needs-as-of-april-4-2024/",
        "keys": ["caprisun", "beef gravy", "v8", "beef broth", "salsa", "mayonnaise", "sugar", "coffee"]
    },
    "Grace Lutheran Church": {
        "type": "static",
        "url": "https://www.gracelutherannashua.org/FoodPantry",
        "keys": ["monetary", "gift cards", "market basket", "donations"]
    },
    "First Baptist Hudson": {"type": "manual", "contact": "Charlene (603-930-7336)", "note": "Contact for current backpack/pantry distribution gaps."},
    "First Church Nashua": {"type": "manual", "contact": "Dianne (dsmigliani@firstchurchnashua.org)", "note": "Coordinates outreach; check for seasonal food drives."},
    "Southern NH Rescue Mission": {"type": "manual", "contact": "Lloyd (director@hope4nashua.org)", "note": "Focus on men's toiletries, shelf-stable protein, and water."},
    "St. John Neumann": {"type": "manual", "contact": "Evelyn (sjnoutreach2@gmail.org)", "note": "Active local outreach; email for weekly high-priority items."},
    "Tolles Street Mission": {"type": "manual", "contact": "Maureen (603-820-1114)", "note": "Immediate inner-city needs; often needs canned meats and soups."},
    "St. James Methodist": {"type": "manual", "contact": "Lesley and Cheryl (mcfp646@gmail.com)", "note": "Check for community food program specific needs."},
    "Trinity Baptist": {"type": "manual", "contact": "Catherine (mightyvitamom@yahoo.com)", "note": "Contact for local pantry updates."}
}

URGENT_TRIGGERS = ['urgent', 'emergency', 'shortage', 'critically', 'priority', 'high need', 'running low']

async def run_unified_tracker():
    print("🚀 UNITED WAY GREATER NASHUA: UNIFIED COMMUNITY NEEDS REPORT")
    print("="*65)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])

        for name, data in RESOURCES.items():
            print(f"\n📡 SOURCE: {name}")

            if data['type'] == 'static':
                try:
                    res = requests.get(data['url'], timeout=15, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'})
                    soup = BeautifulSoup(res.text, 'html.parser')
                    unique_output = []
                    seen_items = set()

                    for tag in soup.find_all(['li', 'p', 'span', 'td']):
                        txt = tag.get_text().strip()
                        if any(k in txt.lower() for k in data['keys']):
                            if 3 < len(txt) < 95:
                                norm_txt = txt.lower().replace("one pound", "1 pound")
                                clean_key = "".join([c for c in norm_txt if not c.isdigit()]).strip()

                                if clean_key not in seen_items:
                                    label = "🚨 [URGENT]" if any(u in txt.lower() for u in URGENT_TRIGGERS) else "🛒 [NEED]"
                                    unique_output.append(f"  {label} {txt}")
                                    seen_items.add(clean_key)

                    if unique_output:
                        for item in sorted(unique_output): print(item)
                    else:
                        print("  ✅ No specific items listed today.")
                except Exception:
                    print(f"  ❌ Web Error: Source might be down.")

            elif data['type'] == 'dynamic':
                try:
                    context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
                    page = await context.new_page()
                    # wait_until="networkidle" is key for Salvation Army's slow site
                    await page.goto(data['url'], timeout=60000, wait_until="networkidle")

                    content = await page.content()
                    found_keywords = sorted(list(set([k for k in data['keys'] if k in content.lower()])))

                    if found_keywords:
                        for kw in found_keywords:
                            print(f"  🛒 [NEED] {kw.title()}")
                    else:
                        print("  ✅ No urgent keywords detected.")
                    await page.close()
                except Exception as e:
                    print(f"  ❌ Dynamic Error: System timed out.")

            elif data['type'] == 'manual':
                print(f"  📧 CONTACT: {data['contact']}")
                print(f"  📝 NOTE: {data['note']}")

        await browser.close()
    print("\n" + "="*65)
    print("✅ DATA AGGREGATION COMPLETE.")

await run_unified_tracker()

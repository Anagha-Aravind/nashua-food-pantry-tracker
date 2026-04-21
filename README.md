# 🚀 Nashua Community Needs Tracker

This is a project I built to help centralize information for food pantries and shelters in Nashua, NH. 

Right now, if you want to know what items are actually needed, you have to hunt through a dozen different websites or social media pages. This script handles the "hunting and gathering" for you, pulling everything into one clean report so it's easier to know what to pick up at the grocery store.

---

## 🛠️ How it works
Web data for nonprofits is usually pretty messy, so I designed this to be a **hybrid tracker** that handles data in three ways:

* **Static Scraping:** Grabs data from simple HTML pages using `BeautifulSoup`.
* **Dynamic Scraping:** Uses a "headless" browser (**Playwright**) to load more complex sites that require JavaScript to show their content.
* **Manual Registry:** For local missions that don't have a website, I built in a contact directory so the user knows exactly who to call.
* **Smart Cleaning:** I added logic to **deduplicate** items (like recognizing that "1 lb ham" and "One pound ham" are the same thing) to keep the list readable.

---

## 🚀 Getting Started

If you want to run this yourself, you'll need to set up the environment and the browser engine first.

### 1. Install the Python libraries
```bash
pip install playwright requests beautifulsoup4
```
### 2. Install the Browser engine
```bash
playwright install chromium
playwright install-deps chromium
```
### 📖 Usage
Once the setup is done, just run the script in your terminal:
```
python nashua_tracker.py
```
### 📡 Current Sources
The tracker is currently set up to monitor 15+ organizations including:
- Nashua Soup Kitchen & Shelter
- Corpus Christi Food Pantry
- Salvation Army Nashua
- End 68 Hours of Hunger
- Southern NH Rescue Mission

Various other local church pantries and missions.


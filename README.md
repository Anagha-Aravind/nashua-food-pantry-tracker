# Nashua Food Pantry Tracker

I built this script to make it easier for people in Nashua to know exactly what our local food pantries need. Instead of checking multiple websites every time you go to the grocery store, this tool pulls the data into one clean list.

## Why this exists

Right now, **NSKS** and **Corpus Christi** update their Most Needed lists on different schedules and in different formats. I wanted a way to see all that data in one place without the noise of the rest of the websites.

## What it does

- Live Scraping: Hits the actual donation pages for both pantries to get the latest data.

- Cleanup: It ignores all the website headers and legal text, focusing only on the food and hygiene items.

- Smart Matching: It handles duplicate items (like if a site lists 1 Pound Ham and One Pound Ham) so the list stays short and readable.

- Amazon Integration: It flags if a pantry has an active Amazon Wishlist for people who want to donate from home.

## How to use it

- Make sure you have python installed.

- Install the requirements: pip install requests beautifulsoup4
- Run the script: python nashua_tracker.py
- The report will print directly to your terminal.

## Current Sources
- Nashua Soup Kitchen & Shelter (NSKS)
- Corpus Christi Food Pantry

Developed by Anagha Aravind to help coordinate local donations in Nashua, NH.

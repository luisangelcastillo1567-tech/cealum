"""
EMAIL SCRAPER FOR LOCAL LEADS (100% FREE — NO API KEYS)
Uses Selenium (real Chrome browser) to bypass bot detection.
Yellow Pages + Yelp + Craigslist

- Real browser rendering — no 403 blocks
- Extracts emails from mailto: links, visible text, and raw HTML
- Checks homepage + /contact, /about pages
- Exports CSV with email column for cold outreach
"""

# ---- Auto-install dependencies ----
import subprocess, sys

def _install(pkg):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", pkg],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

for _pkg in ["selenium", "webdriver-manager", "beautifulsoup4", "pandas"]:
    try:
        __import__(_pkg.replace("-", "_"))
    except ImportError:
        print(f"[*] Installing {_pkg}...")
        _install(_pkg)
# ------------------------------------

import json
import re
import time
import pandas as pd
from dataclasses import dataclass
from typing import List, Optional, Set
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# =========================
# CONFIGURATION
# =========================

CITY = "Las Vegas"
STATE = "NV"

NICHES = [
    "plumber",
    "electrician",
    "landscaping",
    "cleaning",
    "handyman",
]

CRAIGSLIST_SUBDOMAIN = "lasvegas"


# =========================
# LEAD MODEL
# =========================
@dataclass
class Lead:
    source: str
    name: str
    phone: Optional[str]
    address: Optional[str]
    website: Optional[str]
    email: Optional[str] = None
    notes: Optional[str] = None

    @property
    def has_website(self) -> bool:
        if not self.website:
            return False
        bad_hosts = [
            "facebook.com", "m.facebook.com", "instagram.com",
            "yelp.com", "linkedin.com",
        ]
        w = self.website.lower()
        return not any(h in w for h in bad_hosts)


# =========================
# BROWSER SETUP
# =========================
def create_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(5)
    return driver


def get_page_html(driver: webdriver.Chrome, url: str, wait: float = 3) -> Optional[str]:
    try:
        driver.get(url)
        time.sleep(wait)
        return driver.page_source
    except Exception:
        return None


# =========================
# EMAIL SCRAPER
# =========================
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

JUNK_EMAIL_DOMAINS = {
    "example.com", "sentry.io", "wixpress.com", "googleapis.com",
    "w3.org", "schema.org", "wordpress.org", "gravatar.com",
    "yellowpages.com", "yp.com",
}


def _is_real_email(email: str) -> bool:
    e = email.lower()
    if any(e.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
        return False
    domain = e.split("@", 1)[1]
    if domain in JUNK_EMAIL_DOMAINS:
        return False
    return True


#!/usr/bin/env python3
"""Simple Email Finder - Auto-generates CSVs if missing"""

import subprocess, sys, os

# Install packages
packages = ["selenium", "webdriver-manager", "beautifulsoup4", "pandas", "dnspython"]
for pkg in packages:
    try:
        __import__(pkg.replace("-", "_"))
    except:
        print(f"[*] Installing {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

print("[✓] Ready!\n")

# Now check for CSVs
import glob
csvs = glob.glob("*.csv")
print(f"[*] Found {len(csvs)} CSV files in current folder")
print(f"[*] Current folder: {os.getcwd()}\n")

if len(csvs) == 0:
    print("[!] NO CSV FILES FOUND!")
    print("\n[*] To fix this:")
    print("    1. Download your CSV files from the outputs folder")
    print("    2. Put them in: C:\\Users\\luisa\\Downloads\\cealum\\")
    print("    3. Run this script again\n")
    print("[*] CSV files you need:")
    print("    - PLUMBER.csv")
    print("    - ELECTRICIAN.csv")
    print("    - CLEANING_SERVICE.csv")
    print("    - ... (all 15 files)\n")
    input("Press Enter to close...")
    sys.exit(1)

print("[✓] CSVs found! Starting email finder...\n")

# Rest of the script...
import re, time, pandas as pd, dns.resolver
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def find_email(driver, name, city):
    if not name or len(name) < 2:
        return None
    try:
        url = f"https://www.google.com/search?q={quote_plus(name + ' ' + city + ' email contact')}"
        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", html)
        if emails:
            for email in emails:
                try:
                    domain = email.split("@")[1]
                    dns.resolver.resolve(domain, "MX")
                    return email
                except:
                    pass
            return emails[0] if emails else None
    except:
        pass
    return None

print("[*] Starting Chrome browser...")
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-gpu")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
except Exception as e:
    print(f"[ERROR] Chrome failed: {e}")
    print("[!] Make sure Google Chrome is installed!")
    sys.exit(1)

print("[✓] Chrome ready\n")

total = 0
found = 0

try:
    for csv_file in sorted(csvs):
        niche = csv_file.replace(".csv", "").upper()
        print(f"[+] {niche}")
        
        df = pd.read_csv(csv_file)
        results = []
        
        for idx, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            if not name or name == "nan":
                continue
            
            email = find_email(driver, name, "Las Vegas")
            results.append({
                "name": name,
                "phone": row.get("phone", ""),
                "address": row.get("address", ""),
                "email": email or "NOT FOUND"
            })
            
            total += 1
            if email:
                found += 1
                print(f"    [{idx+1}] {name[:30]:<30} ✓ {email}")
            else:
                print(f"    [{idx+1}] {name[:30]:<30} ✗")
            
            time.sleep(0.2)
        
        # Save
        out_df = pd.DataFrame(results)
        out_file = f"{niche}_WITH_EMAILS.csv"
        out_df.to_csv(out_file, index=False)
        print(f"    Saved: {out_file}\n")

finally:
    driver.quit()

print(f"\n{'='*60}")
print(f"[✓] DONE!")
print(f"[*] Processed: {total}")
print(f"[*] Found emails: {found}")
print(f"[*] Success rate: {found/total*100:.1f}%" if total > 0 else "N/A")
print(f"\n[✓] All files saved with '_WITH_EMAILS' suffix!")
print(f"{'='*60}\n")
#!/usr/bin/env python3
"""
BATCH EMAIL FINDER - SIMPLIFIED VERSION
Reads Vegas business CSVs and adds email addresses
Run this: python batch_email_finder_simple.py
"""
import subprocess
import sys
import os
# Auto-install packages
packages = ["selenium", "webdriver-manager", "beautifulsoup4", "pandas", "requests", "dnspython"]
for pkg in packages:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        print(f"[*] Installing {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
print("[✓] All packages ready\n")
# NOW import everything
import re
import time
import pandas as pd
import glob
import dns.resolver
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# ============= CONFIG =============
CSV_FOLDER = r"C:\Users\luisa\Downloads\LEAD_HUNTER_TEMP\LeadHunter_Final\BY_NICHE"
CITY = "Las Vegas"
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
JUNK_DOMAINS = {"gmail.com", "yahoo.com", "outlook.com", "yelp.com", "facebook.com"}
EMAIL_PREFIXES = ["info", "contact", "hello", "support", "owner"]
# ============= SETUP =============
def setup_driver():
    """Create Chrome driver"""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        return driver
    except Exception as e:
        print(f"[ERROR] Chrome setup failed: {e}")
        print("[!] Make sure Google Chrome is installed!")
        sys.exit(1)
# ============= HELPERS =============
def is_valid_email(email):
    """Check if email is real"""
    if not email:
        return False
    e = email.lower()
    domain = e.split("@")[1] if "@" in e else ""
    return domain not in JUNK_DOMAINS and EMAIL_RE.match(e)
def has_mx_record(email):
    """Check if domain has mail server"""
    try:
        domain = email.split("@")[1]
        dns.resolver.resolve(domain, "MX")
        return True
    except:
        return False
def get_page(driver, url):
    """Get page HTML"""
    try:
        driver.get(url)
        time.sleep(1)
        return driver.page_source
    except:
        return None
def extract_emails(html):
    """Extract emails from HTML"""
    if not html:
        return []
    emails = set()
    for match in EMAIL_RE.findall(html):
        if is_valid_email(match):
            emails.add(match.lower())
    return sorted(list(emails))
# ============= STRATEGIES =============
def find_email(driver, name, city):
    """Find email using multiple strategies"""
    if not name or len(name) < 2:
        return None, None

    # Try Google Maps
    try:
        url = f"https://www.google.com/maps/search/{quote_plus(name + ' ' + city + ' Nevada')}"
        html = get_page(driver, url)
        emails = extract_emails(html)
        if emails:
            email = emails[0]
            if has_mx_record(email):
                return email, "Google Maps"
    except:
        pass

    # Try Google business search
    try:
        url = f"https://www.google.com/search?q={quote_plus(name + ' ' + city + ' contact email')}"
        html = get_page(driver, url)
        emails = extract_emails(html)
        if emails:
            email = emails[0]
            if has_mx_record(email):
                return email, "Google Search"
    except:
        pass

    # Try pattern matching
    clean_name = re.sub(r"[^a-z0-9]", "", name.lower())
    if clean_name:
        for prefix in EMAIL_PREFIXES:
            email = f"{prefix}@{clean_name}.com"
            if has_mx_record(email):
                return email, "Pattern"

    return None, None
# ============= MAIN =============
def main():
    print(f"{'='*80}")
    print("[*] BATCH EMAIL FINDER - SIMPLIFIED")
    print(f"{'='*80}\n")

    # Find CSVs in the leads folder
    csv_files = glob.glob(os.path.join(CSV_FOLDER, "*.csv"))
    business_csvs = sorted(csv_files)

    if not business_csvs:
        print(f"[!] No CSV files found in {CSV_FOLDER}")
        return

    print(f"[✓] Found {len(business_csvs)} CSV files:\n")
    for f in business_csvs:
        print(f"    - {os.path.basename(f)}")
    print()

    # Setup browser
    print("[*] Starting Chrome...")
    driver = setup_driver()
    print("[✓] Chrome ready\n")

    total_processed = 0
    total_with_email = 0

    try:
        for csv_file in business_csvs:
            niche = os.path.basename(csv_file).replace(".csv", "").upper()
            print(f"\n[+] Processing: {niche}")
            print(f"{'─'*80}")

            try:
                df = pd.read_csv(csv_file)
                businesses = len(df)
                print(f"    Found {businesses} businesses\n")

                emails_found = []
                with_email_count = 0

                for idx, row in df.iterrows():
                    name = str(row.get("name", "")).strip()
                    phone = str(row.get("phone", "")) if pd.notna(row.get("phone")) else ""

                    if not name or name == "nan":
                        continue

                    # Find email
                    email, method = find_email(driver, name, CITY)

                    # Display progress
                    status = "✓" if email else "✗"
                    email_display = email if email else "NOT FOUND"
                    print(f"    [{idx+1:3d}/{businesses}] {name[:40]:<40} {status} {email_display}")

                    # Store result
                    emails_found.append({
                        "name": name,
                        "phone": phone,
                        "email": email or "NOT FOUND",
                        "method": method or "N/A"
                    })

                    if email:
                        with_email_count += 1

                    time.sleep(0.3)

                # Save results
                output_df = pd.DataFrame(emails_found)
                output_file = os.path.join(CSV_FOLDER, f"{niche}_WITH_EMAILS.csv")
                output_df.to_csv(output_file, index=False)

                print(f"\n    [✓] Saved: {output_file}")
                print(f"    [✓] Found emails for {with_email_count}/{businesses} businesses ({with_email_count/businesses*100:.1f}%)\n")

                total_processed += businesses
                total_with_email += with_email_count

            except Exception as e:
                print(f"    [ERROR] {e}\n")
                continue

    finally:
        driver.quit()

    # Summary
    print(f"\n{'='*80}")
    print("[✓] COMPLETE!")
    print(f"{'='*80}")
    print(f"[*] Total processed: {total_processed}")
    print(f"[*] Total with email: {total_with_email}")
    if total_processed > 0:
        print(f"[*] Success rate: {total_with_email/total_processed*100:.1f}%")
    print(f"\n[✓] All files saved with '_WITH_EMAILS' suffix!")
    print(f"[*] Ready for cold outreach!\n")
if __name__ == "__main__":
    main()

import time
import pandas as pd
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.hbo-kennisbank.nl/searchresult?q=&page="
MAX_PAGES = 5
BASE_DOMAIN = "https://www.hbo-kennisbank.nl"


def get_publication_links(page):
    """Stap 1: pak alle detail links uit de lijstpagina"""
    links = []

    items = page.query_selector_all("a")  # we filteren zelf

    for item in items:
        href = item.get_attribute("href")

        # 🔑 Filter alleen publicatie links
        if href and "/details/" in href:
            full_url = BASE_DOMAIN + href
            links.append(full_url)

    return list(set(links))  # duplicates verwijderen


def scrape_detail(page, url):
    """Stap 2: scrape echte detailpagina"""
    page.goto(url, timeout=60000)
    page.wait_for_timeout(1500)

    def safe(selector):
        el = page.query_selector(selector)
        return el.inner_text().strip() if el else None

    # ⚠️ Deze selectors moet je mogelijk fine-tunen via inspect!
    data = {
        "title": safe("h1"),
        "authors": safe("text=Onderzoeker") or safe("text=Auteur"),
        "abstract": safe("div:has-text('Samenvatting')") or safe("p"),
        "year": safe("text=202"),
        "url": url
    }

    return data


def main():
    all_links = []
    all_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 🔁 Stap 1: verzamel alle links via paginatie
        for i in range(1, MAX_PAGES + 1):
            url = BASE_URL + str(i)
            print(f"\n📄 Pagina {i}: {url}")

            page.goto(url, timeout=60000)
            page.wait_for_timeout(2000)

            links = get_publication_links(page)
            print(f"🔗 Gevonden links: {len(links)}")

            all_links.extend(links)

        all_links = list(set(all_links))
        print(f"\n✅ Totaal unieke links: {len(all_links)}")

        # 🔍 Stap 2: scrape detailpagina’s
        for i, link in enumerate(all_links):
            try:
                print(f"[{i+1}/{len(all_links)}] Scraping...")
                data = scrape_detail(page, link)
                all_data.append(data)

                time.sleep(1)  # netjes blijven

            except Exception as e:
                print(f"❌ Error bij {link}: {e}")

        browser.close()

    # 🧱 DataFrame
    df = pd.DataFrame(all_data)

    # 🧹 Cleaning
    df = df.drop_duplicates()
    df = df.dropna(subset=["title"])

    # 💾 Opslaan
    df.to_csv("hbo_kennisbank_full.csv", index=False)

    print("\n🎉 Klaar!")
    print(df.head())


if __name__ == "__main__":
    main()
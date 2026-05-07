import re
import time
import pandas as pd
from playwright.sync_api import sync_playwright

BASE_DOMAIN = "https://hbo-kennisbank.nl"

# 🔍 meerdere zoekthema's voor grotere dataset
SEARCH_TERMS = [
    "data",
    "dashboard",
    "zorg",
    "ict",
    "onderwijs",
    "ai",
    "duurzaamheid"
]

MAX_PAGES_PER_QUERY = 20

all_publication_links = set()
all_records = []


def extract_publication_links(page):
    """
    Pak ALLE unieke detailpagina links
    """

    links = set()

    anchors = page.query_selector_all("a")

    for a in anchors:
        href = a.get_attribute("href")

        if href:

            # 🔑 detailpagina patroon
            if "/details/" in href:

                # absolute url maken
                if href.startswith("/"):
                    href = BASE_DOMAIN + href

                links.add(href)

    return links


def clean_text(text):
    if not text:
        return None

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def safe_text(page, selector):
    try:
        el = page.query_selector(selector)

        if el:
            return clean_text(el.inner_text())

    except:
        return None

    return None


def scrape_detail_page(page, url):

    page.goto(url, timeout=60000)

    page.wait_for_timeout(1500)

    title = safe_text(page, "h1")

    # 🔥 robuustere extraction
    paragraphs = page.query_selector_all("p")

    all_p = []

    for p in paragraphs:

        txt = clean_text(p.inner_text())

        if txt and len(txt) > 80:
            all_p.append(txt)

    abstract = " ".join(all_p[:3])

    data = {
        "title": title,
        "abstract": abstract,
        "url": url
    }

    return data


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    # ==================================================
    # STAP 1 — ALLE DETAIL LINKS VERZAMELEN
    # ==================================================

    for term in SEARCH_TERMS:

        print(f"\n🔎 Zoekterm: {term}")

        for page_num in range(1, MAX_PAGES_PER_QUERY + 1):

            search_url = (
                f"https://hbo-kennisbank.nl/searchresult?"
                f"q={term}&page={page_num}"
            )

            print(f"📄 Pagina {page_num}")

            page.goto(search_url, timeout=60000)

            page.wait_for_timeout(2000)

            links = extract_publication_links(page)

            before = len(all_publication_links)

            all_publication_links.update(links)

            after = len(all_publication_links)

            print(
                f"Nieuwe links: {after-before} | "
                f"Totaal: {after}"
            )

            # 🛑 stop als pagina leeg raakt
            if len(links) == 0:
                print("Geen nieuwe resultaten meer")
                break

            time.sleep(1)

    print("\n==========================")
    print(f"TOTAAL LINKS: {len(all_publication_links)}")
    print("==========================")

    # ==================================================
    # STAP 2 — DETAILPAGINA'S SCRAPEN
    # ==================================================

    for idx, link in enumerate(all_publication_links):

        try:

            print(
                f"[{idx+1}/{len(all_publication_links)}]"
            )

            record = scrape_detail_page(page, link)

            all_records.append(record)

            time.sleep(0.5)

        except Exception as e:

            print(f"❌ Error: {e}")

    browser.close()

# ==================================================
# STAP 3 — DATAFRAME
# ==================================================

df = pd.DataFrame(all_records)

# cleaning
df = df.drop_duplicates(subset=["url"])

df = df[df["title"].notna()]

df = df[df["abstract"].str.len() > 50]

print("\nDATAFRAME SHAPE:")
print(df.shape)

# ==================================================
# OPSLAAN
# ==================================================

df.to_csv(
    "hbo_kennisbank_full.csv",
    index=False
)

print("\n✅ CSV opgeslagen")
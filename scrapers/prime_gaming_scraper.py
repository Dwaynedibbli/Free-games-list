from playwright.sync_api import sync_playwright

def scrape_prime():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/132.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        
        page.goto("https://gaming.amazon.com/home")
        page.wait_for_timeout(7000)
        
        try:
            page.click("div[data-a-target='cookie-policy-banner'] button", timeout=5000)
        except Exception:
            pass
        page.wait_for_timeout(3000)
        
        try:
            page.click(".offer-filters__button__title--Game")
        except Exception as e:
            print("Error clicking Free Games tab:", e)
        page.wait_for_timeout(7000)
        
        scroll_height = page.evaluate("document.body.scrollHeight")
        attempts = 0
        max_attempts = 10
        while attempts < max_attempts:
            page.keyboard.press("PageDown")
            page.wait_for_timeout(2000)
            new_scroll_height = page.evaluate("document.body.scrollHeight")
            if new_scroll_height > scroll_height:
                scroll_height = new_scroll_height
                attempts = 0
            else:
                attempts += 1
        
        anchors = page.query_selector_all("a[data-a-target='learn-more-card']")
        print("Total learn-more-card anchors found:", len(anchors))
        
        valid_games = []
        for a in anchors:
            if not a.is_visible():
                continue

            title = a.get_attribute("aria-label")
            link = a.get_attribute("href")

            if not link:
                continue

            # 🔧 ALWAYS normalize claims URLs (absolute or relative)
            # e.g. "/claims/gunslugs-gog/dp/..." -> "/gunslugs-gog/dp/..."
            #      "https://gaming.amazon.com/claims/..." -> "https://gaming.amazon.com/..."
            link = link.replace("/claims/", "/")

            # If the link is relative, prepend the domain
            if not link.startswith("http"):
                link = "https://gaming.amazon.com" + link

            has_claim = a.evaluate(
                """(el) => {
                    const block = el.closest('.tw-block');
                    if (!block) return false;
                    const claimBtn = block.querySelector('.item-card__claim-button');
                    if (!claimBtn) return false;
                    return claimBtn.innerText.toLowerCase().includes("claim game");
                }"""
            )
            if not has_claim:
                continue

            if title and link:
                valid_games.append({
                    "title": title.strip(),
                    "link": link.strip()
                })
        
        browser.close()
        return valid_games

if __name__ == "__main__":
    games = scrape_prime()
    print("Total valid free games found:", len(games))
    for idx, game in enumerate(games, start=1):
        print(f"{idx}. {game['title']} - {game['link']}")

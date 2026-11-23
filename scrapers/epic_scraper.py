"""Epic Games Store limited-time giveaways (not permanently free games)."""
from datetime import datetime, timezone
from urllib.parse import quote
import requests

API_URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
STORE_URL = "https://store.epicgames.com/en-US"


def _active_giveaway(element, now):
    promotions = (element.get("promotions") or {}).get("promotionalOffers") or []
    for group in promotions:
        for offer in group.get("promotionalOffers") or []:
            discount = offer.get("discountSetting") or {}
            if discount.get("discountPercentage") != 0:
                continue
            try:
                start = datetime.fromisoformat(offer["startDate"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(offer["endDate"].replace("Z", "+00:00"))
            except (KeyError, TypeError, ValueError):
                continue
            if start <= now < end:
                return True
    return False


def _store_link(element):
    mappings = element.get("catalogNs", {}).get("mappings") or []
    mappings += element.get("offerMappings") or []
    slugs = [m.get("pageSlug") for m in mappings if m.get("pageSlug")]
    if element.get("productSlug"):
        slugs.append(element["productSlug"])
    for slug in slugs:
        slug = slug.strip("/")
        if not slug:
            continue
        if slug.startswith(("http://", "https://")):
            return slug
        if slug.startswith(("p/", "bundles/")):
            return f"{STORE_URL}/{slug}"
        if slug.startswith("home/"):
            continue
        return f"{STORE_URL}/p/{slug}"
    return None


def scrape_epic():
    try:
        response = requests.get(
            API_URL,
            params={"locale": "en-US", "country": "US", "allowCountries": "US"},
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        elements = payload["data"]["Catalog"]["searchStore"]["elements"]
    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        print(f"Epic API error: {exc}")
        return []

    now = datetime.now(timezone.utc)
    games = []
    seen = set()
    for element in elements:
        title = element.get("title")
        price = ((element.get("price") or {}).get("totalPrice") or {})
        original = price.get("originalPrice")
        current = price.get("discountPrice")
        if not title or not isinstance(original, (int, float)) or original <= 0:
            continue  # Exclude permanently free / freemium titles
        if current != 0 or not _active_giveaway(element, now):
            continue
        link = _store_link(element)
        if not link or link in seen:
            continue
        seen.add(link)
        games.append({"title": title, "link": link})
        print(f"Epic giveaway: {title} | {link}")
    print(f"Epic giveaways found: {len(games)} (API entries: {len(elements)})")
    return games


if __name__ == "__main__":
    scrape_epic()

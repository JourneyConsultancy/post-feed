#!/usr/bin/env python
import json, requests, pathlib

API = "https://orlyvlot.nl/wp-json/wp/v2/posts"
PER_PAGE = 100

def all_wp_urls():
    page, urls = 1, []
    while True:
        r = requests.get(API, params={"per_page": PER_PAGE, "page": page}, timeout=30)
        if r.status_code == 400 and page > 1:
            error = r.json()
            if isinstance(error, dict) and error.get("code") == "rest_post_invalid_page_number":
                break
        r.raise_for_status()
        posts = r.json()
        if not posts:
            break
        urls += [p["link"] for p in posts]
        page += 1
    return urls

# schrijf het bestand in de root ( NIET in een map )
feed = {"urls": all_wp_urls()}
with open("posts.json", "w", encoding="utf-8") as output:
    json.dump(feed, output, indent=2)


import requests
from bs4 import BeautifulSoup
import time
import json

BASE_URL = "https://medlineplus.gov"
START_URL = f"{BASE_URL}/lab-tests/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_test_links():
  res = requests.get(START_URL, headers=HEADERS)
  soup = BeautifulSoup(res.text, "html.parser")
  links = []
  for a in soup.select("ul.alpha-links a"):
    page = requests.get(START_URL+a["href"], headers=HEADERS)
    page_soup = BeautifulSoup(page.text, "html.parser")
    for test_link in page_soup.select("div.section-body a"):
      test_url = test_link["href"]
      if "/lab-tests/" in test_url and test_url not in links:
        links.append(test_url)
      if len(links) > 1000:
          break
    if len(links) > 1000:
      break
  with open("medlineplus_lab_tests_links.json", "w") as f:
        json.dump(links, f, indent=2)
  return list(set(links))


def extract_info(url):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("h1").get_text(strip=True)
        description = ""
        div = soup.find("div", class_="mp-content")
        if div:
            paras = div.find_all("p")
            for p in paras:
                description += p.get_text(strip=True)
        else:
            print("div.mp-content not found")
        

        meaning_section = soup.find('h2', string=lambda t: t and "results mean" in t.lower())
        explanation = ""
        if meaning_section:
            for sibling in meaning_section.find_next_siblings():
                if sibling.name == 'h2': break
                explanation += sibling.get_text(" ", strip=True) + " "

        return {
            "name": title,
            "url": url,
            "description": description,
            "explanation": explanation.strip()
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    links = get_test_links()
    print(f"Found {len(links)} lab test pages.")
    results = []
    for i, url in enumerate(links):
        print(f"[{i+1}/{len(links)}] Scraping {url}")
        data = extract_info(url)
        if data and data["explanation"]:
            results.append(data)

    with open("medlineplus_lab_tests.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Saved medlineplus_lab_tests.json with", len(results), "entries.")

if __name__ == "__main__":
   main()
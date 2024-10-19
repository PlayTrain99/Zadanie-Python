import requests
from bs4 import BeautifulSoup
import json

# Funkcja do scrapowania artykułu
def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = "Brak tytułu"
    title = soup.find('title').text

    category = "Brak kategorii"
    date = "Brak daty"

    # Informacjie w skryptach ld+json
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:

        json_data = json.loads(script.string)

        # Sprawdzanie kategorii w 'articleSection' lub 'keywords'
        if '@graph' in json_data:
            for item in json_data['@graph']:
                if 'articleSection' in item:
                    category = item['articleSection']
                elif 'keywords' in item:
                    category = item['keywords']
        elif 'articleSection' in json_data:
            category = json_data['articleSection']
        elif 'keywords' in json_data:
            category = json_data['keywords']

        # Sprawdzanie daty w 'datePublished'
        if '@graph' in json_data:
            for item in json_data['@graph']:
                if 'datePublished' in item:
                    date = item['datePublished']
        elif 'datePublished' in json_data:
            date = json_data['datePublished']

    allowed_tags = ['h2', 'h3', 'p', 'strong']
    content = ''
    for tag in soup.find_all(allowed_tags):
        content += f" {tag} \n "

    return {
        'url': url,
        'title': title,
        'category': category,
        'date': date,
        'content': content
    }

urls = [
    "https://bistrolubie.pl/pierniki-z-miodem-tradycyjny-przepis-na-swiateczne-ciasteczka-pelne-aromatu",
    "https://bistrolubie.pl/piernik-z-mascarpone-kremowy-i-pyszny-przepis-na-deser-idealny-na-swieta",
    "https://spidersweb.pl/2024/07/metamorfoza-w-centrum-warszawy.html",
    "https://spidersweb.pl/2024/07/kontrolery-na-steam-rosnie-popularnosc.html",
    "https://www.chip.pl/2024/06/wtf-obalamy-mity-poprawnej-pozycji-przy-biurku",
    "https://www.chip.pl/2024/07/sony-xperia-1-vi-test-recenzja-opinia",
    "https://newonce.net/artykul/chief-keef-a-sprawa-polska-opowiadaja-benito-gicik-crank-all",
    "https://newonce.net/artykul/glosna-gra-ktorej-akcja-toczy-sie-w-warszawie-1905-roku-gralismy-w-the-thaumaturge"
]

# Prazygotowywanie pliku .json
results = []
for url in urls:
    result = scrape_article(url)
    results.append(result)

with open('response.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print("Dane zostały zapisane do pliku response.json")

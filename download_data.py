import cloudscraper

def download_data(row_number: int):
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
    data_url = f'https://www6.ohiosos.gov/ords/f?p=VOTERFTP:DOWNLOAD::FILE:NO:2:P2_PRODUCT_NUMBER:{row_number}'
    response = scraper.get(data_url).text

    with open(f'county_voter_data/county_voter_data_{row_number}.csv', 'w') as f:
        f.write(response)

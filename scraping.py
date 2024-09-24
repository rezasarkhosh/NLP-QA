from bs4 import BeautifulSoup
import requests
import time

def scrape_BTC(page_number, f):
    url = f'https://www.tradingview.com/symbols/BTCUSDT/ideas/page-{page_number}/?exchange=BINANCE'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")  
    articles = soup.find_all('article', class_='card-exterior-Us1ZHpvJ card-AyE8q7_6 stretch-link-title-AyE8q7_6 idea-card-R05xWTMw js-userlink-popup-anchor')
    
    for index, article in enumerate(articles):
        description = article.find('span', class_='line-clamp-content-t3qFZvNN')
        if description:  
            f.write(f"{description.text.strip()}\n")
            f.write("___\n")
    
    print(f"Page {page_number} for BTC saved")



def scrape_ETH(page_number, f):
    url = f'https://www.tradingview.com/symbols/ETHUSDT/ideas/page-{page_number}/?exchange=BINANCE'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    analysis= soup.find_all('article', class_='card-exterior-Us1ZHpvJ card-AyE8q7_6 stretch-link-title-AyE8q7_6 idea-card-R05xWTMw js-userlink-popup-anchor')

    for index, article in enumerate(analysis):
        description = article.find('span', class_='line-clamp-content-t3qFZvNN')
        if description:
            f.write(f"{description.text.strip()}\n")
            f.write("___\n")

    print(f"Page{page_number} for ETH saved")
    






def scrape_all_pages(total_pages):
    with open('data/BTC.txt', 'w') as f:
        for page in range(1, total_pages + 1):
            scrape_BTC(page, f)
            time_var = 2  
            print(f'BTC: Waiting {time_var} seconds before the next request...')
            time.sleep(time_var)


    with open('data/ETH.txt', 'w') as f:
        for page in range(1, total_pages+1):
            scrape_ETH(page, f)
            time_var= 2
            print(f'ETH: Waiting {time_var} seconds before the next request...')
            time.sleep(time_var)



        

if __name__ == '__main__':
    total_pages = 42 
    scrape_all_pages(total_pages)


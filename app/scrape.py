from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import yfinance as yf
from app import cache
import os 

########################################################## Ether ###############################################################
@cache.memoize(86400)
def get_eth_assets(date):
    print("Getting ETH Assets")
    url = 'https://etherscan.io/address/0x6B6372D6d785752688461cB41b08D155914f42D7'

    req = Request(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})   # I got this line from another post since "uClient = uReq(URL)" and "page_html = uClient.read()" would not work (I beleive that etherscan is attemption to block webscraping or something?)
    response = urlopen(req, timeout=20).read()
    response_close = urlopen(req, timeout=20).close()
    page_soup = soup(response, "html.parser")
    # print(page_soup)
    alloc_table = page_soup.find("div", {"class": "card-body"})
    assets = alloc_table.findAll("span",  {"class": "d-md-none d-lg-inline-block mr-1"})
    values = alloc_table.findAll("div", {"class": "col-md-8"})
    assets = [x.text for x in assets]
    values = [x.text for x in values if x.text[0] == '$']
    values = str(values)
    values = values.split(" ")
    values[0] = values[0].replace("[", '')
    values[0] = values[0].replace("'", '')
    values[0] = values[0].replace("$", '')

    eth_assets = {}
    for i in range(len(assets)):
        if assets[i] == "Ether":
            assets[i] = "ETH"

        eth_assets[assets[i]] = values[i]
    print("Done")
    return eth_assets

########################################################## Solana ###############################################################
@cache.memoize(86400)
def get_sol_assets(date):
    print("Getting SOL Assets")
    url = 'https://solscan.io/account/9zQQvGgDNF57Givi2AVLpaydWNPYgmQhDkxZsxnc3hNj'
    mode = "windows"
    if mode == "heroku":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
    '/html/body/div[1]/section/main/div/div[2]/div/div[1]/div/div[2]/div[3]')))
    dropdown = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/div/div[1]/div/div[2]/div[3]')
    dropdown.click()

    html = driver.page_source
    # print(html)
    soup_ = soup(html, "lxml")
    # print(soup_)

    sol = soup_.findAll("div", {"class" : "ant-col ant-col-24 ant-col-md-16"})
    coins = soup_.findAll("div", {"class" : "ReactVirtualized__Grid__innerScrollContainer"})

    coins = [x.text for x in coins]
    coins = coins[0].split()
    num_w_nfts = len(coins)
    coins = [x for x in coins if '$' in x]
    num_nfts = num_w_nfts - len(coins)

    coins = [x.split("$") for x in coins]

    coins = [[x[0], x[2]] for x in coins]

    # print(coins)


    solana_assets = {}
    for coin in coins:
        solana_assets[coin[0]] = coin[1]
    solana_assets["NFTS"] = "N/A"
    print("Done")
    return solana_assets

########################################################## RONIN ###############################################################
@cache.memoize(86400)
def get_ronin_assets(date):
    print("Getting RONIN Assets")
    url = 'https://explorer.roninchain.com/address/ronin:43229ad2bc430a476492341d47efb7baf5e33b5b'

    req = Request(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})   # I got this line from another post since "uClient = uReq(URL)" and "page_html = uClient.read()" would not work (I beleive that etherscan is attemption to block webscraping or something?)
    response = urlopen(req, timeout=20).read()
    response_close = urlopen(req, timeout=20).close()
    page_soup = soup(response, "html.parser")

    
    networth = page_soup.find_all('div', {"class" : "text-12"})
    networth = [x.text for x in networth if "USD" in x.text]
    networth = networth[0].split()[-2]
    

    df = yf.download("ETH-USD")
    latest_eth = df["Close"][-1]



    assets = page_soup.findAll("div", {"class" : "lg:w-1/4 w-full flex items-center mt-20 mb-8"})
    assets = [x.text for x in assets]
    
    ronin_assets = {}
    for asset in assets:
        split = asset.split()
        ronin_assets[split[1]] = split[0]

    
    try:
        weth_value = latest_eth*float(ronin_assets["WETH"])
        ronin_assets["WETH"] = round(weth_value, 2)

        ronin_assets["SLP"] = round(float(networth) - ronin_assets["WETH"], 2)

    except:
        pass
    ronin_assets["AXIE"] = "N/A"
    
    print("Done")
    return ronin_assets


# print("-----------------------------------------------")
# print(eth_assets)
# print(solana_assets)
# print(ronin_assets)
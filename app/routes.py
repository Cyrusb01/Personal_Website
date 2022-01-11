from flask import render_template
from datetime import datetime
from app import app
from app.scrape import get_eth_assets, get_ronin_assets, get_sol_assets



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/portfolio')
def portfolio():
    #Connect to the sheet and pull all the data in once a day
    today = datetime.now().strftime('%Y/%m/%d')
    sol_assets = get_sol_assets(today)
    eth_assets = get_eth_assets(today)
    ronin_assets = get_ronin_assets(today)
    ronin_assets["SLP"] = ronin_assets["SLP"] / 100

    


    sol_tickers = list(sol_assets.keys())
    eth_tickers = list(eth_assets.keys())
    ronin_tickers = list(ronin_assets.keys())


    sol_allocs = list(sol_assets.values())
    eth_allocs = list(eth_assets.values())
    ronin_allocs = list(ronin_assets.values())

    all_allocs = sol_allocs + eth_allocs + ronin_allocs
    all_tickers = sol_tickers + eth_tickers + ronin_tickers

    sum = 0
    for alloc in all_allocs:
        try: #NFTS have the value N/A 
            sum += float(alloc)
        except:
            pass
    
    pie_data = []
    for i in range(len(all_allocs)):
        pie_dict = {}
        try:
            print(all_allocs[i])
            float(all_allocs[i])
            pie_dict["name"] = all_tickers[i]
            pie_dict["y"] = (float(all_allocs[i])/sum)*100
            pie_data.append(pie_dict)
        except: #When its an NFT
            pass
    
    print(pie_data)


    

    # pie_data =  [ {"name": 'BTC', "y": 61.41}, { "name": 'ETH', "y": 11.84}]
    
    


    return render_template("portfolio.html", 
                            pie_data = pie_data, 

                            eth_l = len(eth_tickers), 
                            eth_tickers = eth_tickers, 

                            sol_l = len(sol_tickers), 
                            sol_tickers = sol_tickers,

                            ronin_l = len(ronin_tickers), 
                            ronin_tickers = ronin_tickers)

@app.route('/trading')
def trading():
    return render_template("trading.html")

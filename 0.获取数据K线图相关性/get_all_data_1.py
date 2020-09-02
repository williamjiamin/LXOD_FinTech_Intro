import bs4 as bs
import pickle
import os
import tushare as ts

ts.set_token('c6099879c49405f61a6da60a910151113c29c9928a40feb5f0f503bd')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20180101', end_date='20181118')
print(df)


#def find_and_save_CSI_300():
#    response = requests.get('https://en.wikipedia.org/wiki/CSI_300_Index')
#    soup = bs.BeautifulSoup(response.text, 'lxml')
#    table = soup.find('table', {'class': 'wikitable sortable'})
#    tickers = []
#    for row in table.findAll('tr')[1:]:
#        ticker = row.findAll('td')[0].text
#        ticker = ticker[:6]
#        tickers.append(ticker)
#        
#    with open("CSI_tickers.pickle","wb") as f:
#        pickle.dump(tickers,f)
#    print(tickers)
#    return tickers
#
#find_and_save_CSI_300()

def find_and_save_CSI_300():
    CSI_300_df=ts.get_hs300s()
    tickers=CSI_300_df['code'].values
#    print(tickers)
    tickers_mod=[]
    for ticker in tickers:
        if ticker[0] == '6':
            ticker=ticker+'.SH'
            tickers_mod.append(ticker)
        else:
            ticker=ticker+'.SZ'
            tickers_mod.append(ticker)
#    print(tickers_mod)           
    with open("CSI_tickers.pickle","wb") as f:
        pickle.dump(tickers_mod,f)
    return tickers_mod
        
find_and_save_CSI_300()

def get_data_from_tushare(reload_CSI_300=False):
    if reload_CSI_300:
        tickers_mod = find_and_save_CSI_300()
    else:
        with open("CSI_tickers.pickle", "rb") as f:
            tickers_mod = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    for ticker_mod in tickers_mod:
        print(ticker_mod)
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker_mod)):
            df = pro.daily(ts_code=str(ticker_mod), start_date='20180101', end_date='20181118')
            df.reset_index(inplace=True)
            df.set_index("trade_date", inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker_mod))
        else:
            print('Already have {}'.format(ticker_mod))


get_data_from_tushare()
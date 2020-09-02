import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Choose the stock you like~ Selected Stock~~~~ Whoooo~~
tickers = ['000001.SZ','000002.SZ','000060.SZ','000503.SZ','002241.SZ']


#Put all selected stock into one dataframe

def put_some_stock_price_into_one_df():
    some_stock_price_df=pd.DataFrame
#    print(some_stock_price_df)
        
    for count , ticker in enumerate(tickers):
        df=pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('trade_date',inplace=True)
        
        df.rename(columns={'close':ticker},inplace=True)
        df.drop(['index','ts_code','open','high','low','pre_close',
                 'change','pct_chg','vol','amount'],1,inplace=True)
        
        if some_stock_price_df.empty:
            some_stock_price_df=df
        else:
            some_stock_price_df=some_stock_price_df.join(df,how='outer')
#        print(count)
#    print(all_stock_price_df.head())
    some_stock_price_df.to_csv('CSI_selected_closes.csv')

put_some_stock_price_into_one_df()


#Make data clean and beautiful. (*Think)  
df=pd.read_csv('CSI_selected_closes.csv')
df=df.set_index('trade_date')
df=df.dropna()
#print(df)


#The basic financal calculation(*Think)

returns_daily=df.pct_change()
returns_annual=returns_daily.mean()*250
#print(returns_annual)

cov_daily=returns_daily.cov()
#print(cov_daily)
cov_annual=cov_daily*250
#print(cov_annual)

portfolio_return=[]
portfolio_volatility=[]
stock_weights=[]


#Make Portfolio
num_assets= len(tickers)
num_portfolio = 10000

for single_portfolio in range(num_portfolio):
    weights= np.random.random(num_assets)
#    print(weights)
    weights/= np.sum(weights)
#    print(weights)
    returns = np.dot(weights , returns_annual)
#    print(returns)
    volatility = np.sqrt(np.dot(np.dot(weights,cov_annual),weights.T))
#    print(volatility)
    portfolio_return.append(returns)
    portfolio_volatility.append(volatility)
    stock_weights.append(weights)
    
#print(portfolio_return)
#print(portfolio_volatility)
#print(stock_weights)


#Make the selected Super Portfolio into one dataframe

portfolio={'Return':portfolio_return,
           'volatility':portfolio_volatility}

for counter , ticker in enumerate(tickers):
    portfolio[ticker+' Weight'] = [Weight[counter] for Weight in stock_weights]

df=pd.DataFrame(portfolio)
#print(df.head())
df.to_csv('big_big_data.csv')

plt.style.use('seaborn')
df.plot.scatter(x='volatility', y='Return' ,figsize=(10,8) ,grid=True)
plt.xlabel('volatility / Std Deviation')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')




















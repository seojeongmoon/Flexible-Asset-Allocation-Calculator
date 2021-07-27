import pandas as pd
import numpy as np
from glob import glob
import os
import sys

dir='result'
if len(sys.argv)>1:
	dir=sys.argv[1]

pth='data/'
file_list = glob(pth+"*.csv")
etf_list = []
for filename in file_list:
    etf_list.append(filename[len(pth):len(pth)+4])
dm = pd.DataFrame()
rf = pd.DataFrame()
pl=[]
sl=[]
# for i in range(len(file_list)):
for i, etf in enumerate(etf_list):
	df = pd.read_csv(pth + etf + ' Historical Data.csv')
	df.rename(columns={"Price":etf},inplace=True)
	df.Date = pd.to_datetime(df['Date'])
	column_price=df[etf]
	pl.append((column_price.iloc[0] - column_price.iloc[-1])/column_price.iloc[-1])
	sl.append( np.std(column_price))
	if i==0:
		dm=df[['Date',etf]]
		dm.set_index('Date')
	else:
		dt=df[['Date',etf]]
		dm=dm.join(dt.set_index('Date'), how='inner', on='Date')

os.mkdir(dir,0o666)
dm.to_csv(dir + "/Price Data.csv")
corr=dm.corr()
cf=corr.sum(axis=1)
cf.to_csv(dir + "/Correlation Table.csv")
cf=cf.rank(axis=0).to_frame()
sf = pd.DataFrame(index=etf_list,data=sl, columns=None)
sf=sf.rank(axis=0)
sf.to_csv(dir + "/Stdev Table.csv")
pf= pd.DataFrame(index=etf_list,data=pl, columns=None)
pf_per=pf*100.0
pf=pf.rank(axis=0,ascending=False)
pf.to_csv(dir + "/Profit Table.csv")
pf=pf*2.1

rf['Rank']=cf.add(sf).add(pf).rank(axis=0)
rf['Profit(%)']=pf_per

rf=rf.sort_values(by='Rank')
print('Invest equally in Top three assets, if its profit is positive. If not, hold cash /n')
rf.to_csv("result/Rank Table.csv")
print(rf)

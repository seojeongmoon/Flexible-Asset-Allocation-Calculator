import pandas as pd
import numpy as np
from glob import glob
import os
import sys

print_mode = True

dir='result'
if len(sys.argv)>1:
	if sys.argv[1] is True or sys.argv[1] is False:
		print_mode=sys.argv[1]
	else:
		dir=sys.argv[1]
	if len(sys.argv)>2:
		print_mode=sys.argv[2]

pth='data/'
file_list = glob(pth+"*.csv")
etf_list = []
for filename in file_list:
    etf_list.append(filename[len(pth):len(pth)+4])

if(print_mode):
	print('etf list = ', etf_list)

dm = pd.DataFrame()
rf = pd.DataFrame()
pl=[]
sl=[]

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

# create a directory
if(not print_mode):
	os.mkdir(dir,0o666)
# add a price data.csv
if(not print_mode):
	dm.to_csv(dir + "/Price Data.csv")

# generate and add correlation data.csv
corr=dm.corr()
cf=corr.sum(axis=1)
if(print_mode):
	print("correlation values: \n", cf)
cf=cf.rank(axis=0).to_frame()
if(not print_mode):
	cf.to_csv(dir + "/Correlation Table.csv")

if(print_mode):
	print("Correlation Table \n", cf, "\n")

# generate and add a stdev data.csv
sf = pd.DataFrame(index=etf_list,data=sl, columns=None)
if(print_mode):
	print("stdev values: \n", sf)
sf=sf.rank(axis=0)
if(not print_mode):
	sf.to_csv(dir + "/Stdev Table.csv")

if(print_mode):
	print("Stdev Table \n", sf, "\n")

# generate and add a profit data.csv
pf= pd.DataFrame(index=etf_list,data=pl, columns=None)
pf_per=round(pf*100.0,2)
if(print_mode):
	print("profit(%) values: \n", pf_per)
pf=pf.rank(axis=0,ascending=False)
if(not print_mode):
	pf.to_csv(dir + "/Profit Table.csv")

if(print_mode):
	print("Profit Table \n", pf, "\n")

# scale pf and add the ranks
pf=pf*2.05
rf['Rank']=cf.add(sf).add(pf).rank(axis=0)
rf['Profit(%)']=pf_per

# sort values by rank
rf=rf.sort_values(by='Rank')
# add rank table.csv
if(not print_mode):
	rf.to_csv(dir + "/Rank Table.csv")

if(print_mode):
	print('Invest equally in Top three assets, if its profit is positive. If not, hold cash /n')
	print(rf)

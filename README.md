# Flexible-Asset-Allocation-Calculator
Calculates and ranks the assets based on flexible asset allocation(FAA) - tactical asset allocation strategy based on generalized momentum.

# What does this code do? #
This code processes ETF or index fund data that represent each asset category. The data are downloaded from www.investing.com historical data in csv forms.
This code ranks the ETF-lists with the principles of the FAA(Flexible Asset Allocation), with Absolute momentum (A), Volatility momentum (V) and Correlation momentum (C) factors.

Each ETF follows indexes of stocks, bonds, REITS and commodities. 

An example for index funds is
Stocks: VTSMX, FDIVX, VEIEX
Bonds: VFISX, VBMFX
Commodities:QRAAX, VGSIX

An example for ETFs is
Stocks: VTI,VEA,VWO
Bonds: SHY,BND
Commodities: GSG,VNQ

The FAA model is theorized in a paper titled "Generalized Momentum and Flexible Asset Allocation (FAA): An Heuristic Approach"(2012)
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2193735

# How do I use this code? #

Download the code and data of each asset classes from investing.com - the duration can be of the last three to six months.
Create a directory called 'data' where the code is and place the data in it. This code is optimized for ETFs with symbols of four letters.

Run 'FAA.py' with python. It will print the rank and the guide on investing. create a 'result' directory with csv files : Price data of ETFs, Correlation Table, Stdev(vollatility) Table, Profit Table, and Rank Table. You can input an argument to change the name of the directory it creates.

For instance, 

`python FAA.py tables`

will generate a "tables" directory with the csv files. 

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 12:27:10 2017

@author: linmich
"""
import pandas as pd
import pytz 
import tia.bbg.datamgr as dm
from tia.bbg import LocalTerminal
import datetime
import tushare as ts
data = ts.get_stock_basics()
report = ts.get_report_data(2014,3)
end = datetime.today() #开始时间结束时间，选取最近一年的数据
start = datetime(2015,1,1)
stock = ts.get_hist_data('300104',end,end)#选取一支股票
ts.get_hist_data('600848')
print pd.__version__
ts.get_stock_basics()
ts.get_report_data(2016,3)
# ALpha Lens implementation
import pandas as pd
file = r"F:\fund_data\csi_indices_all.xlsx"
xl = pd.ExcelFile(file)
# Print the sheet names
#print(xl.sheet_names[500])
# Load a sheet into a DataFrame by name: df1
#xl.parse(xl.sheet_names[650]).columns
fund_dict = {}
for sheet in xl.sheet_names:
    if sheet != 'Sheet1':
        fund_dict[sheet] = xl.parse(sheet).set_index('Date')
fund_panel = pd.Panel.from_dict(fund_dict)    
fund_panel_filled = fund_panel.fillna(method = 'ffill')
#fund_panel_filled = fund_panel_filled.swapaxes('major_axis', 'minor_axis')


universe_stocks = fund_panel_filled[:,'2014-12-31','PE_RATIO'].dropna(how='any').index.tolist()
fund_subset = fund_panel_filled[universe_stocks,:,:]

 
ms = dm.MemoryStorage()
mgr = dm.BbgDataManager()
cmgr = dm.CachedDataManager(mgr, ms, pd.datetime.now())
csids = cmgr[universe_stocks]
tick_sector=LocalTerminal.get_reference_data(universe_stocks, 'GICS_Sector_Name').as_frame().to_dict()['GICS_Sector_Name']

#factor_name = ['PE_RATIO']
#
#factor_data = 

import os
os.chdir(r'C:\Users\HTSB\Documents\Python')
import alpha_lib as al
 
#alpha = al.Alphas(pan)

#for n,f in al.Alphas.__dict__.iteritems():
#    if callable(f) & n.startswith('alpha'):
#        print(n)
#        method_to_call = getattr(alpha, n)
#        result = method_to_call()
#        print(result)
pan = fund_subset 
#universe_stocks[0]
#pan.loc[:,:,"PX_OPEN"]
#pan.iloc[0,0,:]
non_predictive_factor = pan.loc[:,:,'PE_RATIO']
non_predictive_factor = non_predictive_factor.stack()
non_predictive_factor.index = non_predictive_factor.index.set_names(['date', 'asset'])
pricing = pan.loc[:,:,'PX_LAST'].iloc[1:]
non_predictive_factor_data = al.get_clean_factor_and_forward_returns(non_predictive_factor, 
                                                                                  pricing, 
                                                                                  quantiles=5,
                                                                                  bins=None,
                                                                                  groupby=tick_sector
                                                                                   )


 
al.create_full_tear_sheet(non_predictive_factor_data) 

#PX_TO_BOOK_RATIO          9.881000e-01
#PE_RATIO                  6.365300e+00
#NORMALIZED_ROE            1.556560e+01
#RETURN_COM_EQY            1.547240e+01
#PX_LAST                   6.731000e+00
#PX_OPEN                   6.446000e+00
#PX_HIGH                   6.808000e+00
#PX_LOW                    6.402000e+00
#CUR_MKT_CAP               1.004177e+05
#MKT_CAP_TO_NET_REVENUE    1.878900e+00
#MKT_CAP_TO_REVENUE        9.486000e-01
#EQY_DPS                            NaN
#TRAIL_12M_DVD_PER_SH               NaN
#EQY_RAW_BETA                       NaN
#PX_VOLUME                 1.428821e+08
#TURNOVER_EXCH_RATIO       1.483000e+00
#EQY_WEIGHTED_AVG_PX       6.663100e+00
#VOLATILITY_10D            4.298800e+01
#VOLATILITY_20D            3.245800e+01
#VOLATILITY_30D            2.760200e+01
#IVOL_MID                           NaN

non_predictive_factor =pan.loc[:,:,'CUR_MKT_CAP']
non_predictive_factor = non_predictive_factor.stack()
non_predictive_factor.index = non_predictive_factor.index.set_names(['date', 'asset'])
pricing = pan.loc[:,:,'PX_LAST'].iloc[1:]
non_predictive_factor_data = al.get_clean_factor_and_forward_returns(non_predictive_factor, 
                                                                                  pricing, 
                                                                                  quantiles=5,
                                                                                  bins=None,
                                                                                  groupby=tick_sector
                                                                                   )


 
al.create_full_tear_sheet(non_predictive_factor_data) 
al.create_returns_tear_sheet(non_predictive_factor_data) 


non_predictive_factor =-pan.loc[:,:,'CUR_MKT_CAP']
non_predictive_factor = non_predictive_factor.stack()
non_predictive_factor.index = non_predictive_factor.index.set_names(['date', 'asset'])
pricing = pan.loc[:,:,'PX_LAST'].iloc[1:]
non_predictive_factor_data = al.get_clean_factor_and_forward_returns(non_predictive_factor, 
                                                                                  pricing, 
                                                                                  quantiles=5,
                                                                                  bins=None,
                                                                                  groupby=tick_sector
                                                                                   )
 
al.create_full_tear_sheet(non_predictive_factor_data) 
#al.create_returns_tear_sheet(non_predictive_factor_data) 


al.create_full_tear_sheet(non_predictive_factor_data) 
al.create_returns_tear_sheet(non_predictive_factor_data) 


dividend_factor =-pan.loc[:,:,'VOLATILITY_10D']
dividend_factor = dividend_factor.stack()
dividend_factor.index = dividend_factor.index.set_names(['date', 'asset'])
pricing = pan.loc[:,:,'PX_LAST'].iloc[1:]
dividend_factor_data = al.get_clean_factor_and_forward_returns(dividend_factor, 
  pricing, 
  quantiles=5,
  bins=None,
  groupby=tick_sector                                                                                   )
 
al.create_full_tear_sheet(dividend_factor_data) 



exch_ratio_factor =pan.loc[:,:,'TURNOVER_EXCH_RATIO']
exch_ratio_factor = exch_ratio_factor.stack()
exch_ratio_factor.index = exch_ratio_factor.index.set_names(['date', 'asset'])
pricing = pan.loc[:,:,'PX_LAST'].iloc[1:]
exch_ratio_factor_data = al.get_clean_factor_and_forward_returns(exch_ratio_factor, 
  pricing, 
  quantiles=5,
  bins=None,
  groupby=tick_sector                                                                                   )
 
al.create_full_tear_sheet(exch_ratio_factor_data) 


exch_ratio_factor =pan.loc[:,:,'PX_LAST']
exch_ratio_factor = exch_ratio_factor.pct_change(1)
exch_ratio_factor = exch_ratio_factor.dropna(how = 'any')*100
exch_ratio_factor = exch_ratio_factor.stack()
exch_ratio_factor.index = exch_ratio_factor.index.set_names(['date', 'asset'])
pricing = pan.loc[:,:,'PX_LAST'].iloc[1:]
pricing_real = pricing.dropna(how='any')*100
exch_ratio_factor_data =al.get_clean_factor_and_forward_returns(exch_ratio_factor, 
  pricing_real, 
  quantiles=None,
  bins= [-10,-5,-2,2,5,10],
  groupby=tick_sector                                                                                   )
 
al.create_full_tear_sheet(exch_ratio_factor_data) 

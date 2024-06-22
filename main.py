import data_loading as rdata
import datas
from datas import Data
import datetime
import Relative
import Moving_Average
import pandas as pd
import bollinger

def main():
    month_num=6
    stock_id=1101

    month_datas:pd.DataFrame=rdata.Get_N_Month_Data(month_num=month_num,stock_id=stock_id)
    month_datas['日期'] = month_datas['日期'].apply(datas.parse_custom_date)

    data_list:list=rdata.Get_Data_Dict(month_datas)
    data:Data=Data.model_validate(data_list)
    stock_datas:list[dict]=data.model_dump()

    window=20
    sma:pd.Series = Moving_Average.Calculate_Moving_Average(data=month_datas, window=window)

    rsi:pd.Series= Relative.calculate_rsi(data=month_datas,window=window)
    
    month_datas['sma']=sma
    month_datas['rsi']=rsi

    num_std=2
    month_datas:pd.DataFrame=bollinger.calculate_bollinger_bands(data=month_datas,window=window,num_std=num_std)

    print(month_datas)
    
if __name__ =="__main__":
    main()
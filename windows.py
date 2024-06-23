#自定義 套件
import data_loading as rdata
import datas
from datas import Data
import features
from features.feature import Feature

#python 套件
import tkinter 
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from numpy import random    #亂數產生
import numpy as np       #數學處理
import matplotlib.pyplot as plt #繪圖
class Window(tkinter.Tk):
    def __init__(self):
        self._stock_id:int=0
        self._stock_data:pd.DataFrame=None
        super().__init__()
        self.title("stock window")
        self.geometry("600x400")

        style = ttk.Style()
        style.configure("LeftTop.TFrame", background="lightblue")
        style.configure("LeftBottom.TFrame", background="lightgreen")
        style.configure("Right.TFrame", background="lightcoral")

        main_frame=ttk.Frame(self)
        #main_frame的設定 
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        #左-------------------------------------------------------------------------------------------
        left_frame=ttk.Frame(main_frame)
        #left_frame的設定
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        left_top_frame = ttk.Frame(left_frame, style="LeftTop.TFrame")
        self.stock_id_var = tkinter.StringVar()
        ttk.Label(left_top_frame, text="stock_id").grid(row=0,column=0,padx=(10,10),pady=(10,10))
        ttk.Entry(left_top_frame, textvariable=self.stock_id_var).grid(row=0,column=1,padx=(10,10),pady=(10,10))
        ttk.Button(left_top_frame,text="送出",command=self.update_stock_id).grid(row=1,column=1,sticky="se")
        left_top_frame.grid(row=0, column=0, sticky="nsew")

        left_bottom_frame = ttk.Frame(left_frame, style="LeftBottom.TFrame")
        ttk.Label(left_bottom_frame, text="Left Bottom Frame").pack()
        left_bottom_frame.grid(row=1, column=0, sticky="nsew")

        left_frame.grid(row=0,column=0,sticky="nsew")
        #左-------------------------------------------------------------------------------------------

        #右-------------------------------------------------------------------------------------------
        self.right_frame=ttk.Frame(main_frame)
        #right_frame的設定
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid(row=0,column=1,sticky="nsew")
        #右-------------------------------------------------------------------------------------------
        main_frame.pack(fill="both", expand=True)
    
    @property
    def stock_id(self):
        return self._stock_id

    def update_stock_id(self):
        try:
            self._stock_id = int(self.stock_id_var.get())
            self.main()

        except ValueError:
            print("Invalid stock ID input")

    def main(self):
        month_num=6
        stock_id=self.stock_id
        file_path='data.csv'

        month_datas=pd.DataFrame()
        #檢查是否檔案下載了
        if rdata.Check_Data_Csv():
            print("csv 已經存在")
            month_datas = pd.read_csv(file_path)
        else:
            print("下載檔案")
            month_datas:pd.DataFrame=rdata.Get_N_Month_Data(month_num=month_num,stock_id=stock_id)
            #將該網站的日期從str -> datetime
            month_datas['日期'] = month_datas['日期'].apply(datas.parse_custom_date)

        #特徵值使用
        window=20
        sma:pd.DataFrame = Feature().Calculate_Moving_Average(data=month_datas, window=window)
        month_datas=sma

        rsi:pd.DataFrame= Feature().Calculate_Rsi(data=month_datas,window=window)
        month_datas=rsi

        num_std=2
        month_datas:pd.DataFrame=Feature().Calculate_Bollinger_Bands(data=month_datas,window=window,num_std=num_std)
        
        self._stock_data=month_datas
        # 將 month_datas 寫入 data.csv
        month_datas.to_csv('data.csv', index=False)

        self.plot_features()


    def plot_features(self):
            for widget in self.right_frame.winfo_children():
                widget.destroy()

            features = ['upperband', 'lowerband']
            for i, fea in enumerate(features):
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.boxplot(self._stock_data[fea], showmeans=True)
                ax.set_title(fea)
                
                canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
                canvas.draw()
                canvas.get_tk_widget().grid(row=0, column=i, sticky="nsew")
                self.right_frame.grid_columnconfigure(i, weight=1)
        
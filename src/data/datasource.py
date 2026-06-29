import akshare as ak
import pandas as pd


class DataSource:
    def get_stock_list(self):
        df = ak.stock_zh_a_spot_em()
        return df[["代码", "名称", "最新价", "涨跌幅", "成交额"]]

    def get_daily_data(self, code, adjust="qfq"):
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            adjust=adjust
        )
        return df

    def get_stock_name(self, code):
        stock_list = self.get_stock_list()
        row = stock_list[stock_list["代码"] == code]
        if row.empty:
            return "未知股票"
        return row.iloc[0]["名称"]
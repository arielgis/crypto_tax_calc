import re
import pandas as pd
from datetime import datetime

class ConversionDataFrame:

    def __init__(self, csv_file, base_coin, target_coin):
        self.base_coin = base_coin
        self.target_coin = target_coin
        df = pd.read_csv(csv_file)
        df["DateInt"] = df["Date"].apply(lambda x: Convertor.date_to_int(x))
        expanded_range = pd.DataFrame({'DateInt': range(df["DateInt"].min(), df["DateInt"].max())})
        self.result_df = pd.merge(expanded_range, df[["Date", "DateInt", "Close"]], on='DateInt', how='left')
        self.result_df['Close'] = self.result_df['Close'].ffill()


    def get_daily_rate(self, date_string, base_coin, target_coin):
        date_int = Convertor.date_to_int(date_string)
        I = self.result_df['DateInt'] == date_int
        assert I.sum()  == 1, (self.result_df.iloc[0]['Date'], self.result_df.iloc[-1]['Date'])
        row = self.result_df[I].iloc[0]
        if base_coin == self.base_coin and target_coin == self.target_coin:
            return row["Close"]
        else:
            assert base_coin == self.target_coin and target_coin == self.base_coin , f'{self.target_coin}, {self.base_coin} != {base_coin}, {target_coin}'
            return float(1) / row["Close"]











class Convertor:


    def __init__(self, btc_usd_file, usd_nis_file, kas_usd_file, usdt_usd_file):

        self.usd_convertion_df_map = {}
        self.usd_convertion_df_map["BTC"] = ConversionDataFrame(btc_usd_file, "BTC", "USD")
        self.usd_convertion_df_map["NIS"] = ConversionDataFrame(usd_nis_file, "USD", "NIS")
        self.usd_convertion_df_map["KAS"] = ConversionDataFrame(kas_usd_file, "KAS", "USD")
        self.usd_convertion_df_map["USDT"] = ConversionDataFrame(usdt_usd_file, "USDT", "USD")

    def get_conversion_rate_by_date(self, date_string, base_coin, target_coin):
        if base_coin == "USD":
            rate = self.usd_convertion_df_map[target_coin].get_daily_rate(date_string, base_coin, target_coin)
        elif target_coin == "USD":
            rate = self.usd_convertion_df_map[base_coin].get_daily_rate(date_string, base_coin, target_coin)
        else:
            rate1 = self.usd_convertion_df_map[base_coin].get_daily_rate(date_string, base_coin, "USD")
            rate2 = self.usd_convertion_df_map[target_coin].get_daily_rate(date_string, "USD", target_coin)
            #print(f'{base_coin}, USD {rate1}')
            #print(f'USD {target_coin} {rate2}')
            rate =  rate1*rate2
        return rate


    def get_value_in_nis(self, date_string, currency, amount):
        if currency == "NIS":
            return amount
        else:
            rate = self.get_conversion_rate_by_date(date_string, currency, "NIS")
            return amount*rate

    @staticmethod
    def date_to_int(given_date_string):
        date_pattern1 = re.compile(r'^\d{2}/\d{2}/\d{4}$')
        date_pattern2 = re.compile(r'^\d{4}-\d{2}-\d{2}$')

        if date_pattern1.match(given_date_string):
            reference_date = datetime.strptime("01/01/2000", "%d/%m/%Y")
            given_date = datetime.strptime(given_date_string, "%d/%m/%Y")
        else:
            assert date_pattern2.match(given_date_string), given_date_string
            reference_date = datetime.strptime("2000-01-01", "%Y-%m-%d")
            given_date = datetime.strptime(given_date_string, "%Y-%m-%d")

        # Calculate the difference in days
        days_difference = (given_date - reference_date).days
        return (days_difference)




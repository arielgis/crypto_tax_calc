from abc import  abstractmethod
import pandas as pd
import math
from datetime import datetime

class CryptoFileParser:

    @abstractmethod
    def parse_file(self, filename):
        pass


def handle_buy_bit2c(row):
    assert row["accountAction"] == "Buy"
    resulting_target_amount = -row["secondAmount"] - row["feeAmount"]
    assert math.isclose(row["firstAmount"] * row["price"],resulting_target_amount , abs_tol=1e-3), \
        (row["firstAmount"] * row["price"], -row["secondAmount"] - row["feeAmount"])
    dat = {"Time": row["created"], "Platform1": "bit2c", "Platform2": "bit2c",
           "Currency1": row["secondCoin"], "Currency2": row["firstCoin"], "Amount1": resulting_target_amount,
           "Amount2": row["firstAmount"], "Currency1_Fee": row["feeAmount"]}
    return dat


def handle_withdrawal_bit2c(row, prev_row):
    assert row["accountAction"] == "Withdrawal"
    assert prev_row["accountAction"] == "FeeWithdrawal"
    assert math.isclose(-prev_row["firstAmount"] * prev_row["price"], prev_row["feeAmount"], abs_tol=1e-10)
    dat = {"Time": row["created"], "Platform1": "bit2c", "Platform2": "txbit",
           "Currency1": row["firstCoin"], "Currency2": row["firstCoin"], "Amount1": -row["firstAmount"],
           "Amount2": -row["firstAmount"], "Currency1_Fee": -prev_row["firstAmount"]}
    return dat


def handle_deposit_bit2c(row):
    assert row["accountAction"] == "Deposit"
    dat = {"Time": row["created"], "Platform1": "bank", "Platform2": "bit2c",
           "Currency1": row["firstCoin"], "Currency2": row["firstCoin"], "Amount1": row["firstAmount"],
           "Amount2": row["firstAmount"], "Currency1_Fee": 0}
    return dat


def bit2c_date_format(s):
    v = s.split(' ')
    date_time = ['{:02d}'.format(int(x)) for x in v[0].split('/')]
    hour_time = ['{:02d}'.format(int(x)) for x in v[1].split(':')]
    date_time.reverse()
    return "{}_{}".format("_".join(date_time), "_".join(hour_time))


def txbit_change_date_format(date_str, year):

    parsed_date = datetime.strptime(date_str, '%b %dth, %H:%M:%S')
    # Format the datetime object to the desired output string
    output_date_string = f"{year}_" + parsed_date.strftime('%m_%d_%H_%M')
    return output_date_string


def handle_txbit_row(record_list, year):
    column_names = ['created', 'PAIR', 'TYPE', 'PRICE', 'FILLED', 'FEE', 'TOTAL']
    assert len(record_list) == len(column_names)
    timestamp = txbit_change_date_format(record_list[0], year) #created
    coins_list = record_list[1].split("/") #PAIR
    price_list = record_list[3].split(" ") #PRICE
    origin_coin = coins_list[0]
    target_coin = coins_list[1]
    origin_amount = float(record_list[4].split(" ")[0]) #FILLED
    target_amount = float(record_list[6].split(" ")[0]) #TOTAL
    conversion_rate = float(price_list[0])
    fee_origin = float(record_list[5].split(" ")[0]) / conversion_rate #FEE
    if record_list[2] == "Buy": #TYPE
        origin_coin, target_coin = target_coin, origin_coin
        origin_amount, target_amount = target_amount, origin_amount
        conversion_rate = 1 / conversion_rate
        fee_origin = fee_origin / conversion_rate
    else:
        assert record_list[2] == "Sell" #TYPE
    origin_amount -= fee_origin
    target_amount -= (fee_origin * conversion_rate)
    assert math.isclose(origin_amount * conversion_rate, target_amount, abs_tol=1e-3), (origin_amount  , fee_origin, conversion_rate, target_amount)
    dat = {"Time": timestamp, "Platform1": "txbit", "Platform2": "txbit",
           "Currency1": origin_coin, "Currency2": target_coin, "Amount1": origin_amount,
           "Amount2": target_amount, "Currency1_Fee": fee_origin}
    return dat


class Bit2CTxtParser(CryptoFileParser):
    
    #def __init__(self):
    def parse_file(self, filename):
        bit2c_data = pd.read_csv(filename, sep="\t")
        bit2c_data["created"] = bit2c_data["created"].apply(lambda x: bit2c_date_format(x))
        bit2c_data = bit2c_data.sort_values("id").reset_index(drop=True)
        dat_rows = []
        n = bit2c_data.shape[0]
        for i in range(n):
            row = bit2c_data.iloc[i]
            if row["accountAction"] == "Deposit":
                dat_rows.append(handle_deposit_bit2c(row))
            elif row["accountAction"] == "Buy":
                dat_rows.append(handle_buy_bit2c(row))
            elif row["accountAction"] == "Withdrawal":
                assert i > 0
                dat_rows.append(handle_withdrawal_bit2c(row, bit2c_data.iloc[i - 1]))
        return pd.DataFrame(dat_rows)





class TxbitTradingParser(CryptoFileParser):


    def parse_file(self, filename):
        column_names = ['created', 'PAIR', 'TYPE', 'PRICE', 'FILLED', 'FEE', 'TOTAL']

        # Read the file
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Create an empty list to store the record data
        record_data = []

        # Iterate through the lines and combine records
        for i in range(0, len(lines), 7):
            record = [line.strip() for line in lines[i:i+7]]
            dat = handle_txbit_row(record, "2022")
              record_data.append(dat)

        # Create the DataFrame
        df = pd.DataFrame(record_data)
        return df

def main():
    btc_parser = Bit2CTxtParser()
    tx_parser = TxbitTradingParser()
    bit2c_data = btc_parser.parse_file("bit2c-financial-report-2022.txt")
    txbit_data = tx_parser.parse_file("txbit_trading_history.html")
    merged = pd.concat([txbit_data, bit2c_data]).sort_values("Time")
    merged.to_csv("transactions_crypto_2022.tsv", index=False, sep="\t")


if __name__ == "__main__":
    main()




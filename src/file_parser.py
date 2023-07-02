from abc import ABC, abstractmethod
import pandas as pd
from crypto_event import  WalletTransferPartialList
from crypto_event import  CryptoEventList
from crypto_event import WalletTransferComplete
from crypto_event import WalletTransferPartial

class CryptoFileParser:

    @abstractmethod
    def parse_file(self, filename):
        pass


class Bit2CTxtParser(CryptoFileParser):
    
    
    def bit2c_date_format(s):
        v = s.split(' ')
        date_time = ['{:02d}'.format(int(x)) for x in v[0].split('/')]
        hour_time = ['{:02d}'.format(int(x)) for x in v[1].split(':')] 
        date_time.reverse()
        return "{}_{}".format("_".join(date_time), "_".join(hour_time))

    def parse_file(filename):
        bit2c_data = pd.read_csv(filename, sep="\t")
        bit2c_data["created"] = bit2c_data["created"].apply(lambda x: Bit2CTxtParser.bit2c_date_format(x))
        bit2c_data = bit2c_data.sort_values("id").reset_index(drop=True)
        partial_list = WalletTransferPartialList()
        events_list = CryptoEventList()
        for index,row in bit2c_data.iterrows():
            if row["accountAction"] == "Deposit":
                assert row["firstAmount"] > 0
                partial_list.add_event(WalletTransferPartial(row["created"], "bit2c", row["firstCoin"], row["firstAmount"], 0, "deposit"))
            elif row["accountAction"] == "Withdrawal":
                prev_row = bit2c_data.iloc[index - 1]
                assert prev_row["accountAction"] == "FeeWithdrawal"
                assert row["firstAmount"] < 0
                partial_list.add_event(WalletTransferPartial(row["created"], "bit2c", row["firstCoin"], -row["firstAmount"],-prev_row["firstAmount"], "withdraw"))  
        return events_list, partial_list
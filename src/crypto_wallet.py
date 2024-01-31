epsilon = 1e-15

class Value:
    def __init__(self, coin, amount, cost_nis):
        self.coin = coin
        self.amount = amount
        self.cost_nis = cost_nis


    def reduce_value(self, amount):
        """
        reduce the amount of the Value object by the given amount.
        Args:
            amount:

        Returns: A new Value object with the reduced amount.

        """
        assert self.amount > amount
        frac = amount / self.amount
        reduced_val = Value(self.coin, amount, self.cost_nis * frac)
        self.amount -= amount
        self.cost_nis -= reduced_val.cost_nis
        return reduced_val

    def addFee(self, fee):
        """
        Add fee to Value
        Args:
            fee:

        Returns:

        """
        self.cost_nis += fee

    def toString(self):
        return "{},{},{}".format(self.coin, self.amount, self.cost_nis)


class Wallet:
    def __init__(self, wallet_currency):
        self.values = []
        self.wallet_currency = wallet_currency
        self.total_amount = 0

    def add_value(self, value):
        assert value.coin == self.wallet_currency
        self.values.append(value)
        self.total_amount += value.amount

    def toString(self):
        return "\n".join([x.toString() for x in self.values])


    def pop_first_value(self):
        first_value = self.values.pop(0)
        self.total_amount -= first_value.amount
        return first_value

    def reduce_from_first_value(self,request_amount):
        first_value = self.values[0]
        assert first_value.amount > request_amount
        reduced_value = first_value.reduce_value(request_amount)
        self.total_amount -= request_amount
        return reduced_value

    def extract_amount_from_wallet(self,requested_amount):
        """
        Extracts the requested amount from the wallet.
        Args:
            requested_amount: The amount to be extracted.

        Returns: A list of Value objects that represent the extracted amount.

        """
        assert self.total_amount >= (requested_amount - epsilon), f"wallet have {self.total_amount} {self.wallet_currency}, requested {requested_amount} diff {self.total_amount - requested_amount} "
        extracted_values = []
        while requested_amount > epsilon:
            assert len(self.values) > 0
            if self.values[0].amount <= requested_amount:
                extracted_values.append(self.pop_first_value())
                requested_amount -= extracted_values[-1].amount
            else:
                extracted_values.append(self.reduce_from_first_value(requested_amount))
                requested_amount = 0
        total_extracted_amount = sum(x.amount for x in extracted_values)
        total_cost = sum(x.cost_nis for x in extracted_values)
        return Value(self.wallet_currency, total_extracted_amount, total_cost)
        #return extracted_values












"""

    def get_total_wallet_amount(self):
        total_amount = 0
        for value in self.values:
            total_amount += value.amount
        return total_amount

    def add_value(self, value):
        assert value.coin == self.wallet_currency
        prev_amount = self.get_total_wallet_amount()
        self.values.append(value)
        new_amount = self.get_total_wallet_amount()
        assert new_amount == prev_amount + value.amount

    def remove_value(self, value):
        prev_amount = self.get_total_wallet_amount()
        self.values.remove(value)
        new_amount = self.get_total_wallet_amount()
        assert new_amount == prev_amount - value.amount

    def get_total_amount(self, coin):
        total_amount = 0
        for value in self.values:
            if value.coin == coin:
                total_amount += value.amount
        return total_amount

    def toString(self):
        return "\n".join([x.toString() for x in self.values])


    def transfer(self, wallet2, coin, amount, fee):
        required_amount = amount
        index = 0
        while required_amount > 0:
            assert index < len(self.values)
            curr_val = self.values[index]
            if curr_val.coin == coin:
                if required_amount >= curr_val.amount:
                    frac = curr_val.amount / amount
                    self.remove_value(curr_val)
                    curr_val.addFee(frac * fee)
                    wallet2.add_value(curr_val)
                    required_amount -= curr_val.amount
                else:
                    assert required_amount < curr_val.amount
                    frac = required_amount / amount
                    curr_fee = frac * fee
                    new_val = curr_val.deduce_amount(required_amount)
                    wallet2.add_value(new_val)
                    required_amount = 0
            index += 1

"""
"""
class Convertor:
    @staticmethod
    def coin_to_nis_rate(usd_to_nis, coin_to_nis, coin_name):
        merged_df = pd.merge(usd_to_nis, coin_to_nis, on='Date', suffixes=('_usd_to_nis', '_coin_to_nis'))
        merged_df[coin_name] = merged_df['Close_usd_to_nis'] * merged_df['Close_coin_to_nis']
        return merged_df[["Date", coin_name]]

    @staticmethod
    def read_file(filename, dates_list, change_date_format=False):
        all_dates_df = pd.DataFrame({"Date": dates_list})
        df = pd.read_csv(filename)
        if change_date_format:
            # this is for cases when the date is of type 2022-08-01 instead of 01/08/2022
            df["Date"] = df["Date"].apply(
                lambda x: "{}/{}/{}".format(x.split('-')[2], x.split('-')[1], x.split('-')[0]))
        df = pd.merge(all_dates_df, df[["Date", "Close"]], on="Date", how='left')
        assert df["Close"][0:1].isna().sum() == 0, df
        df['Close'].fillna(method='ffill', inplace=True)
        return df

    @staticmethod
    def get_convert_to_nis_table(btc_usd_file, ils_usd_file, kas_usd_file, usdt_usd_file, dates_list):
        btc_usd_data = Convertor.read_file(btc_usd_file, dates_list)
        ils_usd_data = Convertor.read_file(ils_usd_file, dates_list)
        kas_usd_data = Convertor.read_file(kas_usd_file, dates_list, change_date_format=True)
        usdt_usd_data = Convertor.read_file(usdt_usd_file, dates_list, change_date_format=True)
        btc_to_nis = Convertor.coin_to_nis_rate(ils_usd_data, btc_usd_data, "BTC")
        kas_to_nis = Convertor.coin_to_nis_rate(ils_usd_data, kas_usd_data, "KAS")
        usdt_to_nis = Convertor.coin_to_nis_rate(ils_usd_data, usdt_usd_data, "USDT")
        convert_to_nis = btc_to_nis.merge(kas_to_nis, on="Date").merge(usdt_to_nis, on="Date")
        return convert_to_nis

    @staticmethod
    def func():
        return 2

    def __init__(self, btc_usd_file, ils_usd_file, kas_usd_file, usdt_usd_file, dates_list):
        self.convert_to_nis = Convertor.get_convert_to_nis_table(btc_usd_file, ils_usd_file, kas_usd_file,
                                                                 usdt_usd_file, dates_list)

    def get_conversion_rate_by_date(self, date):
        I = self.convert_to_nis["Date"] == date
        assert I.sum() == 1
        row = self.convert_to_nis[I].iloc[0]
        return row
"""


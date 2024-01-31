# mymodule.py

from crypto_wallet import Wallet
from crypto_wallet import Value
from Convertor import Convertor
def process_data(data):
    # Perform some processing on the data
    processed_data = [x * 2 for x in data]
    return processed_data













#def transaction(wallet1, wallet2, currency1, currency2, amount1, amount2):
#    value1 = wallet1.reduce_value(amount1)
#    value2 = Value("BTC", currency2, 297.0297)
#    value2 = wallet2.reduce_value(amount1)

def main():
    base_path = "/Users/arielgispan/Library/CloudStorage/GoogleDrive-arieldoritgispan@gmail.com/My Drive/finance/crypto"
    c = Convertor(f'{base_path}/BTC-USD.csv', f'{base_path}/ILS-USD.csv', f'{base_path}/KAS-USD.csv',
                  f'{base_path}/USDT-USD.csv')
    bank_nis = Wallet("NIS")
    bit2c_nis = Wallet("NIS")
    bit2c_btc = Wallet("BTC")
    txbit_btc = Wallet("BTC")
    txbit_usdt = Wallet("USDT")
    txbit_kas = Wallet("KAS")
    bank_nis.add_value(Value("NIS", 100000, 100000))
    print(1.3877787807814457e-17  + 1)

    #bit2c: 16/08/2022  11:30:49
    transfer_event(bank_nis, bit2c_nis, 300, 0)

    #bit2c: 16/08/2022  13:42:42
    profit1 = transaction_event("16/08/2022", c, bit2c_nis, bit2c_btc, "NIS", "BTC", 299.999997, 0.00360036)
    #print(f"bit2c_nis val = {bit2c_nis.total_amount}")

    #bit2c: 17/08/2022  9:54:18
    transfer_event(bit2c_btc, txbit_btc, 0.00360036, 0.0005)

    #bit2c: 18/08/2022  7:50:14
    transfer_event(bank_nis, bit2c_nis, 9000, 0)

    #bit2c: 18/08/2022  12:00:04
    profit2 = transaction_event("18/08/2022", c, bit2c_nis, bit2c_btc, "NIS", "BTC", 2975.478426, 0.03748115)
    profit3 = transaction_event("18/08/2022", c, bit2c_nis, bit2c_btc, "NIS", "BTC", 6009.379211, 0.07531494)
    #print(f"bit2c_nis val = {bit2c_nis.total_amount}")

    #bit2c: 18/08/2022  12:01:53
    transfer_event(bit2c_btc, txbit_btc, 0.11279609, 0.0005)

    # bit2c: 19/08/2022  7:36:31
    transfer_event(bank_nis, bit2c_nis, 9700, 0)

    # bit2c: 19/08/2022  16:44:44
    profit4 = transaction_event("19/08/2022", c, bit2c_nis, bit2c_btc, "NIS", "BTC", 9715.139839, 0.13069226)
    #print(f"bit2c_nis val = {bit2c_nis.total_amount}")

    # bit2c: 19/08/2022  16:46:41
    transfer_event(bit2c_btc, txbit_btc, 0.13069226, 0.0005)


if __name__ == "__main__":
    # If the module is run as the main program, execute the main function
    main()
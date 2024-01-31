from crypto_wallet import Value

def transfer_event(wallet1, wallet2, amount, fee):
    value = wallet1.extract_amount_from_wallet(amount + fee)
    wallet2.add_value(Value(value.coin, amount, value.cost_nis))


def transaction_event(date, convertor, wallet1, wallet2, currency1, currency2, amount1_including_fee, amount2):
    value1 = wallet1.extract_amount_from_wallet(amount1_including_fee)
    assert value1.coin == currency1
    #The cost of value1 is what we paid so far for this value
    amount_nis_cost = value1.cost_nis

    if currency1 == "NIS":
        amount_nis_revenue = amount1_including_fee
    else:
        amount_nis_revenue = convertor.get_value_in_nis(date, currency2, amount2)
    #The cost of value2 is the market price of this value
    value2 = Value(currency2, amount2, amount_nis_revenue)
    wallet2.add_value(value2)

    profit = amount_nis_revenue - amount_nis_cost
    if currency1 != "NIS":
        print(f"Tax Event {currency1}->{currency2}, cost:{round(amount_nis_cost,2)} revenue:{round(amount_nis_revenue,2)} profit:{round(profit,2)}")
    return profit
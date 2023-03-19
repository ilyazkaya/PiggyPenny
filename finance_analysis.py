from main2 import parse_categorized_transactions
from main2 import parse_unique_transactions
from datetime import datetime
from datetime import date, timedelta
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
import math

unique_transaction_file = 'unique_transactions.csv'
categorized_transaction_file = 'all_transactions.csv'

all_transactions = parse_categorized_transactions(categorized_transaction_file)

#%%
# <editor-fold desc="How much money have I spent on every category in the last month">

today = datetime.today().date()
end_day = today
start_day= today - timedelta(days=90)

last_period_transactions = [transaction for transaction in all_transactions if end_day > transaction['date'] > start_day]

# filtering out internal and intra-family outbound transactions
last_period_transactions = [transaction for transaction in last_period_transactions if transaction['category'] not in [
    'Local_transfer', 'ICBC_Cardpayment']]

transactions_by_category = {}
for transaction in last_period_transactions:
    if transaction['category'] in transactions_by_category.keys():
        transactions_by_category[transaction['category']].append(transaction)
    else:
        transactions_by_category[transaction['category']] = [transaction]


total_by_category = {}
for category, transactions in transactions_by_category.items():
    amounts = [transaction['amount'] for transaction in transactions]
    total = sum(amounts)
    total_by_category[category] = total

total_spent_by_category = {category: amount for category, amount in total_by_category.items() if amount < 0}
total_earned_by_category = {category: amount for category, amount in total_by_category.items() if amount > 0}

# </editor-fold>
#%%
# <editor-fold desc="Pie chart of spending">
# sort by value
sorted_total_spent_by_category = dict(sorted(total_spent_by_category.items(), key=lambda item: item[1]))

values = [abs(amount) for category, amount in sorted_total_spent_by_category.items()]
labels = [category + ': ' + str(np.floor(amount)) for category, amount in sorted_total_spent_by_category.items()]

plt.pie(values, labels=labels, startangle=90)
plt.show()


# </editor-fold>

#%%
# <editor-fold desc="Pie chart of earning">
# sort by value
sorted_total_earned_by_category = dict(sorted(total_earned_by_category.items(), key=lambda item: item[1]))

values = [abs(amount) for category, amount in sorted_total_earned_by_category.items()]
labels = [category + ': ' + str(np.floor(amount)) for category, amount in sorted_total_earned_by_category.items()]

plt.pie(values, labels=labels, startangle=90)
plt.show()


# </editor-fold>
#%%
# <editor-fold desc="Total spending">
total_spent = 0
for amount in total_spent_by_category.values():
    if amount < 0:
        total_spent += amount
# </editor-fold>
#%%
# <editor-fold desc="Total earnings">
total_earned = 0
for amount in total_earned_by_category.values():
    if amount > 0:
        total_earned += amount
# </editor-fold>
#%%
# <editor-fold desc="Running total. Visa + Checking + ICBCVisa">
today_statement_total = 0
flux_total = sum([transaction['amount'] for transaction in last_period_transactions])
initial_statement_total = today_statement_total - flux_total

start_day = min([t['date'] for t in last_period_transactions])
end_day = datetime.today().date()

# calculating totals for the day
day_fluxs = {}
day = start_day
while day != end_day:
    day_flux = sum([t['amount'] for t in last_period_transactions if t['date'] == day])
    day_fluxs[day] = day_flux

    # incrementing by a day
    day += timedelta(days=1)

# creating daily cumulative totals
cumulative_day_totals = {}
for day, flux_amount in day_fluxs.items():
    if cumulative_day_totals != {}:
        cumulative_day_totals[day] = list(cumulative_day_totals.values())[-1] + flux_amount
    else:
        cumulative_day_totals[day] = initial_statement_total + flux_amount

# plotting
plt.plot(cumulative_day_totals.keys(), cumulative_day_totals.values())
plt.show()

# </editor-fold>
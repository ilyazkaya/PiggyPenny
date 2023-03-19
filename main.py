#%%
import csv
import os
from tkinter import *
from tkinter import ttk
from datetime import datetime

def parse_csv(filename, account_name):
    transactions = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        def _name_scrape(row):
            info = row.split('  ')
            info = [name.replace(' ', '') for name in info]

            info = [name for name in info if name != '']
            name = info[0]

            if name == '':
                try:
                    name = info[1]
                except IndexError:
                    print('Could not find a name for transaction')

            return name

        for row in reader:
            transaction = {}
            transaction['date'] = datetime.strptime(row[0], '%Y-%m-%d').date()
            transaction['name'] = _name_scrape(row[1])
            transaction['amount'] = float(row[2])
            transaction['account_name'] = account_name
            transaction['category'] = ''
            transactions.append(transaction)
    return transactions

def parse_categorized_transactions(filename):
    transactions = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row

        for row in reader:
            transaction = {}
            transaction['date'] = datetime.strptime(row[0], '%Y-%m-%d').date()
            transaction['name'] = row[1]
            transaction['amount'] = float(row[2])
            transaction['account_name'] = row[3]
            transaction['category'] = row[4]
            transactions.append(transaction)
    return transactions

# Parse unique transactions
def parse_unique_transactions(filename):
    unique_transactions = {}
    try:
        with open('unique_transactions.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            for row in reader:
                unique_transactions[row[0]] = row[1]
    except FileNotFoundError:
        with open('unique_transactions.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Category'])

    return unique_transactions


def categorize_transactions(transactions, unique_transactions):
    # read in user-defined categories from unique_transactions.csv
    categories = ['Groceries', 'Gas', 'Dining Out', 'Shopping', 'Entertainment']
    with open('unique_transactions.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            if row[1] not in categories:
                categories.append(row[1])

    for transaction in transactions:
        if (transaction['name']) in unique_transactions.keys():
            transaction['category'] = unique_transactions[transaction['name']]
            continue

        # prompt user to categorize transaction
        root = Tk()
        root.title('Categorize Transaction')

        mainframe = ttk.Frame(root, padding='3 3 12 12')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        transaction_label = ttk.Label(mainframe, text='Transaction Details:')
        transaction_label.grid(column=1, row=1, sticky=W)

        transaction_text = Text(mainframe, height=10, width=50)
        transaction_text.insert(END, 'Name: {}\n'.format(transaction['name']))
        transaction_text.insert(END, 'Amount: {}\n'.format(transaction['amount']))
        transaction_text.insert(END, 'Account Name: {}\n'.format(transaction['account_name']))
        transaction_text.insert(END, 'Date: {}\n'.format(transaction['date']))
        transaction_text.grid(column=1, row=2, sticky=W)

        category_label = ttk.Label(mainframe, text='Category:')
        category_label.grid(column=1, row=3, sticky=W)

        category_var = StringVar()
        category_menu = OptionMenu(mainframe, category_var, *categories)
        category_menu.grid(column=1, row=4, sticky=W)

        new_category_entry = ttk.Entry(mainframe)
        new_category_entry.grid(column=1, row=5, sticky=W)

        def save_category():
            if new_category_entry.get():
                category = new_category_entry.get()
                if category not in categories:
                    categories.append(category)
                    category_var.set(category)
                else:
                    category_var.set(category)
            else:
                category = category_var.get()

            transaction['category'] = category

            with open('unique_transactions.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([transaction['name'], category])

            root.destroy()

        save_button = ttk.Button(mainframe, text='Save', command=save_category)
        save_button.grid(column=1, row=6, sticky=W)

        root.mainloop()

        unique_transactions[transaction['name']] = transaction['category']


# filling out the transactions with categories with the unique transaction-category pairs stored in the dedicated csv
# file
def categorize_known_names(transactions, unique_transactions):
    for transaction in transactions:
        if transaction['name'] in unique_transactions.keys():
            transaction['category'] = unique_transactions[transaction['name']]

def save_transactions(transactions):
    with open('all_transactions.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Name', 'Amount', 'Account Name', 'Category'])
        for transaction in transactions:
            writer.writerow([transaction['date'], transaction['name'], transaction['amount'], transaction['account_name'], transaction['category']])


def main():
    # parse CSV files and create list of transactions
    transactions = []
    current_directory = os.getcwd()
    account_folder = os.path.join(current_directory, 'Accounts')
    for filename in os.listdir(account_folder):
        account_name = filename.replace('.csv', '')
        filename = os.path.join(account_folder, filename)
        if filename.endswith('.csv'):
            transactions += parse_csv(filename, account_name)

    # loading unique transactions
    unique_transactions_file = 'unique_transactions.csv'
    unique_transactions = parse_unique_transactions(unique_transactions_file)

    # categorize transactions
    # first with known and already categorized names
    categorize_known_names(transactions, unique_transactions)

    # second, transactions with new names with user's help
    categorize_transactions(transactions, unique_transactions)

    # root.destroy()  # destroy window

    # save transactions to CSV file
    save_transactions(transactions)
    return transactions, unique_transactions

transactions, unique_transactions = main()


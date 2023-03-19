To use categorization app (main.py)
- collect all the bank statement csv files in the folder "Accounts"
- all files have to have the following columns: [date, transaction name, amount].
- amounts have to be negative if outbound, positive if inbound
- ICBC Visa payment that I did through e-transfer has to be labeled 'ICBCVisa_Payment'

- run main.py to load and group all expenses
    - you will be prompted to assign categories for the transactions. If an appropriate category is not present in the
    drop- name categorized automatically. Unique transaction - category pairs are stored in "unique_transactions.csv".
    Do not delete it.

Once all transactions have been categorized and consolidated you can analyze the data in any way you want.
"finance_analysis.py" provides some examples of the insights that you can get about your transaction history. The
analysis file is organized in the Jupyter Notebook style but with using PyCharm cells in "Scientific mode" on.

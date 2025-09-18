import csv
from openpyxl import Workbook

# Save a CSV file of your transactions in the same folder
# as this project and put the name below

FILE = 'data.csv'
OUTPUT_FILE = 'output.xlsx'

def finance_manager(file):
    total_sum = 0
    transactions = []
    workbook = Workbook()
    sheet = workbook.active

    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        for row in csv_reader:
            # Get Period, Data_value, Series_title_1
            Period = row[1]
            Data_value = row[2]
            Series_title_1 = row[7]

            # Replace 'NA' with 0
            if Data_value == 'NA':
                Data_value = '0'

            try:
                Data_value = float(Data_value)
                total_sum += Data_value
            except ValueError:
                print(f"Error: Unable to convert value to float: {Data_value}")
                continue

            transaction = (Period, Series_title_1, Data_value)
            transactions.append(transaction)

    # Write transactions to the Excel sheet
    sheet.append(['Period', 'Series_title_1', 'Data_value'])
    for transaction in transactions:
        sheet.append(transaction)

    # Add total sum at the end
    sheet.append(['Total Sum', '', total_sum])

    # Save the workbook as an Excel file
    workbook.save(OUTPUT_FILE)

    print(f"The sum of your transactions this month is {total_sum}")
    print('')
    return transactions

print(finance_manager(FILE))

#!/usr/bin/env python3

import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('--config', help='path to file containing column header mappings', required=True)
parser.add_argument('--csv-file', help='path to CSV file', required=True)
parser.add_argument('--skip-headers', help='skip first lines of file as headers', type=int, default=0)
parser.add_argument('--reverse-amount', help='reverse the sign of the amount', default=False, action='store_true')
args = parser.parse_args()

skip_lines = args.skip_headers
reverse_amount = args.reverse_amount

with open(args.config, 'r') as config_file:
    column_headings = config_file.readline().strip()
    column_headings = column_headings.split()

with open(args.csv_file, newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file, fieldnames=column_headings)

    print('!Type:Bank')

    for row in csv_reader:
        if skip_lines:
            skip_lines -= 1
        else:
            print('D' + row['date'].replace("-", "/"))
            if 'credit' in column_headings and row['credit'] :
                print('T' + row['credit'])
            elif 'debit' in column_headings and row['debit']:
                print('T-' + row['debit'])
            elif 'amount' in column_headings and row['amount']:
                amount = row['amount']
                if(reverse_amount):
                    if (amount[0] == '-'):
                        amount = amount[1:]
                    else:
                        amount = '-' + amount
                print('T' + amount)
            if row['number']:    
                print('N' + row['number'])
            if row['description']:    
                print('P' + row['description'])
            print('^')

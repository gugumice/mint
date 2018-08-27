#!/usr/bin/python


import csv
from tinydb import TinyDB, Query

db = TinyDB('db.json')
db.purge()
csvf = open('/srv/web/temp/mint.csv', 'rb')

#reader=csv.reader(csvf)
reader = csv.DictReader(csvf)
a=0
e=0
for row in reader:
	#row = unicode(row, errors='ignore')
	
	a += 1
	#print(a, row)
	try:
		rec = {'SKU': row['SKU'], 'Pack': int(row['Pack']), 'Name': row['Name'], 'BAR': row['BAR'], 'Pict': row['Pict']}
		db.insert(rec)
	except:
		e += 1
		print('Error importing record {}, SKU: {}, Name:{}'.format(a, row['SKU'], row['Name']))
print('Total: {}, not inserted {}'.format(a,e))

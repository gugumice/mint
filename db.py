#!/usr/bin/python
# -*- coding: utf-8 -*

from tinydb import TinyDB, Query
import json
db=TinyDB('db.json')

q = Query()
r=db.search(q.SKU.search('^M8020'))
print(len(r))
for row in r:
	print(row)
	#print(json.dumps(row,ensure_ascii=False))
	print ('{}, {}'.format(row['SKU'], row['Name']))


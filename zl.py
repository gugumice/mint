\#!/usr/bin/python
# -*- coding: utf-8 -*
from PIL import Image
import os
class zlabel(object):
	def __init__(self, code,name,ean,dir,file,packing=1,qty=1,zoom=1):
		self.code=code

		self.name=name
		self.ean=ean
		self.packing=packing
		self.pic_dir=dir
		self.pic_file=file
		self.pic_zoom=zoom
		self.qty=qty
	def import_pict(self,pic,zoom=1,x=100,y=100):
		im=Image.open(pic).convert("1").rotate(90)
		im=im.resize([int(s*zoom) for s in im.size])
		data = im.tostring("raw", "1;I")
		size = len(data)
		data = ["%02X" % ord(byte) for byte in data]
		name=os.path.basename(pic)
		fp='~DG{},{},{},'.format(name,size, (im.size[0]+7)/8)
		fp=fp+"".join(data)
		fp=fp+"^FO {},{} ^IM{} ^FS".format(x,y,name)
		return fp
	def make_label(self):
		form='''
CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH10,50^JMA^PR5,5~SD15^JUS^LRN^CI0^XZ
^XA
^MMT
^PW631
^LL1207
^LS0
#perim
^FO0,0^GB615,1180,1^FS
#1
^FO0,0^GB160,680,1^FS
#2
^FO0,680^GB375,500,1^FS
#3
^FO160,0^GB107,340,1^FS
#4
^FO160,340^GB107,340,1^FS
#5
^FO267,0^GB107,680^FS
#6
^FO375,0^GB240,340^FS
#7
^FO375,340^GB240,340^FS
#8
^FO375,680^GB240,500^FS

^FT195,655^ARB,28,40^FH\^FDSKU code^FS
^FT195,325^ARB,28,40^FH\^FDPackaging units^FS
^FT432,1150^AUB,28,40^FH\^FDMINT FURNITURE Ltd.^FS
^FT472,1150^A0B,28,40^FH\^FD24A Ganibu dambis^FS
^FT507,1150^A0B,28,40^FH\^FDRiga, LV-1005, Latvia^FS
^FT542,1150^A0B,28,40^FH\^FDphone +371 22160180^FS
^FT592,1150^A0B,28,40^FH\^FDwww.mintfurniture.lv^FS

'''
		sku='^FT246,655^AUB,28,40^FH\^FD{}^FS'.format(self.code)
		pc='^FT246,325^AUB,28,40^FH\^FD{} item(s) in box^FS'.format(self.packing)
		string=self.name.strip().split(',')
		name1='^FT320,650^AUB,28,40^FH\^FD{}^FS'.format(string[0])
		name2='^FT360,650^ARB,28,40^FH\^FD{}^FS'.format(''.join(s for s in string[1:]))
		bc='^BY3,2,167^FT577,309^BEB,,Y,N^FD{}^FS'.format(self.ean)
		
		#qr=self.import_pict('/srv/web/frm1/static/img/pack/QR2.tif',1,390,390)
		qr=''
		logo=self.import_pict('/srv/web/frm1/static/img/pack/MINT_logo2.tif',1,35,35)
		pic=self.import_pict(self.pic_dir+self.pic_file,.6,20,700)
		qty='^PQ{},0,1,Y'.format(self.qty)
		foot='^XZ'
		
		return form+sku+name1+name2+pc+bc+qr+logo+pic+qty+foot


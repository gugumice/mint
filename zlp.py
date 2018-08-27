#!/usr/bin/python
# -*- coding: utf-8 -*
from PIL import Image
from zebra import zebra
import os

class zlabel(object):
	def __init__(self, code,name,ean,file,inv_no=None,dir='/srv/web/frm1/static/img/mint/',packing=1,qty=1,zoom=1):
		self.code=code
		self.name=name
		self.ean=ean
		self.inv_no=inv_no
		self.packing=packing
		self.pic_dir=dir
		self.pic_file=file
		self.pic_zoom=zoom
		self.qty=qty
	def __import_pict(self,pic,zoom=1,x=100,y=100):
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
	def __make_label(self):
#CT~~CD,~CC^~CT~

		form='''
^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH10,20^JMA^PR5,5~SD15^JUS^LRN^CI0^XZ
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
^FO160,0^GB107,350,1^FS
#4
^FO160,350^GB107,330,1^FS
#5
^FO267,0^GB110,680^FS
#6
^FO375,0^GB240,350^FS
#7
^FO375,350^GB240,330^FS
#8
^FO375,680^GB240,500^FS

^FT195,655^ARB,28,40^FH\^FDSKU code^FS
^FT432,1150^AUB,28,40^FH\^FDMINT FURNITURE Ltd.^FS
^FT472,1150^A0B,28,40^FH\^FD24A Ganibu dambis^FS
^FT507,1150^A0B,28,40^FH\^FDRiga, LV-1005, Latvia^FS
^FT542,1150^A0B,28,40^FH\^FDphone +371 22160180^FS
^FT592,1150^A0B,28,40^FH\^FDwww.mintfurniture.lv^FS

'''
		sku='^FT246,655^AUB,28,40^FH\^FD{} {} {}^FS'.format(self.code[:5],self.code[5:-2],self.code[-2:])
		string=self.name.strip().split(',')
		name1='^FT320,655^AUB,28,40^FH\^FD{}^FS'.format(string[0].strip())
		name2='^FT360,655^ARB,28,40^FH\^FD{}^FS'.format(string[1].strip())
		bc='^BY3,2,167^FT577,309^BEB,,Y,N^FD{}^FS'.format(self.ean)
		inv_txt="\n^FT420,655^A0B,28,40^FH\^FDProforma No:^FS"
		if self.inv_no!=None:
			inv_txt='{0}\n^FT475,655^AUB,28,40^FH\^FD{2}^FS\n^BY2,3,102^FT600,655^BCB,,N,N^FD{1}^FS\n'.format(inv_txt, self.inv_no,
			 '{} {} {}'.format(self.inv_no[:2], self.inv_no[2:-2], self.inv_no[-2:]))
			
		#qr=self.import_pict('/srv/web/frm1/static/img/pack/QR2.tif',1,390,390)
		qr=''
		logo=self.__import_pict('/srv/web/frm1/static/img/pack/MINT_logo2.tif',1,35,35)
		pic=self.__import_pict(self.pic_dir+self.pic_file,.6,20,700)
		qty='^PQ{},0,1,Y'.format(self.qty)

		#return form+sku+name1+name2+pc+bc+inv_txt+logo+pic+qty
		return form+sku+name1+name2+bc+inv_txt+logo+pic+qty

	def print_label(self):
		z=zebra(zebra().getqueues()[0])
		if self.packing<2:
			packing_title="Quantity"
			packing_text="{} item in a box"
		else:
			packing_title="Packaging Units"
			packing_text="{} of {}"
		for i in range(1, self.packing+1):
			#print(packing_title, packing_text.format(i, self.packing))
			pc='^FT195,325^ARB,28,40^FH\^FD{0}^FS\n^FT246,325^AUB,28,40^FH\^FD{1}^FS'.format(packing_title, packing_text.format(i, self.packing))
			lbl=self.__make_label()+pc+'^XZ'
			print(lbl)
			z.output(lbl)	


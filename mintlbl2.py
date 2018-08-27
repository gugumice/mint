#!/usr/bin/python
# -*- coding: utf-8 -*
from PIL import Image
from zebra import zebra
from string import Template
from datetime import datetime
import re, sys, os

class MintLbl(object):
	def __init__(self, Body=" ", Printer="Zebra", Copies=1, Direct=True, **kwargs):
		self.z=zebra()
		for q in self.z.getqueues():
			if re.search(Printer, q):
				#print(q)
				self.z.setqueue(q)
		#Label absolute 0 offset
		LabelOffsetXY=[10,20]
		Prefix="^XA~TA000~JSN^LT0^MNW^MT{}^LH{},{}^PON^PMN^XZ".format(("T", "D")[Direct],
			 LabelOffsetXY[0],  LabelOffsetXY[1])
		self.__LblTxt="{}^XA{}^PQ{}^XZ".format(Prefix,  Template(Body).safe_substitute(kwargs), Copies)
	def PrintLbl(self):
		try:
			self.z.output(self.__LblTxt)
		except:
			sys.exit("Printer <{}> not found!".format(Printer))
	def ShowLbl(self):
			print(self.__LblTxt)
		
#p=MintPrinter()

def LblPicture(Pict="", Zoom=1, x=0, y=0):
	im=Image.open(Pict).convert("1").rotate(90)
	#print(im.size, Zoom)
	if Zoom !=1:
		im=im.resize([int(s*Zoom) for s in im.size])
	#print(im.size)
	data = im.tostring("raw", "1;I")
	size = len(data)
	data = ["%02X" % ord(byte) for byte in data]
	name=os.path.basename(Pict)
	fp='~DG{},{},{},'.format(name,size, (im.size[0]+7)/8)
	fp=fp+"".join(data)
	fp=fp+"^FO {},{} ^IM{} ^FS".format(x,y,name)
        return fp

def PrintAttn(Fragile=False, Copies=1):
        #t="^FO0,0^GB610,1190,1^FS^LH30,30^FO20,10^ADN,90,50^AD^FD$txt^FS$Pic"
	t="^FO0,0^GB610,1190,1^FS$Pic"
        lAttn=MintLbl(Body=t, Copies=Copies,
                Pic=(LblPicture('/srv/web/frm1/static/img/pack/Attention_{}.jpg'.format(('1','2')[Fragile]), x=20, y=50)))
	#lAttn.ShowLbl()
	lAttn.PrintLbl()
	
def PrintPack(sku,pict,name,ean,invno,packing,copies=1):

	t='''
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
^FT246,655^AUB,28,40^FH\^FD$sku^FS
^FT320,655^AUB,28,40^FH\^FD$name1^FS
^FT360,655^ARB,28,40^FH\^FD$name2^FS
^BY3,2,167^FT577,309^BEB,,Y,N^FD$ean^FS
^FT420,655^A0B,28,40^FH\^FDProforma No:^FS
^FT475,655^AUB,28,40^FH\^FD$invbc^FS
^FT195,325^ARB,28,40^FH\^FD$ptitle^FS\n^FT246,325^AUB,28,40^FH\^FD$ptext^FS
$invno
$logo
$icon
'''
	if packing<2:
		ptitle="Quantity"
		ptext="{} item in a box"
	else:
		ptitle="Packaging Units"
		ptext="{} of {}"
	
	for i in range(1, packing+1):
		name1=""
		name2=""
		
		invstr=""
		#Dalam peec kommmata, ja nav - 1 rinda=vaardi lielim burtiem
		try:
			name1=name.split(',')[0].strip()
			name2=name.split(',')[1].strip()
		except IndexError:
			n1=[]
		        n2=[]
			for word in name.split():
				n1.append(word) if word.isupper() else n2.append(word)
				name1=" ".join(n1)
				name2=" ".join(n2)
		print(">>>",bool(invno))
		if invno:
			invstr='^BY2,3,102^FT600,655^BCB,,N,N^FD{}^FS'.format(invno)
		
		lPack=MintLbl(Body=t, Copies=copies, sku="{} {} {}".format(sku[:5],sku[5:-2],sku[-2:]),
			name1=name1, name2=name2,
			invno=invstr, invbc="{} {} {}".format(invno[:2], invno[2:-2], invno[-2:]), 
			ean=ean, ptitle=ptitle, ptext=ptext.format(i, packing),
			logo=LblPicture('/srv/web/frm1/static/img/pack/MINT_logo2.tif',x=35,y=35),
			#icon=LblPicture('/srv/web/frm1/static/img/mint/M1700.jpg',Zoom=.6, x=20, y=700)
			icon=LblPicture(pict,Zoom=.6, x=20, y=700)

			)
		#lPack.ShowLbl()
		lPack.PrintLbl()

def main():
	PrintAttn(True)
	PrintAttn(False)
	'''
	PrintPack(sku="M1700RKZI",
                name="MIRROR, 1000 x 60 x 1000 mm, walnut/ pastel blue",
                ean="4752157000209",
                invno="17083DE",
                packing=2,
		copies=1
		)
	'''
if __name__ == "__main__":
        main()


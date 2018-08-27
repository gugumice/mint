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
				print(q)
				self.z.setqueue(q)
		#Label absolute 0 offset
		LabelOffsetXY=[10,20]
		Prefix="^XA~TA000~JSN^LT0^MNW^MT{}^LH{},{}^PON^PMN^XZ".format(("T", "D")[Direct],
			 LabelOffsetXY[0],  LabelOffsetXY[1])
		LblTxt="{}^XA{}^PQ{}^XZ".format(Prefix,  Template(Body).safe_substitute(kwargs), Copies)
		l=LblTxt
	def PrintLbl(self):
		try:
			self.z.output(l)
	
			#return(True)
		except:
			sys.exit("Printer <{}> not found!".format(Printer))
	def ShowLbl(self):
		print(l)
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

def PrintAttn(Fragile=False):
        #t="^FO0,0^GB610,1190,1^FS^LH30,30^FO20,10^ADN,90,50^AD^FD$txt^FS$Pic"
	t="^FO0,0^GB610,1190,1^FS$Pic"
        MintLbl(Body=t, Copies=1,
                Pic=(LblPicture('/srv/web/frm1/static/img/pack/Attention_{}.jpg'.format(('2','1')[Fragile]), x=20, y=50)))

def PrintPack():
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
'''
	MintLbl(Body=t)	
	pass

def main():
	#PrintAtn(Fragile=True)
	#PrintAttn()
	PrintPack()

if __name__ == "__main__":
        main()



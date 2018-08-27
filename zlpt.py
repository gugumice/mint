#!/usr/bin/python
# -*- coding: utf-8 -*

def main():
	import zlp
	#from zebra import zebra
        l=zlp.zlabel(code='M1001OSBA',
		    name='KTICHEN COUNER SET LARGE, with wooden rack shelf ash/ pastel violet',
		    ean='4752157005181',
		    file='M1001.jpg',
		    inv_no='17083DE',
		    packing=1,
		    qty=1)
	l.print_label()
	#dir='/srv/web/frm1/static/img/mint/',
        #z=zebra(zebra().getqueues()[0])
        #z.output(l.make_label())

if __name__ == "__main__":
	main()

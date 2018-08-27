#!/usr/bin/python
# -*- coding: utf-8 -*

from tinydb import TinyDB, Query
db=TinyDB('db.json')


from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, BooleanField, TextField, TextAreaField, validators, StringField, IntegerField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 

class ReusableForm(Form):
   sku = TextField('SKU:', validators=[validators.required(), validators.Length(min=4,max=9)])

class PrintForm(Form):
   NumCopies = IntegerField('Qty: ', validators=[validators.required(), validators.NumberRange(min=1,max=10)])
   NumInvoice = StringField('Invoice No: ', validators=[validators.optional()])
   BoolPrintAttn = BooleanField('Attn: ', default=False)

@app.route("/", methods=['GET', 'POST'])
@app.route("/<sku_code>", methods=['GET', 'POST'])
def hello(sku_code=None):
    form = ReusableForm(request.form)
    print form.errors
    r={}
    if request.method == 'POST':
        sku_code=request.form['sku'].upper()
        
        if form.validate():
            # Save the comment here.
    	    q=Query()
	    r=db.search(q.SKU.search('^{}'.format(sku_code)))
	    if len(r)==1:
		    return redirect(url_for('print_label', sku_code=sku_code))
	    if len(r)>0:
	            flash('Ok! {} SKU {}'.format(len(r),sku_code))
		    
	    else:
		    flash('SKU {} nav atrasts!'.format(sku_code))
   
	else:
            flash('SKU kluuda!')
 
    return render_template('main.html', form=form, sku_code=sku_code, sku_list=r, sku_len=len(r))


@app.route("/print/<sku_code>", methods=['GET', 'POST'])
def print_label(sku_code=None):
	form=PrintForm(request.form)
	q=Query()
        r=db.search(q.SKU == sku_code)
	if request.method == 'POST':
		if form.validate():
			#print(r[0]['Name'])
			#for field in form:
			#	print("!!!!!",field.name, field.data)
			import mintlbl2 
			mintlbl2.PrintPack(sku=sku_code, 
			name=r[0]['Name'],
			ean=r[0]['BAR'][:12],
			pict='/srv/web/frm1/static/img/mint/{}'.format(r[0]['Pict'].strip()),
			invno=form.NumInvoice.data,
			packing=r[0]['Pack'],
			copies=form.NumCopies.data)

			if form.BoolPrintAttn.data:
				 mintlbl2.PrintAttn(int(r[0]['Attn'])==2, r[0]['Pack']*form.NumCopies.data)
	return  render_template('print_labels.html', form=form, sku_code=sku_code, 
			name=r[0]['Name'], pict=r[0]['Pict'], bar=r[0]['BAR'], pack=r[0]['Pack'], attn_type=int(r[0]['Attn']))


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)

from flask import render_template, flash, redirect, session, url_for
from app import app
from .forms import CompanyForm
from yelp_process import search_yelp

company = None

@app.route('/result')
def result():
    company = session['company']
    first = session['first']
    last = session['last']
    location = session['location']
    yelp_results = search_yelp(company,location)
    return render_template('result.html',
                           title=company,
                           company=company,
                           first=first,
                           last=last,
                           location=location)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def choose_company():
    form = CompanyForm()
    if form.validate_on_submit():
        flash('Data requested for company="%s", owner_first="%s", owner_last="%s", location="%s"' %
          (form.company.data, form.owner_first.data, form.owner_last.data, form.location.data))
        session['company'] = form.company.data
        session['first'] = form.owner_first.data
        session['last'] = form.owner_last.data
        session['location'] = form.location.data
        return redirect(url_for('result'))
    return render_template('index.html',
                           form=form,
                           providers=app.config['YELP_KEY'])

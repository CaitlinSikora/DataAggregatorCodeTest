from flask import render_template, flash, redirect, session, url_for
from app import app
from .forms import BusinessForm
from yelp_process import search_yelp
from facebook_process import get_facebook
from google_process import google_score

@app.route('/result')
def result():
    business_name = session['business_name']
    owner = session['owner']
    business_type = session['business_type']
    location = session['location']
    yelp_results = search_yelp(business_name,location)
    google_results = google_score(business_name,owner,business_type,location)
    facebook_results = get_facebook(business_name,location)
    results = [yelp_results,facebook_results, google_results]
    return render_template('result.html',
                           title=business_name,
                           business_name=business_name,
                           owner=owner,
                           business_type=business_type,
                           location=location,
                           results=results)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def choose_business():
    form = BusinessForm()
    if form.validate_on_submit():
        # flash('Data requested for business_name="%s", owner="%s", business_type="%s", location="%s"' %
        #   (form.business_name.data, form.owner.data, form.business_type.data, form.location.data))
        session['business_name'] = form.business_name.data
        session['owner'] = form.owner.data
        session['business_type'] = form.business_type.data
        session['location'] = form.location.data
        return redirect(url_for('result'))
    return render_template('index.html',
                           form=form)

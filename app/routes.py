from app import app
from flask import render_template, render_template_string, request, redirect, url_for, session, jsonify
import requests, json
from datetime import datetime, timezone
from app.forms import LocationForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LocationForm()
    if form.validate_on_submit():
        session['city'] = form.city.data
        if form.america.data:
            session['america'] = True
            session['state'] = form.state.data
        else:
            session['america'] = False
            session['state'] = ''
        session['country'] = form.country.data
        return redirect(url_for('weather'))
    return render_template('main.html', form=form)

@app.route('/weather')
def weather():
    city = session.get('city').lower()
    country = session.get('country').lower()
    america = session.get('america')
    state = session.get('state').lower()
    api_key = '987d4127a30757d56cef5adb5eef79df'

    # Build safe query from session values
    if america is False:
        resp = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={api_key}')
    else:
        resp = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&appid={api_key}')
    location_data = json.loads(resp.text)
    
    if location_data == []:
        return redirect(url_for('index'))
    
    lat = location_data[0]['lat']
    lon = location_data[0]['lon']
    raw_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
    data = json.loads(raw_data.text)
    return render_template('weather.html', data=data)

def timezone_convert(value, offset):
    timestamp = int(value) + int(offset)
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime("%H:%M:%S")
    
app.jinja_env.filters['convert'] = timezone_convert

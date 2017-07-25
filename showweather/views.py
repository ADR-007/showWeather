import json
from io import StringIO
from itertools import dropwhile

import lxml.html as html
import requests
from flask import render_template, abort

from showweather import app
from tools import parse_fixed_width, to_float

STATION_DATA_INDEX_URL = 'https://data.gov.uk/dataset/historic-monthly-meteorological-station-data'
DATA_SOURCE_PATTERN = 'http://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{}.txt'


@app.route('/')
@app.route('/index')
def index():
    elements = []
    for element in html.parse(StringIO(requests.get(STATION_DATA_INDEX_URL).text)).getroot() \
            .find_class('dataset-resource-text'):
        elements.append({
            'title': element.find_class('inner-cell')[0].text_content().strip(),
            'href': element.find_class('inner-cell')[1].cssselect('a')[1].get('href').split('/')[-1][:-8]
        })

    return render_template(
        'index.html',
        elements=elements
    )


@app.route('/history/<string:city>')
def weather_history(city):
    pass


@app.route('/charts/<string:city>', methods=['GET', 'POST'])
def charts(city: str):
    return render_template(
        'chart.html',
        city=city,
        title=city
    )


@app.route('/data/<string:city>.js')
def get_data_of_weather(city: str):
    url = DATA_SOURCE_PATTERN.format(city)
    response = requests.get(url=url, headers={'User-agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        abort(response.status_code)
    headers, dimension, *data, _ = parse_fixed_width(list(
        dropwhile(lambda row: row[0] != ' ', response.text.split('\n'))
    ))

    joined_by_date_data = [[f'{row[1]}/{row[0]}', *to_float(row[2:-1])] for row in data]
    transposed = list(zip(*([['Date'] + headers[2:-1]] + joined_by_date_data)))

    data_for_graphics = [
        {'title': 'Temperature', 'table': list(zip(*transposed[:3]))},
        {'title': 'Rain', 'table': list(zip(*[transposed[0], transposed[4]]))},
        {'title': 'Sun', 'table': list(zip(*[transposed[0], transposed[5]]))},
    ]

    js_data = json.dumps(data_for_graphics)
    return app.response_class(
        response=f"var data_of_weather = {js_data};",
        status=200,
        mimetype='application/javascript'
    )

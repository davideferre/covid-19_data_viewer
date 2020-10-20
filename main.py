from collections import OrderedDict
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def italy():
    output_format = request.args.get('format', default='html')
    r = requests.get(
        'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json'
    )
    parsed_json = r.json()
    struct = {}
    for j in parsed_json:
        struct[j['data'][0:10]] = {}
        today_obj = datetime.strptime(j['data'][0:10], '%Y-%m-%d')
        today = today_obj.strftime('%Y-%m-%d')
        yesterday_obj = today_obj - timedelta(days=1)
        yesterday = yesterday_obj.strftime('%Y-%m-%d')
        struct[today]['diff'] = {}
        for val, key in enumerate(j):
            if (
                key != 'data' and key != 'denominazione_regione' and key != 'note_it' and key != 'note_en' and
                key != 'codice_regione' and key != 'stato' and key != 'lat' and key != 'long'
            ):
                struct[today][key] = j[key]
                if yesterday in struct:
                    if (struct[today][key] is not None) and (struct[yesterday][key] is not None):
                        try:
                            struct[today]['diff'][key] = struct[today][key] - struct[yesterday][key]
                        except:
                            struct[today]['diff'][key] = 0
    if output_format == 'json':
        return jsonify(OrderedDict(sorted(struct.items(), reverse=True)))
    return render_template('italy.html', body=OrderedDict(sorted(struct.items(), reverse=True)))


@app.route('/regions')
def regions():
    output_format = request.args.get('format', default='html')
    r = requests.get(
        'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json'
    )
    regione = request.args.get('regione')
    parsed_json = r.json()
    struct = {}
    old_date = ""
    for j in parsed_json:
        if old_date != j['data'][0:10]:
            today_obj = datetime.strptime(j['data'][0:10], '%Y-%m-%d')
            today = today_obj.strftime('%Y-%m-%d')
            yesterday_obj = today_obj - timedelta(days=1)
            yesterday = yesterday_obj.strftime('%Y-%m-%d')
            struct[today] = {}
            old_date = today
        actual_region = j['denominazione_regione']
        if regione == str(j['codice_regione']) or regione is None:
            struct[today][actual_region] = {}
            struct[today][actual_region]['diff'] = {}
            for val, key in enumerate(j):
                if (
                    key != 'data' and key != 'denominazione_regione' and key != 'note_it' and key != 'note_en' and
                    key != 'codice_regione' and key != 'stato' and key != 'lat' and key != 'long'
                ):
                    struct[today][actual_region][key] = j[key]
                    if yesterday in struct:
                        if key in struct[yesterday][actual_region]:
                            if (struct[today][actual_region][key] is not None) and (struct[yesterday][actual_region][key] is not None):
                                try:
                                    struct[today][actual_region]['diff'][key] = struct[today][actual_region][key] - \
                                        struct[yesterday][actual_region][key]
                                except:
                                    struct[today][actual_region]['diff'][key] = 0
    if output_format == 'json':
        return jsonify(OrderedDict(sorted(struct.items(), reverse=True)))
    return render_template('regions.html', body=OrderedDict(sorted(struct.items(), reverse=True)))


@app.route('/provinces')
def province():
    output_format = request.args.get('format', default='html')
    province = request.args.get('province')
    struct = {}
    if province is not None:
        r = requests.get(
            'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'
        )
        parsed_json = r.json()
        province = province.capitalize()
        for j in parsed_json:
            if j['denominazione_provincia'] == province:
                struct[j['data'][0:10]] = {}
                today_obj = datetime.strptime(j['data'][0:10], '%Y-%m-%d')
                today = today_obj.strftime('%Y-%m-%d')
                yesterday_obj = today_obj - timedelta(days=1)
                yesterday = yesterday_obj.strftime('%Y-%m-%d')
                struct[today]['diff'] = {}
                key = 'totale_casi'
                struct[today][key] = j[key]
                if yesterday in struct:
                    if (struct[today][key] is not None) and (struct[yesterday][key] is not None):
                        try:
                            struct[today]['diff'][key] = struct[today][key] - \
                                struct[yesterday][key]
                        except:
                            struct[today]['diff'][key] = 0
    if output_format == 'json':
        return jsonify(OrderedDict(sorted(struct.items(), reverse=True)))
    return render_template('province.html', body=OrderedDict(sorted(struct.items(), reverse=True)), province=province)

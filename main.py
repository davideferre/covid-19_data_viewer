from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    r = requests.get(
        'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json'
    )
    regione = request.args.get('regione')
    app.logger.error("REGIONE: " + str(regione))
    parsed_json = r.json()
    output_html = '<a href="/">Home</a>&nbsp;'
    output_html += '<a href="/?regione=1">Piemonte</a>&nbsp;'
    output_html += '<a href="/?regione=2">Valle d\'Aosta</a>&nbsp;'
    output_html += '<a href="/?regione=3">Lombardia</a>&nbsp;'
    output_html += '<a href="/?regione=4">Trentino</a>&nbsp;'
    output_html += '<a href="/?regione=5">Veneto</a>&nbsp;'
    output_html += '<a href="/?regione=6">Friuli Venezia Giulia</a>&nbsp;'
    output_html += '<a href="/?regione=7">Liguria</a>&nbsp;'
    output_html += '<a href="/?regione=8">Emilia Romangna</a>&nbsp;'
    output_html += '<a href="/?regione=9">Toscana</a>&nbsp;'
    output_html += '<a href="/?regione=10">Umbria</a>&nbsp;'
    output_html += '<a href="/?regione=11">Marche</a>&nbsp;'
    output_html += '<a href="/?regione=12">Lazio</a>&nbsp;'
    output_html += '<a href="/?regione=13">Abruzzo</a>&nbsp;'
    output_html += '<a href="/?regione=14">Molise</a>&nbsp;'
    output_html += '<a href="/?regione=15">Campania</a>&nbsp;'
    output_html += '<a href="/?regione=16">Puglia</a>&nbsp;'
    output_html += '<a href="/?regione=17">Basilicata</a>&nbsp;'
    output_html += '<a href="/?regione=18">Calabria</a>&nbsp;'
    output_html += '<a href="/?regione=19">Sicilia</a>&nbsp;'
    output_html += '<a href="/?regione=20">Sardegna</a>&nbsp;'
    output_html += '<br/>'
    output_html += '<h1>Dati COVID-19 Italia</h1>'
    old_date = ""
    for j in parsed_json[::-1]:
        if old_date != j['data'][0:10]:
            output_html += "<h2>" + j['data'][0:10] + "</h2>"
            old_date = j['data'][0:10]
        tmp_output_html = ""
        tmp_output_html += "<h3>" + j['denominazione_regione'] + "</h3>"
        for val, key in enumerate(j):
            if (
                key != 'data' and key != 'denominazione_regione' and
                key != 'codice_regione' and key != 'stato' and key != 'lat' and key != 'long'
            ):
                tmp_output_html += "<u>" + key + "</u>: " + str(j[key]) + '<br/>'
        if regione is None:
            output_html += tmp_output_html
        else:
            if regione is not None and regione == str(j['codice_regione']):
                output_html += tmp_output_html
    output_html += '<hr/><a href="https://github.com/pcm-dpc/COVID-19" target="_self">Dati forniti dal Dipartimento della Protezione Civile</a>'
    return str(output_html)

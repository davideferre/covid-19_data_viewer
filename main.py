from flask import Flask, request, render_template
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
    menu_html = '<nav class="nav nav-pills mb-2">';
    menu_html += '<a class="nav-link" href="/">Home</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=1">Piemonte</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=2">Valle d\'Aosta</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=3">Lombardia</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=4">Trentino</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=5">Veneto</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=6">Friuli Venezia Giulia</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=7">Liguria</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=8">Emilia Romangna</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=9">Toscana</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=10">Umbria</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=11">Marche</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=12">Lazio</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=13">Abruzzo</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=14">Molise</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=15">Campania</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=16">Puglia</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=17">Basilicata</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=18">Calabria</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=19">Sicilia</a>&nbsp;'
    menu_html += '<a class="nav-link" href="/?regione=20">Sardegna</a>&nbsp;'
    menu_html += '<nav/>'
    body_html = ''
    old_date = ""
    for j in parsed_json[::-1]:
        if old_date != j['data'][0:10]:
            body_html += "<h2 class=\"mt-4\">" + j['data'][0:10] + "</h2>"
            old_date = j['data'][0:10]
        tmp_body_html = ''
        if regione is None:
            tmp_body_html += "<h3 class=\"mt-3\">" + j['denominazione_regione'] + "</h3>"
        tmp_body_html += '<ul class="list-group mt-3">'
        for val, key in enumerate(j):
            if (
                key != 'data' and key != 'denominazione_regione' and
                key != 'codice_regione' and key != 'stato' and key != 'lat' and key != 'long'
            ):
                tmp_body_html += '<li class="list-group-item d-flex justify-content-between align-items-center">'
                tmp_body_html += key + '<span class="badge badge-primary badge-pill">' + str(j[key]) + '</span>'
                tmp_body_html += '</li>';
        tmp_body_html += '</ul>'
        if regione is None:
            body_html += tmp_body_html
        else:
            if regione is not None and regione == str(j['codice_regione']):
                body_html += tmp_body_html
    body_html += '<hr/><a href="https://github.com/pcm-dpc/COVID-19" target="_self">Dati forniti dal Dipartimento della Protezione Civile</a>'
    return render_template('index.html', body=body_html, menu=menu_html)

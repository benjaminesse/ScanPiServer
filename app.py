"""Main server script."""
import os
import yaml
from datetime import datetime
from flask import Flask, render_template

from serverpi.plotting import generate_map


app = Flask(__name__)


@app.route('/')
def index():
    """Make index page."""
    # Read in the overall config file
    with open('settings.yaml', 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Get the station status
    try:
      with open(f"{config['DataPath']}/Station/status.txt", 'r') as r:
          status = r.readline()
    except FileNotFoundError:
        status = 'Unknown'

    # Set date to today
    date_to_plot = str(datetime.now().date())

    # Pull config from file
    station_name = config['StationName']
    fpath = f"{config['DataPath']}/Results"
    vlat, vlon = config['VentLocation']
    slat, slon = config['ScannerLocation']
    map_zoom = config['MapZoom']

    # Generate the plots
    SO2graphJSON = generate_map(fpath, date_to_plot, 'SO2', 'SO2 SCD',
                                'viridis', [0, 2e18])
    INTgraphJSON = generate_map(fpath, date_to_plot, 'int_av', 'Intensity',
                                'magma')

    # Read in the log file if it exists
    log_fname = f"{fpath}/{date_to_plot}/{date_to_plot}.log"
    try:
        with open(log_fname, 'r') as r:
            lines = r.readlines()
        log_text = ''
        for line in lines:
            log_text += line.strip() + '\n'
    except FileNotFoundError:
        log_text = 'Log file not found!'


    return render_template('index.html',
                           volcano_latitude=vlat,
                           volcano_longitude=vlon,
                           scanner_latitude=slat,
                           scanner_longitude=slon,
                           zoom=map_zoom,
                           SO2graphJSON=SO2graphJSON,
                           INTgraphJSON=INTgraphJSON,
                           station_name=station_name,
                           log_text=log_text,
                           status=status)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

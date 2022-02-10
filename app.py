"""Main server script."""
import os
import yaml
from datetime import datetime
from flask import Flask, render_template

from serverpi.plotting import generate_map


app = Flask(__name__)

fpath = '/home/pi/OpenSO2/Results'


@app.route('/')
def index():
    """Make index page."""
    # Read in the overall config file
    with open('settings.yaml', 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Set date to today
    date_to_plot = str(datetime.now().date())

    # Pull config from file
    station_name = config['StationName']
    fpath = config['DataPath']
    vlat, vlon = config['VentLocation']
    slat, slon = config['ScannerLocation']
    map_zoom = config['MapZoom']

    # Generate the plots
    SO2graphJSON = generate_map(fpath, date_to_plot, 'SO2', 'SO2 SCD',
                                'viridis', [0, 2e18])
    INTgraphJSON = generate_map(fpath, date_to_plot, 'int_av', 'Intensity',
                                'magma')

    return render_template('index.html',
                           volcano_latitude=vlat,
                           volcano_longitude=vlon,
                           scanner_latitude=slat,
                           scanner_longitude=slon,
                           zoom=map_zoom,
                           SO2graphJSON=SO2graphJSON,
                           INTgraphJSON=INTgraphJSON,
                           station_name=station_name)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

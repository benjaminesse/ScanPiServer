"""Main server script."""
import os
from datetime import datetime
from flask import Flask, render_template

from serverpi.plotting import generate_map


app = Flask(__name__)

fpath = '/home/pi/OpenSO2/Results'


@app.route('/')
def index():
    """Make index page."""
    # Set date to today
    date_to_plot = str(datetime(2022, 1, 27).date())
    station_name = 'ScanPi-5'
    # str(datetime.now().date())

    # Get the available dates
    dates = [d for d in os.listdir(fpath) if os.path.isdir(f'{fpath}/{d}')]
    dates.reverse()

    # Generate the plots
    SO2graphJSON = generate_map(fpath, date_to_plot, 'SO2', 'SO2 SCD',
                                'viridis', [0, 2e18])
    INTgraphJSON = generate_map(fpath, date_to_plot, 'int_av', 'Intensity',
                                'magma')

    return render_template('index.html',
                           volcano_latitude=28.614,
                           volcano_longitude=-17.867,
                           scanner_latitude=28.633414,
                           scanner_longitude=-17.909092,
                           zoom=11,
                           SO2graphJSON=SO2graphJSON,
                           INTgraphJSON=INTgraphJSON,
                           station_name=station_name)


@app.route('/<station_name>/')
def station_landing(station_name):
    """Generate the station landing page."""
    # Set date to today
    date_to_plot = str(datetime(2022, 1, 27).date())
    # str(datetime.now().date())

    # Get the available dates
    dates = [d for d in os.listdir(fpath) if os.path.isdir(f'{fpath}/{d}')]
    dates.reverse()

    # Generate the plots
    SO2graphJSON = generate_map(fpath, date_to_plot, 'SO2', 'SO2 SCD',
                                'viridis', [0, 2e18])
    INTgraphJSON = generate_map(fpath, date_to_plot, 'int_av', 'Intensity',
                                'magma')

    return render_template('station_landing.html',
                           dates=dates,
                           data_date=date_to_plot,
                           SO2graphJSON=SO2graphJSON,
                           INTgraphJSON=INTgraphJSON,
                           station_name=station_name)


@app.route('/<station_name>/<date_to_plot>/')
def station_page(station_name, date_to_plot):
    """Generate the station page."""
    # Get the available dates
    dates = [d for d in os.listdir(fpath) if os.path.isdir(f'{fpath}/{d}')]
    dates.reverse()

    # Generate the plots
    SO2graphJSON = generate_map(fpath, date_to_plot, station_name, 'SO2',
                                'SO2 SCD', 'viridis', [0, 2e18])
    INTgraphJSON = generate_map(fpath, date_to_plot, station_name, 'int_av',
                                'Intensity', 'magma')

    return render_template('station_past_data.html',
                           date_to_plot=date_to_plot,
                           SO2graphJSON=SO2graphJSON,
                           INTgraphJSON=INTgraphJSON,
                           station_name=station_name)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

"""Generate scan plots."""
import os
import json
import plotly
import numpy as np
import pandas as pd
import plotly.express as px


def generate_map(fpath, date_to_plot, parameter, label, cmap='viridis',
                 limits=None):
    """Generate a map of a given value from the OpenSO2 results.

    Parameters
    ----------
    fpath : str
        The filepath to the Results folder on the server
    date_to_plot : str
        The date to look at, formatted as "YYYYY-MM-DD"
    name : str
        The station name
    parameter : str
        THe key of the parameter to plot from the OpenSO2 results files
    label : str
        The label to use on the colorbar for the parameter
    limits : tuple or None, optional
        The limits for the colormap. If None then they are automatically
        generated. Otherwise this gives the min and max values. Default is None
    """
    # Get the scan file names
    try:
        scan_fnames = os.listdir(f'{fpath}/{date_to_plot}/so2')
    except FileNotFoundError:
        return

    # Initialize the DataFrame
    df = pd.DataFrame(index=np.arange(len(scan_fnames)*99),
                      columns=['Scan Time [UTC]', 'Scan Angle', label])
    n = 0

    # Iterate through the files
    for i, fname in enumerate(scan_fnames):

        # Pull year, month and day from file name
        y = int(fname[:4])
        m = int(fname[4:6])
        d = int(fname[6:8])

        # Load the scan file, unpacking the angle and SO2 data
        try:
            scan_df = pd.read_csv(f'{fpath}/{date_to_plot}/so2/{fname}')
        except pd.errors.EmptyDataError:
            continue

        # Pull the time and convert to a timestamp
        for j, t in enumerate(scan_df['Time']):

            H = int(t)
            M = int((t - H)*60)
            S = int((t-H-M/60))*3600
            ts = pd.Timestamp(year=y, month=m, day=d, hour=H, minute=M,
                              second=S)

            # Set the next row
            df.iloc[n] = [ts, scan_df['Angle'].iloc[j],
                          scan_df[parameter].iloc[j]]

            # Iterate the counter
            n += 1

    # Remove row with nan times
    df = df[df['Scan Time [UTC]'].notna()]

    # Set nan values to zero
    df = df.fillna(0)

    # Generate the figure
    fig = px.scatter(df, x='Scan Time [UTC]', y='Scan Angle', color=label,
                     range_color=limits, color_continuous_scale=cmap)

    # Convert to a JSON to allow read into HTML
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

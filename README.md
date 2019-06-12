# Dash Visualization Application
This repository is for the Dash visualization app development. **Publicly available at: https://austin-gentrification-explorer.herokuapp.com/**

![Dash App Screenshot](https://github.gatech.edu/team-data-vis-analytics/project/blob/master/src/Dash%20App/Screenshot%20of%20Dash%20App.PNG)

## To launch the visualization app in a local environment

There are two ways to run this app locally after downloading the source code.

### Option 1: Using Anaconda command line

Make sure you have the following requirements installed:

- `pip install dash==0.39.0`  # The core dash backend
- `pip install dash-daq==0.1.0`  # DAQ components (newly open-sourced!)
- `pip install plotly` 

Launch the app by typing "python app.py". The app will start a local server, and you should be able to access the app in a browser at 127.0.0.1:8020.

Please refer to https://dash.plot.ly/installation for any Dash installation and starting-up questions.

### Option 2: Using a virtual environment

Make sure you have at least Python 3.7 installed on your local machine. Here are the steps to launch the app locally:

- `pip install virtualenv` # Install Python virtual environment
- `virtualenv venv` # creates a virtualenv called "venv"
- `venv/scripts/activate` # uses the virtualenv
- `pip install -r requirements.txt --no-index --find-links file:///tmp/packages` # installs  all requirements 
- `python app.py` # launches the app

Now you can follow the steps in Option 1 to access the app locally in a browser.

## To run "Austin GeoJSON Factory.ipynb" in Jupyter Notebook

This Jupyter notebook was created to generate all geojson files necessary for heatmap coloring and representative points within each tract for the visualization app.

All files created were saved in the "data" folder.

Make sure you have the following requirements installed:

Use conda:
- `conda install -c conda-forge geopandas` # GeoPandas for manipulating geo-data frame.

Use pip:
- `pip install shapely` # Python package for geometric object manipulation. 

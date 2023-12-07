import tempfile
from flask import Flask, jsonify, render_template, send_file
import pandas as pd
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import calendar

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error

import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(6,6))
ax=sns.set_style(style="ticks")


app = Flask(__name__)

# uber_df = pd.read_csv("./uberdata/My Uber Drives - 2016.csv")

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/uberdf', methods=['GET', 'POST'])
def uberdf():
    uber_df = pd.read_csv("./uberdata/My Uber Drives - 2016.csv")
    uber_df.columns = uber_df.columns.str.replace("*","")
    uber_df = uber_df.dropna()
    return uber_df


@app.route('/summary', methods=['GET','POST'])
def summary():
    total_trips = len(uberdf())
    average_distance = uberdf()['MILES'].mean()
    # Calculate other statistics as needed
    return render_template('summary.html', total_trips=total_trips, average_distance=average_distance)
    # return f"Total trips: {total_trips}, Average distance: {average_distance:.2f} miles"

@app.route('/uberdata', methods=['GET', 'POST'])
def uberdata():
    summary_uberdf = uberdf()
    return summary_uberdf.to_html()

@app.route('/extractfeature', methods=['GET', 'POST'])
def extractfeature():
    # set string as datetime format
    descride_uber_df = uberdf().describe()
    return descride_uber_df.to_html()

@app.route('/heatmap', methods=['GET', 'POST'])
def heatmap():
    # Selecting numerical columns for the heatmap
    numeric_columns = ['MILES', 'HOUR', 'DAY', 'MONTH', 'DAY_OF_WEEK', 'DURATION']

    # Calculating correlation matrix
    correlation_matrix = uberdf()[numeric_columns].corr()

    # Creating the heatmap plot
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)

    plt.title('Correlation Heatmap of Uber Data')
    
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()

    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')

@app.route('/category', methods=['GET', 'POST'])
def category():
    plt.title('Category trip of Uber Data')
    sns.countplot(x='CATEGORY',data=uberdf())
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')

@app.route('/purpose', methods=['GET', 'POST'])
def purpose():
    plt.title('purpose Uber trip')
    sns.countplot(x='PURPOSE',data=uberdf())
    plt.xticks(rotation=90)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')


@app.route('/mile', methods=['GET', 'POST'])
def mile():
    plt.title('Mile Uber trip')
    uberdf()['MILES'].plot.hist()
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')

@app.route('/tripduration', methods=['GET', 'POST'])
def tripduration():
    plt.hist(uberdf()['DURATION'], bins=22, color='blue')
    plt.xlabel('Duration (Minutes)')
    plt.ylabel('Frequency')
    plt.title('Distribution of trip Durations')
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')

@app.route('/purposeacrosscategory', methods=['GET', 'POST'])
def purposeacrosscategory():
    sns.countplot(data=uberdf(), x=uberdf()['CATEGORY'], hue=uberdf()['PURPOSE'])
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Trip Purposes by Category')
    plt.legend(title='Purpose')
    
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')

@app.route('/tripdurationsovertime', methods=['GET', 'POST'])
def tripdurationsovertime():
    # Plotting trip durations over time
    plt.plot(uberdf()['START_DATE'], uberdf()['DURATION'], marker='o', linestyle='-')
    plt.xlabel('Start Date')
    plt.ylabel('Duration (minutes)')
    plt.title('Trip Durations Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')

@app.route('/numberoftrip', methods=['GET', 'POST'])
def numberoftrip():
    uberdf()['DAY_NAME'].value_counts().plot(kind='bar')
    plt.xlabel("Week Days")
    plt.ylabel("Freq")
    plt.title("number of trips vs days")
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')

@app.route('/correlationmile', methods=['GET', 'POST'])
def correlationmile():
    plt.scatter(uberdf()['MILES'], uberdf()['DURATION'])
    plt.xlabel('Distance Commuted')
    plt.ylabel('Time to commute')
    plt.title('Correlation between distance(MILES) and Duration')
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name)
    plt.close()
    # Return the image file as response
    return send_file(temp_file.name, mimetype='image/png')






if __name__ == '__main__':
    app.run()

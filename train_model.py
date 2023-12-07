import pandas as pd
from sklearn.cluster import KMeans
import joblib

# Load Uber data
uber_df = pd.read_csv('.uberdata/My Uber Drives - 2016.csv') 

# Data preprocessing and feature selection
segment_data = uber_df[['MILES', 'DURATION', 'PURPOSE']] 

# Train K-means clustering model
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(segment_data)

# Save the trained model
joblib.dump(kmeans, 'model/kmeans_model.pkl')  

# Importing modules and libraries
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Loading training data source
data = pd.read_csv("data.csv")
texts = data["text"]

# Vectorizing the training data
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(texts)

print(vectors)
# Training the data on the DBSCAN algorithm
dbscan = DBSCAN(eps=1.0, min_samples=5)
dbscan.fit(vectors)

# Collecting data labels and coordinates for plotting
cluster_labels = dbscan.labels_
coords = vectors.toarray()

# Collecting clusters informations
no_clusters = len(np.unique(cluster_labels) )
no_noise = np.sum(np.array(cluster_labels) == -1, axis=0)

print('Estimated no. of clusters: %d' % no_clusters)
print('Estimated no. of noise points: %d' % no_noise)
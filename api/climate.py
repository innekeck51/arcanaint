import numpy as np
import pandas as pd
import seaborn as sns
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
from scipy import stats
from bayes_opt import BayesianOptimization
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class ClimateAnalyzer():
    paramsKM = {
        'km_n_init': (1, 50.),
        'km_max_iter': (1, 500.),
        'km_tol': (0.0001, 1.),
        'km_n_clusters': (3, 6)
    }

    df = {}

    def __init__(self):
        matplotlib.use("Agg")

    def objectiveKM(self, km_n_init, km_max_iter, km_tol, km_n_clusters):
        km_n_init = int(np.floor(km_n_init))
        km_max_iter = int(np.floor(km_max_iter))
        km_n_clusters = int(np.floor(km_n_clusters))

        kmeans = KMeans(n_clusters=km_n_clusters, init='k-means++', n_init=km_n_init, max_iter=km_max_iter, tol=km_tol,
                        precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=None, algorithm='auto')
        preds = kmeans.fit_predict(self.df)

        score = silhouette_score(self.df, preds)

        # karena bayesopt perlu objective yg greater is better
        return score

    def handle_file_upload(self, f, inputParam):
        self.df = pd.read_excel(f, engine='openpyxl')
        inputTable = inputParam.split(',')
        df = self.df[inputTable]
        df = df.replace(8888.0, np.nan)
        df = df.replace(9999.0, np.nan)

        imputer = KNNImputer(n_neighbors=100, weights='uniform',
                             metric='nan_euclidean')
        df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(df)
        df_scaled = DataFrame(scaled, columns=df.columns)
        df = df_scaled
        z_scores = stats.zscore(df)
        abs_z_scores = np.abs(z_scores)
        filtered_entries = (abs_z_scores < 3).all(axis=1)
        self.df = df[filtered_entries]

        optimizer = BayesianOptimization(
            self.objectiveKM, pbounds=self.paramsKM, random_state=99)
        optimizer.maximize(init_points=50, n_iter=1)

        result = optimizer.max['params']
        km_n_init = result['km_n_init']
        km_max_iter = result['km_max_iter']
        km_tol = result['km_tol']
        km_n_clusters = result['km_n_clusters']

        km_n_init = int(np.floor(km_n_init))
        km_max_iter = int(np.floor(km_max_iter))
        km_n_clusters = int(np.floor(km_n_clusters))

        kmeans = KMeans(n_clusters=km_n_clusters, init='k-means++', n_init=km_n_init, max_iter=km_max_iter, tol=km_tol,
                        precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=None, algorithm='auto')
        result = KMeans(n_clusters=km_n_clusters).fit(self.df)

        self.df['cluster'] = result.labels_
        buf = BytesIO()
        plt.figure(figsize=(10, 10))
        sns.pairplot(self.df, hue='cluster')
        plt.savefig(buf, format='png')
        return buf

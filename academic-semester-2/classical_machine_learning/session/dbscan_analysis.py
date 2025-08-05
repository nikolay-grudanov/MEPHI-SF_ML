import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    df = pd.read_csv('Run200_Wave_0_1.txt', sep=' ', header=None, skipinitialspace=True)
    signals = df.drop([0, 1, 2, 3, 504], axis=1)
    signals.columns = list(range(500))
    
    processed_data = 2**14 - signals - 1550
    processed_data['max'] = processed_data.max(axis=1)
    processed_data['amplitude'] = processed_data['max'] - processed_data.iloc[:, :-1].min(axis=1)
    processed_data['square'] = processed_data.iloc[:, :-2].sum(axis=1)
    
    X = processed_data[['amplitude', 'square']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    return X_pca, processed_data

def evaluate_dbscan(X_pca):
    results = []
    
    eps_values = np.arange(0.05, 0.5, 0.05)
    min_samples_values = range(2, 15)
    
    for eps in eps_values:
        for min_samples in min_samples_values:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            clusters = dbscan.fit_predict(X_pca)
            
            unique_clusters = len(set(clusters))
            noise_ratio = np.sum(clusters == -1) / len(clusters)
            
            if unique_clusters > 1 and noise_ratio < 0.9:
                try:
                    sil = silhouette_score(X_pca, clusters)
                    ch = calinski_harabasz_score(X_pca, clusters)
                    db = davies_bouldin_score(X_pca, clusters)
                    
                    results.append({
                        'eps': eps,
                        'min_samples': min_samples,
                        'n_clusters': unique_clusters,
                        'noise_ratio': noise_ratio,
                        'silhouette': sil,
                        'calinski_harabasz': ch,
                        'davies_bouldin': db
                    })
                except:
                    continue
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('silhouette', ascending=False)
    
    return results_df

def visualize_best_clustering(X_pca, best_params):
    dbscan = DBSCAN(eps=best_params['eps'], min_samples=best_params['min_samples'])
    clusters = dbscan.fit_predict(X_pca)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', s=5)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title(f'DBSCAN Clustering (eps={best_params["eps"]}, min_samples={best_params["min_samples"]})')
    plt.colorbar(label='Cluster')
    plt.grid(True)
    plt.savefig('best_dbscan_clustering.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    X_pca, processed_data = load_and_preprocess_data()
    results = evaluate_dbscan(X_pca)
    results.to_csv('dbscan_results.csv', index=False)
    
    best_params = results.iloc[0].to_dict()
    best_params['min_samples'] = int(best_params['min_samples'])
    
    visualize_best_clustering(X_pca, best_params)
    
    print("DBSCAN parameter evaluation complete.")
    print(f"Best parameters: eps={best_params['eps']}, min_samples={best_params['min_samples']}")
    print(f"Best silhouette score: {best_params['silhouette']:.4f}")
    print("Results saved to dbscan_results.csv")
    print("Visualization saved to best_dbscan_clustering.png")

if __name__ == "__main__":
    main()
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.ensemble import RandomForestClassifier
from scipy.signal import find_peaks
from scipy import stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Feature engineering functions
def calculate_features(signal):
    """Calculate various features from a signal."""
    # Basic statistics
    max_val = np.max(signal)
    min_val = np.min(signal)
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    
    # Amplitude and range
    amplitude = max_val - min_val
    
    # Statistical moments
    skew = stats.skew(signal)
    kurt = stats.kurtosis(signal)
    
    # Time-domain features
    max_idx = np.argmax(signal)
    rise_time = max_idx
    
    # Width at half maximum
    half_max = max_val / 2
    above_half = signal >= half_max
    fwhm = np.sum(above_half)
    
    # Energy and area
    energy = np.sum(signal**2)
    area = np.trapezoid(signal)
    
    # Peak features
    peaks, _ = find_peaks(signal, height=0.1*amplitude, distance=50)
    n_peaks = len(peaks)
    
    # Frequency domain features (simplified)
    fft_vals = np.abs(np.fft.fft(signal))
    dom_freq = np.argmax(fft_vals[:len(signal)//2])
    
    return {
        'max': max_val,
        'min': min_val,
        'mean': mean_val,
        'std': std_val,
        'amplitude': amplitude,
        'skew': skew,
        'kurt': kurt,
        'rise_time': rise_time,
        'fwhm': fwhm,
        'energy': energy,
        'area': area,
        'n_peaks': n_peaks,
        'dom_freq': dom_freq
    }

# Load and preprocess data
def load_and_preprocess_data():
    # Read data
    df = pd.read_csv('Run200_Wave_0_1.txt', sep=' ', header=None, skipinitialspace=True)
    signals = df.drop([0, 1, 2, 3, 504], axis=1)
    signals.columns = list(range(500))
    
    # Process data
    processed_data = 2**14 - signals - 1550
    
    # Calculate features
    features = []
    for i, signal in processed_data.iterrows():
        signal_features = calculate_features(signal.values)
        features.append(signal_features)
    
    features_df = pd.DataFrame(features)
    
    # Identify special cases
    max_signals = processed_data.max(axis=1) == 14834
    multi_peak = features_df['n_peaks'] > 1
    
    return processed_data, features_df, max_signals, multi_peak

# Evaluate clustering methods
def evaluate_clustering(X, true_labels=None):
    results = []
    
    # Standardize data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # KMeans
    for n_clusters in [2, 3, 4]:
        kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
        labels = kmeans.fit_predict(X_pca)
        
        sil = silhouette_score(X_pca, labels)
        ch = calinski_harabasz_score(X_pca, labels)
        db = davies_bouldin_score(X_pca, labels)
        
        results.append({
            'method': 'KMeans',
            'n_clusters': n_clusters,
            'silhouette': sil,
            'calinski_harabasz': ch,
            'davies_bouldin': db
        })
    
    # Agglomerative
    for n_clusters in [2, 3, 4]:
        agg = AgglomerativeClustering(n_clusters=n_clusters)
        labels = agg.fit_predict(X_pca)
        
        sil = silhouette_score(X_pca, labels)
        ch = calinski_harabasz_score(X_pca, labels)
        db = davies_bouldin_score(X_pca, labels)
        
        results.append({
            'method': 'Agglomerative',
            'n_clusters': n_clusters,
            'silhouette': sil,
            'calinski_harabasz': ch,
            'davies_bouldin': db
        })
    
    # DBSCAN
    for eps in [0.1, 0.2, 0.3, 0.4]:
        for min_samples in [3, 5, 7]:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            labels = dbscan.fit_predict(X_pca)
            
            # Only evaluate if we have more than one cluster and less than 90% noise
            unique_clusters = len(set(labels))
            noise_ratio = np.sum(labels == -1) / len(labels)
            
            if unique_clusters > 1 and noise_ratio < 0.9:
                sil = silhouette_score(X_pca, labels)
                ch = calinski_harabasz_score(X_pca, labels)
                db = davies_bouldin_score(X_pca, labels)
                
                results.append({
                    'method': 'DBSCAN',
                    'eps': eps,
                    'min_samples': min_samples,
                    'n_clusters': unique_clusters,
                    'noise_ratio': noise_ratio,
                    'silhouette': sil,
                    'calinski_harabasz': ch,
                    'davies_bouldin': db
                })
    
    # Gaussian Mixture
    for n_components in [2, 3, 4]:
        gmm = GaussianMixture(n_components=n_components, random_state=42)
        labels = gmm.fit_predict(X_pca)
        
        sil = silhouette_score(X_pca, labels)
        ch = calinski_harabasz_score(X_pca, labels)
        db = davies_bouldin_score(X_pca, labels)
        
        results.append({
            'method': 'GaussianMixture',
            'n_components': n_components,
            'silhouette': sil,
            'calinski_harabasz': ch,
            'davies_bouldin': db
        })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('silhouette', ascending=False)
    
    return results_df, X_pca

# Main function
def main():
    # Load and preprocess data
    processed_data, features_df, max_signals, multi_peak = load_and_preprocess_data()
    
    # Save features for reference
    features_df.to_csv('engineered_features.csv', index=False)
    
    # Evaluate clustering with different feature sets
    print("Evaluating clustering with amplitude and area features...")
    results1, X_pca1 = evaluate_clustering(features_df[['amplitude', 'area']])
    results1.to_csv('clustering_results_amplitude_area.csv', index=False)
    
    print("Evaluating clustering with all features...")
    results2, X_pca2 = evaluate_clustering(features_df)
    results2.to_csv('clustering_results_all_features.csv', index=False)
    
    # Print best results
    print("\nBest results with amplitude and area features:")
    print(results1.head(3))
    
    print("\nBest results with all features:")
    print(results2.head(3))
    
    # Visualize best clustering from each approach
    # Best from amplitude and area
    best1 = results1.iloc[0]
    if best1['method'] == 'KMeans':
        model = KMeans(n_clusters=best1['n_clusters'], n_init=10, random_state=42)
    elif best1['method'] == 'Agglomerative':
        model = AgglomerativeClustering(n_clusters=best1['n_clusters'])
    elif best1['method'] == 'DBSCAN':
        model = DBSCAN(eps=best1['eps'], min_samples=best1['min_samples'])
    else:
        model = GaussianMixture(n_components=best1['n_components'], random_state=42)
    
    labels1 = model.fit_predict(X_pca1)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca1[:, 0], X_pca1[:, 1], c=labels1, cmap='viridis', s=5)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title(f'Best Clustering (Amplitude + Area): {best1["method"]}')
    plt.colorbar(label='Cluster')
    plt.grid(True)
    plt.savefig('best_clustering_amplitude_area.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Best from all features
    best2 = results2.iloc[0]
    if best2['method'] == 'KMeans':
        model = KMeans(n_clusters=best2['n_clusters'], n_init=10, random_state=42)
    elif best2['method'] == 'Agglomerative':
        model = AgglomerativeClustering(n_clusters=best2['n_clusters'])
    elif best2['method'] == 'DBSCAN':
        model = DBSCAN(eps=best2['eps'], min_samples=best2['min_samples'])
    else:
        model = GaussianMixture(n_components=best2['n_components'], random_state=42)
    
    labels2 = model.fit_predict(X_pca2)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca2[:, 0], X_pca2[:, 1], c=labels2, cmap='viridis', s=5)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title(f'Best Clustering (All Features): {best2["method"]}')
    plt.colorbar(label='Cluster')
    plt.grid(True)
    plt.savefig('best_clustering_all_features.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nAnalysis complete. Results saved to CSV files and visualizations saved as PNG.")

if __name__ == "__main__":
    main()
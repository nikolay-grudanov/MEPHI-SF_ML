import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from scipy.signal import find_peaks
from scipy import stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Feature engineering functions
def calculate_features(signal):
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
    area = np.sum(signal)  # Simplified area calculation
    
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
        if i % 1000 == 0:
            print(f'Processing signal {i}/{len(processed_data)}')
        signal_features = calculate_features(signal.values)
        features.append(signal_features)
    
    features_df = pd.DataFrame(features)
    
    # Identify special cases
    max_signals = processed_data.max(axis=1) == 14834
    
    return processed_data, features_df, max_signals

# Main function
def main():
    # Load and preprocess data
    processed_data, features_df, max_signals = load_and_preprocess_data()
    
    # Standardize data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features_df)
    
    # Apply PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Use the best DBSCAN parameters from our analysis
    eps = 0.4
    min_samples = 5  # This is an integer
    
    # Create and fit the model
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(X_pca)
    
    # Handle special cases
    # Mark saturated signals as noise (cluster -1)
    clusters[max_signals.values] = -1
    
    # Create submission format
    submission = pd.DataFrame({
        'index': np.arange(len(clusters)),
        'cluster': clusters
    })
    
    # Save submission
    submission.to_csv('final_submission.csv', index=False)
    
    # Visualize the clustering
    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', s=5)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title(f'Final Clustering: DBSCAN (eps={eps}, min_samples={min_samples})')
    plt.colorbar(label='Cluster')
    plt.grid(True)
    plt.savefig('final_clustering.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Print summary
    unique, counts = np.unique(clusters, return_counts=True)
    print('\nClustering complete. Results:')
    for label, count in zip(unique, counts):
        print(f'Cluster {label}: {count} signals')
    
    print('\nSubmission saved to final_submission.csv')
    print('Visualization saved to final_clustering.png')

if __name__ == "__main__":
    main()
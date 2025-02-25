import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lecroyparser import ScopeData
from ripser import ripser
from persim import plot_diagrams
from tqdm import tqdm

# Set directories (adjust paths as needed)
raw_dir = "/share/blondin/jrfloren/data/raw/pfrc/data/20200309/pressure/"
# Create an output directory for TDA analysis within processed data:
output_dir = "/share/blondin/jrfloren/data/processed/pressure_analysis/"
stats_dir = os.path.join(output_dir, "stats")
plots_dir = os.path.join(output_dir, "plots")
os.makedirs(stats_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

def process_trc_file(file_path, sparse=None):
    """
    Process a Lecroy .trc file using lecroyparser.
    
    Parameters:
      file_path (str): Path to the .trc file.
      sparse (int): Optional parameter to limit the number of samples.
      
    Returns:
      DataFrame: A pandas DataFrame with 'time' and 'amplitude' columns,
                 or None if an error occurs.
    """
    try:
        # Create a ScopeData object; if sparse is provided, limit samples.
        data = ScopeData(file_path, parseAll=False, sparse=sparse) if sparse else ScopeData(file_path)
        # Extract time and waveform data
        df = pd.DataFrame({
            'time': data.x,
            'amplitude': data.y
        })
        return df
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def delay_embedding(time_series, dimension=3, delay=10):
    """
    Perform a delay (Takens) embedding on a 1D time series.
    
    Parameters:
      time_series (np.array): 1D array of data.
      dimension (int): Embedding dimension.
      delay (int): Delay (in samples) between coordinates.
      
    Returns:
      np.array: Embedded point cloud of shape (n_points, dimension).
    """
    n = len(time_series)
    if n - (dimension - 1) * delay <= 0:
        raise ValueError("Time series is too short for the given dimension and delay")
    embedded = np.array([time_series[i : n - (dimension - 1) * delay + i : delay] 
                         for i in range(dimension)]).T
    return embedded

def analyze_file_tda(file_path, embedding_dim=3, delay=10, sparse=1000):
    """
    Process a .trc file, create a delay embedding from the amplitude,
    compute persistent homology, and return the persistence diagrams and statistics.
    
    Parameters:
      file_path (str): Path to the .trc file.
      embedding_dim (int): Embedding dimension for delay embedding.
      delay (int): Delay (in samples) for embedding.
      sparse (int): Optional sample limit.
      
    Returns:
      dict: A dictionary containing:
            - 'diagrams': the persistence diagrams from ripser.
            - 'raw_stats': descriptive statistics of the raw amplitude time-series.
            - 'embedded_stats': descriptive statistics of the embedded point cloud.
    """
    df = process_trc_file(file_path, sparse=sparse)
    if df is None:
        return None
    
    # Compute descriptive statistics for the raw time series
    raw_stats = df['amplitude'].describe()
    
    # Delay embedding on the amplitude data
    try:
        embedded = delay_embedding(df['amplitude'].values, dimension=embedding_dim, delay=delay)
    except Exception as e:
        print(f"Error creating delay embedding for {file_path}: {e}")
        return None
    
    # Compute descriptive statistics for the embedded point cloud
    embedded_df = pd.DataFrame(embedded, columns=[f"dim_{i+1}" for i in range(embedding_dim)])
    embedded_stats = embedded_df.describe()
    
    # Compute persistent homology on the embedded data
    result = ripser(embedded)
    diagrams = result['dgms']
    
    return {'diagrams': diagrams, 'raw_stats': raw_stats, 'embedded_stats': embedded_stats}

def save_analysis_results(file_path, analysis_results):
    """
    Save the analysis results:
      - Persistence diagram plot as a PNG file.
      - Descriptive statistics for raw and embedded data as CSV files.
    Filenames are based on the original .trc filename.
    """
    base_name = os.path.basename(file_path).replace('.trc', '')
    
    # Save persistence diagram plot
    plt.figure(figsize=(8, 4))
    plot_diagrams(analysis_results['diagrams'], show=False)
    plot_filename = os.path.join(plots_dir, f"{base_name}_tda.png")
    plt.title(f"Persistence Diagram for {base_name}")
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close()
    print(f"Saved TDA plot to {plot_filename}")
    
    # Save raw descriptive statistics
    raw_stats_filename = os.path.join(stats_dir, f"{base_name}_raw_stats.csv")
    analysis_results['raw_stats'].to_csv(raw_stats_filename)
    print(f"Saved raw stats to {raw_stats_filename}")
    
    # Save embedded descriptive statistics
    embedded_stats_filename = os.path.join(stats_dir, f"{base_name}_embedded_stats.csv")
    analysis_results['embedded_stats'].to_csv(embedded_stats_filename)
    print(f"Saved embedded stats to {embedded_stats_filename}")

if __name__ == "__main__":
    # Get list of all .trc files in the raw directory
    trc_files = [os.path.join(raw_dir, f) for f in os.listdir(raw_dir) if f.endswith(".trc")]
    print(f"Found {len(trc_files)} .trc files in {raw_dir}")
    
    # Process a sample file first
    sample_file = trc_files[0]
    print(f"Analyzing TDA for sample file: {sample_file}")
    analysis_results = analyze_file_tda(sample_file, embedding_dim=3, delay=10, sparse=1000)
    
    if analysis_results:
        save_analysis_results(sample_file, analysis_results)
    else:
        print("Sample analysis failed.")
    
    # Optionally, iterate over all files
    for file in tqdm(trc_files, desc="Processing TRC files for TDA"):
        results = analyze_file_tda(file, embedding_dim=3, delay=10, sparse=1000)
        if results:
            save_analysis_results(file, results)

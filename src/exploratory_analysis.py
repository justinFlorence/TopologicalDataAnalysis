import os
import pandas as pd
import matplotlib.pyplot as plt
from lecroyparser import ScopeData
from tqdm import tqdm

# Define the directory containing your pressure .trc files
data_dir = "/share/blondin/jrfloren/data/raw/pfrc/data/20200309/pressure/"

# Get a list of all .trc files in the directory
trc_files = [f for f in os.listdir(data_dir) if f.endswith(".trc")]
print(f"Found {len(trc_files)} .trc files in {data_dir}")

def process_trc_file(file_path, sparse=None):
    """
    Processes a Lecroy .trc file using lecroyparser.
    Optionally, the 'sparse' parameter limits the number of samples.
    
    Returns:
      A DataFrame with columns 'time' and 'amplitude' or None on error.
    """
    try:
        # Create a ScopeData object.
        # If you want to limit the number of samples, pass the sparse parameter.
        if sparse:
            data = ScopeData(file_path, parseAll=False, sparse=sparse)
        else:
            data = ScopeData(file_path)
        
        # Extract time and waveform data (attributes 'x' and 'y')
        time = data.x  # timebase array
        waveform = data.y  # waveform (amplitude) array

        # Create a DataFrame
        df = pd.DataFrame({
            'time': time,
            'amplitude': waveform
        })
        return df
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Process a single sample file and plot its waveform
if trc_files:
    sample_file = os.path.join(data_dir, trc_files[0])
    print(f"\nPreviewing sample file: {sample_file}")
    sample_df = process_trc_file(sample_file, sparse=1000)  # limit samples if desired
    if sample_df is not None:
        plt.figure(figsize=(10, 4))
        plt.plot(sample_df['time'], sample_df['amplitude'], label="Pressure Trace")
        plt.title(f"Pressure Data from {os.path.basename(sample_file)}")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()
        plt.show()
        print("Sample statistics:")
        print(sample_df.describe())
    else:
        print("Could not load sample file.")

# Create a directory to store statistics, if desired
stats_dir = os.path.join(data_dir, "stats")
os.makedirs(stats_dir, exist_ok=True)

# Iterate over all files, process them, and compute basic stats
all_stats = {}
print("\nProcessing all .trc files for descriptive statistics:")
for filename in tqdm(trc_files):
    full_path = os.path.join(data_dir, filename)
    df = process_trc_file(full_path, sparse=1000)  # adjust sparse as needed
    if df is not None:
        stats = df.describe()
        all_stats[filename] = stats
        # Save the statistics to a CSV file for future reference
        stats_filename = filename.replace('.trc', '_stats.csv')
        stats.to_csv(os.path.join(stats_dir, stats_filename))
    else:
        print(f"Skipping file: {filename}")

print("\nExploratory analysis complete.")

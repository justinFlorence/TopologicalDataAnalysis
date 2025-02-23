# TopologyProject

This repository contains code, data processing scripts, and notebooks for performing computational topological analysis on plasma data from the Princeton Field Reversal Configuration (PFRC) Experiment. The goal of this project is to extract topological features from the experimental plasma diagnostics and investigate the connectivity and dynamics of the plasma through persistent homology.

## Directory Structure

Below is the recommended structure for the project:

```
TopologyProject/
├── Data/
│   ├── raw/                # Raw experimental data (Excel, HDF5, TXT, TRC, MCA, PDF files)
│   ├── processed/          # Processed data (cleaned and organized for analysis)
│   └── README_data.md      # Documentation on the dataset, file formats, and processing steps
├── notebooks/              # Jupyter notebooks for exploratory analysis and visualization
├── src/                    # Source code for data processing, topological analysis, and machine learning
│   ├── data_processing.py  # Scripts to load, clean, and preprocess the raw data
│   ├── topology_analysis.py# Code to construct simplicial complexes and compute persistent homology
│   └── ml_pipeline.py      # (Optional) Machine learning pipeline for classifying plasma states
├── docs/                   # Additional documentation, literature, and technical notes
├── tests/                  # Unit tests for the code in the src directory
├── requirements.txt        # List of Python dependencies
├── README.md               # This file (project overview, setup instructions, etc.)
└── LICENSE                 # License file (e.g., MIT License)
```

## Getting Started

### Prerequisites

- Python 3.8 or higher  
- Recommended Python libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `ripser`
  - `persim`
  - `scikit-learn`
  - `jupyter`

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

### Data

- **Raw Data:**  
  The `Data/raw/` directory should contain the experimental files from the PFRC experiment. These include Excel, HDF5, TXT, TRC, MCA files, and even scanned PDF documents from oscilloscope outputs.

- **Processed Data:**  
  Use the scripts in the `src/data_processing.py` file to convert and clean the raw data, saving the output to `Data/processed/`.

### Usage

1. **Data Processing:**  
   Run the data processing script to load and preprocess your raw plasma data:
   ```bash
   python src/data_processing.py
   ```

2. **Topological Analysis:**  
   Use the topology analysis script to build a Vietoris–Rips complex and compute persistent homology:
   ```bash
   python src/topology_analysis.py
   ```

3. **Exploratory Notebooks:**  
   For an interactive exploration of the data and analysis, open the Jupyter notebooks in the `notebooks/` directory:
   ```bash
   jupyter notebook notebooks/
   ```

4. **Machine Learning Pipeline (Optional):**  
   If you have labeled data (e.g., stable vs. unstable plasma states), you can run the machine learning pipeline:
   ```bash
   python src/ml_pipeline.py
   ```

## Project Overview

- **Objective:**  
  To analyze the structure and evolution of plasma data using computational topology. We aim to:
  - Preprocess experimental plasma data.
  - Construct simplicial complexes from the data.
  - Compute persistence diagrams to identify robust topological features.
  - (Optionally) Develop a machine learning model to classify plasma behavior based on topological features.

- **Background:**  
  The PFRC experiment at PPPL collects extensive diagnostic data on plasma behavior in a field-reversed configuration. This project leverages these diverse datasets to investigate the "shape" of the data across multiple scales using techniques from topological data analysis.

## Contributing

Contributions are welcome! If you find bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions, feedback, or collaboration, please contact me about potential new directions at jrfloren@ncsu.edu.

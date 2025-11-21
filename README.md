# Nanolaminate Analysis Code

This repository contains Python code and Jupyter notebooks for analyzing 4D-STEM (Scanning Transmission Electron Microscopy) data from amorphous/amorphous nanolaminates. The code is used in the publication: "Interface-mediated softening and deformation mechanics in amorphous/amorphous nanolaminates, Scripta Mat., 2026".

## Repository Contents

- **Density Map Notebooks**: `Density_map_40nm.ipynb`, `Density_map_4nm.ipynb`, `Density_map_SiO2.ipynb` - Jupyter notebooks for computing radial density maps from 4D-STEM diffraction patterns.
- **Line Profile Analysis**: `HAADF_Line_Profile_Combined.ipynb` - Notebook for analyzing High-Angle Annular Dark Field (HAADF) STEM line profiles.
- **Data Folder**: Contains CSV files with experimental line profile data.

## Data Access

The raw 4D-STEM data files (including precession diffraction data) are available at Zenodo: [10.5281/zenodo.17673178](https://doi.org/10.5281/zenodo.17673178).

## Requirements

- Python 3.x
- Required packages: py4DSTEM, hyperspy, numpy, matplotlib
- The raw data file `1120_file.h5` (1.4 GB) is required to run the density map notebooks

## Usage

1. Download the raw data from Zenodo.
2. Place the data files in the repository root.
3. Run the Jupyter notebooks in order.

## License

This code is provided as-is for academic and research purposes.
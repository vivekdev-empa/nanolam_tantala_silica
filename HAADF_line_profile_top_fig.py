import pandas as pd
import numpy as np
from scipy.signal import find_peaks, savgol_filter
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Read the CSV file using relative path
csv_path = script_dir / 'data' / '20250215 1719 710 kx 140 nm HAADF STEM-lp01.csv'
df = pd.read_csv(csv_path, skiprows=2)
df.columns = ['Position', 'Intensity']

# Convert position to nanometers (from meters)
df['Position'] = df['Position'] * 1e9  # Convert to nm

# Apply Savitzky-Golay filter to smooth the data
window_length = 7  # Reduced window for finer features
polynomial_order = 3
smoothed_intensity = savgol_filter(df['Intensity'], window_length, polynomial_order)

# Find peaks with parameters adjusted for 2-3 nm spacing
points_per_nm = len(df) / (df['Position'].max() - df['Position'].min())
min_distance = int(1.5 * points_per_nm)  # Minimum 1.5 nm between peaks

peaks, peak_properties = find_peaks(smoothed_intensity, 
                                  distance=min_distance,  
                                  prominence=500,  
                                  width=(int(points_per_nm), int(4*points_per_nm)))

# Calculate interlayer distances
peak_positions = df['Position'].iloc[peaks]
interlayer_distances = np.diff(peak_positions)

# Create figure with subplots
plt.figure(figsize=(6, 10))

# Create layer indices (starting from 0 to len(interlayer_distances)-1)
layer_indices = np.arange(len(interlayer_distances))

#layer_numbers = np.arange(len(interlayer_distances)-1, -1, -1)  # Reversed layer numbers
plt.plot(interlayer_distances, layer_indices, 'bo-', alpha=0.5)

# Add trend line
z = np.polyfit(interlayer_distances, layer_indices, 1)
p = np.poly1d(z)
plt.plot(interlayer_distances, p(interlayer_distances), 'r-')


plt.gca().invert_yaxis()

plt.ylabel('Layer Number', fontsize=26)
plt.xlabel('Interlayer Distance (nm)', fontsize=26)
plt.grid(True)

# Get current x-tick locations and set every other one
current_ticks = plt.xticks()[0]  # Get current tick locations
plt.xticks(current_ticks[::2], fontsize=26)  # Set every other tick
plt.yticks(fontsize=26)

plt.tight_layout()
# Update output path to save in the same directory as the script
output_path = script_dir / 'HAADF_Line_profile_4nm_top_fig02.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
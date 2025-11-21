import pandas as pd
import numpy as np
from scipy.signal import find_peaks, savgol_filter
import matplotlib.pyplot as plt
from pathlib import Path

def process_and_plot(csv_filename, output_filename, plot_title, use_reversed_layers=False):
    """
    Process HAADF line profile data and create interlayer distance plot.
    
    Parameters:
    -----------
    csv_filename : str
        Name of the CSV file in the data folder
    output_filename : str
        Name for the output PNG file
    plot_title : str
        Title for the plot (can be empty)
    use_reversed_layers : bool
        If True, use layer_indices starting from 0 (for top), 
        if False, use layer_indices starting from 1 (for bottom)
    """
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Read the CSV file using relative path
    csv_path = script_dir / 'data' / csv_filename
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
    
    # Create figure
    plt.figure(figsize=(6, 10))
    
    # Create layer indices based on the use_reversed_layers flag
    if use_reversed_layers:
        # Top figure: starts from 0
        layer_indices = np.arange(len(interlayer_distances))
        plt.plot(interlayer_distances, layer_indices, 'bo-', alpha=0.5)
        
        # Add trend line (fit interlayer_distances vs layer_indices)
        z = np.polyfit(interlayer_distances, layer_indices, 1)
        p = np.poly1d(z)
        plt.plot(interlayer_distances, p(interlayer_distances), 'r-')
    else:
        # Bottom figure: starts from 1
        layer_indices = np.arange(1, len(interlayer_distances) + 1)
        plt.plot(interlayer_distances, layer_indices, 'bo-', alpha=0.5)
        
        # Fit the trend line with x and y swapped
        z = np.polyfit(layer_indices, interlayer_distances, 1)
        p = np.poly1d(z)
        
        # Create a sequence of points for the trend line
        y_line = np.linspace(min(layer_indices), max(layer_indices), 100)
        x_line = p(y_line)
        
        # Plot the trend line
        plt.plot(x_line, y_line, 'r-')
    
    plt.gca().invert_yaxis()
    
    plt.ylabel('Layer Number', fontsize=26)
    plt.xlabel('Interlayer Distance (nm)', fontsize=26)
    plt.grid(True)
    
    # Get current x-tick locations and set every other one
    current_ticks = plt.xticks()[0]  # Get current tick locations
    plt.xticks(current_ticks[::2], fontsize=26)  # Set every other tick
    plt.yticks(fontsize=26)
    
    plt.tight_layout()
    
    # Save figure using relative path
    output_path = script_dir / output_filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

# Process top figure
process_and_plot(
    csv_filename='20250215 1719 710 kx 140 nm HAADF STEM-lp01.csv',
    output_filename='HAADF_Line_profile_4nm_top_fig02.png',
    plot_title='Top',
    use_reversed_layers=True
)

# Process bottom figure
process_and_plot(
    csv_filename='20250215 1723 710 kx 140 nm HAADF STEM-lp01.csv',
    output_filename='HAADF_Line_profile_4nm_bottom_fig01.png',
    plot_title='Bottom',
    use_reversed_layers=False
)

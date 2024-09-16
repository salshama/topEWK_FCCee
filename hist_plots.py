# # importing required packages
# import uproot
# import matplotlib.pyplot as plt
# import glob
# import os
# 
# # determine xlabel based on histogram name
# def determine_xlabel(histogram_name):
# 
#     """
#     Determines the appropriate x-axis label based on keywords in the histogram name.
# 
#     Parameters:
#     - histogram_name: str, name of the histogram.
# 
#     Returns:
#     - xlabel: str, the x-axis label.
#     """
#     
#     # mapping keywords to xlabels
#     keyword_to_label = {
#         "energy": "Energy [GeV]",
#         "pt": "p$_T$ [GeV]",
#         "mass": "Mass [GeV]",
#         "eta": "$\eta$",
#         "phi": "$\phi$"
#     }
#     
#     # default
#     xlabel = "Value"
#     
#     # check for keywords in histogram name
#     for keyword, label in keyword_to_label.items():
#     
#         if keyword in histogram_name.lower():
#             xlabel = label
#             break
#     
#     return xlabel
# 
# # plotting histograms
# def read_and_draw_histogram(root_file, histogram_name):
#     
#     """
#     Reads a histogram from a .root file and draws it using matplotlib.
# 
#     Parameters:
#     - root_file: str, path to the .root file.
#     - histogram_name: str, name of the histogram to be extracted and plotted.
#     """
#     
#     with uproot.open(root_file) as file:
#         
#         # check if the histogram exists
#         if histogram_name in file:
#             
#             # access the histogram
#             histogram = file[histogram_name]
#             
#             # extract histogram data
#             hist_values = histogram.values()
#             bin_edges = histogram.axes[0].edges()
#             
#             # determining xlabel
#             xlabel = determine_xlabel(histogram_name)
#             
#             plt.figure(figsize=(8, 6))
#             plt.hist(bin_edges[:-1], bins=bin_edges, weights=hist_values, histtype='step', label=histogram_name)
#             plt.xlabel(xlabel)
#             plt.ylabel('Events')
#             plt.title(f'Histogram: {histogram_name} from {root_file}')
#             plt.legend()
#             plt.grid(True)
#             plt.show()
#             
#             # create a valid filename for the PDF and save it
#             output_filename = f"{os.path.splitext(os.path.basename(root_file))[0]}_{histogram_name}.pdf"
#             plt.savefig("/ceph/salshamaily/topEWK_FCCee/plots/"+output_filename)
#             
#             plt.close()
#             
#         else:
#             print(f"Histogram {histogram_name} not found in {root_file}.")
#     
# # processing multiple .root files        
# def process_multiple_files(root_files):
#     
#     """
#     Process multiple root files and draw all histograms found in each.
# 
#     Parameters:
#     - root_files: list of str, paths to the .root files.
#     """
#     
#     for root_file in root_files:
#         print(f'Processing file: {root_file}')
#         
#         with uproot.open(root_file) as file:
#             # list all objects in file and filter histograms
#             histogram_names = [key for key in file.keys() if file[key].classname.startswith("TH")]
#             
#             for hist_name in histogram_names:
#                 print(f'  - Drawing histogram: {hist_name}')
#                 read_and_draw_histogram(root_file, hist_name)
#                 
# # glob all .root files
# root_files = glob.glob('/ceph/salshamaily/topEWK_FCCee/root_hists/*.root')
# 
# # process files
# process_multiple_files(root_files)

# importing required packages
import uproot
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# determine xlabel based on histogram name
def determine_xlabel(histogram_name):

    """
    Determines the appropriate x-axis label based on keywords in the histogram name.
    Parameters:
    - histogram_name: str, name of the histogram.
    Returns:
    - xlabel: str, the x-axis label.
    """
    
    keyword_to_label = {
        "energy": "Energy [GeV]",
        "pt": "p$_T$ [GeV]",
        "mass": "Mass [GeV]",
        "eta": "$\eta$",
        "phi": "$\phi$"
    }
    
    xlabel = "Value"
    
    for keyword, label in keyword_to_label.items():
    
        if keyword in histogram_name.lower():
            xlabel = label
            
            break
            
    return xlabel

# classify the file based on the filename
def classify_file(file_name):

    """
    Classifies the file as either 'signal' or 'background' based on the filename.
    Parameters:
    - file_name: str, name of the .root file.
    Returns:
    - classification: str, either 'signal' or 'background'.
    """
    
    if "leplep" in file_name.lower() or "hadhad" in file_name.lower():
        return 'background'
        
    elif "lephad" or "hadlep" in file_name.lower():
        return 'signal'
        
    else:
        return 'unknown'

# function to extract the variation (e.g., 'ttAdown') from the file name
def extract_variation(file_name):

    """
    Extracts the BSM variation from the file name.
    Assumes the variation is the second to last underscore-separated substring, unless no variation is present.
    Parameters:
    - file_name: str, name of the .root file.
    Returns:
    - variation: str, extracted variation from the file name. If no variation is present, returns 'SM' for Standard Model.
    """
    
    base_name = os.path.basename(file_name)
    parts = base_name.split('_')

    # Check if the second-to-last part appears to be a variation
    if len(parts) > 2 and ('down' in parts[-2] or 'up' in parts[-2]):
    
        return parts[-2]  # second-to-last is variation
        
    else:
    
        return 'SM'  # no variation "Standard Model"

def read_histogram_data(root_file, histogram_name):

    """
    Reads a histogram from a .root file and returns the bin edges and values.
    Parameters:
    - root_file: str, path to the .root file.
    - histogram_name: str, name of the histogram to be extracted.
    Returns:
    - bin_edges: numpy array of bin edges.
    - hist_values: numpy array of histogram values.
    """
    
    with uproot.open(root_file) as file:
    
        if histogram_name in file:
        
            histogram = file[histogram_name]
            hist_values = histogram.values()
            bin_edges = histogram.axes[0].edges()
            
            return bin_edges, hist_values
            
        else:
            return None, None

# plot stacked histograms
def plot_stacked_histogram(histogram_name, signal_histograms, background_histograms, variation):

    """
    Plots a stacked histogram for both signal and background processes.
    Parameters:
    - histogram_name: str, name of the histogram.
    - signal_histograms: list of tuples (bin_edges, values) for signal processes.
    - background_histograms: list of tuples (bin_edges, values) for background processes.
    - variation: str, the BSM variation being plotted.
    """
    
    plt.figure(figsize=(8, 6))
    
    # Stack background histograms
    total_background = np.zeros_like(background_histograms[0][1])
    
    for bin_edges, hist_values in background_histograms:
    
        plt.hist(bin_edges[:-1], bins=bin_edges, weights=hist_values, histtype='stepfilled', alpha=0.5, label='Fully hadronic')
        total_background += hist_values
    
    # stack signal histograms
    total_signal = np.zeros_like(signal_histograms[0][1])
    
    for bin_edges, hist_values in signal_histograms:
        plt.hist(bin_edges[:-1], bins=bin_edges, weights=hist_values, histtype='step', label='Signal', linewidth=2)
        total_signal += hist_values

    xlabel = determine_xlabel(histogram_name)
    
    plt.xlabel(xlabel)
    plt.ylabel('Events')
    plt.title(f'Histogram: {histogram_name} ({variation})')
    plt.legend()
    plt.grid(True)
    
    output_filename = f"{histogram_name}_{variation}.pdf"
    plt.savefig("/ceph/salshamaily/topEWK_FCCee/plots/"+output_filename)
    
    plt.show()
    plt.close()

# processing multiple files and organizing histograms for stacking
def process_multiple_files(root_files):

    """
    Process multiple root files and organize histograms for signal and background processes.
    Parameters:
    - root_files: list of str, paths to the .root files.
    """
    
    histograms_by_variation = {}

    for root_file in root_files:
    
        classification = classify_file(root_file)
        variation      = extract_variation(root_file)
        
        print(f"File: {root_file}, Classification: {classification}")
        print(f"File: {root_file}, Variation: {variation}")

        # dictionary entry for each variation if it doesn't exist
        if variation not in histograms_by_variation:
            histograms_by_variation[variation] = {'signal': {}, 'background': {}}

        with uproot.open(root_file) as file:
            histogram_names = [key for key in file.keys() if file[key].classname.startswith("TH")]
            print(f"Histograms in {root_file}: {histogram_names}")

            for hist_name in histogram_names:
                bin_edges, hist_values = read_histogram_data(root_file, hist_name)
                print(f"Histogram {hist_name}: Bin edges: {bin_edges}, Values: {hist_values}")

                if bin_edges is not None and hist_values is not None:
                    hist_data = (bin_edges, hist_values)

                    # Store histogram data in the correct dictionary for each category (signal/background)
                    if classification == 'signal':
                    
                        if hist_name not in histograms_by_variation[variation]['signal']:
                            histograms_by_variation[variation]['signal'][hist_name] = hist_data
                            
                        else:
                            histograms_by_variation[variation]['signal'][hist_name] = (
                                bin_edges,
                                histograms_by_variation[variation]['signal'][hist_name][1] + hist_values
                            )
                    elif classification == 'background':
                    
                        if hist_name not in histograms_by_variation[variation]['background']:
                            histograms_by_variation[variation]['background'][hist_name] = hist_data
                            
                        else:
                            histograms_by_variation[variation]['background'][hist_name] = (
                                bin_edges,
                                histograms_by_variation[variation]['background'][hist_name][1] + hist_values
                            )

    # Plot stacked histograms for each variation
    for variation, histograms in histograms_by_variation.items():
    
        if histograms['signal'] and histograms['background']: # plot histograms only if sig+bkg
        
            for hist_name in histograms['signal'].keys():
            
                if hist_name in histograms['background']:
                    signal_hist_data = histograms['signal'][hist_name]
                    background_hist_data = histograms['background'][hist_name]

                    plot_stacked_histogram(hist_name, [signal_hist_data], [background_hist_data], variation)
                    print(f"Plotting for histogram: {hist_name}, Variation: {variation}")

# Glob all .root files
root_files = glob.glob('/ceph/salshamaily/topEWK_FCCee/root_hists/*.root')

# Process files
process_multiple_files(root_files)
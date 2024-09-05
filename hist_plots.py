# importing required packages
import uproot
import matplotlib.pyplot as plt
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
    
    # mapping keywords to xlabels
    keyword_to_label = {
        "energy": "Energy [GeV]",
        "pt": "p$_T$ [GeV]",
        "mass": "Mass [GeV]",
        "eta": "$\eta$",
        "phi": "$\phi$"
    }
    
    # default
    xlabel = "Value"
    
    # check for keywords in histogram name
    for keyword, label in keyword_to_label.items():
    
        if keyword in histogram_name.lower():
            xlabel = label
            break
    
    return xlabel

# plotting histograms
def read_and_draw_histogram(root_file, histogram_name):
    
    """
    Reads a histogram from a .root file and draws it using matplotlib.

    Parameters:
    - root_file: str, path to the .root file.
    - histogram_name: str, name of the histogram to be extracted and plotted.
    """
    
    with uproot.open(root_file) as file:
        
        # check if the histogram exists
        if histogram_name in file:
            
            # access the histogram
            histogram = file[histogram_name]
            
            # extract histogram data
            hist_values = histogram.values()
            bin_edges = histogram.axes[0].edges()
            
            # determining xlabel
            xlabel = determine_xlabel(histogram_name)
            
            plt.figure(figsize=(8, 6))
            plt.hist(bin_edges[:-1], bins=bin_edges, weights=hist_values, histtype='step', label=histogram_name)
            plt.xlabel(xlabel)
            plt.ylabel('Events')
            plt.title(f'Histogram: {histogram_name} from {root_file}')
            plt.legend()
            plt.grid(True)
            plt.show()
            
            # create a valid filename for the PDF and save it
            output_filename = f"{os.path.splitext(os.path.basename(root_file))[0]}_{histogram_name}.pdf"
            plt.savefig("/ceph/salshamaily/topEWK_FCCee/pdfs/"+output_filename)
            
            plt.close()
            
        else:
            print(f"Histogram {histogram_name} not found in {root_file}.")
    
# processing multiple .root files        
def process_multiple_files(root_files):
    
    """
    Process multiple root files and draw all histograms found in each.

    Parameters:
    - root_files: list of str, paths to the .root files.
    """
    
    for root_file in root_files:
        print(f'Processing file: {root_file}')
        
        with uproot.open(root_file) as file:
            # list all objects in file and filter histograms
            histogram_names = [key for key in file.keys() if file[key].classname.startswith("TH")]
            
            for hist_name in histogram_names:
                print(f'  - Drawing histogram: {hist_name}')
                read_and_draw_histogram(root_file, hist_name)
                
# glob all .root files
root_files = glob.glob('/ceph/salshamaily/topEWK_FCCee/root_hists/*.root')

# process files
process_multiple_files(root_files)
# -*- coding: utf-8 -*-
import pandas as pd
import polars as pl
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


def load_and_preprocess_data(file_path):
    # Load data using polars and convert to pandas
    data = pl.read_csv(file_path)
    df = data.to_pandas()
    
    # Convert response time to milliseconds
    df["idRespTime_ms"] = df["idRespTime"] * 1000
    
    return df

def calculate_correctness(df):
    # Create size correctness column
    df["size_correct"] = np.where(
        ((df["SourceSizeResp"] > 0) & (df["SourceEncodingSize"] == "large")) | 
        ((df["SourceSizeResp"] < 0) & (df["SourceEncodingSize"] == "small")),
        1, 0
    )
    
    # Create location correctness column
    df["loc_correct"] = np.where(
        ((df["SourceLocResp"] > 0) & (df["SourceEncodingLoc"] == "upper")) | 
        ((df["SourceLocResp"] < 0) & (df["SourceEncodingLoc"] == "lower")),
        1, 0
    )
    
    # Count total correct sources
    df["correct_sources"] = df["size_correct"] + df["loc_correct"]
    
    return df

def calculate_recognition_rates(df):
    # Calculate hit rate
    total_targets = df[df['ItemStatus'] == 'target'].shape[0]
    hits = df[(df['ItemStatus'] == 'target') & (df['ItemRecogStatus'] == 'Hit')].shape[0]
    hit_rate = hits / total_targets if total_targets > 0 else 0
    
    # Calculate false alarm rate
    total_lures = df[df['ItemStatus'] == 'lure'].shape[0]
    false_alarms = df[(df['ItemStatus'] == 'lure') & (df['ItemRecogStatus'] == 'FalseAlarm')].shape[0]
    fa_rate = false_alarms / total_lures if total_lures > 0 else 0
    
    return {
        'hit_rate': hit_rate,
        'fa_rate': fa_rate,
        'total_targets': total_targets,
        'hits': hits,
        'total_lures': total_lures,
        'false_alarms': false_alarms
    }

def bar_plot(means, errors, x_labels, title, xlabel, ylabel, filename, 
             figsize=(10, 6), y_range=None, bar_width=0.6, color='C0', 
             edgecolor='black', capsize=5, rotation=0, ha='center',
             show_values=False, value_format=".1f", value_offset=30,
             value_fontsize=9, show_error=False):
    """
    Create a bar plot for the replication.
    
    Parameters:
    -----------
    means : array-like
        The mean values for each bar
    errors : array-like
        The error values (e.g., 95% CI) for each bar
    x_labels : list
        The labels for the x-axis
    title : str
        The title of the plot
    xlabel : str
        The label for the x-axis
    ylabel : str
        The label for the y-axis
    filename : str
        The filename to save the figure
    figsize : tuple, optional
        The figure size (width, height) in inches
    y_range : tuple, optional
        The y-axis range (min, max)
    bar_width : float, optional
        The width of the bars
    color : str, optional
        The color of the bars
    edgecolor : str, optional
        The edge color of the bars
    capsize : int, optional
        The size of the error bar caps
    rotation : int, optional
        The rotation of the x-tick labels
    ha : str, optional
        The horizontal alignment of the x-tick labels
    show_values : bool, optional
        Whether to display the values above each bar
    value_format : str, optional
        Format string for displaying values
    value_offset : float, optional
        Vertical offset for value text above error bars
    value_fontsize : int, optional
        Font size for value text
    show_error : bool, optional
        Whether to include error values in the text display
    
    Returns:
    --------
    fig, ax : tuple
        The matplotlib figure and axes objects
    """
   
    # Create figure and axes
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create x positions
    x_positions = np.arange(len(means))
    
    # Create bar plot
    bars = ax.bar(
        x_positions,
        means,
        width=bar_width,
        color=color,
        edgecolor=edgecolor
    )
    
    # Error bars
    ax.errorbar(
        x_positions,
        means,
        yerr=errors,
        fmt='none',
        color=edgecolor,
        capsize=capsize
    )
    
    # Value labels
    if show_values:
        for i, (mean, error) in enumerate(zip(means, errors)):
            # Format the text
            if show_error:
                value_text = f"{mean:{value_format}} ± {error:{value_format}}"
            else:
                value_text = f"{mean:{value_format}}"
            
            # Text annotation
            ax.text(
                x_positions[i],
                mean + error + value_offset,
                value_text,
                ha='center',
                va='bottom',
                fontsize=value_fontsize,
            )
    
    # Set x-ticks and labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=rotation, ha=ha)
    
    # Set labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Set y-range
    if y_range:
        ax.set_ylim(y_range)
    
    # Use tight layout
    fig.tight_layout()
    
    # Save figure
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    return fig, ax
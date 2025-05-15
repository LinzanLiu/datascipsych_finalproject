# -*- coding: utf-8 -*-
import pandas as pd
import polars as pl
import numpy as np
from pathlib import Path

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
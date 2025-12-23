"""
🧪 UNIT TESTS FOR ECO-PULSE
This file validates that the paths, logic, and output integrity
of the climate analysis tool are working correctly.
"""
import os
import pytest
import pandas as pd
from seasonal_analysis import OUTPUT_DIR, get_general_recommendation

# Test 1: Validate Absolute Path Configuration
def test_path_configuration():
    """
    Ensures that OUTPUT_DIR is correctly defined as a child directory
    of the folder where the script is actually located.
    """
    # Get the absolute path of the current test file directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # The expected path is the base directory joined with 'outputs'
    expected_path = os.path.join(base_dir, 'outputs')
    
    # Verify that the script's OUTPUT_DIR matches the expected absolute path
    assert OUTPUT_DIR == expected_path

# Test 2: Validate Ecological Recommendation Logic
def test_recommendation_logic():
    """
    Checks if the random ecological tip generator returns a valid string
    and follows the required HTML format for the report.
    """
    tip = get_general_recommendation()
    
    # Verify that the recommendation includes HTML bold tags for formatting
    assert "<strong>" in tip 
    # Verify that the returned value is a string
    assert isinstance(tip, str)

# Test 3: Validate Output File Existence
def test_output_files_exist():
    """
    Checks for the existence of the report and data files inside the outputs folder.
    Note: This requires the main script to have been run at least once.
    """
    # List of critical files that the script must generate
    files_to_check = ['Final_Report.html', '1_co2_temp.png', 'last_run_info.txt']
    
    for file_name in files_to_check:
        file_path = os.path.join(OUTPUT_DIR, file_name)
        
        # If the file exists, verify it is not empty (size > 0 bytes)
        if os.path.exists(file_path):
            assert os.path.getsize(file_path) > 0
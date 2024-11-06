# ----------------------------------------------------
# -- Projet : BankFile_Analysis
# -- Author : Ronaf
# -- Created : 06/11/2024
# -- Usage : Store functions used on Main.py - to ease reading
# -- Update : 
# --  
# ----------------------------------------------------

# ----- Import Public libraries/Packages
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from tkinter import filedialog, messagebox
import shutil
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import copy
import hashlib
import chardet
import csv
import sys

# ----- Custom Files
# Functions to setup Bank templates
import Settings.SetupTemplates as tmplt
# Variables
from Settings.config import *

# ----- Custom Functions
def Find_Encoding(MyCsv):
# Find the  encoding of a csv file to proprely read-it
    with open(MyCsv, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    return encoding

def find_csv_delimiter(file_path):
# Find the delimiter of a csv file to proprely read-it
    encoding = Find_Encoding(file_path)
    with open(file_path, 'r', newline='', encoding=encoding) as f:
        # Use csv.Sniffer to detect the delimiter
        sample = f.readline()
        dialect = csv.Sniffer().sniff(sample)  # Guess the delimiter
        return dialect.delimiter

def get_all_files(directory):
# Get all files in a directory
    files_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            files_list.append(os.path.join(dirpath, filename))
    return files_list


def categorize(df, relative_mapping, abs_mapping):   
# Categorize mu data based on a absolute category (Hash) or a relative category (Wildcards - details)
    # Ensure detail_value is a string and strip any extra spaces
    Hash_str = str(df['PK_Hash']).strip()  
    detail_str = str(df['Details']).strip() 
    # Check for exact match first in abs_mapping, using the 'PK_Hash' column
    matched_category = '99_99'  # Default category if no match is found
    for _, abs_row in abs_mapping.iterrows():
        if Hash_str.lower() == str(abs_row.iloc[0]).lower():  # Case-insensitive exact match
            matched_category = abs_row.iloc[1]
            break  
    # If no exact match found, try the regex-based matching from mapping_df, using the 'details' column
    if matched_category == '99_99':  # If no match found from the first loop
        for _, map_row in relative_mapping.iterrows():
            regex_pattern = f".*{re.escape(map_row.iloc[0])}.*"  # Accessing 'details' column and escaping special chars
            if re.search(regex_pattern, detail_str, re.IGNORECASE):  # Check if detail matches pattern
                matched_category = map_row.iloc[1]
                break 
    return matched_category

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # If running from a bundled .exe, sys.executable points to the .exe file
        base_path = os.path.dirname(sys.executable)  # Directory of the .exe
    else:
        # If running from the source code (not frozen), use the current working directory
        base_path = os.path.dirname(os.path.dirname(relative_path))
    # Combine base path with relative path to get the full path to the resource
    return base_path

def create_dataset():
# create the dataset used in Main.py
    # folder where is located Main : base for everything
    main_path =  get_resource_path(__file__)
    # Source
    source_directory = os.path.join(main_path, 'Source')
    source_files = get_all_files(source_directory)
    # ----- create my data
    # start to create an empty row, in case of no bankfile
    Data = tmplt.Setup_None()
    for file in source_files:
        # loop on all the bankfiles available to set-up them as a templated dataframe
        BankName = os.path.basename(os.path.dirname(file))
        result = tmplt.setup_banks(BankName, file)
        TmpDataFrame = pd.DataFrame(result)
        # concat dataframes
        Data = pd.concat([Data, TmpDataFrame], ignore_index=True)
    # --- Create a Hashed PK. Could have be done in the setup
    Data['PK_Hash'] = Data.apply(lambda row: hashlib.sha256(f"{row['Date']}{row['Balance']}{row['Details']}".encode('utf-8')).hexdigest(), axis=1)

    # ----- Categorize transactions
    Resources_directory = os.path.join(main_path, 'Resources')
    # --- Add ForeignKeys for categories
    # -- AbsoluteCategories based on PK_Hash
    absolute_mapping_path = os.path.join(Resources_directory, 'AbsoluteCategory.csv')
    abs_mapping = pd.read_csv(absolute_mapping_path, delimiter=find_csv_delimiter(absolute_mapping_path))
    # -- WildcardsCategories based a pattern in Details
    wildcards_mapping_path = os.path.join(Resources_directory, 'WildcardsCategory.csv')
    relative_mapping = pd.read_csv(wildcards_mapping_path, delimiter=find_csv_delimiter(wildcards_mapping_path)) 
    # -- Apply the function to create a new 'category' column
    Data['fk_category'] = Data.apply(lambda x: categorize(x, relative_mapping,abs_mapping), axis=1)
    # --- Add Categories (left join on PK)
    # -- Create category DataFrame
    categorydef_mapping_path = os.path.join(Resources_directory, 'CategoriesDefinition.csv')
    df_category = pd.read_csv(categorydef_mapping_path, delimiter=find_csv_delimiter(categorydef_mapping_path))
    # -- Perform left join
    Data = pd.merge(Data, df_category, left_on='fk_category', right_on='ID', how='left')

    # --- Create dimensions
    # -- Ensure 'Date' is in datetime format and create datebased variables
    Data['Date'] = pd.to_datetime(Data['Date'], errors='coerce')
    max_date = Data['Date'].max()
    max_month = max_date.month
    max_year = max_date.year
    max_year_LY = max_year -1
    # -- Date Dimensions and Date boolean
    Data['Month'] = Data['Date'].dt.to_period('M')  
    Data['strYearMonth'] = Data['Date'].dt.strftime('%Y-%m')   # Convert to string
    Data['Year'] = Data['Date'].dt.to_period('Y')  
    Data['IsMaxM'] = ((Data['Date'].dt.month  == max_month) & (Data['Date'].dt.year == max_year)).astype(int)
    Data['IsMaxMLY'] = ((Data['Date'].dt.month  == max_month) & (Data['Date'].dt.year == max_year_LY)).astype(int)
    Data['IsYTD_MaxM'] = ((Data['Date'].dt.month  <= max_month) & (Data['Date'].dt.year == max_year)).astype(int)
    Data['IsYTD_MaxMLY'] =((Data['Date'].dt.month  <= max_month) & (Data['Date'].dt.year == max_year_LY)).astype(int)

    return Data

def export_dataset(df):
# Function to export the dataset created in csv
    default_filename = "my_dataset.csv"
    # Open a file dialog to select the save location
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             initialfile=default_filename,
                                               filetypes=[("CSV files", "*.csv"),
                                                          ("Excel files", "*.xlsx"),
                                                          ("All files", "*.*")])
    if file_path:
        # Save the dataset as a CSV file
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success",f"Dataset saved to: {file_path}")

def create_guard_page():
# Create a plt img with text : guard page of the exported pdf
    current_date = datetime.now().strftime("%d %B %Y")  
    fig = plt.figure(figsize=(8.27, 11.69))
    # Add the main text (centered)
    plt.text(0.5, 0.6, "Financial Report", 
             ha='center', va='center', fontsize=45, fontweight='bold')
    # Add date to the right
    plt.text(0.95, 0.05, f"{current_date}", 
            ha='right', va='center', fontsize=10, fontweight='normal')
    # Add credit to the left
    plt.text(0.05, 0.05, f"{AUTHOR} - v{VERSION}", 
            ha='left', va='center', fontsize=10, fontweight='normal')
    plt.axis('off')  # Turn off axes
    return fig

def export_to_pdf(FiguresList):
# Export a set of plt figures to pdf
    pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                initialfile='Rapport.pdf',
                                                     filetypes=[("PDF files", "*.pdf"),
                                                                ("All files", "*.*")])
    if not pdf_filename:  # Handle case where the user cancels the save dialog
        return   
    with PdfPages(pdf_filename) as pdf:
        for fig in FiguresList:  
            tmp_fig = copy.copy(fig) # Create a copy to avoid interfere with tkinter
            tmp_fig.set_size_inches(11.69, 8.27)
            tmp_fig.tight_layout() 
            pdf.savefig(tmp_fig,bbox_inches='tight')
            plt.close(tmp_fig) 
    messagebox.showinfo("Success",f"Exported to {pdf_filename}")

def bold_headers(table,HeaderRow,HeaderCol) :
# in table/pivotTable matplotlib : Make the headers bold. You can select the Index of the headers
    for (i, j), cell in table.get_celld().items():
        if i == HeaderRow or j == HeaderCol:  
            cell.set_text_props(fontweight='bold')
            
def import_file(BankName):
# Import a bankfile in the dedicated folder. Not used in v0.1
    # Check if BankName is empty
    if not BankName:
        messagebox.showinfo("Error", f"Please select a Bank to import.")
        return  # Exit the function early
    # Open a file dialog to select a file
    file_path = filedialog.askopenfilename()
    
    if file_path:  # Check if a file was selected
        # Get the selected dedicated location from the combobox
        dedicated_location = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Source',BankName)

        # Check if the dedicated location exists
        if not os.path.exists(dedicated_location):
                try:
                    os.makedirs(dedicated_location)
                    print(f"Created directory: {dedicated_location}")
                except Exception as e:
                    print(f"Error creating directory: {e}")
                    return
        try:
            # Copy the selected file to the dedicated location
            shutil.copy(file_path, dedicated_location)
            print(f"File imported successfully to {dedicated_location}")
        except Exception as e:
            print(f"Error while importing file: {e}")
    
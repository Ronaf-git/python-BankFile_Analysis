# ----------------------------------------------------
# -- Projet : BankFile_Analysis
# -- Author : Ronaf
# -- Created : 06/11/2024
# -- Usage : Store functions used to setup the bankfiles in a dedicated template
# -- Update : 
# --  
# ----------------------------------------------------

# --- Imports
import pandas as pd
import Settings.Functions as fct

# ===============================================================
# Individual setup
# ===============================================================
def Setup_Beobank(source):
    # Setup Beobank File in the desired format
    # --- Find encoding and delim
    encoding = fct.Find_Encoding(source)
    delim = fct.find_csv_delimiter(source)
    # --- Load data
    df = pd.read_csv(source, encoding=encoding, delimiter=delim)
    # --- Create my final df
    new_df = pd.DataFrame()
    # -- Index 0 : DateTime
    DateTime = pd.to_datetime(df.iloc[:, 0], format='%d-%m-%y')  # Conversion de la colonne 'Date' Index 0 en datetime 
    new_df.insert(0, 'Date', DateTime)
    # -- Index 1 : Balance
    # Convert (I2) and (I3) to numeric, coercing errors to NaN
    debit = pd.to_numeric(df.iloc[:, 2].astype(str).str.replace(',', '.'), errors='coerce')
    credit = pd.to_numeric(df.iloc[:, 3].astype(str).str.replace(',', '.'), errors='coerce')
    # create balance
    balance = debit.fillna(0) + credit.fillna(0)
    new_df.insert(1, 'Balance', balance)
    # -- Index 2 : Details (I4)
    Details = df.iloc[:, 4]
    new_df.insert(2, 'Details', Details)
    # -- Index 3 : Source
    new_df.insert(3, 'Source', source)
    # -- Index 4 : Revenues/Expenses
    flow = new_df['Balance'].apply(lambda x: 'revenues' if x > 0 else ('expenses' if x < 0 else 'neutral')) 
    new_df.insert(4, 'Flow', flow)
    
    return new_df
def Setup_BNP_Paribas_Fortis(source):
    # Setup BNP File in the desired format
    
    # --- Find encoding and delim
    encoding = fct.Find_Encoding(source)
    delim = fct.find_csv_delimiter(source)

    # --- Load data
    df = pd.read_csv(source, encoding=encoding, delimiter=delim)
   
    # --- Create my final df
    new_df = pd.DataFrame()
    # -- Index 0 : DateTime
    DateTime = pd.to_datetime(df.iloc[:, 1], format='%d-%m-%y')  # Convert 'Date' Index 1 in datetime 
    new_df.insert(0, 'Date', DateTime)
    # -- Index 1 : Balance
    # balance I3
    balance = pd.to_numeric(df.iloc[:, 3].str.replace(',', '.'), errors='coerce')
    new_df.insert(1, 'Balance', balance)
    # -- Index 2 : Details (I10)
    Details = df.iloc[:, 10]
    new_df.insert(2, 'Details', Details)
    # -- Index 3 : Source
    new_df.insert(3, 'Source', source)
    # -- Index 4 : Revenues/Expenses
    flow = new_df['Balance'].apply(lambda x: 'revenues' if x > 0 else ('expenses' if x < 0 else 'neutral')) 
    new_df.insert(4, 'Flow', flow)


    return new_df
def Setup_Belfius(source):
    # Setup Belfius File in the desired format
    # --- Find encoding and delim
    encoding = fct.Find_Encoding(source)
    delim = fct.find_csv_delimiter(source)

    # --- Load data
    # Load the CSV file, skipping the first 12 rows, they are not data
    df = pd.read_csv(source, encoding=encoding, delimiter=delim, skiprows=12)
   
    # --- Create my final df
    new_df = pd.DataFrame()
    # -- Index 0 : DateTime
    DateTime = pd.to_datetime(df.iloc[:, 9], format='%d/%m/%Y')  # Convert 'Date' Index 1 in datetime 
    new_df.insert(0, 'Date', DateTime)
    # -- Index 1 : Balance
    # balance I3
    balance = pd.to_numeric(df.iloc[:, 10].str.replace(',', '.'), errors='coerce')
    new_df.insert(1, 'Balance', balance)
    # -- Index 2 : Details (I10)
    Details = df.iloc[:, 8]
    new_df.insert(2, 'Details', Details)
    # -- Index 3 : Source
    new_df.insert(3, 'Source', source)
        # -- Index 4 : Revenues/Expenses
    flow = new_df['Balance'].apply(lambda x: 'revenues' if x > 0 else ('expenses' if x < 0 else 'neutral')) 
    new_df.insert(4, 'Flow', flow)

    return new_df
def Setup_Sample(source):
    # Setup Sample File in the desired format
    # --- Find encoding and delim
    encoding = fct.Find_Encoding(source)
    delim = fct.find_csv_delimiter(source)
    # --- Load data
    df = pd.read_csv(source, encoding=encoding, delimiter=delim)
    # --- Create my final df
    new_df = pd.DataFrame()
    # -- Index 0 : DateTime
    DateTime = pd.to_datetime(df.iloc[:, 0], format='%d-%m-%y')  # Convert 'Date' Index 1 in datetime 
    new_df.insert(0, 'Date', DateTime)
    # -- Index 1 : Balance
    # balance I3
    balance = pd.to_numeric(df.iloc[:, 1])
    new_df.insert(1, 'Balance', balance)
    # -- Index 2 : Details (I10)
    Details = df.iloc[:, 2]
    new_df.insert(2, 'Details', Details)
    # -- Index 3 : Source
    new_df.insert(3, 'Source', source)
        # -- Index 4 : Revenues/Expenses
    flow = new_df['Balance'].apply(lambda x: 'revenues' if x > 0 else ('expenses' if x < 0 else 'neutral')) 
    new_df.insert(4, 'Flow', flow)
    return new_df
def Setup_None():
    Data = [
        {"Date": 0, "Balance": 0, "Details": 'Init','Source':'HardCoded', 'Flow':0}  # Sample row with null values
    ]
    Data = pd.DataFrame(Data)
    return Data


# ===============================================================
# Aggregate setup
# ===============================================================
# Create a mapping of function names to actual functions
setup_functions = {
    'Beobank': Setup_Beobank,
    'BNP Paribas Fortis': Setup_BNP_Paribas_Fortis,
    'Belfius': Setup_Belfius,
    'Sample': Setup_Sample,
    # Add more mappings as needed
}

# All setups
def setup_banks(BankName, source):
    # Initialize a list to hold the results
    result = []
    if BankName in setup_functions:
        result = setup_functions[BankName](source)
    else:
        print(f"Function for {BankName} not found.")
    return result
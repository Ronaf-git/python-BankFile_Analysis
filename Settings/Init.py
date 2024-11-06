# ----------------------------------------------------
# -- Projet : BankFile_Analysis
# -- Author : Ronaf
# -- Created : 06/11/2024
# -- Usage : Install/Update needed packages to run the code
# -- Update : 
# --  
# ----------------------------------------------------

# ------------------ Install Package -------------
import subprocess
import sys

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print('''============================================
Start Install/Updates needed Python Packages
============================================''')

# List of packages to install
packages = ["pandas", "matplotlib", "seaborn","chardet","plotly"]

# Installing each package
for package in packages:
    install(package)

print('''============================================
Packages Installed/Updated
============================================''')


# ----------------------------------------------------
# -- Projet : BankFile_Analysis
# -- Author : Ronaf
# -- Created : 06/11/2024
# -- Usage : Main script : create dataset, figures and display them
# -- Update : 
# --  
# ----------------------------------------------------

# Init - If needed to run the script
#import Settings.Init
# ----- Public libraries/Packages
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import sys
import tkinter as tk
from tkinter import  ttk,filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# ----- Custom Functions
#  Functions to setup Bank templates
import Settings.SetupTemplates as tmplt
#  Other functions
import Settings.Functions as fct
# Variables
from Settings.config import *

# ===============================================================
# Create Dataset
# ===============================================================
Data = fct.create_dataset()
# Check if there is other data than my empty row. If not, feed a variable
# the variable will adjust some figures, as well adjust the readme to notify the user
if Data.shape[0] == 1:
    IsNoData = 1
else :
    IsNoData = 0 

# ===============================================================
# Init Window
# ===============================================================
root = tk.Tk()
root.title("BankFile Analysis - Financial Data Visualizations")
root.state('zoomed')  # This will maximize the window
# Set the window to fullscreen
#root.attributes('-fullscreen', True)
#root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))
# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)
style = ttk.Style()
style.configure(
    'TNotebook.Tab',
    font=('Arial', 16, 'bold'),
    padding=(20, 10),
    borderwidth=21,
    relief='solid',
    background='lightblue',
    foreground='black',
    highlightthickness=10,
    highlightcolor='red',
    highlightbackground='gray'
)

# ===============================================================
# Tab 0 : Setup and exports
# ===============================================================
# Create my tab
tab0 = ttk.Frame(notebook)
notebook.add(tab0, text='Home/Exports' )

# --- Part 1 : Buttons
# Frame to store buttons
button_frame_tab0 = tk.Frame(tab0)
button_frame_tab0.grid(row=0, column=0,sticky="nsew")  # Sticky ensures it fills space
tab0.grid_rowconfigure(0, weight=0)  # Button frame does not expand vertically
tab0.grid_columnconfigure(0, weight=1)  # Allow this column to expand horizontally
button_frame_tab0.grid_columnconfigure(0, weight=1)  # Expand first column to fill available space
button_frame_tab0.grid_columnconfigure(1, weight=1)  # Expand second column (for the second button)
# 1st button
download_button_tab0 = tk.Button(
    button_frame_tab0,
    text="Export Dataset CSV",
    command=lambda: fct.export_dataset(Data),  # Use a lambda to delay the call
    font=("Helvetica", 20),  # Increase font size
    bg="blue",               # Background color
    fg="white",              # Text color
    width=40,                # Width of the button
    height=2                 # Height of the button
)
download_button_tab0.grid(row=0, column=0, padx=10, pady=20)  
# second button
exportPDF_button_tab0 = tk.Button(
    button_frame_tab0,
    text="Export a PDF Rapport",
    command=lambda: fct.export_to_pdf(ExportedFiguresToPDF),  # Use a lambda to delay the call
    font=("Helvetica", 20),  # Increase font size
    bg="blue",               # Background color
    fg="white",              # Text color
    width=40,                # Width of the button
    height=2                 # Height of the button
)
exportPDF_button_tab0.grid(row=0, column=1, padx=10, pady=20)  

# --- Part 1 : ReadMe
# Frame
ReadMe_frame_tab0 = tk.Frame(tab0)
ReadMe_frame_tab0.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")  # sticky="nsew" makes it fill
tab0.grid_rowconfigure(1, weight=1)  # Allow this row to expand vertically
tab0.grid_columnconfigure(0, weight=1)  # Allow this column to expand horizontally
# Adding a Text widget to ReadMe_frame
text_widget_tab0 = tk.Text(ReadMe_frame_tab0, wrap='word' , bg=style.lookup("TFrame", "background"), fg='Black', bd=0)
# Says if NoData
if IsNoData == 1 :
    text_widget_tab0.tag_configure("big_red", foreground="red", font=("Arial", 40))
    text_widget_tab0.insert(tk.END, "Please Add BankFile")
    text_widget_tab0.tag_add("big_red", "1.0", "1.20")  # Apply the style from position 1.1 to 1.20
# Text
Text_tab0 = f"""
Author : {AUTHOR}
Version : {VERSION}

How-to :
1) Add your BankFile in the dedicated folder (Source)
2) Adjust categories based on your desires
    A) Config "CategoriesDefinition.csv" 
        Unique ID that will be used to categorize data
    B) Config "WildcardsCategory.csv"
        When a pattern word will be find in your BankFile details, it will link the dedicated category (Set up in A))
    C) Config "AbsoluteCategory.csv"
        Usefull to categorize dedicated transaction, based on their unique PK_Hash (PK_Hash is available in the exported csv dataset)

See https://github.com/Ronaf-git/python-BankFile_Analysis for more informations
"""
text_widget_tab0.insert(tk.END,Text_tab0) 
# Set the Text widget to "disabled" to make it unwritable
text_widget_tab0.config(state=tk.DISABLED)
text_widget_tab0.bind("<FocusIn>", lambda e: text_widget_tab0.config(state=tk.DISABLED))
# pack it
text_widget_tab0.pack(fill="both", expand=True)

'''
# Not use yet because i need to reload the whole UI after loading data
# Create a label for the combobox
label = tk.Label(tab0, text="Add a Bankfile and reload dataset:")
label.pack(pady=5)
combo = ttk.Combobox(tab0)
combo['values'] = list(tmplt.setup_functions.keys())  # Fill with keys from the dictionary
combo.pack(pady=5)

# Create a button to trigger the file import
def handle_import():
    filename = combo.get()
    fct.import_file(filename)        # Call your import function
    global Data 
    Data = fct.create_dataset()      # Call the dataset creation function
    messagebox.showinfo("Success", f"File imported successfully and dataset reloaded")
import_button = tk.Button(tab0, text="Import File", command=lambda: handle_import())
import_button.pack(pady=20)
'''

# ==============================================================================================================================
# Tab 1 : Recap
# ==============================================================================================================================
# Create Tab
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Recap' )
# Create a main frame for the plots
plot_frame_tab1 = tk.Frame(tab1)  
plot_frame_tab1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
# Create a figure for plotting
figs_tab1, ax_tab1 = plt.subplots(figsize=(19.16,9.58))
# create canvas to store them
canvas_tab1 = FigureCanvasTkAgg(figs_tab1, master=plot_frame_tab1)
canvas_tab1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def update_plots_tab1() :
    # --- Create DataFrame
    # Get the current month name. Current = Max data available
    max_date = Data['Date'].max()
    str_current_month = max_date.strftime('%b')  
    current_year = max_date.year  
    current_year_LY = current_year -1 
    # Dynamically create column names
    balance_if_CM1 = f"Balance {str_current_month} {current_year}"
    balance_if_CM1LY = f"Balance {str_current_month} {current_year_LY}"
    balance_if_YTD_CM1 = f"Balance YTD {str_current_month} {current_year}"
    balance_if_YTD_CM1LY = f"Balance YTD {str_current_month} {current_year_LY}"
    str_delta_CM1_CM1LY = f"Delta {str_current_month} {current_year}-{current_year_LY}"
    str_delta_YTD_CM1_YTD_CM1LY = f"Delta YTD {str_current_month} {current_year}-{current_year_LY}"
    # Group by 'C1_Code' and calculate the balances for each condition
    Df_Tab1 = Data.groupby('C1_Label').agg(
        **{
        balance_if_CM1LY : ('Balance', lambda x: x[Data['IsMaxMLY'] == 1].sum()),
        balance_if_CM1 : ('Balance', lambda x: x[Data['IsMaxM'] == 1].sum()),
        balance_if_YTD_CM1LY : ('Balance', lambda x: x[Data['IsYTD_MaxMLY'] == 1].sum()),
        balance_if_YTD_CM1 : ('Balance', lambda x: x[Data['IsYTD_MaxM'] == 1].sum())
        }
    ).reset_index()
    # Calculate deltas for CM1 - CM1LY and YTD_CM1 - YTD_CM1LY
    delta_CM1_CM1LY = Df_Tab1[balance_if_CM1] - Df_Tab1[balance_if_CM1LY]
    delta_YTD_CM1_YTD_CM1LY = Df_Tab1[balance_if_YTD_CM1] - Df_Tab1[balance_if_YTD_CM1LY]
    # Insert the delta columns at given positions in the dataframe
    Df_Tab1.insert(3, str_delta_CM1_CM1LY , delta_CM1_CM1LY)
    Df_Tab1.insert(6,str_delta_YTD_CM1_YTD_CM1LY, delta_YTD_CM1_YTD_CM1LY)
    # Add a total row
    # Summing the values for each of the required columns
    total_row = Df_Tab1.sum()
    # Add a label for the total row
    total_row['C1_Label'] = 'Total'
    # Convert total_row to a DataFrame and pivot it
    total_row_df = total_row.to_frame().T 
    # Append the total row to the DataFrame
    Df_Tab1 = pd.concat([Df_Tab1, total_row_df], ignore_index=True)
    
    # --- setup figure
    # Hide axes
    ax_tab1.axis('off')
    # Get column names and apply a newline after the first part of the name (if necessary)
    col_labels_table_tab1 = []
    for col in Df_Tab1.columns:
        if len(col) > 20:  # If the column name is long, split it
            col_labels_table_tab1.append(col[:col.rfind(' ')] + '\n' + col[col.rfind(' ') + 1:])
        else:
            col_labels_table_tab1.append(col)
    # Plot the table
    table_tab1 = ax_tab1.table(cellText=Df_Tab1.values, colLabels=col_labels_table_tab1, loc='center', cellLoc='center', colColours=['#f2f2f2']*len(Df_Tab1.columns))
    # Customize the table's appearance (optional)
    table_tab1.auto_set_font_size(False)
    table_tab1.set_fontsize(10)
    table_tab1.scale(1.2, 1.2)
    # Apply conditional formatting 
    for i, key in enumerate(Df_Tab1.columns[1:], start=1):  # Skip the first col
        table_tab1[(0, i)].set_height(0.05) # Adjust the height of the header row to accommodate multi-line headers
        for j, value in enumerate(Df_Tab1[key]):
            # Ensure value is numeric
            value = float(value) if isinstance(value, str) and value.replace('.', '', 1).isdigit() else value
            # Format value to '00.00€'
            formatted_value = f"{value:,.2f}€"
            # Set both formatted value and color
            cell = table_tab1[(j + 1, i)]  # +1 to skip the header row
            text = cell.get_text()  # Get the Text object of the cell
            text.set_text(formatted_value)  # Update the value in the cell
            if key in [str_delta_CM1_CM1LY, str_delta_YTD_CM1_YTD_CM1LY]:  # Only apply to the delta columns
                # Set the color based on the value
                color = '#FF6347' if value < 0 else '#32CD32'  # Red for negative, green for positive
                cell.set_facecolor(color)  # Apply the background color
    fct.bold_headers(table_tab1,0,0)
    # Adjust layout to prevent overlap
    figs_tab1.tight_layout()
    # draw it
    canvas_tab1.draw()
update_plots_tab1()

# ===============================================================================================================
# Tab 2 : Yearly
# ===============================================================================================================
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Yearly Report - Last 3 Years')
# Create a main frame for the plots
plot_frame_tab2 = tk.Frame(tab2)  
plot_frame_tab2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
# Create a figure for plotting
figs_tab2, axs_tab2 = plt.subplots(2, 1, figsize=(19.16,9.58))
figs_tab2.set_size_inches(19.16, 9.58)
canvas_tab2 = FigureCanvasTkAgg(figs_tab2, master=plot_frame_tab2)
canvas_tab2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
# Update plots
def update_plots_tab2() :
    # Create Filtered set
    DataLast3Years = Data[(Data['Date'].dt.year >= Data['Date'].dt.year.max()-2)]
    # --- First Figure
    MonthlyData = DataLast3Years.groupby(['Month'])['Balance'].sum().reset_index()
    MonthlyData.plot(kind='line', ax=axs_tab2[0])
    axs_tab2[0].set_title('Net Balance  - Last 3 Years')
    axs_tab2[0].set_xlabel('Date')
    axs_tab2[0].set_ylabel('Balance')
    axs_tab2[0].tick_params(axis='x', rotation=45)
    # Format x-ticks as strings if necessary
    axs_tab2[0].set_xticks(range(len(MonthlyData)))
    axs_tab2[0].set_xticklabels(MonthlyData['Month'].dt.strftime('%Y-%m'), rotation=45)

    # --- Second Figure: Monthly Balance by Category ---
    # Group by Month and C1_Label
    grouped = DataLast3Years.groupby(['Month', 'C1_Label'])['Balance'].sum().unstack(fill_value=0)
    # Plotting the second figure
    grouped.plot(kind='bar', stacked=True, ax=axs_tab2[1])
    axs_tab2[1].set_title('Net Balance  - Last 3 Years by Category')
    axs_tab2[1].set_xlabel('Month')
    axs_tab2[1].set_ylabel('Balance')
    axs_tab2[1].tick_params(axis='x', rotation=45)
    axs_tab2[1].legend(title='Category', loc='upper center', bbox_to_anchor=(0.5, -0.30), ncol=15)
    # Adjust layout to prevent overlap
    figs_tab2.tight_layout()
    # Create a canvas for the figure
    canvas_tab2.draw()
update_plots_tab2()

# ===============================================================================================================
# Tab 3 : Monthly
# ===============================================================================================================
# --- Create Tab
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Monthly Focus')

# --- Combobox Select Year/Month
# -- Create Frame for Label/Combobox
label_combo_frame_tab3 = ttk.Frame(tab3)
label_combo_frame_tab3.pack(pady=10, padx=10)  # Pack the frame with padding
# -- Create Label
label_tab3 = tk.Label(label_combo_frame_tab3, text="Please select an option from the list:")
label_tab3.pack()
# -- Create Combobox
years = sorted(Data['Month'].unique(), reverse=True)
combo_year_tab3 = ttk.Combobox(label_combo_frame_tab3, values=years)
combo_year_tab3.set(years[0])
combo_year_tab3.bind("<<ComboboxSelected>>", lambda event: update_plots_tab3(combo_year_tab3.get()))
combo_year_tab3.pack(pady=5)  # Pack the ComboBox into the frame

# --- Plots
# Create a main frame for the plots
plot_frame_tab3 = tk.Frame(tab3)  
plot_frame_tab3.pack(pady=40, padx=40, fill='both', expand=True)
# Create a figure for plotting
# Create a figure
figs_tab3 = plt.figure(figsize=(18.36, 8.06))
gs_tab3 = gridspec.GridSpec(2, 2, height_ratios=[1, 5])  # Set height ratios for rows
# Create subplots
axs_tab3 = [figs_tab3.add_subplot(gs_tab3[0, 0]),  # First row, first column
       figs_tab3.add_subplot(gs_tab3[0, 1]),  # First row, second column
       figs_tab3.add_subplot(gs_tab3[1, 0]),  # Second row, first column
       figs_tab3.add_subplot(gs_tab3[1, 1])]  # Second row, second column
# Create a canvas for the figure
canvas_tab3 = FigureCanvasTkAgg(figs_tab3, master=plot_frame_tab3)
canvas_tab3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Pie Chart Expenses by category and KPIs
def update_plots_tab3(MyYear) :
    # Filter the data based on the specified condition
    filtered_data_tab3 = Data[(Data['Month'] == MyYear)]

    # -- KPis
    # cash net
    # Group by the desired categories and sum the balances
    KPICash_data_tab3 = filtered_data_tab3['Balance'].sum()
    # Clear the previous plot
    axs_tab3[0].cla()  # Clear the first subplot
    # Display the KPI in the center of the subplot
    axs_tab3[0].text(0.5, 0.5, f'Net Cash after Investments\n€{KPICash_data_tab3:,.0f}', 
                    ha='center', va='center', fontsize=20, 
                    bbox=dict(facecolor='lightgreen', alpha=0.8))
    axs_tab3[0].axis('off')  # Turn off the axis for a cleaner look
    # gross cash
    # Group by the desired categories and sum the balances
    KPIGrossCash_data_tab3 = filtered_data_tab3[filtered_data_tab3['C1_Code'] != '03']['Balance'].sum()
    # Clear the previous plot
    axs_tab3[1].cla()  # Clear the first subplot
    # Display the KPI in the center of the subplot
    axs_tab3[1].text(0.5, 0.5, f'Gross Cash before Investments\n€{KPIGrossCash_data_tab3:,.0f}', 
                    ha='center', va='center', fontsize=20, 
                    bbox=dict(facecolor='lightgreen', alpha=0.8))
    axs_tab3[1].axis('off')  # Turn off the axis for a cleaner look

    # -- Pies
    # Group by the desired categories and sum the balances
    expenses_data_tab3 = filtered_data_tab3[(filtered_data_tab3['Flow'] == 'expenses')].groupby('C1_Label')['Balance'].sum().reset_index() 
    # Clear the previous plot
    axs_tab3[2].cla()  # Clear the first subplot
    # Prepare data for the pie chart
    labels_tab3_2 = expenses_data_tab3['C1_Label']
    sizes_tab3_2 = expenses_data_tab3['Balance'].abs() #pie chart only need postives values
    colors_tab3_2 = plt.cm.Paired(range(len(labels_tab3_2)))  
    # Create the pie chart
    axs_tab3[2].pie(sizes_tab3_2, labels=labels_tab3_2, colors=colors_tab3_2, autopct=lambda p: f'€{int(p * sum(sizes_tab3_2) / 100):,} ({p:.1f}%)', shadow=False, startangle=140, labeldistance=1.1)
    axs_tab3[2].set_title('Expenses')
    axs_tab3[2].axis('equal')

    # -- Revenues
    # Group by the desired categories and sum the balances
    revenues_data_tab3 = filtered_data_tab3[(filtered_data_tab3['Flow'] == 'revenues')].groupby('C1_Label')['Balance'].sum().reset_index() 
    # Clear the previous plot
    axs_tab3[3].cla()  # Clear the first subplot
    # Prepare data for the pie chart
    labels_tab3_3 = revenues_data_tab3['C1_Label']
    sizes_tab3_3 = revenues_data_tab3['Balance'].abs()
    colors_tab3_3 = plt.cm.Paired(range(len(labels_tab3_3)))  # Optional: use a colormap for colors
    # Create the pie chart
    axs_tab3[3].pie(sizes_tab3_3, labels=labels_tab3_3, colors=colors_tab3_3,  autopct=lambda p: f'€{int(p * sum(sizes_tab3_3) / 100):,} ({p:.1f}%)', shadow=False, startangle=140)
    axs_tab3[3].set_title('Incomes')
    axs_tab3[3].axis('equal')

    # Set fixed limits for the axes to ensure a consistent appearance
    axs_tab3[2].set_xlim(-1.2, 1.2)  # Slightly larger limits to ensure pie chart fits well
    axs_tab3[2].set_ylim(-1.2, 1.2)
    axs_tab3[3].set_xlim(-1.2, 1.2)
    axs_tab3[3].set_ylim(-1.2, 1.2)
    # Adjust layout to prevent overlap
    figs_tab3.tight_layout()
    # Create a canvas for the figure
    canvas_tab3.draw()

# Set the default value to the first item in the list (most recent Month)
if years:  # Check if there are any years available
    update_plots_tab3(years[0]) 

# ===============================================================================================================
# Tab 4 : Focus
# ===============================================================================================================
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text='Focus')
# --- Plots
# Create a main frame for the plots
plot_frame_tab4 = tk.Frame(tab4)  
plot_frame_tab4.pack(fill='both', expand=True)
# Create a figure for plotting
# Create a figure
figs_tab4 = plt.figure(figsize=(20,10))
# Define the grid: 2 rows, 2 columns, with the first row spanning both columns
gs_tab4 = gridspec.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])
# Create the subplots
ax0_tab4 = figs_tab4.add_subplot(gs_tab4[0, :])  # First row, spanning both columns
ax1_tab4 = figs_tab4.add_subplot(gs_tab4[1, 0])  # Second row, first column
ax2_tab4 = figs_tab4.add_subplot(gs_tab4[1, 1])  # Second row, second column
# Create a canvas for the figure
canvas_tab4 = FigureCanvasTkAgg(figs_tab4, master=plot_frame_tab4)
canvas_tab4.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def update_plots_tab4_0() :
    # --- First Figure: Balance by Revenues and Expenses ---
    DataTab4_0 = Data[(Data['Date'].dt.year >= Data['Date'].dt.year.max() - 2) & (Data['C1_Code'] != '03')].groupby(['strYearMonth','IsExp'])['Balance'].sum().reset_index()
    DataTab4_0['Balance'] = DataTab4_0['Balance'].abs()
    DataTab4_0['IsExp'] = DataTab4_0['IsExp'].replace({'0': 'Revenues', '1': 'Expenses'})
    # Set the style of the plot
    sns.set_theme(style="whitegrid")
    # Create the line plot in the first subplot
    sns.lineplot(data=DataTab4_0, x='strYearMonth', y='Balance', hue='IsExp', marker='o', ax=ax0_tab4)
    # Get the line objects from the plot
    lines_tab4_0 = ax0_tab4.get_lines()
    # Add shadow effect: fill the area under each line
    for line in lines_tab4_0:
        # Get the data for the line
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        # Fill the area under the line with a shaded region (using fill_between)
        ax0_tab4.fill_between(xdata, ydata, alpha=0.2, color=line.get_color(), zorder=-1)
    # Add titles and labels
    ax0_tab4.set_title('Gross Savings without investments', fontsize=16)
    ax0_tab4.set_xlabel('')
    ax0_tab4.set_ylabel('')
    # Rotate x-axis labels by 45 degrees
    # give a warning but who cares ?
    ax0_tab4.set_xticklabels(ax0_tab4.get_xticklabels(), rotation=45)
    # Set legend title and move it under the plot
    ax0_tab4.legend(title='Legend', loc='upper center', bbox_to_anchor=(0.5, 1), ncol=2)
update_plots_tab4_0()

# --- Second figure 20/30/50 CYTD
#data
DataTab4_1_expenses = Data[(Data['IsYTD_MaxM'] == 1) & (Data['Cat_20_30_50'] != '100%')].groupby('Cat_20_30_50')['Balance'].sum().reset_index() 
DataTab4_1_revenues = Data[(Data['IsYTD_MaxM'] == 1) & (Data['Cat_20_30_50'] == '100%')]['Balance'].sum()
expenses_tab4_1 = DataTab4_1_expenses['Balance'].abs()
CashAvailable_tab4_1 = max(DataTab4_1_revenues - expenses_tab4_1.sum(), 0)
# Pie chart
# Add 'extra_value' at the end of the labels and sizes
labels_tab4_1 = pd.concat([ DataTab4_1_expenses['Cat_20_30_50'], pd.Series(['Cash available'])], ignore_index=True)
sizes_tab4_1 = pd.concat([expenses_tab4_1, pd.Series([CashAvailable_tab4_1])], ignore_index=True)
# If no value, add 1 to avoid crash
if IsNoData == 1 :
    sizes_tab4_1 = np.nan_to_num(sizes_tab4_1)
    sizes_tab4_1[sizes_tab4_1 == 0] = 1 
ax1_tab4.pie(sizes_tab4_1, labels=labels_tab4_1, autopct=lambda p: f'€{int(p * sum(sizes_tab4_1) / 100):,} ({p:.1f}%)', shadow=False, startangle=140)
ax1_tab4.set_title('20/30/50 strategy')
ax1_tab4.axis('equal')

# --- Third figure Investments
#data
DataTab4_2 = Data[(Data['IsYTD_MaxM'] == 1) & (Data['AssetType'] != '0')].groupby('AssetType')['Balance'].sum().reset_index() 
# Pie chart
# Add 'extra_value' at the end of the labels and sizes
labels_tab4_2 = DataTab4_2['AssetType']
sizes_tab4_2 = DataTab4_2['Balance'].abs()
ax2_tab4.pie(sizes_tab4_2, labels=labels_tab4_2, autopct=lambda p: f'€{int(p * sum(sizes_tab4_2) / 100):,} ({p:.1f}%)', shadow=False, startangle=140)
ax2_tab4.set_title('Investments')
ax2_tab4.axis('equal')

# Adjust layout to fit in the frame
figs_tab4.tight_layout()
# Show the plot
canvas_tab4.draw()

# ===============================================================================================================
# Tab 5 : Pivot Table
# ===============================================================================================================
# Create the 5 tab
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text='Table Category by Month')
# Create a main frame for the plots
plot_frame_tab5 = tk.Frame(tab5)  
plot_frame_tab5.pack(fill=tk.BOTH, expand=True)
# Set up the figure and axis
figs_tab5, ax_tab5 = plt.subplots(figsize=(19.16,9.58))
# Create a canvas for the figure
canvas_tab5 = FigureCanvasTkAgg(figs_tab5, master=plot_frame_tab5)
canvas_tab5.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- create fig
# Create a Pivot Table
pivot_table_tab5 = Data[(Data['Date'].dt.year >= Data['Date'].dt.year.max()-2)].pivot_table(values='Balance', index='Month', columns=['C1_Label'], aggfunc='sum', fill_value=0)
# Format the values as currency
formatted_values = pivot_table_tab5.map(lambda x: f"{x:,.2f}€")  # Formats the numbers to '00.00€'
# Hide axes
ax_tab5.axis('off')
# Create a table
table_tab5 = ax_tab5.table(cellText=formatted_values.values,
                 colLabels=formatted_values.columns.tolist(),
                 rowLabels=formatted_values.index.astype(str).tolist(),
                 cellLoc='center',
                 loc='center')
# Style the table
table_tab5.auto_set_font_size(False)  # Set to False to customize font size
table_tab5.set_fontsize(10)  # Adjust font size as needed
table_tab5.scale(1.2, 1.2)
fct.bold_headers(table_tab5,0,-1) # 0 is the 1 col of the pivot table data
# Adjust layout to fit in the frame
figs_tab5.tight_layout()
canvas_tab5.draw()


# ===============================================================================================================
# Exported Figures to PDF
# ===============================================================================================================
# Global list to store figures, exported to pdf
ExportedFiguresToPDF = []
guard_page = fct.create_guard_page()
# Store the figures in the global list to export to pdf
ExportedFiguresToPDF.append(guard_page)
ExportedFiguresToPDF.append(figs_tab1)
ExportedFiguresToPDF.append(figs_tab2)
ExportedFiguresToPDF.append(figs_tab3)
ExportedFiguresToPDF.append(figs_tab4)
ExportedFiguresToPDF.append(figs_tab5)


# ===============================================================================================================
# Start the Tkinter main loop
# ===============================================================================================================
def on_closing():
    root.destroy()
    sys.exit()  # Ensures the application exits completely

root.protocol("WM_DELETE_WINDOW", on_closing)   
root.mainloop()


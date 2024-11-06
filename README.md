# Python BankFile Analysis

**Version:** 0.1

Note : sample file provided to test

### How-to:

1. **Delete the provided sample file.**

2. **Add your BankFile to the designated folder (Source).**
   > **Note:** There is currently no check to validate if the file fits with the parser. Please ensure that you provide the correct BankFile in the appropriate folder.

3. **Adjust categories as desired.**

   A) **Config: "CategoriesDefinition.csv"**

   This file contains unique IDs that will be used to categorize data.  
   - **Category 3: Investments** should remain unchanged to ensure the related graph displays relevant data.
   - You can create your own categories, but they must follow the structure shown below (Categories 2 to 5 are optional):

     ![image](https://github.com/user-attachments/assets/38432122-1b02-4728-bff8-f0b262c96672)
   
   Fields:
   - `IsExp`: Set to 1 if this category is related to an expense.
   - `Cat_20_30_50`: Refers to the 50/30/20 budget (see [here](https://en.wikipedia.org/wiki/Personal_budget)). Use 100% when it is an income.
   - `AssetType`: The type of asset when the category is for **Category 3: Investments**.

   B) **Config: "WildcardsCategory.csv"**

   In this file, you define patterns for words found in your BankFile details. When a matching pattern is detected, it will link to the appropriate category (as set up in **CategoriesDefinition.csv**). You need to provide an existing ID from **CategoriesDefinition.csv**.

   C) **Config: "AbsoluteCategory.csv"**

   This file is useful for categorizing specific transactions based on their unique **PK_Hash** (available in the exported CSV dataset). Transactions in **AbsoluteCategory.csv** will take precedence over those categorized through **WildcardsCategory.csv**.

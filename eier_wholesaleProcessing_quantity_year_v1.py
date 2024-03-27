"""
Read csv-File with new values.
Read excel-File with old values.
Compare corresponding values according to Product_Name and Date.
Output results in txt-File.
"""

import pandas as pd
from datetime import datetime

""" set parameters """
# Enter NEW_FILENAME. An abbreviation of it will also be used to
# create the output-file name with the results.
NEW_FILENAME = "F_MARS_708_FACT_VW410_Public_Eggs_WholesaleProcessing__Quantity_Year.csv"

# VERSION will be used to create the output-file name with the results.
VERSION = "v1"

# round to number of decimals.
# There will be as many iterations, as values are given.
ACCURACY = [2, 4]

""" read new file and create a dataframe for each Product_Name """
new_file = pd.read_csv(
    f"new/{NEW_FILENAME}", header=0, sep=";"
)

list_of_new_dataframes = []
for product in new_file["Product_Name"].unique():
    new_dataframe = new_file.loc[new_file["Product_Name"] == product]
    new_dataframe.set_index("YearMonthCode", inplace=True)
    new_dataframe = new_dataframe.sort_index()
    new_dataframe.Name = product
    list_of_new_dataframes.append(new_dataframe)

""" prepare old file 
read in the old file. Names of columns had to be changed manually so that
the correspond to the Product_Name in the new files """
old_file = pd.read_excel(
    "old/WholesaleProcessing_quantity_Year_OLD.xlsx",
    names=[
        "Year",
        "Inland Verarbeitungeier"
    ],
    skiprows=1,
    index_col=None,
)

old_file["Year"] = old_file["Year"].astype(str) + "01"
old_file.set_index("Year", inplace=True)


""" parameters for output-file name """
output_name = NEW_FILENAME[22:-4]
now = datetime.now().replace(microsecond=0).strftime('%Y%m%d%H%M%S')

""" compare values in new and old files with writing result in an output-file """
iter_over = list_of_new_dataframes[0].index.to_list()
with open(f"output/{output_name}_{VERSION}_{now}.txt", "a") as f:
    for round_to in ACCURACY:
        f.write(
            f'{"#"*100}\n\nValues accuracy: Values rounded to {round_to}\n\n{"#"*100}\n\n')
        for _, df in enumerate(list_of_new_dataframes):
            f.write(f'{"="*20}\n{df.Name}\n\n')
            total = 0  # counter to keep track of total entries
            correct = 0  # counter to keep track of correct entries

            for date in df.index:
                date_str = str(date)

                try:
                    total += 1
                    old = old_file[df.Name].loc[date_str]
                    old = round(old, round_to)
                    new = df["KeyIndicator"].loc[date]
                    new = round(new, round_to)
                    differenz = (old-new)*100

                    if old != new:
                        f.write(
                            f"{date} : test passed: {old == new}. "
                            f"Old value: {old}, new value: {new}. "
                            f"Differenz <old - new> in "
                            f"Rappen = {differenz}\n"
                        )
                    else:
                        correct += 1

                except KeyError as e:
                    f.write(f"{e} : No Value found.\n")

            f.write(f"\nnumber correct entries: {correct} / {total} \n\n")

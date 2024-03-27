"""
Read csv-File with new values.
Read excel-File with old values.
Compare corresponding values according to Product_Name and Date.
Output results in txt-File.
"""

import pandas as pd
from datetime import datetime

""" set parameters 
Enter NEW_FILENAME. An abbreviation of it will also be used to create the 
output-file name with the results."""
NEW_FILENAME = "F_MARS_708_FACT_VW405_Public_Eggs_Consumption__Price_Month.csv"

"""VERSION will be used to create the output-file name with the results."""
VERSION = "v1"

"""round to number of decimals.
There will be as many iterations, as values are given."""
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
read in the old file. Names of columns had to be changed manually to 
correspond to the Product_Name in the new files """
old_file = pd.read_excel(
    "old/KPEier_2016_01_d.xlsx",
    sheet_name="Preise",
    names=[
        "Monat",
        "Bio, Inland roh",
        "Bodenhaltung, Inland roh",
        "Freiland-/Auslaufhaltung, Inland roh",
        "Spezial, Inland roh",
        "alle Produktionsformen, gewichteter Mittelwert, Inland roh",
        "Bio, Importeier roh",
        "Bodenhaltung, Import roh",
        "Freiland-/Auslaufhaltung, Importeier roh",
        "Alle Produktionsformen, gewichteter Mittelwert, Importeier roh",
        "Bio, Inland gekocht",
        "Bodenhaltung, Inland gekocht",
        "Freiland-/Auslaufhaltung, Inland gekocht",
        "Spezial, Inland gekocht",
        "alle Produktionsformen, gewichteter Mittelwert, Inland gekocht",
        "Bodenhaltung, Import gekocht",
        "Freiland-/Auslaufhaltung, Importeier gekocht",
        "alle Produktionsformen, gewichteter Mittelwert, Importeier gekocht",
        "Bio, Inland Region 1 roh",
        "Bodenhaltung, Inland Region 1 roh",
        "Freiland-/Auslaufhaltung, Inland Region 1 roh",
        "Spezial, Inland Region 1 roh",
        "alle Produktionsformen gewichteter Mittelwert Inland Region 1 roh",
        "Bio, Inland Region 2 roh",
        "Bodenhaltung, Inland Region 2 roh",
        "Freiland-/Auslaufhaltung, Inland Region 2 roh",
        "Spezial, Inland Region 2 roh",
        "alle Produktionsformen gewichteter Mittelwert Inland Region 2 roh",
        "Bio, Inland Region 3 roh",
        "Bodenhaltung, Inland Region 3 roh",
        "Freiland-/Auslaufhaltung, Inland Region 3 roh",
        "Spezial, Inland Region 3 roh",
        "alle Produktionsformen gewichteter Mittelwert Inland Region 3 roh",
        "Bio, Inland Region 4 roh",
        "Bodenhaltung, Inland Region 4 roh",
        "Freiland-/Auslaufhaltung, Inland Region 4 roh",
        "Spezial, Inland Region 4 roh",
        "alle Produktionsformen gewichteter Mittelwert Inland Region 4 roh",
        "Bio, Inland Region 5 roh",
        "Bodenhaltung, Inland Region 5 roh",
        "Freiland-/Auslaufhaltung, Inland Region 5 roh",
        "Spezial, Inland Region 5 roh",
        "alle Produktionsformen gewichteter Mittelwert Inland Region 5 roh",
        "Eier roh, CH und Import, gewichteter Mittelwert",
        "Eier gekocht, CH und Import, gewichteter Mittelwert",
        "Bio, Inland roh 4er-packung",
        "Bodenhaltung, Inland roh 4er-packung",
        "Freiland-/Auslaufhaltung, Inland roh 4er-packung",
        "alle Produktionsformen, gewichteter Mittelwert, Inland roh 4er-packung",
        "Bio, Inland roh 6er-packung",
        "Bodenhaltung, Inland roh 6er-packung",
        "Freiland-/Auslaufhaltung, Inland roh 6er-packung",
        "Spezial, Inland roh 6er-packung",
        "alle Produktionsformen, gewichteter Mittelwert, Inland roh 6er-packung",
        "Bodenhaltung, Inland roh 10er-packung",
        "Freiland-/Auslaufhaltung, Inland roh 10er-packung",
        "alle Produktionsformen, gewichteter Mittelwert, Inland roh 10er-packung",
    ],
    header=0,
    skiprows=11,
)


old_file.set_index("Monat", inplace=True)
old_file.index = pd.to_datetime(
    old_file.index, errors="coerce").strftime("%Y%m")


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
                total += 1
                date_str = str(date)

                try:
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

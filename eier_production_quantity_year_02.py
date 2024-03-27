
# eier_production_quantity_year_02.py

# py_script for eier production month

import pandas as pd

round_to_iter = [2, 4]

""" read in the old file"""
new_file = pd.read_csv(
    "new/F_MARS_708_FACT_VW404_Public_Eggs_Production__Quantity_Year.csv",
    header=0,
    sep=";",
)
# print(new_file.head())


""" prepare old file """
""" read in the old file"""

old_file = pd.read_excel(
    "old/MBE_Excel.xlsm",
    sheet_name="D.1 Prod + AH + Verbrauch",
    names=[
        "Year",
        "Bevölkerung inkl. Tourismus",
        "Inland Produktion",  # old "Produktion Schaleneier Inland Total in Mio Stück"
        "Import Schaleneier, total CH",  # "Import Konsumeier in Mio Stück",
        "Import Verarbeitungseier in Mio Stück",
        "Total Import in Mio Stück",
        "Inland Verarbeitungeier",  # old "Verarbeitung CH-Eier zu Eiprodukten in Mio Stück"
        "Import Eiprodukte flüssig in Mio Stück",
        "Import Eiprodukte getrocknet in Mio Stück",
        "Import Verarbeitungseier in Mio Stück",
        "Inland Konsumeier, Total",  # "Verbrauch Inland Schaleneier  in Mio Stück"
        "Verbrauch Inland Schaleneier Import in Mio Stück",
        "Verbrauch Inland Schaleneier Total in Mio Stück",
        "Verbrauch Inland Schaleneier Anteil Inland in %",
        "Verbrauch Inland Schaleneier Anteil Import in %",
        "Verbrauch Inland Eiprodukte in Mio Stück",
        "Verbrauch Inland Eiprodukte Import in Mio Stück",
        "Verbrauch Inland Eiprodukte Total in Mio Stück",
        "Verbrauch Inland Eiprodukte Anteil Inland in %",
        "Verbrauch Inland Eiprodukte Anteil Import in %",
        "Gesamtverbrauch",
        "Verbrauch Inland Total Anteil Inland in %",
        "Verbrauch Inland Total Anteil Import in %",
        "Pro-Kopf-Verbrauch Total Inland in Stück/Kopf",
        "Pro-Kopf-Verbrauch Total Import in Stück/Kopf",
        "Pro-Kopf-Verbrauch Total Total in Stück/Kopf",
        "Pro-Kopf-Verbrauch Schaleneier Inland in Stück/Kopf",
        "Pro-Kopf-Verbrauch Schaleneier Import in Stück/Kopf",
        "Pro-Kopf-Verbrauch Schaleneier Total in Stück/Kopf",
        "Pro-Kopf-Verbrauch Schaleneier Eiprodukte Inland in Stück/Kopf",
        "Pro-Kopf-Verbrauch Schaleneier Eiprodukte Import in Stück/Kopf",
        "Pro-Kopf-Verbrauch Schaleneier Eiprodukte Total in Stück/Kopf",
    ],
    skiprows=17,
    index_col=None,
)

# print(old_file.head())

old_file["Year"] = old_file["Year"].astype(str) + "01"
# print(old_file.head())
old_file.set_index("Year", inplace=True)
# print(old_file.head())

# old_file.index = pd.to_datetime(old_file.index, errors="coerce").strftime("%Y")
# print(old_file.head())


"""change format of index to match new file's YearMonthCode format and select relevant data from 2016 onwards"""

old_file["Inland Produktion"] = old_file["Inland Produktion"]
old_file["Inland Konsumeier, Total"] = old_file["Inland Konsumeier, Total"]
old_file["Gesamtverbrauch"] = old_file["Gesamtverbrauch"]

inland_produktion_old = old_file["Inland Produktion"]
inland_verarbeitungeier_old = old_file["Gesamtverbrauch"]
inland_konsumeier_old = old_file["Inland Konsumeier, Total"]


""" prepare new file """

""" split new file into different dataframes according to production forms"""
new_file.set_index("YearMonthCode", inplace=True)
new_file = new_file.sort_index()

"""
import_verarbeitungseier_new = new_file.loc[
    new_file["Product_Name"] == "Import Verarbeitungseier"
]
import_verarbeitungseier_new = import_verarbeitungseier_new.sort_index()
import_verarbeitungseier_new.Name = "Import Verarbeitungseier"
# print(import_verarbeitungseier_new.head())
"""
inland_verarbeitungeier_new = new_file.loc[
    (new_file["Product_Name"] == "Gesamtverbrauch")
    & (new_file["Unit_Name"] == "Stück")
]
inland_verarbeitungeier_new = inland_verarbeitungeier_new.sort_index()
inland_verarbeitungeier_new.Name = "Gesamtverbrauch"


inland_konsumeier_total_new = new_file.loc[
    new_file["Product_Name"] == "Inland Konsumeier, Total"
]
inland_konsumeier_total_new = inland_konsumeier_total_new.sort_index()
inland_konsumeier_total_new.Name = "Inland Konsumeier, Total"


inland_produktion_total_new = new_file.loc[
    new_file["Product_Name"] == "Inland Produktion"
]
inland_produktion_total_new = inland_produktion_total_new.sort_index()
inland_produktion_total_new.Name = "Inland Produktion"


""" validate values in old and new file"""

product_names = new_file["Product_Name"].unique()
missing_products_in_newfile = []

for entry in product_names:
    if entry not in new_file["Product_Name"].unique():
        missing_products_in_newfile.append(entry)


iter_over = inland_konsumeier_total_new.index.to_list()

list_df_new = [
    inland_verarbeitungeier_new,
    inland_konsumeier_total_new,
    inland_produktion_total_new,
]

with open("output/ma_eier_production_quantity_year_04.txt", "a") as f:

    for round_to in round_to_iter:

        f.write(
            f'{"#"*20}\n\nValues accuracy: Values rounded to {round_to}\n\n{"#"*20}\n\n')
        for x, y in enumerate(list_df_new):

            try:
                for p in product_names:

                    if y["Product_Name"].loc[202201] == p:
                        f.write(f'{"="*20}\n{y.Name}\n\n\n')

                        try:
                            correct = 0  # counter to keep track of correct entries
                            total = 0

                            for i, v in enumerate(iter_over):
                                date = v
                                date_str = str(v)

                                try:
                                    total += 1
                                    old = old_file[p].loc[date_str]
                                    old = round(old, round_to)

                                    new = y["KeyIndicator"].loc[date]
                                    new = round(new, round_to)
                                    differenz = round(old-new, round_to)

                                    if old != new:
                                        f.write(
                                            f"{date} : test passed: {old == new} --> old value: {old}, new value: {new}. Differenz <old - new> in Mio. Stück = {differenz}\n"
                                        )
                                    else:
                                        correct += 1
                                except KeyError as e:
                                    f.write(f"{e} : No Value found.\n")
                            f.write(
                                f"\nnumber correct entries: {correct} / {total} \n\n")

                        except IndexError as ie:
                            # f.write(f"IndexError {ie}: Data missing -> {y}\n")
                            continue
                        except KeyError as ke:
                            # f.write(f"KeyError {ke}: Data missing -> {y}\n")
                            continue
                        # print(f"end: {p} for {list_df_new[x].Name} \n")
                    else:
                        # f.write(f"No entry in {y.Name} for {p}. Abort.\n")
                        continue
            except IndexError as ie:
                f.write(
                    f"IndexError {ie}: Elements missing for {p}\n{'='*20}\n")
                continue
            except KeyError as ke:
                # f.write(f"KeyError {ke}: Data missing for {p}\n")
                continue

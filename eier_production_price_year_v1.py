# consumption_price_month_02.py

import pandas as pd

""" read in the old file"""
new_file = pd.read_csv(
    "new/F_MARS_708_FACT_VW402_Public_Eggs_Production__Price_Year.csv", header=0, sep=";"
)

round_to_iter = [2, 4]


""" prepare old file """
""" read in the old file"""

old_file = pd.read_excel(
    "old/MBE_Excel.xlsm",
    sheet_name="D.4 PP",
    names=[
        "Year",
        "Bio, <50g",
        "Bio, 50-53g",
        "Bio, >53g",
        "Bio, 2.Klasse",
        "Bio, gewichteter Mittelwert",
        "Bodenhaltung, <50g",
        "Bodenhaltung, 50-53g",
        "Bodenhaltung, >53g",
        "Bodenhaltung, 2.Klasse",
        "Bodenhaltung, gewichteter Mittelwert",
        "Freiland-/Auslaufhaltung, <50g",
        "Freiland-/Auslaufhaltung, 50-53g",
        "Freiland-/Auslaufhaltung, >53g",
        "Freiland-/Auslaufhaltung, 2.Klasse",
        "Freiland-/Auslaufhaltung, gewichteter Mittelwert",
        "CH Gesamt",
        "Import Verarbeitungseier",  # old "Verarbeitungseier Import"
        "Import Konsumeier",  # old "Konsumeier Import"
        "CH und Import",
    ],
    skiprows=15,
    index_col=None,
)
# print(old_file.head())
# old_file.set_index("Year", inplace=True)

# print(old_file.head())

old_file["Year"] = old_file["Year"].astype(str) + "01"
# print(old_file.head())
old_file.set_index("Year", inplace=True)
# print(old_file.head())

# print(old_file.head())


"""change format of index to match new file's YearMonthCode format and select relevant data from 2016 onwards"""
"""import_old = old_file.loc[:, old_file.columns.str.startswith("Import")]
import_verarbeitungseier_old = old_file["Import Verarbeitungseier"]
import_konsumeier_old = old_file["Import Konsumeier"]
"""
""" prepare new file """
""" read in the old file"""

""" split new file into different dataframes according to production forms"""
new_file.set_index("YearMonthCode", inplace=True)
new_file = new_file.sort_index()


""" split new file into different dataframes according to production forms"""
bio_under50_new = new_file.loc[new_file["Product_Name"] == "Bio, <50g"]
bio_under50_new = bio_under50_new.sort_index()
bio_under50_new.Name = "Bio, <50g"

bio_over53_new = new_file.loc[new_file["Product_Name"] == "Bio, >53g"]
bio_over53_new = bio_over53_new.sort_index()
bio_over53_new.Name = "Bio, >53g"

bio_5053_new = new_file.loc[new_file["Product_Name"] == "Bio, 50-53g"]
bio_5053_new = bio_5053_new.sort_index()
bio_5053_new.Name = "Bio, 50-53g"


bio_gewichteter_Mittelwert_new = new_file.loc[
    (new_file["Product_Name"] == "Bio, gewichteter Mittelwert") & (
        new_file["ProductProperties_Name"] == "roh")
]
bio_gewichteter_Mittelwert_new = bio_gewichteter_Mittelwert_new.sort_index()
bio_gewichteter_Mittelwert_new.Name = "Bio, gewichteter Mittelwert"


bodenhaltung_under50_new = new_file.loc[
    new_file["Product_Name"] == "Bodenhaltung, <50g"
]
bodenhaltung_under50_new = bodenhaltung_under50_new.sort_index()
bodenhaltung_under50_new.Name = "Bodenhaltung, <50g"

bodenhaltung_over53_new = new_file.loc[new_file["Product_Name"]
                                       == "Bodenhaltung, >53g"]
bodenhaltung_over53_new = bodenhaltung_over53_new.sort_index()
bodenhaltung_over53_new.Name = "Bodenhaltung, >53g"

bodenhaltung_5053_new = new_file.loc[new_file["Product_Name"]
                                     == "Bodenhaltung, 50-53g"]
bodenhaltung_5053_new = bodenhaltung_5053_new.sort_index()
bodenhaltung_5053_new.Name = "Bodenhaltung, 50-53g"

bodenhaltung_gewichteter_Mittelwert_new = new_file.loc[
    (new_file["Product_Name"] == "Bodenhaltung, gewichteter Mittelwert") & (
        new_file["ProductProperties_Name"] == "roh")
]
bodenhaltung_gewichteter_Mittelwert_new = (
    bodenhaltung_gewichteter_Mittelwert_new.sort_index()
)
bodenhaltung_gewichteter_Mittelwert_new.Name = "Bodenhaltung, gewichteter Mittelwert"


freiland_under50_new = new_file.loc[
    new_file["Product_Name"] == "Freiland-/Auslaufhaltung, <50g"
]
freiland_under50_new = freiland_under50_new.sort_index()
freiland_under50_new.Name = "Freiland-/Auslaufhaltung, <50g"

freiland_over53_new = new_file.loc[
    new_file["Product_Name"] == "Freiland-/Auslaufhaltung, >53g"
]
freiland_over53_new = freiland_over53_new.sort_index()
freiland_over53_new.Name = "Freiland-/Auslaufhaltung, >53g"

freiland_5053_new = new_file.loc[
    new_file["Product_Name"] == "Freiland-/Auslaufhaltung, 50-53g"
]
freiland_5053_new = freiland_5053_new.sort_index()
freiland_5053_new.Name = "Freiland-/Auslaufhaltung, 50-53g"

freiland_gewichteter_Mittelwert_new = new_file.loc[
    (new_file["Product_Name"] == "Freiland-/Auslaufhaltung, gewichteter Mittelwert") & (
        new_file["ProductProperties_Name"] == "roh")
]
freiland_gewichteter_Mittelwert_new = freiland_gewichteter_Mittelwert_new.sort_index()
freiland_gewichteter_Mittelwert_new.Name = (
    "Freiland-/Auslaufhaltung, gewichteter Mittelwert"
)


bio_2klasse_new = new_file.loc[
    (new_file["Product_Name"] == "Bio, 2. Klasse") & (
        new_file["ProductProperties_Name"] == "roh")
]

bio_2klasse_new = bio_2klasse_new.sort_index()
bio_2klasse_new.Name = (
    "Bio, 2. Klasse"
)

bodenhaltung_2klasse_new = new_file.loc[
    (new_file["Product_Name"] == "Bodenhaltung, 2. Klasse") & (
        new_file["ProductProperties_Name"] == "roh")
]
bodenhaltung_2klasse_new = bodenhaltung_2klasse_new.sort_index()
bodenhaltung_2klasse_new.Name = (
    "Bodenhaltung, 2. Klasse"
)

freiland_2klasse_new = new_file.loc[
    (new_file["Product_Name"] == "Freiland-/Auslaufhaltung, 2. Klasse") & (
        new_file["ProductProperties_Name"] == "roh")
]
freiland_2klasse_new = freiland_2klasse_new.sort_index()
freiland_2klasse_new.Name = (
    "Freiland-/Auslaufhaltung, 2. Klasse"
)


""" validate values in old and new file"""

product_names = [
    "Bio, <50g",
    "Bio, 50-53g",
    "Bio, >53g",
    "Bio, 2.Klasse",
    "Bio, gewichteter Mittelwert",
    "Bodenhaltung, <50g",
    "Bodenhaltung, 50-53g",
    "Bodenhaltung, >53g",
    "Bodenhaltung, 2.Klasse",
    "Bodenhaltung, gewichteter Mittelwert",
    "Freiland-/Auslaufhaltung, <50g",
    "Freiland-/Auslaufhaltung, 50-53g",
    "Freiland-/Auslaufhaltung, >53g",
    "Freiland-/Auslaufhaltung, 2.Klasse",
    "Freiland-/Auslaufhaltung, gewichteter Mittelwert",
    "alle Produktionsformen, gewichteter Mittelwert",
    "alle Produktionsformen, Import",
    "alle Produktionsformen CH und Import, gewichteter Mittelwert",
    "Anteil_Erhebung_an_Gesamtproduktion_CH",
    "Anteil_Bio",
    "Anteil_Bodenhaltung",
    "Anteil_Freiland",
]
missing_products_in_newfile = []

for entry in product_names:
    if entry not in new_file["Product_Name"].unique():
        missing_products_in_newfile.append(entry)


iter_over = bio_under50_new.index.to_list()


list_df_new = [
    bio_over53_new,
    bio_under50_new,
    bio_5053_new,
    bio_gewichteter_Mittelwert_new,
    bodenhaltung_under50_new,
    bodenhaltung_over53_new,
    bodenhaltung_5053_new,
    bodenhaltung_gewichteter_Mittelwert_new,
    freiland_under50_new,
    freiland_5053_new,
    freiland_over53_new,
    freiland_gewichteter_Mittelwert_new,
    bio_2klasse_new,
    bodenhaltung_2klasse_new,
    freiland_2klasse_new
]


"""
for df in list_df_new:
    print(df.Name)
"""

with open("output/ma_eier_production_price_year_04.txt", "a") as f:

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

                                    differenz = (old-new)*100

                                    if old != new:
                                        f.write(
                                            f"{date} : test passed: {old == new} --> old value: {old}, new value: {new}. Differenz <old - new> in Rappen = {differenz}\n"
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


# get values from differen year-aggregation
old_file_2 = pd.read_excel(
    "old/MBE_Excel.xlsm",
    sheet_name="D.3 MEM",
    names=[
        "Year",
        "Aufschlagsaktion Beitrag in CHF / Ei",  # old: "Inland, Frisch, Bio",
        "Aufschlagsaktion, Ist",  # "Aufschlagsaktion in Stück",
        "Verbilligungsaktion Beitrag in CHF / Ei",
        # Verbilligungsaktion in Stück" "Eingesetzte Mittel Aufschlagsaktion in CHF",
        "Verbilligungsaktion, Ist",
        "Eingesetzte Mittel Aufschlagsaktion in CHF",
        "Eingesetzte Mittel Verbilligungsaktion in CHF",
        "Eingesetzte Mittel Total in CHF",
        "Maximal zur Verfügung stehende Bundesmitttel Aufschlagsaktion in CHF",
        "Maximal zur Verfügung stehende Bundesmitttel Verbilligungsaktion in CHF",
        "Maximal zur Verfügung stehende Bundesmitttel Total in CHF",
        "Auslastung Mittel",
        "Anteil betroffene Eier an Inlandproduktion",
    ],
    header=0,
    skiprows=18,
)


old_file_2["Year"] = old_file_2["Year"].astype(str) + "01"

old_file_2.set_index("Year", inplace=True)


""" split new file into different dataframes according to production forms"""
aufschlagsaktion_ist_new = new_file.loc[new_file["Product_Name"]
                                        == "Aufschlagsaktion, Ist"]
aufschlagsaktion_ist_new = aufschlagsaktion_ist_new.sort_index()
aufschlagsaktion_ist_new.Name = "Aufschlagsaktion, Ist"

verbilligungsaktion_ist_new = new_file.loc[new_file["Product_Name"]
                                           == "Verbilligungsaktion, Ist"]
verbilligungsaktion_ist_new = verbilligungsaktion_ist_new.sort_index()
verbilligungsaktion_ist_new.Name = "Verbilligungsaktion, Ist"


"""
product_names = [
    "Bio, <50g",
    "Bio, 50-53g",
    "Bio, >53g",
    "Bio, 2.Klasse",
    "Bio, gewichteter Mittelwert",
    "Bodenhaltung, <50g",
    "Bodenhaltung, 50-53g",
    "Bodenhaltung, >53g",
    "Bodenhaltung, 2.Klasse",
    "Bodenhaltung, gewichteter Mittelwert",
    "Freiland-/Auslaufhaltung, <50g",
    "Freiland-/Auslaufhaltung, 50-53g",
    "Freiland-/Auslaufhaltung, >53g",
    "Freiland-/Auslaufhaltung, 2.Klasse",
    "Freiland-/Auslaufhaltung, gewichteter Mittelwert",
    "alle Produktionsformen, gewichteter Mittelwert",
    "alle Produktionsformen, Import",
    "alle Produktionsformen CH und Import, gewichteter Mittelwert",
    "Anteil_Erhebung_an_Gesamtproduktion_CH",
    "Anteil_Bio",
    "Anteil_Bodenhaltung",
    "Anteil_Freiland",
]
missing_products_in_newfile = []

for entry in product_names:
    if entry not in new_file["Product_Name"].unique():
        missing_products_in_newfile.append(entry)

"""
iter_over = bio_under50_new.index.to_list()


list_df_new = [
    aufschlagsaktion_ist_new,
    verbilligungsaktion_ist_new
]


"""
for df in list_df_new:
    print(df.Name)
"""

with open("output/ma_eier_production_price_year_04.txt", "a") as f:

    for round_to in round_to_iter:

        f.write(
            f'{"#"*20}\n\nValues accuracy: Values rounded to {round_to}\n\n{"#"*20}\n\n')
        for x, y in enumerate(list_df_new):

            try:
                for p in product_names:

                    try:
                        if y["Product_Name"].loc[202001] == p:

                            f.write(f'{"="*20}\n{y.Name}\n\n\n')

                            correct = 0  # counter to keep track of correct entries
                            total = 0

                            for i, v in enumerate(iter_over):
                                date = v
                                date_str = str(v)

                                try:
                                    total += 1
                                    old = old_file_2[p].loc[date_str]
                                    old = round(old, round_to)

                                    new = y["KeyIndicator"].loc[date]
                                    new = round(new, round_to)

                                    differenz = (old-new)*100

                                    if old != new:
                                        f.write(
                                            f"{date} : test passed: {old == new} --> old value: {old}, new value: {new}. Differenz <old - new> in Rappen = {differenz}\n"
                                        )

                                    else:
                                        correct += 1
                                except KeyError as e:
                                    f.write(f"{e} : No Value found.\n")
                            f.write(
                                f"\nnumber correct entries: {correct} / {total} \n\n")
                        else:
                            # f.write(f"No entry in {y.Name} for {p}. Abort.\n")
                            continue

                    except IndexError as ie:
                        # f.write(f"IndexError {ie}: Data missing -> {y}\n")
                        continue
                    except KeyError as ke:
                        # f.write(f"KeyError {ke}: Data missing -> {y}\n")
                        continue
                    # print(f"end: {p} for {list_df_new[x].Name} \n")
            except IndexError as ie:
                f.write(
                    f"IndexError {ie}: Elements missing for {p}\n{'='*20}\n")
                continue
            except KeyError as ke:
                # f.write(f"KeyError {ke}: Data missing for {p}\n")
                continue

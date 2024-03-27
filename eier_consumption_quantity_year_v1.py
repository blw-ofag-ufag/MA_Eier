import pandas as pd

round_to_iter = [2, 4]

""" read the new file"""
new_file = pd.read_csv(
    "new/F_MARS_708_FACT_VW408_Public_Eggs_Consumption_NotLD_Quantity_Year.csv",
    header=0,
    sep=";",
)

""" prepare old file """
""" read in the old file"""
old_file = pd.read_excel(
    "old/MBE_Excel.xlsm",
    sheet_name="D.7 MS",
    names=[
        "Year",
        "Bio, Produktion Inland Erhebung Sammelstellen in %",
        "Bodenhaltung, Produktion Inland Erhebung Sammelstellen in %",
        "Freilandhaltung, Produktion Inland Erhebung Sammelstellen in %",
        "Abdeckung durch Erhebung, Produktion Inland Erhebung Sammelstellen in %",
        "Bio, Produktion Inland, Produktion Total aus Kükenstatistik in %",
        "Boden- und Freilaldnhaltung, Produktion Inland, Produktion Total aus Kükenstatistik in %",
        "Bio, Liefer- und Abholgrosshandel Schaleneier in %",
        "Bodenhaltung, Liefer- und Abholgrosshandel Schaleneier in %",
        "Freilandhaltung, Liefer- und Abholgrosshandel Schaleneier in %",
        "Anteil Inland, Liefer- und Abholgrosshandel Schaleneier in %",
        "Anteil Import, Liefer- und Abholgrosshandel Schaleneier in %",
        "Ohne Angabe, Liefer- und Abholgrosshandel Schaleneier in %",
        "Anteil Inland, Liefer- und Abholgrosshandel Eiprodukte in %",
        "Anteil Import, Liefer- und Abholgrosshandel Eiprodukte in %",
        "Anteil Ohne Angabe, Liefer- und Abholgrosshandel Eiprodukte in %",
        "Total in % Anteil Inland",
        "Total in % Anteil Import",
        "Total in % Ohne Angabe",
        "Total in % Schaleneier",
        "Total in % Eiprodukte",
        "Bio, Detailhandel Schaleneier in %",
        "Bodenhaltung, Detailhandel Schaleneier in %",
        "Freilandhaltung, Detailhandel Schaleneier in %",
        "Import, Detailhandel Schaleneier in %",
        "Anteil Inland, Detailhandel Schaleneier in %",
        "Anteil Import, Detailhandel Schaleneier in %",
        "Total",
        "Bio, CH",
        "Bodenhaltung, CH",
        "Freiland-/Auslaufhaltung, CH",
        "alle Produktionsformen, Import"

    ],
    header=None,
    skiprows=4,
)

old_file["Year"] = old_file["Year"].astype(str) + "01"

old_file.set_index("Year", inplace=True)


""" prepare new file """
""" split new file into different dataframes according to production forms"""
new_file.set_index("YearMonthCode", inplace=True)
new_file = new_file.sort_index()


total_new = new_file.loc[(new_file["Product_Name"] == "Total") & (
    new_file["ForeignTrade_Name"] == "Import")]
total_new["KeyIndicator"] = total_new["KeyIndicator"].groupby(
    total_new.index).sum()
total_new = total_new.sort_index()
total_new.Name = "Total"

freiland_ch_new = new_file.loc[
    (new_file["Product_Name"] == "Freiland-/Auslaufhaltung, CH") & (
        new_file["CostComponent_Name"] == "inkl. MwSt")
]
freiland_ch_new = freiland_ch_new.sort_index()
freiland_ch_new.Name = "Freiland-/Auslaufhaltung, CH"

bio_ch_new = new_file.loc[
    (new_file["Product_Name"] == "Bio, CH") & (
        new_file["CostComponent_Name"] == "inkl. MwSt")
]
bio_ch_new = bio_ch_new.sort_index()
bio_ch_new.Name = "Bio, CH"

bodenhaltung_ch_new = new_file.loc[
    (new_file["Product_Name"] == "Bodenhaltung, CH") & (
        new_file["CostComponent_Name"] == "inkl. MwSt")
]

bodenhaltung_ch_new = bodenhaltung_ch_new.sort_index()
bodenhaltung_ch_new.Name = "Bodenhaltung, CH"


list_df_new = [
    total_new,
    bio_ch_new,
    bodenhaltung_ch_new,
    freiland_ch_new,
    # ohne_angabe_new,
    # alle_import_new,

]


missing_products_in_newfile = []
product_names = []

for df in list_df_new:
    product_names.append(df.Name)

for entry in product_names:
    if entry not in new_file["Product_Name"].unique():
        missing_products_in_newfile.append(entry)


iter_over = bio_ch_new.index.to_list()


with open("output/ma_eier_consumption_quantity_year_04.txt", "a") as f:

    for round_to in round_to_iter:

        f.write(
            f'{"#"*20}\n\nValues accuracy: Values rounded to {round_to}\n\n{"#"*20}\n\n')
        for x, y in enumerate(list_df_new):

            try:
                for p in product_names:

                    try:
                        if y["Product_Name"].loc[202001] == p:
                            f.write(f'{"="*20}\n{y.Name}\n\n\n')
                            n = 0  # counter to keep track of correct entries
                            for i, v in enumerate(iter_over):

                                date = v
                                date_str = str(v)

                                try:
                                    old = old_file[p].loc[date_str]

                                    old = round(old, 4)

                                    new = y["KeyIndicator"].loc[date]

                                    new = round(new, 4)
                                    differenz = (old-new)

                                    if old != new:
                                        f.write(
                                            f"{date} : test passed: {old == new} --> old value: {old}, new value: {new}. Differenz <old - new> in Stück = {differenz}\n"
                                        )
                                    else:
                                        n += 1
                                except KeyError as e:
                                    f.write(f"{e} : No Value found.\n")
                            f.write(f"\nnumber correct entries: {n} \n\n")
                        else:
                            # f.write(f"No entry in {y.Name} for {p}. Abort.\n")
                            # print("bla")
                            # print(f"end: {p} for {list_df_new[x].Name} \n")

                            continue
                    except IndexError as ie:
                        # f.write(f"IndexError {ie}: Data missing -> {y}\n")
                        # print(f"IndexError {ie}: Data missing -> {y}\n")
                        continue
                    except KeyError as ke:
                        # f.write(f"KeyError {ke}: Data missing -> {y}\n")
                        # print(f"KeyError {ke}: Data missing -> {y}\n")
                        continue

            except IndexError as ie:
                f.write(
                    f"IndexError {ie}: Elements missing for {p} in {y}\n{'='*20}\n")
                continue
            except KeyError as ke:
                # f.write(f"KeyError {ke}: Data missing for {p}\n")
                print(f"KeyError {ke}: Data missing for {p} in {y.name}\n")
                continue

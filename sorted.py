import glob
from pathlib import Path
import re
import pandas as pd
import os
import jinja2
from datetime import date

total = 0


def csvToHtml():

    # Set location of CSV files
    csv = "./CSV/*/*.csv"

    # Iterate through CSV files
    for f in glob.glob(csv):
        try:
                    # Get the name for file from folder name
            p = Path(f)
            name = p.parts[1]

            # Get the number of package
            pattern = re.compile(r"\d+")
            m = pattern.search(f).group(0)

            # test if name is retrieved correctly
            # print(name + " contaians CSV file " + m)

            # Variable for the final file name used at the end
            finalName = ("./final/" + name + " - " + m + ".html")
            debug = ("./debug/" + name + " - " + m + " - " + "debug" + ".html")

            # Remove special characters
            with open(f, "r") as file:
                filedata = file.read()

                # replace undesired values
                mapping = [
                    ('"', ""), ("&quot;", ""), ("&lrm;", ""), ("®",
                                                               ""), ("™", ""), ("&#178;", ""), ("&infin;", ""),
                    ("V7M X;", "V7M X"), ("@", "at"), ("”", ""), ("Ņ⑤",
                                                                  ""), ("/n", ""), ("&amp;", ""), ("&#39;", ""),
                    ("&gt;", ""), ("&#176;", ""), ("&#174;",
                                                   ""), ("&#160;", ""), ("&nbsp;", ""), ("â", "a"),
                    ("&apos;", ""), ("&minus;", ""),

                ]
                for k, v in mapping:
                    filedata = filedata.replace(k, v)

            with open(f, "w") as file:
                file.write(filedata)

            # Load cleaned CSV into pandas
            df = pd.read_csv(f, encoding="cp1252", sep=";",
                             error_bad_lines=False, engine="python")

            # Categories

            # Replace Null values in XML with space for sorting
            df.loc[df["XML"].isnull(), 'XML'] = " "
            df["RECIEVER"] = df["CATEGORY"]

            # Zone categories based on their location in warehouse for maximum efficency

            zone1 = ["Headset",]
            zone11 = ["Digital boards",]
            zone12 = ["DDR3 laptop RAM",]
            zone13 = ["Mice",]
            zone14 = ["Laptop batteries"]
            zone15 = ["Network cards",]
            zone16 = ["Mousepads",]
            zone17 = ["Mini-Tower",]
            zone18 = ["Printer Ink"] 
            zones = {
                'zone1': zone1,
                'zone11': zone11,
                'zone12': zone12,
                'zone13': zone13,
                'zone14': zone14,
                'zone15': zone15,
                'zone16': zone16,
                'zone17': zone17,
                'zone18': zone18,
            }

            for zone_name, zone in zones.items():
                zone = dict.fromkeys(zone, f"{zone_name}")
                df["CATEGORY"] = df["CATEGORY"].replace(zone)

            # Sort Columns
            shipment = df.sort_values(
                ["CATEGORY", "CATEGORY"], ascending=(True, True))
            shipment["INVOICE"] = shipment["INVOICE"].fillna("")
            shipment["XML"] = shipment["XML"].fillna("")

            pd.set_option('precision', 0)
            pd.set_option('display.float_format', lambda x: '%.0f' % x)

            with pd.option_context('display.max_colwidth', 1):
                output_html = shipment.to_html(finalName, index=None, border=0,
                                           columns=("ID", "PRICE", "PRODUCT", "EAN",
                                                    "PN", "INVOICE", "TK",
                                                    "XML"), na_rep=" ")

            with pd.option_context('display.max_colwidth', 1):
                output_html = shipment.to_html(debug, index=None, border=0,
                                           columns=("ID", "PRODUCT", "EAN",
                                                    "PN", "CATEGORY", "RECIEVER", "ADDED",
                                                    "SENDER", "XML"), na_rep=" ")
            total_rows = len(df.index)
            global total
            total += total_rows
        except UnicodeDecodeError as e:
            z = e
            print(f'Encoding error in file {f} - {z}')


def html():

    html = "./final/*.html"
    for f in glob.glob(html):
        patternShipment = re.compile(r"\d+")
        shipment = patternShipment.search(f).group(0)
        patternStore = re.compile(r"\\(\w+)")
        store = patternStore.search(f).group(1)
        print(f'{store} - {shipment}')

        with open(f, "r") as myfile:
            data = myfile.read()

        # setup loader
        templates_path = os.path.join(__file__, "../templates")
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_path))

        # get and fill the template
        data_as_html = data  # from pandas
        store = store
        number = shipment
        date_created = date.today()
        mod_date = date_created.strftime("%d/%m/%Y")
        base_tmpl = env.get_template("base.html")
        html = base_tmpl.render(data_as_html=data_as_html,
                                store=store, number=shipment, date=mod_date)

        # # write to disk
        output_filename = os.path.join(
            __file__, "../final/" + "shipments" + "/" + store + " - " + shipment + ".html")
        with open(output_filename, "w", encoding="cp1252") as outfile:
            outfile.write(html)
        os.remove(f)


csvToHtml()

html()

print(f'Total of {total} lines of products')

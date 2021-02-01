import glob
from pathlib import Path
import re
import pandas as pd
import os
import sys
import jinja2
from datetime import date
import requests
from bs4 import BeautifulSoup
from decouple import config


total = 0
komplekt = []
payload = {
    "login": config("LOGIN"),
    "username": config("NAME"),
    "password": config("PASSWORD"),
    "store": config("STORE")
}
with requests.Session() as s:
    # bundle is for live service that cannot be included here because it is company asset with sensitive information
    bundle = []
    login = s.post(config("LOGIN_URL"), data=payload)
    dest = s.get(config("DESTINATION"))

    soup = BeautifulSoup(dest.content, "lxml")

    for invoice in soup.findAll("a", {"target": "_blank"}):
        bundle.append(invoice.string)

    with open("bundle.txt", "w") as outfile:
        for item in bundle:
            if item == None:
                pass
            else:
                try:
                    outfile.write(f'{item}\n')
                except:
                    pass


def csvToHtmlUnsorted(komplekt):
    try:
        # Set location of CSV files
        csv = "CSV/*/*.csv"

        # Iterate through CSV files
        for f in glob.glob(csv):

            # Get the name for file from folder name
            p = Path(f)
            name = p.parts[1]

            # Get the number of package
            pattern = re.compile(r"\d+")
            m = pattern.search(f).group(0)

            # test if name is retrieved correctly
            # print(name + " contaians CSV file " + m)

            # Variable for the final file name used at the end
            finalName = ("final/" + name + " - " + m + ".html")
            debug = ("debug/" + name + " - " + m + " - " + "debug" + ".html")

            # Remove special characters
            with open(f, "r", encoding="cp1252") as file:
                filedata = file.read()
                # replace undesired values
                mapping = [
                    ('"', ""), ("&quot;", ""), ("&lrm;", ""), ("®", ""), ("™", ""),
                    ("&#178;", ""), ("&infin;", ""), ("V7M X;", "V7M X"), ("@", "at"),
                    ("”", ""), ("Ņ⑤", ""), ("/n", ""), ("&amp;", ""), ("&#39;", ""),
                    ("&gt;", ""), ("&#176;", ""), ("&#174;", ""), ("&#160;", ""),
                    ("&nbsp;", ""), ("â", "a"), ("&apos;", ""), ("&minus;", ""),
                    # custom label for orders
                    ("X_21_000543", "PRODUCTION"),
                    ("X_21_000553", "DAMAGED"),

                ]
                for k, v in mapping:
                    filedata = filedata.replace(k, v)
                for item in bundle:
                    try:
                        filedata = filedata.replace(item, "PROD")
                    except:
                        pass

            with open(f, "w") as file:
                file.write(filedata)

            # Load cleaned CSV into pandas
            df = pd.read_csv(f, encoding="cp1252", sep=";",
                             error_bad_lines=False, engine="python")

            # Categories

            # Replace Null values in XML with space for sorting
            df.loc[df["XML"].isnull(), 'XML'] = " "

            pakk = df.sort_values(["XML", "CATEGORY", "RECIEVER"])
            df["INVOICE"] = df["INVOICE"].fillna("")
            df["XML"] = df["XML"].fillna("")
            df["EAN"] = df["EAN"].fillna("----")

            pd.set_option('precision', 0)
            pd.set_option('display.float_format', lambda x: '%.0f' % x)

            with pd.option_context('display.max_colwidth', 1):
                output_html = df.to_html(finalName, index=None, border=0,
                                           columns=("ID", "PRICE", "PRODUCT", "EAN",
                                                    "PN", "INVOICE", "TK",
                                                    "XML"), na_rep=" ")

            with pd.option_context('display.max_colwidth', 1):
                output_html = df.to_html(debug, index=None, border=0,
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


csvToHtmlUnsorted(komplekt)

html()

print(f'Total of {total} lines of products')

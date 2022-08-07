import os
import pandas as pd
import json
import itertools
import sys
import numpy as np

data = []
for i, js in enumerate(os.listdir("./dataset/")):

    js = os.path.join("dataset", js)
    # print(f"File {i}")
    with open(js, "r") as js_file:
        data.append([di for di in json.loads(js_file.read())[0]["elementList"]])


# print(json.dumps(data, ensure_ascii=False))


with open("merged_dataset.json", "w") as output_file:
    json.dump(list(itertools.chain(*data)), output_file, ensure_ascii=False)

with open("merged_dataset.json", "r") as input_file:
    new_data = json.load(input_file)
    # print(json.dumps(data))
    df = pd.DataFrame.from_dict(new_data)

    print(df.head())
    df = df.drop(["description", "thumbnail"], axis=1)
    print(df.columns)
    df.replace({False: "No", True: "Si"}, inplace=True)
    df = (
        df.sort_values("numPhotos", ascending=False)
        .drop_duplicates("propertyCode")
        .sort_index()
        .reset_index(drop=True)
    )
    df.to_csv("salida.csv", sep=";")
    df.to_excel("cordoba_propiedades_venta.xlsx")

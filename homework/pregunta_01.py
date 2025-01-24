"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import glob
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    def charge(input_dir):
        for a in glob.glob(os.path.join(input_dir, "*.csv")):
            return pd.read_csv(a, sep=";", index_col=0)

    def clean(df):
        df = df.drop_duplicates()
        df = df.dropna()
        return df

    def transform_date(date):
        if "/" in date:
            p = date.split("/")
            if len(p[0]) > 2:
                return f"{p[0]}-{p[1]}-{p[2]}"
            else:
                return f"{p[2]}-{p[1]}-{p[0]}"
        return date

    def process_date(df):

        df["fecha_de_beneficio"] = df["fecha_de_beneficio"].map(transform_date)
        df["fecha_de_beneficio"] = pd.to_datetime(
            df["fecha_de_beneficio"], errors="coerce"
        )
        return df

    def clean_text(df):
        cols = df.columns.tolist()
        cols.remove("barrio")

        df["barrio"] = df["barrio"].map(
            lambda x: x.lower().replace("_", "-").replace("-", " ")
        )

        df[cols] = df[cols].applymap(
            lambda x: (
                x.lower()
                .replace("-", " ")
                .replace("_", " ")
                .replace("$", "")
                .replace(".00", "")
                .replace(",", "")
                .strip()
                if isinstance(x, str)
                else x
            )
        )
        return df

    def save_file(df, output_dir, file_name):
        ruta_salida = os.path.join(output_dir, file_name)
        if os.path.exists(ruta_salida):
            os.remove(ruta_salida)
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(ruta_salida, sep=";", index=False)

    input_dir = "files/input"
    output_dir = "files/output"
    file_name = "solicitudes_de_credito.csv"

    df = charge(input_dir)
    df = clean(df)
    df = process_date(df)
    df = clean_text(df)
    df = clean(df)
    save_file(df, output_dir, file_name)


pregunta_01()

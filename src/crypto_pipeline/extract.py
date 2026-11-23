import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"


def armar_dataframe(datos: dict, coin_id: str) -> pd.DataFrame:
    """Convierte la respuesta de CoinGecko en un DataFrame limpio.

    Descarta precios nulos o no positivos y mediciones repetidas.
    """
    df = pd.DataFrame(datos["prices"], columns=["ts_ms", "precio_usd"])
    df = df.dropna(subset=["precio_usd"])
    df = df[df["precio_usd"] > 0]
    df = df.drop_duplicates(subset="ts_ms")
    df["fecha_hora"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True)
    df["coin_id"] = coin_id
    return df.reset_index(drop=True)


def extraer_precios(coin_id: str, desde: datetime, hasta: datetime) -> pd.DataFrame:
    """Pide a CoinGecko los precios de una moneda entre dos fechas.

    Devuelve un DataFrame con una fila por cada medición.
    """
    load_dotenv()  # lee el .env

    respuesta = requests.get(
        URL.format(coin_id=coin_id),
        params={
            "vs_currency": "usd",
            "from": int(desde.timestamp()),
            "to": int(hasta.timestamp()),
        },
        headers={"x-cg-demo-api-key": os.environ["COINGECKO_API_KEY"]},
        timeout=30,
    )
    respuesta.raise_for_status()  # si hay error, corta y avisa
    return armar_dataframe(respuesta.json(), coin_id)


if __name__ == "__main__":
    from datetime import timedelta, timezone

    hasta = datetime.now(timezone.utc)
    desde = hasta - timedelta(days=1)
    df = extraer_precios("bitcoin", desde, hasta)
    print(df.head())
    print(df.dtypes)
    print("filas:", len(df))
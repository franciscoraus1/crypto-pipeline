import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"


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
    datos = respuesta.json()

    df = pd.DataFrame(datos["prices"], columns=["ts_ms", "precio_usd"])
    df["fecha_hora"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True)
    df["coin_id"] = coin_id
    return df


if __name__ == "__main__":
    from datetime import timedelta, timezone

    hasta = datetime.now(timezone.utc)
    desde = hasta - timedelta(days=1)
    df = extraer_precios("bitcoin", desde, hasta)
    print(df.head())
    print(df.dtypes)
    print("filas:", len(df))
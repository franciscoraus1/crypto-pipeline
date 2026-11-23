from crypto_pipeline.extract import armar_dataframe


def test_descarta_precios_nulos_y_no_positivos():
    datos = {"prices": [[1000, 50.0], [2000, None], [3000, -5.0], [4000, 0]]}

    df = armar_dataframe(datos, "bitcoin")

    assert len(df) == 1
    assert df["precio_usd"].iloc[0] == 50.0


def test_elimina_mediciones_duplicadas():
    datos = {"prices": [[1000, 50.0], [1000, 50.0], [2000, 51.0]]}

    df = armar_dataframe(datos, "bitcoin")

    assert len(df) == 2


def test_agrega_coin_id_y_fecha_utc():
    datos = {"prices": [[0, 10.0]]}

    df = armar_dataframe(datos, "ethereum")

    assert df["coin_id"].iloc[0] == "ethereum"
    assert str(df["fecha_hora"].iloc[0]) == "1970-01-01 00:00:00+00:00"
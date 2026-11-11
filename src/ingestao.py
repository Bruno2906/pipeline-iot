"""
Ingestão: lê o CSV de temperaturas IoT, trata os dados
e insere na tabela temperature_readings do PostgreSQL.
"""
import pandas as pd
from sqlalchemy import create_engine

CSV_PATH = "data/IOT-temp.csv"
DB_URL = "postgresql+psycopg2://postgres:bruno123@localhost:5432/postgres"

def main():
    # 1. Leitura do CSV
    df = pd.read_csv(CSV_PATH)
    print(f"Linhas lidas: {len(df)}")

    # 2. Renomeia as colunas para nomes limpos
    df = df.rename(columns={
        "id": "reading_id",
        "room_id/id": "device_id",
        "noted_date": "noted_at",
        "temp": "temperature",
        "out/in": "location",
    })

    # 3. Converte a data (formato dia-mês-ano hora:minuto)
    df["noted_at"] = pd.to_datetime(df["noted_at"], format="%d-%m-%Y %H:%M")

    # 4. Limpeza: remove nulos e leituras duplicadas
    df = df.dropna()
    df = df.drop_duplicates(subset="reading_id")
    print(f"Linhas após limpeza: {len(df)}")

    # 5. Conexão com o PostgreSQL e inserção
    engine = create_engine(DB_URL)
    df.to_sql(
        "temperature_readings",
        engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
    )
    print("Dados inseridos com sucesso em temperature_readings!")


if __name__ == "__main__":
    main()
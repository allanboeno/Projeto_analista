import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Criar a conexão
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Lê os dados brutos da camada RAW (tabela netflix_titles)
df = pd.read_sql('SELECT * FROM raw.netflix_titles', con=engine)

# Padroniza os nomes das colunas (minúsculo, sem espaços, substitui por "_")
df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_"))

# Converte a coluna 'date_added' para o formato de data (datetime)
# Corrige strings mal formatadas e ignora erros (errors="coerce")
df["date_added"] = pd.to_datetime(df['date_added'].str.strip(), format='%B %d, %Y', errors="coerce")

# Quebra a coluna 'duration' em duas: valor numérico e unidade (ex: "90 min" → 90 | min)
df[['duration_value', 'duration_unit']] = df['duration'].str.split(' ', expand=True)
df.drop(columns=['duration'], inplace=True)

# Remove espaços extras das colunas do tipo string
# Substitui strings vazias por valores nulos (pd.NA)
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
df = df.replace(r'^\s*$', pd.NA, regex=True)

# Normaliza algumas colunas categóricas para letras minúsculas
cat_columns = ['type', 'rating', 'listed_in']
for col in cat_columns:
    df[col] = df[col].str.lower()

# Define quais são os ratings válidos
valid_ratings = [
    "g", "pg", "pg-13", "r", "nc-17",
    "tv-y", "tv-y7", "tv-g", "tv-pg", "tv-14", "tv-ma", "tv-y7-fv"
]

# Se o rating não está na lista de válidos, substitui por "not_rated"
df.loc[~df['rating'].isin(valid_ratings) & df['rating'].notna(), 'rating'] = "not_rated"

# Salva os dados limpos na camada TRUSTED
df.to_sql("netflix_titles_clean", engine, schema="trusted", if_exists="replace", index=False)

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

# Lê a tabela limpa da camada TRUSTED
df = pd.read_sql('SELECT * FROM trusted.netflix_titles_clean', con=engine)

# Tabela fato
fact_titles = df.drop(columns=['country', 'listed_in', 'cast', 'director'])
fact_titles.to_sql('fact_titles', engine, schema='refined', if_exists='replace', index=False)

# Dimensão País
dim_country = df[['show_id', 'country']].copy()
dim_country = dim_country.assign(country=df['country'].str.split(', '))
dim_country = dim_country.explode('country')
dim_country['country'] = dim_country['country'].str.strip().fillna('unknown')
dim_country.to_sql('dim_country', engine, schema='refined', if_exists='replace', index=False)

# Dimensão Gênero
dim_genre = df[['show_id', 'listed_in']].copy()
dim_genre = dim_genre.assign(listed_in=df['listed_in'].str.split(', '))
dim_genre = dim_genre.explode('listed_in')
dim_genre['listed_in'] = dim_genre['listed_in'].str.strip()
dim_genre.to_sql('dim_genre', engine, schema='refined', if_exists='replace', index=False)

# Dimensão Ator
dim_actor = df[['show_id', 'cast']].copy()
dim_actor = dim_actor.assign(cast=df['cast'].str.split(', '))
dim_actor = dim_actor.explode('cast')
dim_actor['cast'] = dim_actor['cast'].str.strip().fillna('unknown')
dim_actor.to_sql('dim_actor', engine, schema='refined', if_exists='replace', index=False)

# Dimensão Diretor
dim_director = df[['show_id', 'director']].copy()
dim_director = dim_director.assign(director=df['director'].str.split(', '))
dim_director = dim_director.explode('director')
dim_director['director'] = dim_director['director'].str.strip().fillna('unknown')
dim_director.to_sql('dim_director', engine, schema='refined', if_exists='replace', index=False)

# Dimensão Data
dim_date = df[['show_id', 'date_added']].copy()
dim_date['year'] = dim_date['date_added'].dt.year
dim_date['month'] = dim_date['date_added'].dt.month
dim_date['day'] = dim_date['date_added'].dt.day
dim_date.to_sql('dim_date', engine, schema='refined', if_exists='replace', index=False)

-- Adiciona a chave primária na tabela fato
ALTER TABLE refined.fact_titles
ADD CONSTRAINT pk_fact_titles
PRIMARY KEY (show_id);

-- Cria chave estrangeira da dimensão País para a tabela fato
ALTER TABLE refined.dim_country
ADD CONSTRAINT fk_dim_country_fact
FOREIGN KEY (show_id)
REFERENCES refined.fact_titles(show_id);

-- Cria chave estrangeira da dimensão Gênero para a tabela fato
ALTER TABLE refined.dim_genre
ADD CONSTRAINT fk_dim_genre_fact
FOREIGN KEY (show_id)
REFERENCES refined.fact_titles(show_id);

-- Cria chave estrangeira da dimensão Ator para a tabela fato
ALTER TABLE refined.dim_actor
ADD CONSTRAINT fk_dim_actor_fact
FOREIGN KEY (show_id)
REFERENCES refined.fact_titles(show_id);

-- Cria chave estrangeira da dimensão Diretor para a tabela fato
ALTER TABLE refined.dim_director
ADD CONSTRAINT fk_dim_director_fact
FOREIGN KEY (show_id)
REFERENCES refined.fact_titles(show_id);

-- Cria chave estrangeira da dimensão Data para a tabela fato
ALTER TABLE refined.dim_date
ADD CONSTRAINT fk_dim_date_fact
FOREIGN KEY (show_id)
REFERENCES refined.fact_titles(show_id);

-- Cria índices para melhorar a performance de consultas envolvendo show_id
CREATE INDEX idx_dim_actor_show_id ON refined.dim_actor(show_id);
CREATE INDEX idx_dim_director_show_id ON refined.dim_director(show_id);
CREATE INDEX idx_dim_country_show_id ON refined.dim_country(show_id);
CREATE INDEX idx_dim_genre_show_id ON refined.dim_genre(show_id);
CREATE INDEX idx_dim_date_show_id ON refined.dim_date(show_id);

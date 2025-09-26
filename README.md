# Descrição

Este projeto consiste em um pipeline ETL completo construído no PostgreSQL, utilizando a base pública da Netflix como fonte de dados.
Os dados foram organizados em três camadas (Raw, Trusted e Refined), passando por etapas de limpeza, padronização e modelagem.
Por fim, foi aplicado um Star Schema para possibilitar análises rápidas e eficientes em ferramentas de BI.

## 📂 Camadas do Data Lake  

### 🗃️ RAW  
- Armazena os dados **originais**, exatamente como foram extraídos da fonte (Netflix).  
- Mantém um **histórico bruto**, sem alterações.  

### 🔎 TRUSTED  
Na camada **Trusted**, os dados passam por um processo de **limpeza e padronização** para garantir consistência:  

- **Padronização de colunas** → nomes em minúsculo e com `_` no lugar de espaços.  
- **Datas organizadas** → `date_added` convertido para tipo `datetime`, corrigindo formatos inconsistentes.  
- **Tratamento de duração** → separação da coluna `duration` em `duration_value` e `duration_unit`.  
- **Strings normalizadas** → remoção de espaços extras, valores vazios transformados em `NULL`.  
- **Colunas categóricas ajustadas** → `type`, `rating` e `listed_in` padronizados para minúsculo.  
- **Ratings validados** → apenas valores dentro da lista oficial permanecem, os demais viram `not_rated`.  

➡️ O objetivo dessa camada é fornecer uma base **limpa, organizada e confiável**, pronta para análises mais avançadas na **Refined**. 



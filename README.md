# E-commerce Data Pipeline & Dashboard

Este projeto implementa um simples pipeline de dados para análises, incluindo processamento em camadas (bronze, silver, gold) e dashboard interativo.

## 📊 Dataset

O projeto utiliza o **Brazilian E-Commerce Public Dataset by Olist** disponível no Kaggle:

**Link:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?select=olist_geolocation_dataset.csv

### Arquivos necessários:
- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv` 
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

## 🚀 Setup

### 1. Preparar os dados
```bash
# Criar a pasta data na raiz do projeto
mkdir data

# Baixar e extrair os arquivos CSV do dataset do Kaggle
# Colocar todos os arquivos CSV na pasta data/
```

### 2. Estrutura do projeto
```
ecommerce-project/
├── data/                    # Arquivos CSV do dataset
├── spark_jobs/             # Jobs de processamento Spark
│   ├── bronze/             # Ingestão para camada bronze
│   ├── silver/             # Limpeza e transformação
│   └── gold/               # Agregações e métricas
├── api/                    # API FastAPI para simular stream de dados
├── dags/                   # DAGs do Airflow
├── dashboard.py            # Dashboard Streamlit
```

### 3. Executar o dashboard
```bash
streamlit run dashboard.py
```

## 🏗️ Arquitetura

- **Bronze Layer**: Dados brutos em formato Parquet
- **Silver Layer**: Dados limpos e transformados
- **Gold Layer**: Tabelas dimensionais e fatos para análise
- **Dashboard**: Interface interativa com métricas e visualizações

## 📈 Features

- Pipeline de dados
- Dashboard interativo com KPIs
- Análise temporal de vendas
- Análise geográfica por estados
- API para ingestão de dados via stream

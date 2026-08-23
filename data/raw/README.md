# data/raw

Esta pasta guarda os arquivos originais da Olist, exatamente como vêm do Kaggle, sem nenhuma alteração.

Ela está vazia no repositório de propósito. Os 9 arquivos somam mais de 120 MB e são dados de terceiros, então
não foram versionados.

## O que colocar aqui

Baixe o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
e coloque os 9 CSVs nesta pasta:

```
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

O notebook `01_limpeza.ipynb` lê daqui. Sem esses arquivos, nenhum notebook roda.

Nada nesta pasta é modificado pelo projeto. Todo tratamento acontece em memória e o resultado vai para
`data/processed/`.

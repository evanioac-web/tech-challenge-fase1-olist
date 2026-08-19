# Olist E-commerce | Crescimento, Receita e Concentração

Análise da base pública de e-commerce da Olist, voltada a quem precisa decidir se investe na empresa.

Tech Challenge Fase 1, POSTECH Data Analytics.

**Autor:** Evanio Alves Carvalho

---

## A pergunta central

A Olist está crescendo, e esse crescimento é sustentável?

A resposta curta é que ela cresceu muito até o fim de 2017 e parou em 2018. O restante deste projeto é sobre
o porquê disso e o que isso significa para uma decisão de investimento.

| Indicador | Resultado |
|---|---|
| Receita (jan/2017 a ago/2018) | R$ 15,68 milhões (R$ 13,45mi produto + R$ 2,23mi frete) |
| Pedidos | 97.905 |
| Crescimento no período | cerca de 628% |
| Valor do pedido (média / mediana) | R$ 160,19 / R$ 105,28 |
| Concentração: São Paulo | 37,4% da receita |
| Concentração: top 5 estados | 73,1% (sobram 26,9% para os outros 22) |
| Concentração: top 5 categorias | 39,3% de 72 categorias |
| Concentração: top 10 vendedores | 12,9% de 3.029 |
| Projeção do trimestre seguinte | cerca de R$ 1 milhão por mês |

## Os três achados que importam

**O número de 628% descreve 2017, não 2018.** A receita sobe forte no primeiro ano e depois estaciona. A média
mensal do segundo quadrimestre de 2018 é 4,3% menor que a do primeiro. A projeção confirma: a melhor
estimativa para os meses seguintes é repetir os últimos.

**O que travou foi a demanda, não a oferta.** Em 2018 os vendedores ativos cresceram 31%, de 968 para 1.266, e
a receita não subiu. Os clientes caíram 10% e a receita por vendedor encolheu 31%, de R$ 1.138 para R$ 788. A
plataforma continuou atraindo quem vende sem atrair quem compra.

**A entrega explica parte da concentração geográfica.** Os cinco estados que fazem 73% da receita recebem em 8
a 15 dias. Os que quase não vendem esperam de 21 a 29 dias e ainda pagam quase o dobro de frete em proporção
ao produto. A correlação entre tempo de entrega e participação na receita é -0,60.

---

## Estrutura do repositório

```
data/
  raw/        CSVs originais da Olist, não versionados (ver "Como reproduzir")
  kpis/       indicadores calculados, exportados em CSV
notebooks/
  01_limpeza_e_preparacao.ipynb    base comum, sem filtros de análise
  02_crescimento_e_receita.ipynb   evolução, platô e projeção
  03_concentracao_e_entrega.ipynb  por que a receita está presa a São Paulo
reports/      achados em markdown, relatório executivo e apresentação
figures/      gráficos gerados pelos notebooks
```

Os notebooks rodam na ordem numerada. O `01` grava em `data/processed/`, que não é versionado por tamanho, e
os outros dois leem de lá. Rodar o `02` ou o `03` sem ter rodado o `01` não funciona.

### Por que a limpeza fica separada

O `01` não aplica nenhum filtro de análise: não corta período e não remove status de pedido. Isso é
proposital. Quem analisa receita não quer pedido cancelado, mas quem analisa cancelamento quer justamente
ele. Filtrar na base comum inviabilizaria outras análises.

Cada notebook de análise aplica o próprio recorte e justifica ali mesmo.

---

## Decisões de tratamento de dados

Todas estão justificadas com evidência dentro dos notebooks, não apenas afirmadas.

**Receita = preço do produto + frete**, no grão de item. É o valor transacionado, não o que a Olist ganha.

**Atraso é comparado apenas pela data, ignorando a hora.** A data prometida vem sem hora na base, sempre
meia-noite, e a data real vem com hora cheia. Comparar as duas direto marca como atrasado um pedido entregue
no dia certo às 15h. São 1.292 pedidos, e isso muda o atraso da base de 6,8% para 8,1%.

**Exclusão dos status `canceled` e `unavailable`** nas análises de receita. A checagem mostrou que 0% dos
`unavailable` e apenas 77,2% dos `canceled` têm produto associado, ou seja, a venda não se concretizou. Os
demais status têm 100% e foram mantidos.

**Janela de janeiro de 2017 a agosto de 2018.** A base vai de setembro de 2016 a outubro de 2018, mas as
pontas são resíduo de operação. O efeito de escolher outro mês como base de cálculo:

| Mês tomado como base | Pedidos no mês | Crescimento até ago/2018 |
|---|---|---|
| set/2016 | 4 | 356.357% |
| dez/2016 | 1 | 5.081.314% |
| out/2016 | 324 | 1.841% |
| **jan/2017** | **800** | **628%** |

Nenhum dado foi removido da base: a série completa é calculada e plotada, para que a decisão possa ser
conferida em vez de aceita.

**`payments` e `reviews` agregados por pedido antes dos merges.** As duas tabelas têm mais de uma linha por
pedido. Sem agregar antes, cada item viraria várias linhas e a receita contaria em dobro.

**Outliers de preço mantidos.** O IQR aponta 7,5% dos itens acima de R$ 277, chegando a R$ 6.735. São valores
plausíveis para móvel e eletrônico, e não há preço negativo nem zerado. Remover cortaria justamente as vendas
maiores. A assimetria é tratada reportando mediana junto com a média.

**Recompra medida por `customer_unique_id`**, não por `customer_id`, que é gerado a cada pedido. Medir pelo
`customer_id` daria recompra zero.

**Tabela `geolocation` fora do escopo.** Tem muita linha repetida por listar coordenadas por prefixo de CEP, e
as análises usam a UF do cliente, que já vem em `customers`.

---

## Modelagem

Modelo estrela com a tabela fato no grão de item de pedido:

```
fato_itens  (grão: item do pedido)
  ├── dim_clientes
  ├── dim_produtos
  ├── dim_vendedores
  └── dim_data
```

A tabela fato é validada logo depois de construída: o número de linhas tem que continuar igual ao de
`order_items` (112.650), a soma de `price` tem que bater com a origem e nenhuma chave pode ficar órfã. As três
checagens passam. Se alguma falhar, há duplicação em algum merge.

---

## Como reproduzir

1. Baixe o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
   no Kaggle
2. Coloque os 9 arquivos CSV em `data/raw/`
3. Crie o ambiente e instale as dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Rode os notebooks de `notebooks/` na ordem numerada

Todos os números do relatório executivo saem destes notebooks. Cada percentual citado tem uma célula
correspondente que o calcula.

---

## Limitações

A base não informa a comissão que a Olist retém sobre cada venda, nem o custo de aquisição de clientes. Por
isso o que este projeto chama de receita é o valor transacionado, e não é possível calcular margem, lucro ou
retorno de investimento em marketing. As conclusões se limitam a receita, volume e concentração.

A relação entre tempo de entrega e receita por estado é correlação, não prova de causa. São Paulo também
concentra população e renda, e isso explica parte da diferença.

O efeito do atraso sobre a recompra é estatisticamente significativo (p = 0,007) mas pequeno em termos
absolutos: 0,92 ponto percentual. Mesmo com entrega no prazo, cerca de 96% dos clientes não voltam.

---

## Tecnologias

Python, pandas, matplotlib, seaborn, scipy, Jupyter.

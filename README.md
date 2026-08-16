# Olist E-commerce | Análise de Crescimento e Receita

Análise exploratória e de indicadores comerciais sobre a base pública de e-commerce da Olist, com foco em
evolução de receita, ticket médio e concentração de vendas por categoria, região e vendedor.

Projeto individual do Tech Challenge da Fase 1, POSTECH Data Analytics.

**Autor:** Evanio Alves Carvalho

---

## O que este projeto responde

A pergunta central é simples: **a Olist está crescendo, e esse crescimento é sustentável?**

Os principais achados:

| Indicador | Resultado |
|---|---|
| Receita no período | R$ 15,68 milhões (R$ 13,45 mi em produtos + R$ 2,23 mi em frete) |
| Pedidos | 97.905 |
| Crescimento jan/2017 a ago/2018 | ~628% |
| Ticket médio (média / mediana) | R$ 160,19 / R$ 105,28 |
| Concentração: top 5 categorias | 39,3% da receita (de 72 categorias) |
| Concentração: top 5 estados | 73,1% da receita (SP sozinho: 37,4%) |
| Concentração: top 10 vendedores | 12,9% da receita (de 3.029 ativos) |

**A conclusão não é o número de crescimento.** É o que vem depois dele: a receita cresce forte até o começo de
2018 e então estaciona. A média mensal do segundo quadrimestre de 2018 é 4,3% menor que a do primeiro. O maior
mês de toda a série é novembro de 2017, puxado pela Black Friday, e não um mês de 2018.

Junte a isso a concentração geográfica, com quase 40% da receita vindo de um único estado, e o quadro é de um
negócio que ganhou escala rápido e precisa encontrar novas fontes de crescimento.

---

## Estrutura do repositório

```
notebooks/    análise completa em Python (CRISP-DM), do carregamento à conclusão
relatorios/   relatório executivo (.docx) e apresentação (.pptx)
dados/kpis/   indicadores calculados, exportados em CSV
imagens/      gráficos gerados pelo notebook
```

Os 9 CSVs originais da Olist **não estão versionados** neste repositório, por serem dados de terceiros e
somarem mais de 120 MB. A seção "Como reproduzir" explica onde baixá-los.

---

## Decisões de tratamento de dados

Estas são as escolhas que mais afetam os números finais. Todas estão justificadas com evidência dentro do
notebook, não apenas afirmadas.

**Receita = preço do produto + frete.** As duas parcelas somadas representam o valor transacionado em cada
item.

**Exclusão dos status `canceled` e `unavailable`.** Não foi uma escolha por intuição. A checagem mostrou que
0% dos pedidos `unavailable` e apenas 77,2% dos `canceled` têm produto associado, ou seja, a venda não se
concretizou. Já `shipped`, `processing` e `invoiced` têm pagamento e produto associados em 100% dos casos, e
por isso foram mantidos.

**Janela de janeiro de 2017 a agosto de 2018.** A base vai de setembro de 2016 a outubro de 2018, mas as
pontas são resíduo: setembro de 2016 tem 4 pedidos, dezembro de 2016 tem 1, novembro de 2016 nem existe na
base, e outubro de 2018 tem 4.

O efeito de escolher um desses meses como base de cálculo:

| Mês tomado como base | Volume do mês | Crescimento até ago/2018 |
|---|---|---|
| set/2016 | 2 pedidos | 356.357% |
| dez/2016 | 1 pedido | 5.081.314% |
| out/2016 | 290 pedidos | 1.841% |
| **jan/2017** | **787 pedidos** | **628%** |

Os três primeiros não descrevem o desempenho da empresa, descrevem o fato de que a plataforma estava
começando. E a ausência de novembro de 2016 abre um vão que impede o cálculo contínuo de variação mês a mês.

Nenhum dado foi removido: a série completa é calculada, aparece no notebook e é plotada com o período
analisado destacado, justamente para que essa decisão possa ser verificada por quem lê em vez de ter que ser
aceita como afirmação.

**Nulos mantidos, com justificativa por coluna.** Três tabelas têm nulos, mas nenhum deles cai em coluna usada
no cálculo: em `orders` são datas de entrega, em `reviews` são campos de comentário opcionais, e em `products`
são dimensões físicas. A única exceção tratada é `product_category_name`, preenchida como `unknown`.

**Tabela `geolocation` removida do escopo.** Ela tem 261.831 linhas duplicadas, o que é esperado por listar
coordenadas por prefixo de CEP. Como a análise usa a UF do cliente, que já vem em `customers`, a tabela não
entra em nenhum cálculo e foi retirada em vez de tratada.

**Outliers de preço mantidos.** O método do IQR aponta 7,5% dos itens acima de R$ 277, chegando a R$ 6.735.
São valores altos mas plausíveis para eletrônicos e móveis, e não há sinal de erro de digitação: zero preços
negativos, zerados ou absurdos. Remover 7,5% da base cortaria justamente as vendas de maior valor e
subestimaria a receita. A assimetria que eles causam é tratada reportando **mediana junto com a média**.

---

## Modelagem

Os dados foram organizados em um **star schema**, com a tabela fato no grão de item de pedido:

```
fact_order_items  (grão: item do pedido)
  ├── dim_customers
  ├── dim_products
  ├── dim_sellers
  └── dim_date
```

`payments` e `reviews` têm mais de uma linha por pedido, então foram agregadas por `order_id` **antes** dos
merges (soma para pagamento, média para avaliação). Sem esse cuidado, cada item viraria várias linhas e a
receita ficaria inflada.

A tabela fato é validada logo depois de construída: o número de linhas tem que continuar igual ao de
`order_items` (112.650), a soma de `price` tem que bater com a origem, e nenhuma chave pode ficar sem
correspondência. As três checagens passam.

---

## Como reproduzir

1. Baixe o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
   no Kaggle
2. Coloque os 9 arquivos CSV em uma pasta `data/` na raiz do projeto
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o notebook `notebooks/analise_crescimento_receita.ipynb`

O notebook também roda no Google Colab: ele detecta o ambiente e monta o Google Drive automaticamente,
esperando os CSVs em uma pasta `Tech_Challenge_Fase-1`.

Todos os números do relatório executivo saem deste notebook. Cada percentual citado tem uma célula
correspondente que o calcula.

---

## Limitações

A base pública da Olist **não informa a comissão** que a plataforma retém sobre cada venda, nem o custo de
aquisição de clientes. Por isso o que este projeto chama de receita é o valor transacionado, e não é possível
calcular margem, lucro ou retorno de investimento em marketing a partir destes dados. As conclusões se limitam
ao comportamento transacional: receita, volume e concentração.

---

## Tecnologias

Python, pandas, matplotlib, seaborn, Jupyter.

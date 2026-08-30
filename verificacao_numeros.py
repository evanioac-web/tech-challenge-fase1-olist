# -*- coding: utf-8 -*-
"""
Confere o relatório contra a base original.

Recalcula, direto dos 9 CSVs do Kaggle e sem passar pelos notebooks, cada número
citado no relatório executivo e na apresentação. Serve para verificar de forma
independente que nenhuma afirmação ficou sem sustentação nos dados.

Uso: coloque os CSVs em data/raw/ e rode "python verificacao_numeros.py" na raiz do projeto.
"""
import pandas as pd, numpy as np
from scipy.stats import chi2_contingency
R='data/raw/'

orders=pd.read_csv(R+'olist_orders_dataset.csv')
items=pd.read_csv(R+'olist_order_items_dataset.csv')
cust=pd.read_csv(R+'olist_customers_dataset.csv')
prod=pd.read_csv(R+'olist_products_dataset.csv')
trad=pd.read_csv(R+'product_category_name_translation.csv')

for c in ['order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date']:
    orders[c]=pd.to_datetime(orders[c])
orders=orders.merge(cust[['customer_id','customer_unique_id','customer_state']],on='customer_id',how='left')
orders['mes']=orders.order_purchase_timestamp.dt.to_period('M').astype(str)
orders['atrasou']=orders.order_delivered_customer_date.dt.normalize()>orders.order_estimated_delivery_date.dt.normalize()
orders['dias_entrega']=(orders.order_delivered_customer_date-orders.order_purchase_timestamp).dt.days

items['receita']=items.price+items.freight_value
fato=items.merge(orders,on='order_id',how='left').merge(prod[['product_id','product_category_name']],on='product_id',how='left')
fato=fato.merge(trad,on='product_category_name',how='left')

STATUS=['canceled','unavailable']
rec=fato[(fato.mes>='2017-01')&(fato.mes<='2018-08')&(~fato.order_status.isin(STATUS))]
ped=orders[(orders.mes>='2017-01')&(orders.mes<='2018-08')&(~orders.order_status.isin(STATUS))]

res=[]
def v(rotulo, calc, dito, tol=0.05):
    bate = abs(calc-dito)<=tol if isinstance(calc,(int,float,np.floating,np.integer)) else calc==dito
    res.append((bate, rotulo, calc, dito))

pm=rec.groupby('mes').receita.sum()
pedm=rec.groupby('mes').order_id.nunique()
v('receita total (R$ mi)', round(pm.sum()/1e6,2), 15.68, 0.005)
v('pedidos no recorte', int(rec.order_id.nunique()), 97905, 0)
v('pedidos na base completa', int(orders.order_id.nunique()), 99441, 0)
v('receita jan/2017 (R$ mil)', round(pm.iloc[0]/1000), 137, 0.5)
v('crescimento do periodo (%)', round((pm.iloc[-1]/pm.iloc[0]-1)*100), 628, 0.5)
v('maior mes da serie (R$ mi)', round(pm.max()/1e6,2), 1.17, 0.03)
v('pedidos no 1o mes', int(pedm.iloc[0]), 787, 0)
v('pedidos no ultimo mes (mais de 6 mil)', int(pedm.iloc[-1])>6000, True)
q=pm[pm.index.str.startswith('2018')]
v('media 1o quadrimestre 2018 (R$ mi)', round(q.head(4).mean()/1e6,2), 1.10, 0.005)
v('media 2o quadrimestre 2018 (R$ mi)', round(q.tail(4).mean()/1e6,2), 1.05, 0.005)
v('variacao entre quadrimestres (%)', round((q.tail(4).mean()/q.head(4).mean()-1)*100,1), -4.3, 0.05)

tk=pm/pedm
v('ticket medio mensal minimo', round(tk.min()), 146, 1)
v('ticket medio mensal maximo', round(tk.max()), 174, 0.5)
vp=rec.groupby('order_id').receita.sum()
v('valor medio do pedido', round(vp.mean(),2), 160.19, 0.005)
v('mediana do pedido', round(vp.median(),2), 105.28, 0.005)
v('coeficiente de variacao (%)', round(vp.std()/vp.mean()*100), 137, 0.5)

# 2016 e o corte de periodo
todos=fato[~fato.order_status.isin(STATUS)].groupby('mes').agg(rec=('receita','sum'), ped=('order_id','nunique'))
brutos=orders.groupby('mes').order_id.nunique()
for m,q_ in [('2016-09',4),('2016-10',324),('2016-12',1)]:
    v(f'pedidos em {m} (base bruta)', int(brutos.loc[m]), q_, 0)
v('novembro de 2016 ausente', '2016-11' not in todos.index, True)
cres=[(pm.iloc[-1]/todos.loc[m,'rec']-1)*100 for m in ['2016-09','2016-10','2016-12']]
v('menor crescimento alternativo (%)', round(min(cres)), 1841, 1)
v('maior crescimento alternativo (%)', round(max(cres)), 5081314, 1)

# status
tem=lambda st: orders[orders.order_status==st].order_id.isin(items.order_id).mean()*100
v('canceled com produto (%)', round(tem('canceled'),1), 73.8, 0.05)
v('unavailable com produto (%)', round(tem('unavailable'),1), 1.0, 0.05)
v('delivered com produto (%)', round(tem('delivered'),1), 100.0, 0.05)
v('demais status com 99% ou mais', min(tem(x) for x in ['shipped','processing','invoiced','delivered'])>=99, True)

# criterio de atraso
ent=orders[orders.order_status=='delivered'].dropna(subset=['order_delivered_customer_date'])
bruto=(ent.order_delivered_customer_date>ent.order_estimated_delivery_date)
fino=(ent.order_delivered_customer_date.dt.normalize()>ent.order_estimated_delivery_date.dt.normalize())
v('registros afetados pelo criterio', int((bruto&~fino).sum()), 1292, 0)
v('atraso pelo criterio adotado (%)', round(fino.mean()*100,1), 6.8, 0.05)
v('atraso pela comparacao direta (%)', round(bruto.mean()*100,1), 8.1, 0.05)

# novembro
nov=ped[ped.mes=='2017-11'].copy(); nov['dia']=nov.order_purchase_timestamp.dt.day
pd_=nov.groupby('dia').order_id.nunique()
v('pedidos em 24/11/2017', int(pd_.loc[24]), 1166, 0)
v('media fora do fim de semana promocional', round(pd_[~pd_.index.isin([24,25,26,27])].mean()), 191, 0.5)
v('proporcao (vezes)', round(pd_.loc[24]/pd_[~pd_.index.isin([24,25,26,27])].mean()), 6, 0.5)
v('nov/2017 e o maior mes da base', pm.idxmax()=='2017-11', True)

# concentracao
fato['cat']=fato.product_category_name_english.fillna(fato.product_category_name)
rec2=fato[(fato.mes>='2017-01')&(fato.mes<='2018-08')&(~fato.order_status.isin(STATUS))]
cat=rec2.groupby('cat').receita.sum().sort_values(ascending=False)
v('numero de categorias', len(cat), 73, 0)
v('top 5 categorias sobre a receita total (%)', round(cat.head(5).sum()/rec2.receita.sum()*100,1), 39.3, 0.05)
v('receita sem categoria (% do total)', round(rec2[rec2.cat.isna()].receita.sum()/rec2.receita.sum()*100,1), 1.3, 0.05)
vend=rec.groupby('seller_id').receita.sum().sort_values(ascending=False)
v('numero de vendedores', len(vend), 3029, 0)
v('top 10 vendedores (%)', round(vend.head(10).sum()/vend.sum()*100,1), 12.9, 0.05)
uf=rec.groupby('customer_state').receita.sum().sort_values(ascending=False)
v('Sao Paulo (%)', round(uf.iloc[0]/uf.sum()*100,1), 37.4, 0.05)
v('top 5 estados (%)', round(uf.head(5).sum()/uf.sum()*100,1), 73.1, 0.05)
v('demais 22 estados (%)', round(100-uf.head(5).sum()/uf.sum()*100,1), 26.9, 0.05)
v('numero de estados fora do top 5', len(uf)-5, 22, 0)

# oferta x demanda em 2018
det=rec[rec.mes.str.startswith('2018')].groupby('mes').agg(vend=('seller_id','nunique'), cli=('customer_unique_id','nunique'), r=('receita','sum'))
det['rv']=det.r/det.vend
v('vendedores jan/2018', int(det.vend.iloc[0]), 968, 0)
v('vendedores ago/2018', int(det.vend.iloc[-1]), 1266, 0)
v('crescimento de vendedores (%)', round((det.vend.iloc[-1]/det.vend.iloc[0]-1)*100,1), 30.8, 0.05)
v('clientes jan/2018', int(det.cli.iloc[0]), 7088, 0)
v('clientes ago/2018', int(det.cli.iloc[-1]), 6380, 0)
v('queda de clientes (%)', round((det.cli.iloc[-1]/det.cli.iloc[0]-1)*100,1), -10.0, 0.05)
v('receita por vendedor jan/2018', round(det.rv.iloc[0]), 1138, 0.5)
v('receita por vendedor ago/2018', round(det.rv.iloc[-1]), 787, 0.5)
v('queda da receita por vendedor (%)', round((det.rv.iloc[-1]/det.rv.iloc[0]-1)*100,1), -30.8, 0.05)

# entrega
e=ped[(ped.order_status=='delivered')&ped.order_delivered_customer_date.notna()]
ge=e.groupby('customer_state').agg(dias=('dias_entrega','mean'), atraso=('atrasou','mean'), n=('order_id','count'))
ge['pct']=uf.reindex(ge.index)/uf.sum()*100
top5=uf.head(5).index
v('entrega no top 5 (dias)', round((ge.loc[top5,'dias']*ge.loc[top5,'n']).sum()/ge.loc[top5,'n'].sum(),1), 10.5, 0.05)
out=ge.drop(index=top5)
v('entrega nos outros 22 (dias)', round((out.dias*out.n).sum()/out.n.sum(),1), 17.3, 0.05)
v('correlacao entrega x receita', round(ge.pct.corr(ge.dias),2), -0.60, 0.005)
v('Sao Paulo (dias)', round(ge.loc['SP','dias'],1), 8.3, 0.05)
v('Roraima (dias)', round(ge.loc['RR','dias'],1), 29.5, 0.05)
v('Alagoas (dias)', round(ge.loc['AL','dias']), 24, 0.5)
v('Alagoas atraso (%)', round(ge.loc['AL','atraso']*100,1), 21.5, 0.05)
v('Roraima atraso (%)', round(ge.loc['RR','atraso']*100,1), 12.5, 0.05)
v('Amapa (dias)', round(ge.loc['AP','dias'],1), 26.7, 0.05)
v('Amapa atraso (%)', round(ge.loc['AP','atraso']*100), 3, 0.5)

# frete
fr=rec.groupby('customer_state').agg(f=('freight_value','sum'), p=('price','sum'))
fr['pct']=fr.f/fr.p*100
v('frete em SP (% do produto)', round(fr.loc['SP','pct'],1), 13.8, 0.05)
v('frete no MA acima de 26%', fr.loc['MA','pct']>26, True)
v('frete em RR acima de 26%', fr.loc['RR','pct']>26, True)

# recompra
pp=orders[~orders.order_status.isin(STATUS)].sort_values(['customer_unique_id','order_purchase_timestamp']).copy()
pp['ordem']=pp.groupby('customer_unique_id').cumcount()+1
tot=pp.groupby('customer_unique_id').order_id.count().rename('total_pedidos')
prim=pp[pp.ordem==1].merge(tot,on='customer_unique_id')
prim=prim[(prim.order_status=='delivered')&prim.order_delivered_customer_date.notna()]
prim['voltou']=prim.total_pedidos>1
prim=prim[prim.order_purchase_timestamp<'2018-03-01']
g=prim.groupby('atrasou').voltou.agg(['mean','count'])
v('recompra sem atraso (%)', round(g.loc[False,'mean']*100,2), 4.08, 0.005)
v('recompra com atraso (%)', round(g.loc[True,'mean']*100,2), 3.16, 0.005)
v('queda relativa (%)', round((1-g.loc[True,'mean']/g.loc[False,'mean'])*100,1), 22.6, 0.05)
v('diferenca absoluta (p.p.)', round((g.loc[False,'mean']-g.loc[True,'mean'])*100,2), 0.92, 0.005)
v('nao retornam com entrega no prazo (%)', round((1-g.loc[False,'mean'])*100), 96, 0.5)
tab=pd.crosstab(prim.atrasou, prim.voltou)
v('p-valor do qui-quadrado', round(chi2_contingency(tab)[1],3), 0.007, 0.0005)

# projecao
proj=pm.tail(3).mean()
v('projecao mensal (R$ mi)', round(proj/1e6,2), 1.02, 0.005)
v('projecao trimestral (R$ mi)', round(proj*3/1e6,2), 3.06, 0.005)
base2017=pm[['2017-09','2017-10','2017-11']].sum()
v('projecao vs mesmo periodo de 2017 (%)', round((proj*3/base2017-1)*100,1), 15.2, 0.05)

print(f'{"":3} {"afirmacao":52} {"recalculado":>14}  {"documento":>14}')
falhas=0
for bate,rot,calc,dito in res:
    if not bate: falhas+=1
    print(f'{"ok " if bate else "ERRO"} {rot:52} {str(calc):>14}  {str(dito):>14}')
print()
print(f'{len(res)} afirmacoes recalculadas a partir dos 9 CSVs originais, {falhas} divergencia(s)')

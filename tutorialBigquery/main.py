from google.cloud import bigquery
import credentials

bqclient = bigquery.Client.from_service_account_json(credentials.path_to_service_account_key_file)
query_job = bqclient.query(
    """
    SELECT ClavedeNodo, Fecha, Hora, PMLTotal, PMLCongestion, PMLEnergia, PMLPerdidas, TipodeMercado
    FROM `info-publica-mem`.Mercado.PML
    WHERE ClavedeNodo in ( 'ENSENADA','CARMEN') 
    and TipodeMercado in ('MDA','MTR') 
    and fecha BETWEEN '2018-01-01' AND '2021-01-01' 
    Limit 100
    """
)
results = query_job.result()  

for row in results:
    print(f" {row.ClavedeNodo} {row.Fecha} {row.Hora} {row.PMLTotal} {row.PMLCongestion} {row.PMLEnergia} {row.PMLPerdidas} {row.TipodeMercado}")
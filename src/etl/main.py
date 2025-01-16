import pandas as pd

csv_urls = {
    "2019": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial?fq=anomes_s:2019*&fq=tipo_s:mes_mu&wt=csv&q=*&fl=ibge:codigo_ibge,anomes:anomes_s,qtd_familias_beneficiarias_bolsa_familia,valor_repassado_bolsa_familia&rows=10000000&sort=anomes_s%20asc,%20codigo_ibge%20asc",
    "2020": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial?fq=anomes_s:2020*&fq=tipo_s:mes_mu&wt=csv&q=*&fl=ibge:codigo_ibge,anomes:anomes_s,qtd_familias_beneficiarias_bolsa_familia,valor_repassado_bolsa_familia&rows=10000000&sort=anomes_s%20asc,%20codigo_ibge%20asc",
    "2021": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial?fq=anomes_s:2021*&fq=tipo_s:mes_mu&wt=csv&q=*&fl=ibge:codigo_ibge,anomes:anomes_s,qtd_familias_beneficiarias_bolsa_familia,valor_repassado_bolsa_familia&rows=10000000&sort=anomes_s%20asc,%20codigo_ibge%20asc",
    "2023": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial/?fq=anomes_s:2023*&fl=codigo_ibge%2Canomes_s%2Cqtd_familias_beneficiarias_bolsa_familia_s%2Cvalor_repassado_bolsa_familia_s%2Cpbf_vlr_medio_benef_f&fq=valor_repassado_bolsa_familia_s%3A*&q=*%3A*&rows=100000&sort=anomes_s%20desc%2C%20codigo_ibge%20asc&wt=csv",
    "2024": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial/?fq=anomes_s:2024*&fl=codigo_ibge%2Canomes_s%2Cqtd_familias_beneficiarias_bolsa_familia_s%2Cvalor_repassado_bolsa_familia_s%2Cpbf_vlr_medio_benef_f&fq=valor_repassado_bolsa_familia_s%3A*&q=*%3A*&rows=100000&sort=anomes_s%20desc%2C%20codigo_ibge%20asc&wt=csv"
}
xlsx_url = "../../data/raw_data/taxa_desocupacao_br.xlsx"
load_local = "../../data/processed_data/"

class extract:
    def extract_xlsx(local):

        # Extração do arquivo
        df = pd.read_excel(local, sheet_name='Tabela', skiprows=3)
        df.drop(0, axis=0, inplace=True)
        transform.transform_xlsx(df)

    def extract_csv():
        pass

class transform:
    def transform_xlsx(df):
        pass
    def transform_csv():
        pass

def load():
    pass

def main():
    extract.extract_xlsx(xlsx_url)

if __name__ == '__main__':
    main()
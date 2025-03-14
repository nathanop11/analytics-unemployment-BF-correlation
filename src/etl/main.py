import pandas as pd

class DataExtractor:
    @staticmethod
    def extract_xlsx(local):
        """Extração de dados do arquivo Excel"""
        df = pd.read_excel(local, sheet_name='Tabela', skiprows=3)
        df.drop(0, axis=0, inplace=True)
        return df

    @staticmethod
    def extract_html(local):
        """Extração de dados do arquivo HTML"""
        df = pd.read_html(local)
        return df[0]

    @staticmethod
    def extract_csv(local):
        """Extração de dados de arquivos CSV por ano"""
        dfs = []
        for ano, url in local.items():
            if ano in ('2019', '2020', '2021'):
                print(f"Baixando dados de {ano}...")
                df = pd.read_csv(url, delimiter=",")  
                df["ano"] = ano  
                dfs.append(df)
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.fillna(0, inplace=True)

        dfs_1 = []
        for ano, url in local.items():
            if ano in ('2023', '2024'):
                print(f"Baixando dados de {ano}...")
                df_1 = pd.read_csv(url, delimiter=",")  
                df_1["ano"] = ano  
                dfs_1.append(df_1)
        df_final_1 = pd.concat(dfs_1, ignore_index=True)
        df_final_1.fillna(0, inplace=True)
        df_final_1.to_csv('test1.csv')

        return df_final, df_final_1


class DataTransformer:
    @staticmethod
    def transform_date(df):
        """Transformação de dados de data (não implementada)"""
        pass

    @staticmethod
    def transform_csv(df1, df2):
        """Transformação dos dados do CSV"""
        df2.rename(columns={
            "codigo_ibge": "ibge", 
            "anomes_s": "anomes", 
            "qtd_familias_beneficiarias_bolsa_familia_s": "qtd_familias_beneficiarias_bolsa_familia", 
            "valor_repassado_bolsa_familia_s": "valor_repassado_bolsa_familia"
        }, inplace=True)
        df2.drop(columns={"pbf_vlr_medio_benef_f"}, inplace=True)
        df_final = pd.concat([df1, df2], ignore_index=True)
        return df_final

    @staticmethod
    def transform_html(df):
        """Transformação dos dados extraídos de HTML"""
        df['Códigos'] = df['Códigos'].str.replace('ver municípios', '', regex=False)
        return df

    @staticmethod
    def group_by_quarter_csv(df):
        """Agrupamento por trimestre dos dados do CSV"""
        df['data'] = pd.to_datetime(df['anomes'].astype(str), format='%Y%m')
        df['trimestre'] = df['data'].dt.to_period('Q')
        df_trimestral = df.groupby(['trimestre', 'ibge']).agg({
            'qtd_familias_beneficiarias_bolsa_familia': 'mean', 
            'valor_repassado_bolsa_familia': 'mean'
        }).reset_index()
        df_trimestral['trimestre_formatado'] = df_trimestral['trimestre'].dt.strftime('%qº trimestre %Y') 
        df_trimestral['Códigos'] = df_trimestral['ibge'].astype(str).str[:2]
        return df_trimestral

    @staticmethod
    def join_by_state(df_csv, df_html):
        """União dos dados do CSV e HTML por estado"""
        df_result = df_csv.merge(df_html, how='left', on='Códigos')
        return df_result

    @staticmethod
    def group_by_state(df):
        """Agrupamento por estado"""
        df = df.groupby(['trimestre_formatado', 'UFs']).agg({
            'qtd_familias_beneficiarias_bolsa_familia': 'mean', 
            'valor_repassado_bolsa_familia': 'mean'
        }).reset_index()
        df.rename(columns={"trimestre_formatado": "Trimestre"}, inplace=True)
        df['qtd_familias_beneficiarias_bolsa_familia'] = df['qtd_familias_beneficiarias_bolsa_familia'].astype(float).round(2)
        df['valor_repassado_bolsa_familia'] = df['valor_repassado_bolsa_familia'].astype(float).round(2)
        return df


def main():
    """Função principal para orquestrar o processo"""
    
    # URLs para extração de dados
    csv_urls = {
        "2019": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial?fq=anomes_s:2019*&fq=tipo_s:mes_mu&wt=csv&q=*&fl=ibge:codigo_ibge,anomes:anomes_s,qtd_familias_beneficiarias_bolsa_familia,valor_repassado_bolsa_familia&rows=10000000&sort=anomes_s%20asc,%20codigo_ibge%20asc",
        "2020": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial?fq=anomes_s:2020*&fq=tipo_s:mes_mu&wt=csv&q=*&fl=ibge:codigo_ibge,anomes:anomes_s,qtd_familias_beneficiarias_bolsa_familia,valor_repassado_bolsa_familia&rows=10000000&sort=anomes_s%20asc,%20codigo_ibge%20asc",
        "2021": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial?fq=anomes_s:2021*&fq=tipo_s:mes_mu&wt=csv&q=*&fl=ibge:codigo_ibge,anomes:anomes_s,qtd_familias_beneficiarias_bolsa_familia,valor_repassado_bolsa_familia&rows=10000000&sort=anomes_s%20asc,%20codigo_ibge%20asc",
        "2023": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial/?fq=anomes_s:2023*&fl=codigo_ibge%2Canomes_s%2Cqtd_familias_beneficiarias_bolsa_familia_s%2Cvalor_repassado_bolsa_familia_s%2Cpbf_vlr_medio_benef_f&fq=valor_repassado_bolsa_familia_s%3A*&q=*%3A*&rows=100000&sort=anomes_s%20desc%2C%20codigo_ibge%20asc&wt=csv",
        "2024": "https://aplicacoes.mds.gov.br/sagi/servicos/misocial/?fq=anomes_s:2024*&fl=codigo_ibge%2Canomes_s%2Cqtd_familias_beneficiarias_bolsa_familia_s%2Cvalor_repassado_bolsa_familia_s%2Cpbf_vlr_medio_benef_f&fq=valor_repassado_bolsa_familia_s%3A*&q=*%3A*&rows=100000&sort=anomes_s%20desc%2C%20codigo_ibge%20asc&wt=csv"
    }
    xlsx_url = "data/raw_data/taxa_desocupacao_br.xlsx"
    cod_municipios_html = "https://www.ibge.gov.br/explica/codigos-dos-municipios.php"

    # Extração dos dados
    df_xlsx = DataExtractor.extract_xlsx(xlsx_url)
    df_juntado_csv, df_juntado_1_csv = DataExtractor.extract_csv(csv_urls)

    # Transformação dos dados
    df_all_csv = DataTransformer.transform_csv(df_juntado_csv, df_juntado_1_csv)
    df_group_by_quarter_csv = DataTransformer.group_by_quarter_csv(df_all_csv)

    try:
        df_html = DataExtractor.extract_html(cod_municipios_html)
        df_html_transform = DataTransformer.transform_html(df_html)
    except:
        print('Erro na extração do HTML')

    # Junção dos dados CSV com HTML
    df_bf = DataTransformer.join_by_state(df_group_by_quarter_csv, df_html_transform)

    # Agrupamento final por estado
    df_bf_final = DataTransformer.group_by_state(df_bf)

    print(df_bf_final)


if __name__ == '__main__':
    main()

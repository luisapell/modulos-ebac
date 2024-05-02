import streamlit as st
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import sys
import re

sns.set_theme()

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada', output_dir='./output/figs/'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    # Remover caracteres inválidos do nome do arquivo
    filename = re.sub(r'[\\/*?:"<>|]', '', f'{max_data}_{ylabel}.png')
    plt.savefig(os.path.join(output_dir, filename))
    st.pyplot(fig=plt)
    plt.show()

def gerar_graficos(df, meses, output_dir='./output/figs/'):
    for mes in meses:
        dados_mes = df[df['DTNASC'].str.contains(mes, case=False)] 
        if not dados_mes.empty:
            plt.figure(figsize=(10, 6))
            plt.title(f'Gráfico para o mês de {mes}')
            plt.plot(dados_mes['data'], dados_mes['valor'])
            plt.xlabel('Data')
            plt.ylabel('Valor')
            plt.grid(True)
            output_dir_mes = os.path.join(output_dir, mes)
            os.makedirs(output_dir_mes, exist_ok=True)
            filename = re.sub(r'[\\/*?:"<>|]', '', f'{max_data}_{mes}.png')
            plt.savefig(os.path.join(output_dir_mes, filename))
            st.pyplot(fig=plt)
            plt.show()
        else:
            print(f'Não há dados disponíveis para o mês de {mes}.')

st.set_page_config(page_title='SINASC Rondonia',
                   page_icon='https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_map_of_Rondonia.png',
                   layout='wide')
st.write('# Analise SINASC')
output_dir = './output/figs/'
meses = ['JAN','FEV','MAR', 'ABR', 'MAI', 'JUN', 'JUL','AGO','SET','OUT','NOV','DEZ']
opcao_grafico = st.sidebar.selectbox('Selecione o gráfico:', ['IDADEMAE x DTNASC', 'IDADEMAE x DTNASC x SEXO', 'PESO x DTNASC x SEXO', 'PESO x ESCMAE', 'APGAR1 x GESTACAO', 'APGAR5 x GESTACAO'])
for mes in meses:
    arquivo_csv = f'./input/SINASC_RO_2019_{mes}.csv'
    sinasc = pd.read_csv(arquivo_csv)
    max_data = sinasc['DTNASC'].max()[:7]
    print(max_data)

    # Criar diretório de saída específico para o mês atual, se ainda não existir
    output_dir_mes = os.path.join(output_dir, mes)
    os.makedirs(output_dir_mes, exist_ok=True)
    sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)
    max_data = sinasc.DTNASC.max()
    min_data = sinasc.DTNASC.min()
    st.write(max_data)
    st.write(min_data)
    datas = sinasc.DTNASC.unique()
    datas = pd.Series(datas).sort_values()
    st.write(datas)
    data_intervalo = st.sidebar.date_input('Intervalo de datas', value=(min_data, max_data),
                                 min_value=min_data, 
                                 max_value=max_data)
    st.write('Intervalo de datas selecionado:', data_intervalo)

    data_inicial = data_intervalo[0]
    data_final = data_intervalo[1]
    teste = sinasc.query('@data_inicial <= DTNASC <= @data_final')
    st.write(teste)

    if opcao_grafico == 'IDADEMAE x DTNASC':
        plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'quantidade_de_nascimento',
                      'data_de_nascimento', output_dir=output_dir_mes)
    elif opcao_grafico == 'IDADEMAE x DTNASC x SEXO':
        plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media_idade_mae', 'data_de_nascimento',
                      'unstack', output_dir=output_dir_mes)
    elif opcao_grafico == 'PESO x DTNASC x SEXO':
        plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media_peso_bebe', 'data_de_nascimento',
                      'unstack', output_dir=output_dir_mes)
    elif opcao_grafico == 'PESO x ESCMAE':
        plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'apgar1_medio',
                      'gestacao', 'sort', output_dir=output_dir_mes)
    elif opcao_grafico == 'APGAR1 x GESTACAO':
        plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1_medio',
                      'gestacao', 'sort', output_dir=output_dir_mes)
    elif opcao_grafico == 'APGAR5 x GESTACAO':
        plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'apgar5_medio',
                      'gestacao', 'sort', output_dir=output_dir_mes)

novos_meses = ['JAN','FEV','MAR', 'ABR', 'MAI', 'JUN', 'JUL','AGO','SET','OUT','NOV','DEZ']
gerar_graficos(sinasc, novos_meses, output_dir=output_dir)

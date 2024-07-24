import pandas as pd
import streamlit as st
from io import BytesIO
from data.queries import *

# Esconde a sidebar caso de problema no config
def function_hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

# resolve o bug de carregamento dos gráficos de echart
def function_fix_tab_echarts():
    streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 300px;} 
   </style>
    """
    return st.markdown(streamlit_style, unsafe_allow_html=True)

# função para procurar usuários:
def function_search_user(choose, search):
    try:
        if choose == 'Artista':
            if search.isdigit():
                if len(search) < 9:
                    return search_artist_id(f"WHERE TA.ID LIKE '%{search}%'")
                else:
                    return search_artist_id(f"WHERE TA.CELULAR LIKE '%{search}%'")
            else:
                if '@' in search:
                    return search_artist_id(f"WHERE AU.LOGIN LIKE '%{search}%'")
                else:
                    return search_artist_id(f"WHERE TA.NOME LIKE '%{search}%'")
        elif choose == 'Contratante':
            if search.isdigit():
                if len(search) < 9:
                    return search_companie_id(f"WHERE TC.ID LIKE '%{search}%'")
                else:
                    return search_companie_id(f"WHERE TC.PHONE LIKE '%{search}%'")
            else:
                if '@' in search:
                    return search_companie_id(f"WHERE TC.EMAIL LIKE '%{search}%'")
                else:
                    return search_companie_id(f"WHERE TC.NAME LIKE '%{search}%'")
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# conta o checkin e checkout para a tela de Desempenho Operacional
def transform_show_statement(df):
    # Filtrar apenas as linhas que têm "Checkout Realizado" ou "Checkin Realizado" na coluna "STATUS_PROPOSTA"
    df_filtered = df.copy()
    
    # Inicializar colunas para armazenar a contagem
    df_filtered['CHECKIN_REALIZADO'] = 0
    df_filtered['CHECKOUT_REALIZADO'] = 0

    # Atualizar as colunas com base no valor de 'STATUS_PROPOSTA'
    df_filtered.loc[df_filtered['STATUS_PROPOSTA'] == 'Checkin Realizado', 'CHECKIN_REALIZADO'] = 1
    df_filtered.loc[df_filtered['STATUS_PROPOSTA'] == 'Checkout Realizado', 'CHECKOUT_REALIZADO'] = 1

    # Agrupar por 'ARTISTA' e contar o número de ocorrências
    grouped = df_filtered.groupby('ARTISTA').agg({
        'STATUS_PROPOSTA': 'size',  # Conta o número de ocorrências (número de shows)
        'CHECKIN_REALIZADO': 'sum',
        'CHECKOUT_REALIZADO': 'sum'
    }).reset_index()

    grouped['CHECKIN_REALIZADO'] = (((grouped['CHECKIN_REALIZADO'] + grouped['CHECKOUT_REALIZADO'])*100)/grouped['STATUS_PROPOSTA']).map("{:.2f}%".format)
    grouped['CHECKOUT_REALIZADO'] = ((grouped['CHECKOUT_REALIZADO']*100)/grouped['STATUS_PROPOSTA']).map("{:.2f}%".format)
    
    # Renomear as colunas para refletir o que foi pedido
    grouped.rename(columns={
        'STATUS_PROPOSTA': 'NÚMERO DE SHOWS',
        'CHECKIN_REALIZADO': 'PORCENTAGEM DE CHECKIN(%)',
        'CHECKOUT_REALIZADO': 'PORCENTAGEM DE CHECKOUT(%)'
    }, inplace=True)

    return grouped.sort_values(by='NÚMERO DE SHOWS', ascending=False)

# Função para converter o arquivo para excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

# Função para aplicar filtro da data e estabelecimento
def function_apply_filter_date_establishment(dataframe, date=None, establishment=None):
    df = dataframe.copy()
    if date is not None:
        if len(date) > 1 and date[0] is not None and date[1] is not None:
            startDate = pd.Timestamp(date[0])
            endDate = pd.Timestamp(date[1] + pd.Timedelta(days=1)) 
            try:
                df['DATA DE INÍCIO'] = pd.to_datetime(df['DATA DE INÍCIO'], dayfirst=True)
                df = df.dropna(subset=['DATA DE INÍCIO'])
                df = df[(df['DATA DE INÍCIO'] >= startDate) & (df['DATA DE INÍCIO'] <= endDate)]
                df['DATA DE INÍCIO'] = df['DATA DE INÍCIO'].dt.strftime('%d/%m/%Y')
            except Exception as e:
                st.error(f'Erro: {e}')
                
    if establishment is not None:
        try:
            df = df[df['ESTABELECIMENTO'] == establishment]
        except:
            pass
    
    return df

# Função para aplicar filtro da data e estabelecimento
def function_apply_filter_date_artist(dataframe, date=None, artist=None):
    df = dataframe.copy()
    if date is not None:
        if len(date) > 1 and date[0] is not None and date[1] is not None:
            startDate = pd.Timestamp(date[0])
            endDate = pd.Timestamp(date[1] + pd.Timedelta(days=1)) 
            try:
                df['DATA DE INÍCIO'] = pd.to_datetime(df['DATA DE INÍCIO'], dayfirst=True)
                df = df.dropna(subset=['DATA DE INÍCIO'])
                df = df[(df['DATA DE INÍCIO'] >= startDate) & (df['DATA DE INÍCIO'] <= endDate)]
                df['DATA DE INÍCIO'] = df['DATA DE INÍCIO'].dt.strftime('%d/%m/%Y')
            except Exception as e:
                st.error(f'Erro: {e}')
                
    if artist is not None:
        try:
            df = df[df['ARTISTA'] == artist]
        except:
            pass
    
    return df

# Função para combinar dois dataframes
def concat_column_in_two_dataframes(df1, df2, column):
    if not df1.empty and not df2.empty:
        df_combined = pd.concat([df1[column], df2[column]], ignore_index=True)
        df_combined = pd.DataFrame(df_combined, columns=[column])
    else:
        # Caso algum dos DataFrames seja vazio
        if df1.empty and not df2.empty:
            df_combined = pd.DataFrame(df2[column], columns=[column])
        elif not df1.empty and df2.empty:
            df_combined = pd.DataFrame(df1[column], columns=[column])
        else:
            df_combined = pd.DataFrame(columns=[column])  # Ambos os DataFrames estão vazios
    
    return df_combined

# Modal para quando há mais de um resultado de busca
@st.experimental_dialog("Opa, mais de um resultado encontrado!")
def modalChooseResultComponent(choose, result):
    st.write('Escolha um:')
    for index, row in result.iterrows():
        if choose == 'Artista':
            if st.button(f"ID: {row['ID']} | Nome: {row['NOME']}", key=index):
                st.session_state['Search']['TIPO'] = choose
                st.session_state['Search']['ID'] = row['ID']
                st.session_state['Search']['FULL_NAME'] = str(row['FULL_NAME'])
                st.session_state['Search']['NOME'] = str(row['NOME'])
                st.session_state['Search']['LOGIN'] = str(row['LOGIN'])
                st.session_state['Search']['CELULAR'] = str(row['CELULAR'])
                st.rerun()
        elif choose == 'Contratante':
            if st.button(f"ID: {row['ID']} | Nome: {row['NAME']}", key=index):
                st.session_state['Search']['TIPO'] = choose
                st.session_state['Search']['ID'] = row['ID']
                st.session_state['Search']['NOME'] = str(row['NAME'])
                st.session_state['Search']['EMAIL'] = str(row['EMAIL'])
                st.session_state['Search']['PHONE'] = str(row['PHONE'])
                st.rerun()

# lógica salvar o id do usuário buscado na sessão ou trocar caso feita outra busca
def function_salve_search_in_session(choose, search_user):
    if not search_user.empty:
        if search_user.shape[0] > 1:
            modalChooseResultComponent(choose, search_user)
        else:
            if choose == 'Artista':
                st.session_state['Search']['TIPO'] = choose
                st.session_state['Search']['ID'] = search_user['ID'].loc[0]
                st.session_state['Search']['FULL_NAME'] = str(search_user['FULL_NAME'].loc[0])
                st.session_state['Search']['NOME'] = str(search_user['NOME'].loc[0])
                st.session_state['Search']['LOGIN'] = str(search_user['LOGIN'].loc[0])
                st.session_state['Search']['CELULAR'] = str(search_user['CELULAR'].loc[0])
            elif choose == 'Contratante':
                st.session_state['Search']['TIPO'] = choose
                st.session_state['Search']['ID'] = search_user['ID'].loc[0]
                st.session_state['Search']['NOME'] = str(search_user['NAME'].loc[0])
                st.session_state['Search']['EMAIL'] = str(search_user['EMAIL'].loc[0])
                st.session_state['Search']['PHONE'] = str(search_user['PHONE'].loc[0])
    elif st.session_state['Search']['ID'] is not None and search_user.empty:
            search_user = search_user_from_session(choose, st.session_state['Search']['ID'])
    
        
    return search_user  

# Filtro de estabelecimento dataframes
def apply_filter_artist_in_dataframe(df, artist):
    if artist is not None:
        try:
            df = df[df['ESTABELECIMENTO'] == artist]
        except:
            return df
    return df

# Chamas as funções de filtro
def apply_filter_in_dataframe(df, artist):
    df = apply_filter_artist_in_dataframe(df, artist)
    return df

# Gerando dados de reclamações por artista
def get_report_artist(df):
    df['QUANTIDADE'] = df.groupby('ARTISTA')['ARTISTA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['ARTISTA'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    df_grouped['RANKING'] = df_grouped['QUANTIDADE'].rank(method='first', ascending=False).astype(int)
    df_grouped = df_grouped.reset_index(drop=True)

    return df_grouped

# Agrupa dataframe por semana e cria um campo quantidade para colocar valores
def get_report_artist_by_week(df):
    df['QUANTIDADE'] = df.groupby('SEMANA')['SEMANA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['SEMANA'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    return df_grouped

# Agrupa por ocorrência
def get_report_by_occurrence(df):
    df['QUANTIDADE'] = df.groupby(['TIPO'])['ARTISTA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['TIPO'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    return df_grouped
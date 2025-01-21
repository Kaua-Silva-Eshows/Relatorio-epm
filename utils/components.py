import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date
from streamlit_echarts import st_echarts
from utils.functions import *
from decimal import Decimal
import calendar

# resolve o bug de carregamento dos gráficos de echart
def fix_tab_echarts():
    streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 300px;} 
   </style>
    """

    return st.markdown(streamlit_style, unsafe_allow_html=True)

# Esconde a sidebar caso de problema no config.toml
def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def plotDataframe(df, name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    column_with_link = next((col_name for col_name in df.columns if 'LINK' in col_name.upper()), None)
    if column_with_link:
        st.dataframe(df,column_config={column_with_link: st.column_config.LinkColumn(
            column_with_link, display_text="Link"
        ),}, hide_index=True,)
    else:
        st.dataframe(df, hide_index=True, use_container_width=True)

def plotPizzaChart(labels, sizes, name):
    chart_key = f"{labels}_{sizes}_{name}_"
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    

    # Preparar os dados para o gráfico
    data = [{"value": size, "name": label} for size, label in zip(sizes, labels)]
    
    options = {
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: {c} ({d}%)" 
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "top": "top", 
            "textStyle": {
                "color": "orange"
            }
        },
        "grid": {  # Adicionado para organizar o layout
            "left": "50%", 
            "right": "50%", 
            "containLabel": True
        },
        "series": [
            {
                "name": "Quantidade",
                "type": "pie",
                "radius": "75%",
                "center": ["75%", "45%"],  # Posiciona o gráfico no meio verticalmente
                "data": data,
                "label": {
                    "show": False  # Ocultar os textos nas fatias
                },
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }
    
    st_echarts(options=options, height="300px", key=chart_key)

def plotBarChart(df, xValue, yValue,name):
    chart_key = f"{xValue}_{yValue}_{name}"
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)

    if yValue == 'VALOR_GANHO_BRUTO':
        df = df.rename(columns={'VALOR_GANHO_BRUTO': 'VALOR INVESTIDO'})
        yValue = 'VALOR INVESTIDO'

    if yValue == 'VALOR_BRUTO':
        df = df.rename(columns={'VALOR_BRUTO': 'VALOR INVESTIDO'})
        yValue = 'VALOR INVESTIDO'
    
    if df[xValue].dtype == 'object':
        # Tentar converter os valores para o tipo datetime
        try:
            df_sorted = df.sort_values(by=xValue)
            df_sorted[xValue] = pd.to_datetime(df_sorted[xValue])
            df_sorted[xValue] = df_sorted[xValue].dt.strftime('%d/%m/%Y')
        except ValueError:
            df_sorted = df

    options = {
        "xAxis": {
            "type": "category",
            "data": df_sorted[xValue].tolist(),
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": yValue,
                "data": df_sorted[yValue].tolist(),
                "type": "bar",
                "itemStyle": {
                    "color": "#ff6600"
                },
                "barWidth": "50%"  # Ajuste a largura das colunas aqui
            }
        ],
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "legend": {
            "data": [yValue],
            "textStyle": {
                "color": "#808080"
            }
        }
    }
    
    st_echarts(options=options, height="300px", key=chart_key)

# Modal de busca
def modalSearchComponent():
    choose = st.radio('', ["Artista", "Contratante"], horizontal=True, label_visibility="collapsed")

    col = st.columns([5,1])
    with col[0]:
        search_term = st.text_input('',label_visibility="collapsed")

    with col[1]:
        if st.button("🔎", help=None):
            return choose, function_search_user(choose, search_term)
        else:
            return choose, pd.DataFrame()

# Mostra os dados do artista buscado na nav
def searchUserDataComponent(choose, user):
    with st.container(border=True):
        if choose == 'Artista':
            row1 = st.columns([1,2,2,2.5,2,0.5])
            with row1[0]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Id: {str(user['ID'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[1]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Nome: {str(user['FULL_NAME'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[2]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Projeto: {str(user['NOME'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[3]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>E-mail: {str(user['LOGIN'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[4]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Celular: {str(user['CELULAR'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[5]:
                if st.button('X'):
                    st.session_state['Search']['TIPO'] = None
                    st.session_state['Search']['ID'] = None
                    st.session_state['Search']['FULL_NAME'] = None
                    st.session_state['Search']['NOME'] = None
                    st.session_state['Search']['LOGIN'] = None
                    st.session_state['Search']['CELULAR'] = None
                    st.rerun()
        
        elif choose == 'Contratante':
            row1 = st.columns([1,2,2,2.5,2,0.5,0.5])
            with row1[0]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Id: {str(user['ID'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[1]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Estabelecimento: {str(user['NAME'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[2]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>E-mail: {str(user['EMAIL'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[3]:
                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Celular: {str(user['PHONE'].loc[0])}</p>", unsafe_allow_html=True)
            with row1[4]:
                
                search_result = search_companie_id(f"WHERE TC.ID LIKE '%{user['ID'].loc[0]}%'")
                adiantamento = search_result['ADIANT_CASA'].iloc[0]
                if adiantamento == 1:
                    adiantamento = 'Sim'
                else:
                    adiantamento = 'Não'

                st.markdown(f"<p style='text-align: center; margin-top: 1vh;'>Adiantamento: {adiantamento}</p>", unsafe_allow_html=True)
        
            with row1[5]:
                if st.button('X'):
                    st.session_state['Search']['ID'] = None
                    st.session_state['Search']['NAME'] = None
                    st.session_state['Search']['EMAIL'] = None
                    st.session_state['Search']['PHONE'] = None
                    st.session_state['Search']['ADIANT_CASA'] = None
                    st.session_state['Search']['TIPO'] = None
                    st.rerun()

def filterReportType(df):
    df = df.sort_values(by='TIPO')
    option = st.selectbox("Tipo de ocorrência:",(df['TIPO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def filterReportArtist(df):
    df = df.sort_values(by='ARTISTA')
    option = st.selectbox("Buscar artista:",(df['ARTISTA'].unique()),
            index=None, placeholder="Selecione um artista")
    return option

def filterClosureByShow(df):
    df = df.sort_values(by='ID FECHAMENTO')
    option = st.selectbox("Buscar fechamento:",(df['ID FECHAMENTO'].unique()),
            index=None, placeholder="Selecione um ID")
    return option

def filterPaymentSlipByShow(df):
    df = df.sort_values(by='ID BOLETO')
    option = st.selectbox("Buscar boleto:",(df['ID BOLETO'].unique()),
            index=None, placeholder="Selecione um ID")
    return option

def buttonDowloadDash(df, name):
    button_key = f"_{name}_"
    st.download_button(
    label='Baixar em Excel',
    data=to_excel(df),
    file_name=f"{name}.xlsx",
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    key=button_key
    )

def filterCalendarComponent():
    today = datetime.date.today()

    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    d = st.date_input("Filtro de data:", (first_day_of_month, last_day_of_month),
                      format="DD/MM/YYYY")
    return d

def filterEstablishmentComponent(df):
    df_sorted = df.sort_values(by='ESTABELECIMENTO')
    option = st.selectbox("Estabelecimentos:",(df_sorted['ESTABELECIMENTO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def filterArtistComponent(df):
    df_sorted = df.sort_values(by='ARTISTA')
    option = st.selectbox("Artistas:",(df_sorted['ARTISTA'].unique()),
            index=None, placeholder="Escolha um")
    return option


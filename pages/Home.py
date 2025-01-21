import streamlit as st
import pandas as pd

from utils.components import *
from utils.functions import *
from utils.user import logout
from data.get_data import *

# modularização das páginas
from menu.show_history import ShowHistory
from menu.operational_performance import OperationalPerformacePage
from menu.finances import FinancesPage

st.set_page_config(
    page_title="Home | Projetos Eshows",
    page_icon="./assets/imgs/eshows-logo100x100.png",
    layout="wide",
)

function_hide_sidebar()
function_fix_tab_echarts()

if 'loggedIn' not in st.session_state:
    st.switch_page("main.py")

if st.session_state['loggedIn']:
    user_id = st.session_state['user_data']["data"]["user_id"]
    user_name = st.session_state['user_data']["data"]['full_name']

    if 'Search' not in st.session_state:
        st.session_state['Search'] = {'ID': None,
        'FULL_NAME' : None,
        'NOME' : None,
        'LOGIN' : None,
        'CELULAR' : None,
        'ADIANT_CASA' : None
        }

    # Header
    with st.container(border=True):
        row1 = st.columns([3, 0.5, 4, 2, 1, 1])
        with row1[0]:
            #Criando componente de busca e salvando resultado
            choose, search_user = modalSearchComponent() 
            search_user = function_salve_search_in_session(choose, search_user) 
                
        with row1[2]:
            st.markdown("<h2 style='text-align: center;'>Informações dos projetos</h2>", unsafe_allow_html=True, help=None)
        
        with row1[4]:
            st.image("./assets/imgs/eshows100x100.png")
        
        with row1[5]:
            st.markdown("<p style='padding-top:0.4em'></p>", unsafe_allow_html=True)
            if st.button("Logout"):
                logout()
                st.switch_page("main.py")
    
    # Nav
    if not search_user.empty: searchUserDataComponent(choose, search_user)

    # Body
    if st.session_state['Search']['ID'] is not None:
        data = initialize_data(user_id)
        search_user_id = st.session_state['Search']['ID']
        
        if st.session_state['Search']['TIPO'] == 'Artista':
            data = get_artist_data_OperationalPerformace(data, user_id, search_user_id)
            data = get_artist_data_ShowHistory(data, user_id, search_user_id)
            data = get_artist_data_Finance(data, user_id, search_user_id)
        elif st.session_state['Search']['TIPO'] == 'Contratante':
            data = get_establishment_data_OperationalPerformace(data, user_id, search_user_id)
            data = get_establishment_data_ShowHistory(data, user_id, search_user_id)
            data = get_establishment_data_Finance(data, user_id, search_user_id)

        tab1, tab2, tab3 = st.tabs(["OPERACIONAL", "HISTÓRICO DE SHOWS", "FINANCEIRO"])
        with tab1: # Operacional
            try:    
                page = OperationalPerformacePage(data)
                page.render()
            except Exception as e:
                st.error(f'Não foi possível carregar a página. Erro: {e}')
        with tab2: # Histórico de shows
            try:
                page = ShowHistory(data)
                page.render()
            except Exception as e:
                st.error(f'Não foi possível carregar a página. Erro: {e}')
        with tab3: # Financeiro
            try:
                page = FinancesPage(data)
                page.render()
            except Exception as e:
                st.error(f'Não foi possível carregar a página. Erro: {e}')

else:
    st.switch_page("main.py")

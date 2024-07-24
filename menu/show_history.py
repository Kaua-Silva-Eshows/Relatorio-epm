# menu/show_history.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildArtistShowHistory(oldShowHistory, newShowHistory):
    df_combined = concat_column_in_two_dataframes(oldShowHistory, newShowHistory, 'ESTABELECIMENTO')

    row1 = st.columns([2.5,2.5,5])
    with row1[0]:
        filterData = filterCalendarComponent()
    with row1[1]:
        filterEstablishment = filterEstablishmentComponent(df_combined)
    
    oldShowHistory = function_apply_filter_date_establishment(oldShowHistory, filterData, filterEstablishment)
    newShowHistory = function_apply_filter_date_establishment(newShowHistory, filterData, filterEstablishment)

    tab = st.tabs(["Shows Antigos", "Shows Futuros"])
    with tab[0]:
        container1 = st.container(border=True)
        with container1: 
            plotDataframe(oldShowHistory, "Histórico de shows antigos")

    with tab[1]:
        container1 = st.container(border=True)
        with container1: 
            plotDataframe(newShowHistory, "Histórico de shows futuros")

def buildEstablishmentShowHistory(oldShowHistory, newShowHistory):
    df_combined = concat_column_in_two_dataframes(oldShowHistory, newShowHistory, 'ARTISTA')

    row1 = st.columns([2.5,2.5,5])
    with row1[0]:
        filterData = filterCalendarComponent()
    with row1[1]:
        filterArtist= filterArtistComponent(df_combined)
    oldShowHistory = function_apply_filter_date_artist(oldShowHistory, filterData, filterArtist)
    newShowHistory = function_apply_filter_date_artist(newShowHistory, filterData, filterArtist)

    tab = st.tabs(["Shows Antigos", "Shows Futuros"])
    with tab[0]:
        container1 = st.container(border=True)
        with container1: 
            plotDataframe(oldShowHistory, "Histórico de shows antigos")

    with tab[1]:
        container1 = st.container(border=True)
        with container1: 
            plotDataframe(newShowHistory, "Histórico de shows futuros")

class ShowHistory(Page):
    def render(self):
        if st.session_state['Search']['TIPO'] == 'Artista':
            buildArtistShowHistory(self.data['oldShowHistory'],
                        self.data['newShowHistory'],)
        elif st.session_state['Search']['TIPO'] == 'Contratante':
            buildEstablishmentShowHistory(self.data['oldShowHistory'],
                      self.data['newShowHistory'],)
        

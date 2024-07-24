# menu/operational_performance.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildArtistOperationalPerformace(exploreStages, oportunites, casting, favorite, operationalPerformace, ByOccurrence, ByWeek, allOperationalPerformaceByOccurrenceAndDate, financeDash):
    tab= st.tabs(["Explorar palcos", "Artístico", "Resumos de ocorrências", "Extrato de ocorrências"])
    
    with tab[0]:
        container1 = st.container(border=True)
        with container1: 
            plotDataframe(exploreStages, "Explorar palcos do artista")
            plotDataframe(oportunites, "Oportunidades do artista")

    with tab[1]:
        container1 = st.container(border=True)
        with container1: 
            col = st.columns([1,2])
            with col[0]: plotDataframe(casting, "Casting do artista")
            with col[1]: plotDataframe(favorite, "Casas em que o artista está favoritado")
        
    with tab[2]:
        # filtrando pelo artista a partir do session_state
        art = st.session_state['Search']['NOME']
        operationalPerformace = operationalPerformace[operationalPerformace['ARTISTA']==art]
        financeDash = financeDash[financeDash['ARTISTA']==art]
        allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[allOperationalPerformaceByOccurrenceAndDate['ARTISTA']==art]

        if not financeDash.empty:
            row1 = st.columns(4)
            financeDash = transform_show_statement(financeDash)

            tile = row1[0].container(border=True)
            tile.markdown(f"<p style='text-align: center;'>Número de shows</br>{financeDash['NÚMERO DE SHOWS'].loc[0]}</p>", unsafe_allow_html=True)

            tile = row1[1].container(border=True)
            tile.markdown(f"<p style='text-align: center;'>Porcentagem de Checkin(%)</br>{financeDash['PORCENTAGEM DE CHECKIN(%)'].loc[0]}</p>", unsafe_allow_html=True)

            tile = row1[2].container(border=True)
            tile.markdown(f"<p style='text-align: center;'>Porcentagem de Checkout(%)</br>{financeDash['PORCENTAGEM DE CHECKOUT(%)'].loc[0]}</p>", unsafe_allow_html=True)

            tile = row1[3].container(border=True)
            tile.markdown(f"<p style='text-align: center;'>Total de Ocorrências</br>{sum(ByOccurrence['QUANTIDADE'])}</p>", unsafe_allow_html=True)

        container1 = st.container(border=True)
        with container1: 
            row1 = st.columns(2)
            with row1[0]:
                plotPizzaChart(ByOccurrence['TIPO'], ByOccurrence['QUANTIDADE'], "Tipos de Ocorrências")
            with row1[1]:
                plotBarChart(ByWeek, 'SEMANA', 'QUANTIDADE', "Quantidade de ocorrêcias por dia")
    
    with tab[3]:
        # removendo valores e reordenando o dataset
        allOperationalPerformaceByOccurrenceAndDate.drop(columns=['SEMANA'], inplace=True)
        allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[['ARTISTA', 'ESTILO','ESTABELECIMENTO','DATA','TIPO']]
        allOperationalPerformaceByOccurrenceAndDate['DATA'] = allOperationalPerformaceByOccurrenceAndDate['DATA'].apply(lambda x: x.strftime('%d/%m/%Y') if not pd.isnull(x) else None)
        
        row1 = st.columns(6)
        with row1[0]:
            type = filterReportType(allOperationalPerformaceByOccurrenceAndDate)
        with row1[5]:
            st.markdown("<p style='padding-top:0.5em'></p>", unsafe_allow_html=True)
            buttonDowloadDash(allOperationalPerformaceByOccurrenceAndDate, "Extrato-de-Ocorrencias")
        container = st.container(border=True)
        with container:
            if type is not None:
                allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[allOperationalPerformaceByOccurrenceAndDate['TIPO']==type]

            plotDataframe(allOperationalPerformaceByOccurrenceAndDate, "Relatório completo de ocorrências")
    pass

def buildEstablishmentOperationalPerformace(casting,favoriteArtists,aprovedArtists,blockedArtists,performance,reportByOccurenceAndDate,generalInformationAndFinance,byOccurrence,operationalPerformace,byWeek):
    tab= st.tabs(["Artístico", "Resumos de ocorrências", "Extrato de ocorrências"])
    
    with tab[0]:
        container1 = st.container(border=True)
        with container1: 
            with st.expander("Casting"): plotDataframe(casting, 'Casting do estabelecimento')
            col = st.columns(3)
            with col[0]:
                plotDataframe(favoriteArtists, 'Artistas favoritados')
            with col[1]:
                plotDataframe(aprovedArtists, 'Artistas aprovados')
            with col[2]:
                plotDataframe(blockedArtists, 'Artistas bloqueados')
    
    with tab[1]:
        if not generalInformationAndFinance.empty:
            row1 = st.columns(4)
            financeDash = transform_show_statement(generalInformationAndFinance)

            tile = row1[0].container(border=True)
            tile.markdown(f"<p style='text-align: center;'>Número de shows</br>{sum(financeDash['NÚMERO DE SHOWS'])}</p>", unsafe_allow_html=True)

            tile = row1[3].container(border=True)
            tile.markdown(f"<p style='text-align: center;'>Total de Ocorrências</br>{sum(byOccurrence['QUANTIDADE'])}</p>", unsafe_allow_html=True)

        container1 = st.container(border=True)
        with container1: 
            row1 = st.columns(2)
            with row1[0]:
                plotPizzaChart(byOccurrence['TIPO'], byOccurrence['QUANTIDADE'], "Tipos de Ocorrências")
            with row1[1]:
                plotBarChart(byWeek, 'SEMANA', 'QUANTIDADE', "Quantidade de ocorrêcias por dia")
    
    with tab[2]:
        row1 = st.columns(6)
        with row1[0]:
            type = filterReportType(performance)
        with row1[5]:
            st.markdown("<p style='padding-top:0.5em'></p>", unsafe_allow_html=True)
            buttonDowloadDash(performance, "Extrato-de-Ocorrencias")

        container1 = st.container(border=True)
        with container1:
            if type is not None:
                performance = performance[performance['TIPO']==type] 
            plotDataframe(performance, 'Relatório completo de ocorrências')

class OperationalPerformacePage(Page):
    def render(self):
        if st.session_state['Search']['TIPO'] == 'Artista':
            buildArtistOperationalPerformace(
                                    self.data['exploreStages'],
                                    self.data['oportunites'],
                                    self.data['casting'],
                                    self.data['favorite'],
                                    self.data['operationalPerformace'],  
                                    self.data['ByOccurrence'], 
                                    self.data['ByWeek'],  
                                    self.data['allOperationalPerformaceByOccurrenceAndDate'], 
                                    self.data['financeDash'])
                                    
        elif st.session_state['Search']['TIPO'] == 'Contratante':
            buildEstablishmentOperationalPerformace(
                                    self.data['Casting'],
                                    self.data['FavoriteArtists'],
                                    self.data['AprovedArtists'],
                                    self.data['BlockedArtists'],
                                    self.data['Performance'],
                                    self.data['ReportByOccurenceAndDate'],
                                    self.data['GeneralInformationAndFinance'],
                                    self.data['ByOccurrence'],
                                    self.data['OperationalPerformace'],
                                    self.data['ByWeek']
                                    )

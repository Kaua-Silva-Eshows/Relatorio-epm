# menu/finances.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildArtistFinances(financesClosures, financesClosuresShows,financesPeddingInvoices, financesAntecipationInvoices, financesSendedInvoices, financesPaymentSlip, financesPaymentSlipShows):
    tab= st.tabs(["Fechamentos", "Notas Fiscais", "Boletos"])
    with tab[0]:
        row1 = st.columns([2.5,2.5,5])
        with row1[0]:
            filterClosure = filterClosureByShow(financesClosures)

        container1 = st.container(border=True)
        with container1: 
            plotDataframe(financesClosures, 'Fechamentos')
            if filterClosure is not None:
                plotDataframe(financesClosuresShows[financesClosuresShows['ID FECHAMENTO'] == filterClosure], 'Shows dentro do fechamento')
    
    with tab[1]:
        container1 = st.container(border=True)
        with container1:     
            plotDataframe(financesPeddingInvoices, 'Notas fiscais pendentes')
            plotDataframe(financesAntecipationInvoices, 'Notas fiscais antecipadas')
            plotDataframe(financesSendedInvoices, 'Notas fiscais envidas')
    
    with tab[2]:
        row1 = st.columns([2.5,2.5,5])
        with row1[0]:
            filterPaymentSlip = filterPaymentSlipByShow(financesPaymentSlip)

        container1 = st.container(border=True)
        with container1: 
            plotDataframe(financesPaymentSlip, 'Boletos do artista')
            if filterPaymentSlip is not None:
                plotDataframe(financesPaymentSlipShows[financesPaymentSlipShows['ID BOLETO']==filterPaymentSlip], 'Shows do boleto')
            
def buildEstablishmentFinances(financesClosures, financesClosuresShows,financesPeddingInvoices, financesAntecipationInvoices, financesSendedInvoices, financesPaymentSlip, financesPaymentSlipShows):
    tab= st.tabs(["Fechamentos", "Notas Fiscais", "Boletos"])
    with tab[0]:
        row1 = st.columns([2.5,2.5,5])
        with row1[0]:
            filterClosure = filterClosureByShow(financesClosures)

        container1 = st.container(border=True)
        with container1: 
            plotDataframe(financesClosures, 'Fechamentos')
            if filterClosure is not None:
                plotDataframe(financesClosuresShows[financesClosuresShows['ID FECHAMENTO'] == filterClosure], 'Shows dentro do fechamento')
    
    with tab[1]:
        container1 = st.container(border=True)
        with container1:     
            plotDataframe(financesPeddingInvoices, 'Notas fiscais pendentes')
            plotDataframe(financesAntecipationInvoices, 'Notas fiscais antecipadas')
            plotDataframe(financesSendedInvoices, 'Notas fiscais envidas')
    
    with tab[2]:
        row1 = st.columns([2.5,2.5,5])
        with row1[0]:
            filterPaymentSlip = filterPaymentSlipByShow(financesPaymentSlip)

        container1 = st.container(border=True)
        with container1: 
            plotDataframe(financesPaymentSlip, 'Boletos do estabelecimento')
            if filterPaymentSlip is not None:
                plotDataframe(financesPaymentSlipShows[financesPaymentSlipShows['ID BOLETO']==filterPaymentSlip], 'Shows do boleto')
                

class FinancesPage(Page):
    def render(self):
        if st.session_state['Search']['TIPO'] == 'Artista':
            buildArtistFinances(self.data['financesClosures'],
                            self.data['financesClosuresShows'],
                            self.data['financesPeddingInvoices'],
                            self.data['financesAntecipationInvoices'],
                            self.data['financesSendedInvoices'],
                            self.data['financesPaymentSlip'],
                            self.data['financesPaymentSlipShows'])
        elif st.session_state['Search']['TIPO'] == 'Contratante':
            buildEstablishmentFinances(self.data['financesClosures'],
                            self.data['financesClosuresShows'],
                            self.data['financesPeddingInvoices'],
                            self.data['financesAntecipationInvoices'],
                            self.data['financesSendedInvoices'],
                            self.data['financesPaymentSlip'],
                            self.data['financesPaymentSlipShows'])

                    

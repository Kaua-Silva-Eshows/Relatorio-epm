from utils.functions import *
from data.queries import *
from data.artist_queries import *
from data.establishment_queries import *
import pandas as pd
import streamlit as st

#user_id -> id do usário que fez login
#id -> id do usuário buscado

# Inicializa os valores de data
def initialize_data(id):
    # Dicionário com dados de entrada
    data = {
        'financesClosures': pd.DataFrame(),
        'financesClosuresShows': pd.DataFrame(),
        'financesPeddingInvoices': pd.DataFrame(),
        'financesAntecipationInvoices': pd.DataFrame(),
        'financesSendedInvoices': pd.DataFrame(),
        'financesPaymentSlip': pd.DataFrame(),
        'financesPaymentSlipShows': pd.DataFrame(),
        'oldShowHistory': pd.DataFrame(),
        'newShowHistory': pd.DataFrame(),
        'exploreStages': pd.DataFrame(),
        'oportunites': pd.DataFrame(),
        'casting': pd.DataFrame(),
        'favorite': pd.DataFrame(),
        'financeDash': pd.DataFrame(),
        'ByOccurrence': pd.DataFrame(),
        'allOperationalPerformaceByOccurrenceAndDate': pd.DataFrame(),
        'operationalPerformace': pd.DataFrame(),
        'ByWeek': pd.DataFrame(),
        'Casting': pd.DataFrame(),
        'FavoriteArtists': pd.DataFrame(),
        'AprovedArtists': pd.DataFrame(),
        'BlockedArtists': pd.DataFrame(),
        'Performance': pd.DataFrame(),
        'ReportByOccurenceAndDate': pd.DataFrame(),
        'GeneralInformationAndFinance': pd.DataFrame(),
        'OperationalPerformace': pd.DataFrame(),
        'id':id
    }

    return data

def get_artist_data_Finance(data, user_id, id):
    try:
        financesClosures = artist_finances_closures(id)
        data['financesClosures'] = financesClosures
    except Exception as e:
        data['financesClosures'] = pd.DataFrame()

    try:
        financesClosuresShows = artist_finances_closures_shows(id)
        data['financesClosuresShows'] = financesClosuresShows
    except Exception as e:
        data['financesClosuresShows'] = pd.DataFrame()
    
    try:
        financesPeddingInvoices = artist_finances_pedding_invoices(id)
        data['financesPeddingInvoices'] = financesPeddingInvoices
    except Exception as e:
        data['financesPeddingInvoices'] = pd.DataFrame()
    
    try:
        financesAntecipationInvoices = artist_finances_antecipation_invoices(id)
        data['financesAntecipationInvoices'] = financesAntecipationInvoices
    except Exception as e:
        data['financesAntecipationInvoices'] = pd.DataFrame()
    
    try:
        financesSendedInvoices = artist_finances_sended_invoices(id)
        data['financesSendedInvoices'] = financesSendedInvoices
    except Exception as e:
        data['financesSendedInvoices'] = pd.DataFrame()
    
    try:
        financesPaymentSlip = artist_finances_payment_slip(id)
        data['financesPaymentSlip'] = financesPaymentSlip
    except Exception as e:
        data['financesPaymentSlip'] = pd.DataFrame()
    
    try:
        financesPaymentSlipShows = artist_finances_payment_slip_shows(id)
        data['financesPaymentSlipShows'] = financesPaymentSlipShows
    except Exception as e:
        data['financesPaymentSlipShows'] = pd.DataFrame()

    return data

def get_artist_data_ShowHistory(data, user_id,id):
    try:
        oldShowHistory = artist_showhistory_old_show_history(id)
        data['oldShowHistory'] = oldShowHistory
    except Exception as e:
        data['oldShowHistory'] = pd.DataFrame()

    try:
        newShowHistory = artist_showhistory_new_show_history(id)
        data['newShowHistory'] = newShowHistory
    except Exception as e:
        data['newShowHistory'] = pd.DataFrame()

    return data

def get_artist_data_OperationalPerformace(data, user_id,id):
    try:
        exploreStages = artist_operational_explore_stages(id)
        data['exploreStages'] = exploreStages
    except Exception as e:
        data['exploreStages'] = pd.DataFrame()

    try:
        oportunites = artist_operational_oportunities(id)
        data['oportunites'] = oportunites
    except Exception as e:
        data['oportunites'] = pd.DataFrame()

    try:
        casting = artist_operational_casting(id)
        data['casting'] = casting
    except Exception as e:
        data['casting'] = pd.DataFrame()

    try:
        favorite = artist_operational_favorite(id)
        data['favorite'] = favorite
    except Exception as e:
        data['favorite'] = pd.DataFrame()

    try:
        financeDash = artist_operational_general_information_and_finance(id)
        data['financeDash'] = financeDash
    except Exception as e:
        data['financeDash'] = pd.DataFrame()

    try:
        ByOccurrence = get_report_by_occurrence(artist_operational_report_by_occurence_and_date(id))
        data['ByOccurrence'] = ByOccurrence
    except Exception as e:
        data['ByOccurrence'] = pd.DataFrame()

    try:
        allOperationalPerformaceByOccurrenceAndDate = artist_operational_performance(id)
        data['allOperationalPerformaceByOccurrenceAndDate'] = allOperationalPerformaceByOccurrenceAndDate
    except Exception as e:
        data['allOperationalPerformaceByOccurrenceAndDate'] = pd.DataFrame()

    try:
        operationalPerformace = get_report_artist(allOperationalPerformaceByOccurrenceAndDate)
        data['operationalPerformace'] = operationalPerformace
    except Exception as e:
        data['operationalPerformace'] = pd.DataFrame()

    try:
        ByWeek = get_report_artist_by_week(allOperationalPerformaceByOccurrenceAndDate)
        data['ByWeek'] = ByWeek
    except Exception as e:
        data['ByWeek'] = pd.DataFrame()
    
    return data

def get_establishment_data_Finance(data, user_id, id):
    try:
        financesClosures = establishment_finances_closures(id)
        data['financesClosures'] = financesClosures
    except Exception as e:
        data['financesClosures'] = pd.DataFrame()

    try:
        financesClosuresShows = establishment_finances_closures_shows(id)
        data['financesClosuresShows'] = financesClosuresShows
    except Exception as e:
        data['financesClosuresShows'] = pd.DataFrame()

    try:
        financesPeddingInvoices = establishment_finances_pedding_invoices(id)
        data['financesPeddingInvoices'] = financesPeddingInvoices
    except Exception as e:
        data['financesPeddingInvoices'] = pd.DataFrame()

    try:
        financesAntecipationInvoices = establishment_finances_antecipation_invoices(id)
        data['financesAntecipationInvoices'] = financesAntecipationInvoices
    except Exception as e:
        data['financesAntecipationInvoices'] = pd.DataFrame()

    try:
        financesSendedInvoices = establishment_finances_sended_invoices(id)
        data['financesSendedInvoices'] = financesSendedInvoices
    except Exception as e:
        data['financesSendedInvoices'] = pd.DataFrame()

    try:
        financesInvoicesShows = establishment_finances_invoices_shows(id)
        data['financesInvoicesShows'] = financesInvoicesShows
    except Exception as e:
        data['financesInvoicesShows'] = pd.DataFrame()

    try:
        financesPaymentSlip = establishment_finances_payment_slip(id)
        data['financesPaymentSlip'] = financesPaymentSlip
    except Exception as e:
        data['financesPaymentSlip'] = pd.DataFrame()

    try:
        financesPaymentSlipShows = establishment_finances_payment_slip_shows(id)
        data['financesPaymentSlipShows'] = financesPaymentSlipShows
    except Exception as e:
        data['financesPaymentSlipShows'] = pd.DataFrame()

    return data

def get_establishment_data_ShowHistory(data, user_id, id):
    try:
        oldShowHistory = establishment_showhistory_old_show_history(id)
        data['oldShowHistory'] = oldShowHistory
    except Exception as e:
        data['oldShowHistory'] = pd.DataFrame()

    try:
        newShowHistory = establishment_showhistory_new_show_history(id)
        data['newShowHistory'] = newShowHistory
    except Exception as e:
        data['newShowHistory'] = pd.DataFrame()

    return data
    
def get_establishment_data_OperationalPerformace(data, user_id,id):
    try:
        Casting = establishment_operational_casting(id)
        data['Casting'] = Casting
    except Exception as e:
        data['Casting'] = pd.DataFrame()

    try:
        FavoriteArtists = establishment_operational_favorite_artists(id)
        data['FavoriteArtists'] = FavoriteArtists
    except Exception as e:
        data['FavoriteArtists'] = pd.DataFrame()

    try:
        AprovedArtists = establishment_operational_aproved_artists(id)
        data['AprovedArtists'] = AprovedArtists
    except Exception as e:
        data['AprovedArtists'] = pd.DataFrame()

    try:
        BlockedArtists = establishment_operational_blocked_artists(id)
        data['BlockedArtists'] = BlockedArtists
    except Exception as e:
        data['BlockedArtists'] = pd.DataFrame()

    try:
        Performance = establishment_operational_performance(id)
        data['Performance'] = Performance
    except Exception as e:
        data['Performance'] = pd.DataFrame()

    try:
        ReportByOccurenceAndDate = establishment_operational_report_by_occurence_and_date(id)
        data['ReportByOccurenceAndDate'] = ReportByOccurenceAndDate
    except Exception as e:
        data['ReportByOccurenceAndDate'] = pd.DataFrame()

    try:
        GeneralInformationAndFinance = establishment_operational_general_information_and_finance(id)
        data['GeneralInformationAndFinance'] = GeneralInformationAndFinance
    except Exception as e:
        data['GeneralInformationAndFinance'] = pd.DataFrame()

    try:
        ByOccurrence = get_report_by_occurrence(ReportByOccurenceAndDate)
        data['ByOccurrence'] = ByOccurrence
    except Exception as e:
        data['ByOccurrence'] = pd.DataFrame()

    try:
        OperationalPerformace = get_report_artist(ReportByOccurenceAndDate)
        data['OperationalPerformace'] = OperationalPerformace
    except Exception as e:
        data['OperationalPerformace'] = pd.DataFrame()

    try:
        ByWeek = get_report_artist_by_week(ReportByOccurenceAndDate)
        data['ByWeek'] = ByWeek
    except Exception as e:
        data['ByWeek'] = pd.DataFrame()

    return data

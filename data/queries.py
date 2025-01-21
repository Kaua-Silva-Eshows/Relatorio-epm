from data.dbconnect import getDfFromQuery
from utils.functions import *
import streamlit as st

def search_artist_id(filter):
    result = getDfFromQuery("""
    SELECT 
    TA.ID,
    AU.LOGIN,
    AU.FULL_NAME,
    TA.CELULAR,
    TA.NOME
    FROM ADMIN_USERS AU
    LEFT JOIN T_ATRACOES TA ON AU.ID = TA.FK_USUARIO
    """ +filter)

    return result

def search_companie_id(filter):
    result = getDfFromQuery("""
    SELECT 
    TC.ID,
    TC.EMAIL,
    TC.NAME,
    TC.PHONE,
    TC.ADIANT_CASA
    FROM T_COMPANIES TC
    """ + filter)

    return result

def get_search_artist_from_session(id):
    result = getDfFromQuery(f"""
    SELECT 
    TA.ID,
    AU.LOGIN,
    AU.FULL_NAME,
    TA.CELULAR,
    TA.NOME
    FROM ADMIN_USERS AU
    LEFT JOIN T_ATRACOES TA ON AU.ID = TA.FK_USUARIO
    WHERE TA.ID = '{id}'
    """)
    return result

def get_search_companie_from_session(id):
    result = getDfFromQuery(f"""
    SELECT 
    TC.ID,
    TC.EMAIL,
    TC.NAME,
    TC.PHONE
    FROM T_COMPANIES TC
    WHERE TC.ID = '{id}'
    """)
    return result

def search_establishment_id(filter):
    result = getDfFromQuery("QUERY"+filter)
    return result.loc[0, 'ID']

def search_user_from_session(choose, id):
    if choose == 'Artista':
        return get_search_artist_from_session(id)
    elif choose == 'Contratante':
        return get_search_companie_from_session(id)












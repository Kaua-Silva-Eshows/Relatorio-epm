from data.dbconnect import getDfFromQuery
from utils.functions import *
import streamlit as st

#histórico de shows
@st.cache_data
def establishment_showhistory_old_show_history(id):
    query = (f"""
    SELECT
    P.ID AS 'ID DA PROPOSTA',

    CASE 
    WHEN S.DESCRICAO IS NULL THEN "Cancelada"
    ELSE S.DESCRICAO
    END AS 'STATUS DA PROPOSTA',
    A.NOME AS ARTISTA,
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'DATA DE INÍCIO', 
    DATE_FORMAT(P.DATA_INICIO, '%H:%i') AS 'HORÁRIO INÍCIO',
    DATE_FORMAT(P.DATA_FIM, '%H:%i') AS 'HORÁRIO FIM',
    CONCAT('R$ ', FORMAT(P.VALOR_BRUTO, 2))  AS 'VALOR BRUTO',
    CONCAT('R$ ', FORMAT(P.VALOR_LIQUIDO, 2)) AS 'VALOR LÍQUIDO',
    CONCAT('R$ ', FORMAT(P.VALOR_ARTISTA_A_RECEBER, 2)) AS 'VALOR A RECEBER ARTISTA',
    CONCAT('R$ ', FORMAT(P.VALOR_ESHOWS_RECEBIMENTO, 2)) AS 'VALOR RECEBIDO ESHOWS',
    SF.DESCRICAO AS 'STATUS FINANCEIRO',
    P.FK_FECHAMENTO AS 'ID DO FECHAMENTO',

    CASE 
    WHEN P.ADIANTAMENTO IS NULL THEN 0
    ELSE P.ADIANTAMENTO
    END AS 'ADIANTAMENTO',

    DATE_FORMAT(P.PREVISAO_PGTO, '%d/%m/%Y') AS 'PREVISÃO DE PAGAMENTO',

    CASE 
    WHEN P.DATA_PAGAMENTO IS NULL THEN ""
    ELSE DATE_FORMAT(P.DATA_PAGAMENTO, '%d/%m/%Y')
    END AS 'DATA DO PAGAMENTO',

    DATE_FORMAT(P.PREVISAO_VENCIMENTO_BOLETO, '%d/%m/%Y') AS 'PREVISÃO DE VENCIMENTO DO BOLETO',
    DATE_FORMAT(P.PREVISAO_PGTO_ATUALIZADA, '%d/%m/%Y') AS 'PREVISÃO DE PAGAMENTO ATUALIZADA',

    CASE 
    WHEN C.NOTA_FISCAL = 1 THEN 'Sim'
    WHEN C.NOTA_FISCAL = 0 THEN 'Não'
    ELSE ' '
    END AS 'EXIGE NF?',

    CASE 
    WHEN P.FK_NOTA_FISCAL IS NULL THEN ""
    ELSE P.FK_NOTA_FISCAL
    END AS 'ID DA NF',

    CASE 
    WHEN P.FK_STATUS_PROPOSTA = 102 THEN CONCAT(MR.MOTIVO,": ",MRP.DESCRICAO_RECUSA)
    WHEN MCP.FK_PROPOSTA = P.ID THEN CONCAT(MC.TEXTO_MOTIVO,": ",MCP.DESCRICAO_CANCELAMENTO)
    WHEN SPP.FK_PROPOSTA = P.ID THEN CONCAT(SP.TITULO,": ",SPP.SINAL_PROBLEMA_DESCRICAO)
    END AS 'OBSERVAÇÃO MOTIVO',
    CONCAT('https://admin.eshows.com.br/proposta/', P.ID) AS LINK

    FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
    LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
    LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
    LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
    LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
    LEFT JOIN T_PALCOS PAL ON PAL.ID = P.FK_PALCOS
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON GC.ID = C.FK_GRUPO
    LEFT JOIN T_MOTIVO_RECUSA_PROPOSTA MRP ON MRP.FK_PROPOSTA = P.ID
    LEFT JOIN T_MOTIVO_RECUSA MR ON MR.ID = MRP.FK_MOTIVO_RECUSA
    LEFT JOIN T_MOTIVO_CANCELAMENTO_PROPOSTA MCP ON MCP.FK_PROPOSTA = P.ID
    LEFT JOIN T_MOTIVO_CANCELAMENTO MC ON MC.ID = MCP.FK_ID_SOLICITACAO_CANCELAMENTO
    LEFT JOIN T_SINAL_PROBLEMA_PROPOSTA SPP ON SPP.FK_PROPOSTA = P.ID
    LEFT JOIN T_SINAL_PROBLEMA SP ON SP.ID = SPP.FK_SINAL_PROBLEMA
    LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    LEFT JOIN T_ATRACAO_BANCOS AB ON (AB.ID = P.FK_ATRACAO_BANCO)


    WHERE (P.TESTE = 0 OR P.TESTE IS NULL) 
    AND C.NAME IS NOT NULL 
    AND A.NOME IS NOT NULL 
    AND P.DATA_INICIO IS NOT NULL
    AND DATE(P.DATA_INICIO) <= CURDATE()
    AND P.DATA_INICIO > DATE_SUB(CURDATE(), INTERVAL 120 DAY)
    AND C.ID = {id}

    ORDER BY P.DATA_INICIO DESC;
    """)
    
    return getDfFromQuery(query)

@st.cache_data     
def establishment_showhistory_new_show_history(id):
    return getDfFromQuery(f"""
    SELECT
    P.ID AS 'ID DA PROPOSTA',

    CASE 
    WHEN S.DESCRICAO IS NULL THEN "Cancelada"
    ELSE S.DESCRICAO
    END AS 'STATUS DA PROPOSTA',
    A.NOME AS ARTISTA,
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'DATA DE INÍCIO', 
    DATE_FORMAT(P.DATA_INICIO, '%H:%i') AS 'HORÁRIO INÍCIO',
    DATE_FORMAT(P.DATA_FIM, '%H:%i') AS 'HORÁRIO FIM',
    CONCAT('R$ ', FORMAT(P.VALOR_BRUTO, 2))  AS 'VALOR BRUTO',
    CONCAT('R$ ', FORMAT(P.VALOR_LIQUIDO, 2)) AS 'VALOR LÍQUIDO',
    CONCAT('R$ ', FORMAT(P.VALOR_ARTISTA_A_RECEBER, 2)) AS 'VALOR A RECEBER ARTISTA',
    CONCAT('R$ ', FORMAT(P.VALOR_ESHOWS_RECEBIMENTO, 2)) AS 'VALOR RECEBIDO ESHOWS',
    SF.DESCRICAO AS 'STATUS FINANCEIRO',
    P.FK_FECHAMENTO AS 'ID DO FECHAMENTO',

    CASE 
    WHEN P.ADIANTAMENTO IS NULL THEN 0
    ELSE P.ADIANTAMENTO
    END AS 'ADIANTAMENTO',

    DATE_FORMAT(P.PREVISAO_PGTO, '%d/%m/%Y') AS 'PREVISÃO DE PAGAMENTO',

    CASE 
    WHEN P.DATA_PAGAMENTO IS NULL THEN ""
    ELSE DATE_FORMAT(P.DATA_PAGAMENTO, '%d/%m/%Y')
    END AS 'DATA DO PAGAMENTO',

    DATE_FORMAT(P.PREVISAO_VENCIMENTO_BOLETO, '%d/%m/%Y') AS 'PREVISÃO DE VENCIMENTO DO BOLETO',
    DATE_FORMAT(P.PREVISAO_PGTO_ATUALIZADA, '%d/%m/%Y') AS 'PREVISÃO DE PAGAMENTO ATUALIZADA',

    CASE 
    WHEN C.NOTA_FISCAL = 1 THEN 'Sim'
    WHEN C.NOTA_FISCAL = 0 THEN 'Não'
    ELSE ' '
    END AS 'EXIGE NF?',

    CASE 
    WHEN P.FK_NOTA_FISCAL IS NULL THEN ""
    ELSE P.FK_NOTA_FISCAL
    END AS 'ID DA NF',

    CASE 
    WHEN P.FK_STATUS_PROPOSTA = 102 THEN CONCAT(MR.MOTIVO,": ",MRP.DESCRICAO_RECUSA)
    WHEN MCP.FK_PROPOSTA = P.ID THEN CONCAT(MC.TEXTO_MOTIVO,": ",MCP.DESCRICAO_CANCELAMENTO)
    WHEN SPP.FK_PROPOSTA = P.ID THEN CONCAT(SP.TITULO,": ",SPP.SINAL_PROBLEMA_DESCRICAO)
    END AS 'OBSERVAÇÃO MOTIVO',
    CONCAT('https://admin.eshows.com.br/proposta/', P.ID) AS LINK

    FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
    LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
    LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
    LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
    LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
    LEFT JOIN T_PALCOS PAL ON PAL.ID = P.FK_PALCOS
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON GC.ID = C.FK_GRUPO
    LEFT JOIN T_MOTIVO_RECUSA_PROPOSTA MRP ON MRP.FK_PROPOSTA = P.ID
    LEFT JOIN T_MOTIVO_RECUSA MR ON MR.ID = MRP.FK_MOTIVO_RECUSA
    LEFT JOIN T_MOTIVO_CANCELAMENTO_PROPOSTA MCP ON MCP.FK_PROPOSTA = P.ID
    LEFT JOIN T_MOTIVO_CANCELAMENTO MC ON MC.ID = MCP.FK_ID_SOLICITACAO_CANCELAMENTO
    LEFT JOIN T_SINAL_PROBLEMA_PROPOSTA SPP ON SPP.FK_PROPOSTA = P.ID
    LEFT JOIN T_SINAL_PROBLEMA SP ON SP.ID = SPP.FK_SINAL_PROBLEMA
    LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    LEFT JOIN T_ATRACAO_BANCOS AB ON (AB.ID = P.FK_ATRACAO_BANCO)


    WHERE (P.TESTE = 0 OR P.TESTE IS NULL) 
    AND C.NAME IS NOT NULL 
    AND A.NOME IS NOT NULL 
    AND P.DATA_INICIO IS NOT NULL
    AND DATE(P.DATA_INICIO) >= CURDATE()
    AND P.DATA_INICIO > DATE_SUB(CURDATE(), INTERVAL 120 DAY)
    AND C.ID = {id}

    ORDER BY P.DATA_INICIO DESC;
    """)

#operacional
@st.cache_data
def establishment_operational_casting(id):
    result = getDfFromQuery(f"""
    SELECT
    A.ID AS 'ID',
    A.NOME AS ARTISTA,
    A.CELULAR

    FROM T_CASTING CAST
    INNER JOIN T_ATRACOES A ON A.ID = CAST.FK_ATRACAO
    INNER JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    INNER JOIN T_COMPANIES C ON C.ID = CAST.FK_CONTRATANTE

    WHERE C.ID = {id}
    """)
    return result

@st.cache_data
def establishment_operational_favorite_artists(id):
    return getDfFromQuery(f"""
    SELECT
    A.ID AS 'ID',
    A.NOME AS ARTISTA
    FROM T_FAVORITO F
    INNER JOIN T_ATRACOES A ON A.ID = F.FK_ATRACAO
    INNER JOIN T_COMPANIES C ON C.ID = F.FK_CONTRATANTE
    WHERE F.FAVORITE = 1
    AND F.BLOCKED = 0
    AND C.ID = {id}
    ORDER BY A.NOME ASC;
    """)

@st.cache_data
def establishment_operational_aproved_artists(id):
    return getDfFromQuery(f"""
    SELECT
    A.ID AS 'ID',
    A.NOME AS ARTISTA
    FROM T_FAVORITO F
    INNER JOIN T_ATRACOES A ON A.ID = F.FK_ATRACAO
    INNER JOIN T_COMPANIES C ON C.ID = F.FK_CONTRATANTE
    WHERE F.APROVADO = 1
    AND F.FAVORITE = 0
    AND F.BLOCKED = 0
    AND C.ID = {id}
    ORDER BY A.NOME ASC;
    """)

@st.cache_data
def establishment_operational_blocked_artists(id):
    return getDfFromQuery(f"""
    SELECT
    A.ID AS 'ID',
    A.NOME AS ARTISTA
    FROM T_FAVORITO F
    INNER JOIN T_ATRACOES A ON A.ID = F.FK_ATRACAO
    INNER JOIN T_COMPANIES C ON C.ID = F.FK_CONTRATANTE
    WHERE F.BLOCKED = 1
    AND C.ID = {id}
    ORDER BY A.NOME ASC;
    """)

@st.cache_data
def establishment_operational_performance(id):
    df = getDfFromQuery(f"""
                    SELECT
                    A.FK_USUARIO AS ID,
                    A.NOME AS ARTISTA,
                    EM.DESCRICAO AS ESTILO,
                    TIPO.TIPO AS TIPO,
                    DATE_FORMAT(OA.DATA_OCORRENCIA, '%d/%m/%Y') AS DATA
                    
                    FROM 
                    T_OCORRENCIAS_AUTOMATICAS OA
                    LEFT JOIN T_PROPOSTAS P ON P.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_PROPOSTAS'
                    LEFT JOIN T_NOTAS_FISCAIS NF ON NF.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND NF.TIPO = 'NF_UNICA'
                    LEFT JOIN T_NOTAS_FISCAIS NF2 ON NF2.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND (NF2.TIPO = 'NF_SHOW_ANTECIPADO' OR NF2.TIPO = 'NF_SHOW_SOZINHOS')
                    INNER JOIN T_ATRACOES A ON A.ID = OA.FK_ATRACAO
                    INNER JOIN T_TIPOS_OCORRENCIAS TIPO ON TIPO.ID = OA.FK_TIPO_OCORRENCIA
                    LEFT JOIN T_FECHAMENTOS F ON F.ID = NF.FK_FECHAMENTO
                    LEFT JOIN T_PROPOSTAS P2 ON P2.ID = NF2.FK_PROPOSTA
                    LEFT JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE OR C.ID = F.FK_CONTRATANTE OR C.ID = P2.FK_CONTRANTE)
                    LEFT JOIN T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID
                    
                    WHERE
                    C.ID = {id} 
                    AND C.ID NOT IN (102,343,632,633)
                    AND A.ID NOT IN (12166)
                    AND OA.DATA_OCORRENCIA >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)

                    ORDER BY OA.DATA_OCORRENCIA DESC
                    """)

    return df

@st.cache_data
def establishment_operational_report_by_occurence_and_date(id):
    df = getDfFromQuery(f"""
                            SELECT
                            A.FK_USUARIO AS ID,
                            A.NOME AS ARTISTA,
                            DATE(OA.DATA_OCORRENCIA) AS DATA,
                            DATE_ADD(DATE(OA.DATA_OCORRENCIA), INTERVAL(2-DAYOFWEEK(OA.DATA_OCORRENCIA)) DAY) AS SEMANA,
                            TIPO.TIPO AS TIPO,
                            EM.DESCRICAO AS ESTILO,
                            C.NAME AS ESTABELECIMENTO

                            FROM 
                            T_OCORRENCIAS_AUTOMATICAS OA
                            LEFT JOIN T_PROPOSTAS P ON P.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_PROPOSTAS'
                            LEFT JOIN T_NOTAS_FISCAIS NF ON NF.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND NF.TIPO = 'NF_UNICA'
                            LEFT JOIN T_NOTAS_FISCAIS NF2 ON NF2.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND (NF2.TIPO = 'NF_SHOW_ANTECIPADO' OR NF2.TIPO = 'NF_SHOW_SOZINHOS')
                            INNER JOIN T_ATRACOES A ON A.ID = OA.FK_ATRACAO
                            INNER JOIN T_TIPOS_OCORRENCIAS TIPO ON TIPO.ID = OA.FK_TIPO_OCORRENCIA
                            LEFT JOIN T_FECHAMENTOS F ON F.ID = NF.FK_FECHAMENTO
                            LEFT JOIN T_PROPOSTAS P2 ON P2.ID = NF2.FK_PROPOSTA
                            LEFT JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE OR C.ID = F.FK_CONTRATANTE OR C.ID = P2.FK_CONTRANTE)
                            LEFT JOIN T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID

                            WHERE C.ID = {id} 
                            AND C.ID NOT IN (102,343,632,633)
                            AND A.ID NOT IN (12166)
                            AND OA.DATA_OCORRENCIA >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    """)

    return df

@st.cache_data
def establishment_operational_general_information_and_finance(id): 
    df =getDfFromQuery(f"""
                        SELECT
                        A.FK_USUARIO AS ID,
                        A.NOME AS ARTISTA,
                        C.NAME AS ESTABELECIMENTO,
                        S.DESCRICAO AS STATUS_PROPOSTA,
                        SF.DESCRICAO AS STATUS_FINANCEIRO,
                        P.DATA_INICIO AS DATA_INICIO,
                        P.DATA_FIM AS DATA_FIM,
                        CONCAT(
                        TIMESTAMPDIFF(HOUR, P.DATA_INICIO, P.DATA_FIM), 'h ',
                        TIMESTAMPDIFF(MINUTE, P.DATA_INICIO, P.DATA_FIM) % 60, 'm ',
                        TIMESTAMPDIFF(SECOND, P.DATA_INICIO, P.DATA_FIM) % 60, 's'
                        ) AS DURACAO,
                        DAYNAME(P.DATA_INICIO) AS DIA_DA_SEMANA,
                        P.VALOR_BRUTO,
                        P.VALOR_LIQUIDO,
                        F.ID AS ID_FECHAMENTO,
                        F.DATA_INICIO AS INICIO_FECHAMENTO,
                        F.DATA_FIM AS FIM_FECHAMENTO
                        FROM T_PROPOSTAS P
                        INNER JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
                        INNER JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
                        LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
                        INNER JOIN T_FECHAMENTOS F ON F.ID = P.FK_FECHAMENTO
                        LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
                        WHERE 
                        C.ID = {id}
                        AND P.FK_STATUS_PROPOSTA IN (100,101,103,104)
                        AND A.ID NOT IN (12166)
                        ORDER BY
                        P.DATA_INICIO ASC
                        """)
    
    return df

#financeiro
@st.cache_data
def establishment_finances_closures(id):
    return getDfFromQuery(f"""
    SELECT
    F.ID as "ID FECHAMENTO",
    DATE_FORMAT(F.LAST_UPDATE, '%d/%m/%Y') as "DATA DE CRIAÇÃO",
    DATE_FORMAT(F.DATA_INICIO, '%d/%m/%Y') as "PERÍODO DE INÍCIO",
    DATE_FORMAT(F.DATA_FIM, '%d/%m/%Y') as "PERÍODO FIM",
    F.OBSERVACAO as "OBSERVAÇÃO DO FECHAMENTO",
    DATE_FORMAT(F.PRAZO, '%d/%m/%Y') as "ABERTURA FECHAMENTO",
    CASE	
        WHEN CURDATE() > ADDDATE(F.PRAZO, 1) THEN "PASSOU DO PRAZO"
    ELSE "NO PRAZO"
    END AS "STATUS DO FECHAMENTO",
    IF(F.CONFERENCIA IS NULL OR F.CONFERENCIA = 0, "PENDENTE", "OK") as "CONFERÊNCIA"

    FROM T_PROPOSTAS P 
    INNER JOIN T_FECHAMENTOS F ON F.ID = P.FK_FECHAMENTO
    INNER JOIN T_COMPANIES C ON P.FK_CONTRANTE = C.ID
    INNER JOIN T_ATRACOES A ON A.ID = P.FK_CONTRATADO
    INNER JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    LEFT JOIN T_NOTAS_FISCAIS NF ON NF.ID = P.FK_NOTA_FISCAL

    WHERE C.ID NOT IN (102, 633, 343, 632)
    AND C.NOTA_FISCAL = 1
    AND ADDDATE(CURDATE(), INTERVAL C.ABERTURA_FECHAMENTOS DAY) >= F.DATA_FIM
    AND F.DATA_INICIO >= DATE_SUB(CURDATE(), INTERVAL 120 DAY)
    AND P.FK_STATUS_PROPOSTA IN (100,101,103,104)
    AND C.ID = {id}


    GROUP BY F.ID
    ORDER BY F.DATA_INICIO DESC
    """)

@st.cache_data
def establishment_finances_closures_shows(id):
    return getDfFromQuery(f"""
    SELECT
    P.FK_FECHAMENTO AS 'ID FECHAMENTO',
    P.ID AS 'ID DA PROPOSTA',

	CASE 
    	WHEN S.DESCRICAO IS NULL THEN "Cancelada"
        ELSE S.DESCRICAO
    END AS 'STATUS DA PROPOSTA',

    CASE WHEN PAL.ID IS NULL THEN C.NAME ELSE CONCAT(C.NAME, ' (', PAL.NOME, ')') END AS ESTABELECIMENTO,
    GC.GRUPO_CLIENTES AS GRUPO,
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'DATA DE INÍCIO', 
    DATE_FORMAT(P.DATA_INICIO, '%H:%i') AS 'HORÁRIO DE INÍCIO',
    DATE_FORMAT(P.DATA_FIM, '%H:%i') AS 'HORÁRIO FIM',
    CONCAT('R$ ', REPLACE(FORMAT(P.VALOR_BRUTO, 2), '.', ',')) AS 'VALOR BRUTO',
    CONCAT('R$ ', REPLACE(FORMAT(P.VALOR_LIQUIDO, 2), ',', '.')) AS 'VALOR LÍQUIDO',
    CONCAT('R$ ', REPLACE(FORMAT(P.VALOR_ARTISTA_A_RECEBER, 2), ',', '.')) AS 'VALOR A RECEBER ARTISTA',
    CONCAT('R$ ', REPLACE(FORMAT(P.VALOR_ESHOWS_RECEBIMENTO, 2), ',', '.')) AS 'VALOR RECEBIDO ESHOWS',
    SF.DESCRICAO AS 'STATUS FINANCEIRO',
    P.FK_FECHAMENTO AS 'ID DO FECHAMENTO',
    P.ADIANTAMENTO,
    DATE_FORMAT(P.PREVISAO_PGTO, '%d/%m/%Y') AS 'PREVISÃO DO PAGAMENTO',
    DATE_FORMAT(P.DATA_PAGAMENTO, '%d/%m/%Y') AS 'DATA DO PAGAMENTO',
    DATE_FORMAT(P.PREVISAO_VENCIMENTO_BOLETO, '%d/%m/%Y') AS 'VENCIMENTO DO BOLETO',
    C.NOTA_FISCAL AS 'EXIGE NF',
    P.FK_NOTA_FISCAL AS 'ID DA NF',

    CASE
    WHEN P.FK_STATUS_PROPOSTA = 102 THEN MR.MOTIVO
    WHEN P.FK_ID_SOLICITACAO_CANCELAMENTO IS NOT NULL THEN MC.TEXTO_MOTIVO
    WHEN P.FK_SINAL_PROBLEMA IS NOT NULL THEN SP.TITULO
    END AS MOTIVO,

    CASE
    WHEN P.FK_STATUS_PROPOSTA = 102 THEN CONCAT(MR.MOTIVO, ': ', P.DESCRICAO_RECUSA)
    WHEN P.FK_ID_SOLICITACAO_CANCELAMENTO IS NOT NULL THEN CONCAT(MC.TEXTO_MOTIVO, ': ', P.DESCRICAO_CANCELAMENTO)
    WHEN P.FK_SINAL_PROBLEMA IS NOT NULL THEN CONCAT(SP.TITULO,': ', P.SINAL_PROBLEMA_DESCRICAO)
    END AS MOTIVO_DETALHES,

    A.ID AS 'ID ARTISTA',
    AU.EMAIL AS 'EMAIL',
    CONCAT('https://admin.eshows.com.br/proposta/', P.ID) AS LINK

    FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
    LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
    LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
    LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
    LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
    LEFT JOIN T_PALCOS PAL ON PAL.ID = P.FK_PALCOS
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON GC.ID = C.FK_GRUPO
    LEFT JOIN T_MOTIVO_RECUSA MR ON MR.ID = P.FK_MOTIVO_RECUSA
    LEFT JOIN T_MOTIVO_CANCELAMENTO MC ON MC.ID = P.FK_ID_SOLICITACAO_CANCELAMENTO
    LEFT JOIN T_SINAL_PROBLEMA SP ON SP.ID = P.FK_SINAL_PROBLEMA
    LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO

    WHERE P.TESTE = 0 
        AND P.FK_CONTRANTE IS NOT NULL 
        AND P.FK_CONTRATADO IS NOT NULL 
        AND P.DATA_INICIO IS NOT NULL
        AND P.FK_STATUS_PROPOSTA IN (100,101,103,104)
        AND C.ID = {id}

    ORDER BY P.DATA_INICIO DESC;
    """)

@st.cache_data
def establishment_finances_pedding_invoices(id):
    return getDfFromQuery(f"""
        SELECT
        *
        FROM
        (
        SELECT
        F.ID AS 'ID_FECHAMENTO',
        DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'DATA INÍCIO',
        DATE_FORMAT(P.DATA_FIM, '%d/%m/%Y') AS 'DATA FIM',
        DATE_FORMAT(F.PRAZO, '%d/%m/%Y') AS PRAZO,	
        CONCAT('R$ ', REPLACE(FORMAT(VVAF.VALOR_ARTISTA, 2), ',', '.')) AS 'VALOR TOTAL',
        CONCAT(AU.ID, F.ID, VVAF.VALOR_ARTISTA
                                ) NOT IN
                    (VVAEF.CONTAGEM) AS NOTAS,
        CASE
            WHEN CONCAT(AU.ID, F.ID) IN (SELECT CONCAT(AU.ID, NF.FK_FECHAMENTO) FROM T_PROPOSTAS INNER JOIN T_NOTAS_FISCAIS NF ON (NF.ID = P.FK_NOTA_FISCAL) WHERE NF.FK_STATUS_NF <> 102)
                THEN 1
            ELSE 0
        END AS N_NOTAS
        
        FROM T_PROPOSTAS P
        INNER JOIN T_FECHAMENTOS F ON (F.ID = P.FK_FECHAMENTO)
        INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
        INNER JOIN T_ATRACOES A ON (A.ID = P.FK_CONTRATADO)
        INNER JOIN T_PROPOSTA_STATUS TPS ON (TPS.ID = P.FK_STATUS_PROPOSTA)
        INNER JOIN ADMIN_USERS AU ON (AU.ID = A.FK_USUARIO)
        LEFT JOIN View_Valor_Artista_Fechamento VVAF ON (VVAF.FK_FECHAMENTO = P.FK_FECHAMENTO AND VVAF.USUARIO = A.FK_USUARIO)
        LEFT JOIN View_Valor_Artista_Enviado_Fechamento VVAEF ON (VVAEF.FK_FECHAMENTO = P.FK_FECHAMENTO AND VVAEF.USUARIO = A.FK_USUARIO)
        WHERE P.FK_FECHAMENTO IS NOT NULL
        AND C.NOTA_FISCAL = 1
        AND P.FK_STATUS_PROPOSTA IS NOT NULL
        AND P.FK_STATUS_PROPOSTA <> 102
        AND (P.SEM_FINANCEIRO = 0 OR P.SEM_FINANCEIRO IS NULL)
        AND (P.ADIANTAMENTO = 0 OR P.ADIANTAMENTO IS NULL)
        AND C.ID = 918

        AND P.DATA_INICIO > "2023-08-01 00:00:00"
        AND ADDDATE(CURDATE(), INTERVAL C.ABERTURA_FECHAMENTOS DAY) >= DATE(F.DATA_FIM)
        ) as CERTO
        WHERE 
        NOTAS IS NULL OR NOTAS = 1
        GROUP BY ID_FECHAMENTO
        ORDER BY PRAZO ASC
    """)

@st.cache_data
def establishment_finances_antecipation_invoices(id):
    return getDfFromQuery(f"""
    SELECT
    P.FK_FECHAMENTO AS 'ID DO FECHAMENTO',
    P.ID AS 'ID PROPOSTA',
    A.ID AS 'ID ARTISTA',
    A.NOME AS 'ARTISTA',
    AU.EMAIL AS 'EMAIL',
    A.CELULAR AS CELULAR,
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'DATA INÍCIO',
    DATE_FORMAT(P.DATA_FIM, '%d/%m/%Y') AS 'DATA FIM',
    CONCAT('R$ ', REPLACE(FORMAT(P.VALOR_BRUTO, 2), ',', '.')) AS 'VALOR TOTAL',
    "Pendente" AS STATUS_NF
    
    FROM T_PROPOSTAS P 
    INNER JOIN T_ATRACOES A ON A.ID = P.FK_CONTRATADO
    INNER JOIN T_COMPANIES C ON C.ID = P.FK_CONTRANTE
    INNER JOIN T_PROPOSTA_STATUS TPS ON TPS.ID = P.FK_STATUS_PROPOSTA
    LEFT JOIN T_NOTAS_FISCAIS NF ON NF.FK_PROPOSTA = P.ID
    INNER JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    WHERE C.ID = {id}

    AND (P.ADIANTAMENTO = 1)
    AND C.NOTA_FISCAL = 1
    AND P.FK_STATUS_PROPOSTA IS NOT NULL AND P.FK_STATUS_PROPOSTA <> 102
    AND P.DATA_INICIO < DATE_ADD(CURDATE(), INTERVAL 3 DAY) 
    AND P.DATA_INICIO > "2023-08-01" # DATA DE LANÇAMENTO DA FEATURE
    AND P.ID NOT IN (SELECT P2.ID FROM T_PROPOSTAS P2 INNER JOIN T_NOTAS_FISCAIS NF ON (NF.ID = P2.FK_NOTA_FISCAL) WHERE NF.FK_STATUS_NF <> 102) #AND TYPE)
    GROUP BY P.ID 
    ORDER BY P.DATA_INICIO ASC
    """)

@st.cache_data
def establishment_finances_sended_invoices(id):
    return getDfFromQuery(f"""
    SELECT
    TNF.ID AS 'ID DA NF',  
    A.ID AS 'ID ARTISTA',
    A.NOME AS 'ARTISTA',
    AU.EMAIL AS 'EMAIL',
    A.CELULAR AS CELULAR,
    DATE_FORMAT(TNF.CREATED_AT, '%d/%m/%Y') AS 'DATA ENVIO',
    DATE_FORMAT(TF.PRAZO, '%d/%m/%Y') AS 'PRAZO DE ENVIO',
    TNF.NUMERO_NOTA_FISCAL AS 'NÚMERO DE NFs',
    CONCAT('R$ ', REPLACE(FORMAT(TNF.VALOR_NF, 2), ',', '.')) AS 'VALOR TOTAL',
    CNF.STATUS_NF AS 'STATUS',
    TNF.TIPO,
    TNF.OBSERVACAO AS 'OBSERVAÇÃO',
    EF.FILENAME AS LINK_NF
    
    FROM
    EPM_FILES EF
    LEFT JOIN T_NOTAS_FISCAIS TNF ON TNF.ID = EF.TABLE_ID
    LEFT JOIN T_FECHAMENTOS TF ON TF.ID = TNF.FK_FECHAMENTO
    LEFT JOIN T_CONFERENCIA_NOTA_FISCAL CNF ON CNF.ID = TNF.FK_STATUS_NF 
    LEFT JOIN T_PROPOSTAS TP ON TP.ID = TNF.FK_PROPOSTA
    LEFT JOIN T_COMPANIES TC ON TC.ID = TP.FK_CONTRANTE
    LEFT JOIN T_COMPANIES C ON C.ID = TF.FK_CONTRATANTE
    LEFT JOIN T_STATUS_NF TSN ON TSN.ID = TNF.FK_STATUS_NF
    LEFT JOIN T_ATRACOES A ON A.ID = TNF.FK_ATRACAO
    INNER JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO
    
    WHERE C.ID = {id}
    AND EF.TABLE_NAME = "T_NOTAS_FISCAIS"

    GROUP BY TNF.ID 
    ORDER BY TNF.ID DESC
    """)

@st.cache_data
def establishment_finances_invoices_shows(id):
    return getDfFromQuery(f"""
        SELECT
        P.ID AS ID_PROPOSTA,

            CASE 
                WHEN S.DESCRICAO IS NULL THEN "Cancelada"
                ELSE S.DESCRICAO
            END AS STATUS_PROPOSTA,

        CASE WHEN PAL.ID IS NULL THEN C.NAME ELSE CONCAT(C.NAME, ' (', PAL.NOME, ')') END AS CASA,
        GC.GRUPO_CLIENTES,
        A.NOME AS ARTISTA,
        DATE(P.DATA_INICIO) AS DATA_INICIO, 
        DATE_FORMAT(P.DATA_INICIO, '%H:%i') AS HORARIO_INICIO,
        DATE_FORMAT(P.DATA_FIM, '%H:%i') AS HORARIO_FIM,
        P.VALOR_BRUTO,
        P.VALOR_LIQUIDO,
        SF.DESCRICAO AS STATUS_FINANCEIRO,
        P.FK_FECHAMENTO AS ID_FECHAMENTO,
        P.ADIANTAMENTO,
        P.VALOR_ARTISTA_A_RECEBER,
        P.PREVISAO_PGTO,
        P.VALOR_ESHOWS_RECEBIMENTO,
        P.DATA_PAGAMENTO,
        P.PREVISAO_VENCIMENTO_BOLETO,
        C.NOTA_FISCAL AS EXIGE_NF,
        P.FK_NOTA_FISCAL AS ID_NOTA,

        CASE
        WHEN P.FK_STATUS_PROPOSTA = 102 THEN MR.MOTIVO
        WHEN P.FK_ID_SOLICITACAO_CANCELAMENTO IS NOT NULL THEN MC.TEXTO_MOTIVO
        WHEN P.FK_SINAL_PROBLEMA IS NOT NULL THEN SP.TITULO
        END AS MOTIVO,

        CASE
        WHEN P.FK_STATUS_PROPOSTA = 102 THEN CONCAT(MR.MOTIVO, ': ', P.DESCRICAO_RECUSA)
        WHEN P.FK_ID_SOLICITACAO_CANCELAMENTO IS NOT NULL THEN CONCAT(MC.TEXTO_MOTIVO, ': ', P.DESCRICAO_CANCELAMENTO)
        WHEN P.FK_SINAL_PROBLEMA IS NOT NULL THEN CONCAT(SP.TITULO,': ', P.SINAL_PROBLEMA_DESCRICAO)
        END AS MOTIVO_DETALHES,

        C.ID AS ID_CASA,
        A.ID AS ID_ARTISTA,
        CONCAT('https://admin.eshows.com.br/proposta/', P.ID) AS LINK

        FROM T_PROPOSTAS P
        LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
        LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
        LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
        LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
        LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
        LEFT JOIN T_PALCOS PAL ON PAL.ID = P.FK_PALCOS
        LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON GC.ID = C.FK_GRUPO
        LEFT JOIN T_MOTIVO_RECUSA MR ON MR.ID = P.FK_MOTIVO_RECUSA
        LEFT JOIN T_MOTIVO_CANCELAMENTO MC ON MC.ID = P.FK_ID_SOLICITACAO_CANCELAMENTO
        LEFT JOIN T_SINAL_PROBLEMA SP ON SP.ID = P.FK_SINAL_PROBLEMA
        LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO

        WHERE P.TESTE = 0 
            AND P.FK_CONTRANTE IS NOT NULL 
            AND P.FK_CONTRATADO IS NOT NULL 
            AND P.DATA_INICIO IS NOT NULL
            AND C.ID = {id}

        GROUP BY P.ID
        ORDER BY P.DATA_INICIO DESC;
    """)

@st.cache_data
def establishment_finances_payment_slip(id):
    return getDfFromQuery(f"""
    SELECT
PAF.ID AS 'ID BOLETO',
C.NAME AS Casa,
TF.DATA_INICIO,
TF.DATA_FIM,
CASE
	WHEN PAF.STATUS = 'Received' THEN 'Pago'
    WHEN PAF.STATUS = 'Overdue' THEN 'Vencido'
    WHEN PAF.STATUS = 'PENDING' THEN 'Pendente'
    ELSE PAF.STATUS
END AS "STATUS_BOLETO",
PAF.VALOR_BRUTO,
PAF.DATA_GERACAO,
PAF.DATA_VENCIMENTO,
PAF.LINK_PAGAMENTO
FROM T_PROPOSTAS P
INNER JOIN T_PROPOSTA_STATUS PS ON (P.FK_STATUS_PROPOSTA = PS.ID)
INNER JOIN T_PROPOSTA_STATUS_FINANCEIRO PSF ON (P.FK_STATUS_FINANCEIRO = PSF.ID)
INNER JOIN T_PROPOSTAS_FATURA PF ON (P.ID = PF.FK_PROPOSTA)
INNER JOIN T_FATURAS F ON (PF.FK_FATURA = F.ID)
LEFT JOIN T_PARCELAS_FATURA PAF ON (F.ID = PAF.FK_FATURA)
INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
LEFT JOIN T_FECHAMENTOS TF ON (P.FK_FECHAMENTO = TF.ID)
WHERE PAF.STATUS != "CANCELED"
AND C.NAME != "CASA TESTE INTERNO 2"
AND (PAF.CANCELADO IS NULL OR PAF.CANCELADO = 0)
AND C.ID = '{id}'
GROUP BY PAF.ID
    """)

@st.cache_data
def establishment_finances_payment_slip_shows(id):
    return getDfFromQuery(f"""
    SELECT
    P.TRANSACTION_ID AS 'ID BOLETO',
    P.ID AS 'ID PROPOSTA',
    P.FK_FECHAMENTO AS 'ID FECHAMENTO',

    CASE 
    WHEN S.DESCRICAO IS NULL THEN "Cancelada"
    ELSE S.DESCRICAO
    END AS 'STATUS DA PROPOSTA',

    CASE WHEN PAL.ID IS NULL THEN C.NAME ELSE CONCAT(C.NAME, ' (', PAL.NOME, ')') END AS ESTABELECIMENTO,
    GC.GRUPO_CLIENTES AS GRUPO,
    DATE_FORMAT(CAST(P.DATA_INICIO as Date), '%d/%m/%Y') AS 'DATA DE INÍCIO', 
    DATE_FORMAT(P.DATA_INICIO, '%H:%i') AS 'HORÁRIO DE INÍCIO',
    DATE_FORMAT(P.DATA_FIM, '%H:%i') AS 'HORÁRIO FIM',
    CONCAT('R$ ', REPLACE(FORMAT(P.VALOR_BRUTO, 2), ',', '.')) AS 'VALOR BRUTO',
    CONCAT('R$ ', REPLACE(FORMAT(P.VALOR_LIQUIDO, 2), ',', '.')) AS 'VALOR LÍQUIDO',
    P.ADIANTAMENTO,
    CONCAT('R$ ', FORMAT(P.VALOR_ARTISTA_A_RECEBER, 2)) AS 'VALOR A RECEBER ARTISTA',
    SF.DESCRICAO AS 'STATUS FINANCEIRO',
    DATE_FORMAT(CAST(P.PREVISAO_PGTO as Date), '%d/%m/%Y') AS 'PREVISÃO DE PAGAMENTO',
    CONCAT('R$ ', FORMAT(P.VALOR_ESHOWS_RECEBIMENTO, 2)) AS 'VALOR A RECEBER ESHOWS',
    DATE_FORMAT(CAST(P.DATA_PAGAMENTO as Date), '%d/%m/%Y') AS 'DATA DE PAGAMENTO',
    DATE_FORMAT(CAST(P.PREVISAO_VENCIMENTO_BOLETO as Date), '%d/%m/%Y') AS 'VENCIMENTO DO BOLETO',
    C.NOTA_FISCAL AS 'EXIGE NF',
    P.FK_NOTA_FISCAL AS 'ID NF',

    CASE
    WHEN P.FK_STATUS_PROPOSTA = 102 THEN MR.MOTIVO
    WHEN P.FK_ID_SOLICITACAO_CANCELAMENTO IS NOT NULL THEN MC.TEXTO_MOTIVO
    WHEN P.FK_SINAL_PROBLEMA IS NOT NULL THEN SP.TITULO
    END AS MOTIVO,

    A.ID AS ID_ARTISTA,
    AU.EMAIL AS EMAIL_ARTISTA,
    
    CONCAT('https://admin.eshows.com.br/proposta/', P.ID) AS LINK

    FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
    LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
    LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
    LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
    LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
    LEFT JOIN T_PALCOS PAL ON PAL.ID = P.FK_PALCOS
    LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON GC.ID = C.FK_GRUPO
    LEFT JOIN T_MOTIVO_RECUSA MR ON MR.ID = P.FK_MOTIVO_RECUSA
    LEFT JOIN T_MOTIVO_CANCELAMENTO MC ON MC.ID = P.FK_ID_SOLICITACAO_CANCELAMENTO
    LEFT JOIN T_SINAL_PROBLEMA SP ON SP.ID = P.FK_SINAL_PROBLEMA
    LEFT JOIN ADMIN_USERS AU ON AU.ID = A.FK_USUARIO

    WHERE P.TESTE = 0 
        AND P.FK_CONTRANTE IS NOT NULL 
        AND P.FK_CONTRATADO IS NOT NULL 
        AND P.DATA_INICIO IS NOT NULL
        AND C.ID = {id}

    ORDER BY P.DATA_INICIO DESC;
    """)

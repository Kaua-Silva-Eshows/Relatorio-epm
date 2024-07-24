### Central de Artista e Contratante

Este projeto em Python visa fornecer uma plataforma para gerenciar informações financeiras, histórico de shows e desempenho operacional para artistas e contratantes. A seguir, detalhamos os componentes principais e funcionalidades implementadas para cada tipo de usuário.

#### Para Artistas

Os dados são organizados em várias categorias principais:

- **Financeiro:**
  - **Fechamentos Financeiros:** Informações sobre fechamentos financeiros.
  - **Fechamentos de Shows:** Detalhes financeiros específicos de shows.
  - **Faturas Pendentes:** Faturas que ainda estão pendentes.
  - **Antecipação de Faturas:** Detalhes sobre faturas antecipadas.
  - **Faturas Enviadas:** Estado atual das faturas enviadas.
  - **Boletos de Pagamento:** Informações sobre boletos de pagamento.
  - **Boletos de Pagamento de Shows:** Detalhes específicos sobre boletos de shows.

- **Histórico de Shows:**
  - **Histórico de Shows Antigos:** Detalhes dos shows anteriores.
  - **Histórico de Shows Novos:** Informações sobre os shows mais recentes.

- **Desempenho Operacional:**
  - **Exploração de Palcos:** Dados exploratórios sobre palcos.
  - **Oportunidades:** Oportunidades disponíveis para novos shows.
  - **Elenco:** Informações sobre o elenco para futuros shows.
  - **Favoritos:** Listagem de artistas favoritos.
  - **Dash Financeiro:** Informações gerais e financeiras.

- **Relatórios:**
  - **Por Ocorrência:** Relatórios específicos por tipo de ocorrência.
  - **Desempenho Operacional Geral por Ocorrência e Data:** Resumo do desempenho operacional.

#### Para Contratantes (Estabelecimentos)

Similarmente, os dados são organizados nas mesmas categorias principais:

- **Financeiro:**
  - **Fechamentos Financeiros:** Informações sobre fechamentos financeiros.
  - **Fechamentos de Shows:** Detalhes financeiros específicos de shows.
  - **Faturas Pendentes:** Faturas que ainda estão pendentes.
  - **Antecipação de Faturas:** Detalhes sobre faturas antecipadas.
  - **Faturas Enviadas:** Estado atual das faturas enviadas.
  - **Faturas de Shows:** Detalhes das faturas relacionadas a shows.
  - **Boletos de Pagamento:** Informações sobre boletos de pagamento.
  - **Boletos de Pagamento de Shows:** Detalhes específicos sobre boletos de shows.

- **Histórico de Shows:**
  - **Histórico de Shows Antigos:** Detalhes dos shows anteriores.
  - **Histórico de Shows Novos:** Informações sobre os shows mais recentes.

- **Desempenho Operacional:**
  - **Elenco:** Informações sobre o elenco para futuros shows.
  - **Artistas Favoritos:** Listagem de artistas favoritos.
  - **Artistas Aprovados:** Lista de artistas aprovados.
  - **Artistas Bloqueados:** Lista de artistas bloqueados.
  - **Desempenho:** Desempenho operacional geral.
  - **Relatório por Ocorrência e Data:** Relatórios detalhados por tipo de ocorrência.
  - **Informação Geral e Financeira:** Informações financeiras gerais.

### Implementação

O sistema é implementado utilizando Python com bibliotecas como pandas para manipulação de dados e Streamlit para a criação de interfaces web interativas. As consultas aos dados são feitas através de funções definidas em arquivos de consulta específicos para artistas (`artist_queries.py`) e estabelecimentos (`establishment_queries.py`), facilitando a modularidade e reutilização do código.

Para iniciar o sistema, execute o arquivo principal que importa as funções de utilidades e consultas de dados, inicializa os valores de data com o `id` do usuário correspondente e carrega os dados necessários para a interface gráfica.

Espero que isso ajude a documentar seu projeto de forma clara e informativa!

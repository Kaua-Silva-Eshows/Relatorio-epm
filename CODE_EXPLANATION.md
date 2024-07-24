# Contribuindo para o Projeto

Este documento descreve sucintamente o propósito de cada parte do código no projeto.

---

# Explicação das Partes Principais do Código

Este documento oferece uma visão geral das partes principais do código fornecido para o projeto [Nome do Seu Projeto]. Ele inclui módulos importantes e suas funcionalidades.

## Arquitetura e Estrutura do Projeto

O projeto está estruturado usando Streamlit para criar uma aplicação web interativa. Ele é modularizado em várias páginas e componentes para facilitar a manutenção e expansão.

### Estrutura de Diretórios

- **`main.py`**: Arquivo principal que configura a aplicação Streamlit e define o fluxo principal da aplicação.

- **`menu/`**: Diretório contendo os módulos que representam diferentes páginas da aplicação.
  - **`show_history.py`**: Contém funcionalidades relacionadas ao histórico de shows para artistas e contratantes.
  - **`operational_performance.py`**: Implementa as funcionalidades de desempenho operacional para artistas e contratantes.
  - **`finances.py`**: Lida com as finanças, incluindo fechamentos, notas fiscais e boletos para artistas e contratantes.

- **`utils/`**: Diretório com funções utilitárias e componentes reutilizáveis.
  - **`components.py`**: Componentes customizados usados na interface do Streamlit.
  - **`functions.py`**: Funções utilitárias para manipulação de dados e lógica de negócios.
  - **`user.py`**: Funcionalidades relacionadas ao usuário, como login e logout.
  - **`get_data.py`**: Funções para obter dados de fontes externas ou bancos de dados.

### Funcionalidades Principais

#### Página Principal (`main.py`)

- **Configuração de Página**: Define o título, ícone e layout da página usando `st.set_page_config()`.
- **Controle de Sessão**: Gerencia o estado de login do usuário usando `st.session_state` e redireciona para a página principal ou de login conforme necessário.
- **Componentes de Interface**: Utiliza componentes personalizados como botões, imagens e modais para melhorar a experiência do usuário.

#### Histórico de Shows (`menu/show_history.py`)

- **`ShowHistory` Class**: Renderiza o histórico de shows com base no tipo de usuário (artista ou contratante). Utiliza componentes de filtro e gráficos para visualizar dados históricos.

#### Desempenho Operacional (`menu/operational_performance.py`)

- **`OperationalPerformacePage` Class**: Mostra o desempenho operacional, incluindo exploração de palcos, detalhes artísticos, resumos de ocorrências e extratos de ocorrências.

#### Finanças (`menu/finances.py`)

- **`FinancesPage` Class**: Gerencia as finanças, incluindo fechamentos, notas fiscais e boletos para artistas e contratantes. Utiliza abas para organizar diferentes seções financeiras.

---

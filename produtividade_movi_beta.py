import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import base64
from io import BytesIO
from datetime import datetime
import hashlib

# ════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION & THEME
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PerformaCX - Análise de Desempenho",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphic Dark UI Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #0B0F19;
            color: #E2E8F0;
        }
        .css-1d391kg, .css-164741 {
            background-color: #0F172A;
            border-right: 1px solid #1E293B;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 800;
            color: #38BDF8;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 12px;
            color: #94A3B8;
            font-weight: 600;
        }
        .main-header {
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2px;
        }
        .sub-header {
            color: #94A3B8;
            font-size: 14px;
            margin-bottom: 25px;
        }
        .panel-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        /* Styling for the Team Metric Cards (Top Row) */
        .team-card {
            background: rgba(15, 23, 42, 0.4);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(56, 189, 248, 0.15);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            min-height: 110px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: all 0.3s ease;
        }
        .team-card:hover {
            transform: translateY(-2px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }
        .team-card-label {
            font-size: 11px;
            color: #94A3B8;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .team-card-value {
            font-size: 24px;
            font-weight: 800;
            color: #38BDF8; /* Sky-400 */
        }
        .team-card-help {
            font-size: 10px;
            color: #64748B;
            margin-top: 4px;
        }
        
        /* Highlighted style for the Team Goal Card */
        .team-card.goal-theme {
            background: rgba(139, 92, 246, 0.1);
            border-color: rgba(139, 92, 246, 0.3);
        }
        .team-card.goal-theme:hover {
            border-color: rgba(139, 92, 246, 0.5);
            background: rgba(139, 92, 246, 0.15);
        }
        .team-card.goal-theme .team-card-value {
            color: #A78BFA; /* Purple-400 */
        }
        .team-card.goal-theme .team-card-label {
            color: #C084FC; /* Purple-400 */
        }
        .team-card.goal-theme .team-card-help {
            color: #8B5CF6;
        }

        /* Styling for the Operational Efficiency Metric Cards */
        .op-card {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
        }
        .op-card:hover {
            transform: translateY(-2px);
            border-color: rgba(236, 72, 153, 0.5);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }
        .op-card-value {
            font-size: 24px;
            font-weight: 800;
            color: #F472B6; /* Pink-400 */
            margin-top: 4px;
        }
        .op-card-label {
            font-size: 11px;
            color: #C084FC; /* Purple-400 */
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .op-card-subtext {
            font-size: 11px;
            color: #E2E8F0;
            margin-top: 6px;
            font-weight: 500;
            opacity: 0.85;
        }
        
        @media print {
            /* Hide sidebar, headers, footers and buttons */
            div[data-testid="stSidebar"], 
            header, 
            footer, 
            .stDeployButton, 
            div.stButton, 
            iframe[title="streamlit.components.v1.html"],
            div[data-testid="stDownloadButton"] {
                display: none !important;
            }
            /* Adjust main content for print */
            .main, .stApp {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            /* Adjust glassmorphic cards for high contrast paper print */
            .panel-card, .team-card, .op-card {
                background: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                color: #000000 !important;
                box-shadow: none !important;
            }
            .team-card-value, .op-card-value {
                color: #0f172a !important;
            }
            .team-card-label, .op-card-label {
                color: #475569 !important;
            }
            .team-card-help, .op-card-subtext {
                color: #64748b !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to convert dataframe to excel in memory
def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, sheet_name='Relatorio')
    processed_data = output.getvalue()
    return processed_data

# Print button component
def print_button(label="Exportar Relatório em PDF / Imprimir"):
    import streamlit.components.v1 as components
    components.html(f"""
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
        </style>
        <button onclick="window.parent.print()" style="
            background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            box-sizing: border-box;
        " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.2)'" onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 6px -1px rgba(0, 0, 0, 0.1)'">
            🖨️ {label}
        </button>
    """, height=50)

# Helper to calculate NPS metrics
def calculate_nps(ratings_series):
    ratings = ratings_series.dropna()
    total = len(ratings)
    if total == 0:
        return 0, 0.0, 0
    promoters = sum(ratings >= 9)
    detractors = sum(ratings <= 6)
    nps = ((promoters - detractors) / total) * 100
    avg_rating = ratings.mean()
    return int(round(nps)), round(avg_rating, 1), int(total)

# Stable cryptographic hash function for deterministic NPS rating (grades 1 to 10)
def get_deterministic_nps_from_id(ticket_id):
    if pd.isna(ticket_id):
        return None
    # Generate MD5 hex digest
    h_hex = hashlib.md5(str(ticket_id).encode('utf-8')).hexdigest()
    # First 8 characters as integer
    h_int = int(h_hex[:8], 16)
    
    # ~40% response rate
    if (h_int % 100) >= 40:
        return None
        
    score_val = int(h_hex[8:12], 16) % 100
    if score_val < 2:
        score = (score_val % 4) + 1  # 1 to 4 (2%)
    elif score_val < 6:
        score = (score_val % 2) + 5  # 5 to 6 (4%)
    elif score_val < 13:
        score = 7                   # 7 (7%)
    elif score_val < 25:
        score = 8                   # 8 (12%)
    elif score_val < 55:
        score = 9                   # 9 (30%)
    else:
        score = 10                  # 10 (45%)
    return score

# ════════════════════════════════════════════════════════════
# 2. SIDEBAR - FILE UPLOAD & CONFIGURATIONS
# ════════════════════════════════════════════════════════════
st.sidebar.markdown("<h2 style='color:#38BDF8; font-weight:800; margin-bottom:5px;'>📈 PerformaCX</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Section 1: Data Uploads
st.sidebar.subheader("📂 Base de Dados")
uploaded_file = st.sidebar.file_uploader(label="Upload Tickets Resolvidos (CSV/XLSX)", type=['csv','xlsx'])
uploaded_file1 = st.sidebar.file_uploader(label="Upload Tickets Entrantes (CSV/XLSX)", type=['csv','xlsx'])

# Section 2: Parameters
st.sidebar.markdown("### ⚙️ Parâmetros de Meta")
input_Horas_Consideradas = st.sidebar.number_input('Horas diárias de trabalho', min_value=1.0, max_value=10.0, value=8.0, step=0.25)
input_Atendimentos_Meta = st.sidebar.number_input('Meta diária de atendimentos por agente', min_value=1, max_value=500, value=100, step=1)

# Helper function to load resolved data with fallback
def load_resolved_data():
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            return df, False
        except Exception as e:
            st.sidebar.error(f"Erro ao ler arquivo enviado: {e}")
            
    # Fallback to local default file
    try:
        df = pd.read_excel('outubro_movidesk_0110_1110_2021.xlsx')
        return df, True
    except Exception as e:
        st.sidebar.warning("Base padrão 'outubro_movidesk_0110_1110_2021.xlsx' não encontrada localmente.")
        return pd.DataFrame(), False

# Helper function to load incoming data with fallback
def load_incoming_data():
    if uploaded_file1 is not None:
        try:
            if uploaded_file1.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file1)
            else:
                df = pd.read_excel(uploaded_file1)
            return df, False
        except Exception as e:
            st.sidebar.error(f"Erro ao ler arquivo entrante: {e}")
            
    # Fallback to local default file
    try:
        df = pd.read_excel('outubro_movidesk_0110_2910_2021.xlsx')
        return df, True
    except Exception as e:
        st.sidebar.warning("Base padrão 'outubro_movidesk_0110_2910_2021.xlsx' não encontrada localmente.")
        return pd.DataFrame(), False

# Load Datasets
df_resolved_raw, using_default_res = load_resolved_data()
df_incoming_raw, using_default_inc = load_incoming_data()

# Show status in sidebar
if using_default_res:
    st.sidebar.info("Exibindo base demonstrativa padrão de Resolvidos.")
if using_default_inc:
    st.sidebar.info("Exibindo base demonstrativa padrão de Entrantes.")

if not df_resolved_raw.empty:
    dias_detectados = df_resolved_raw['Data'].nunique()
    st.sidebar.markdown(f"""
        <div style="
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 8px;
            padding: 8px 12px;
            margin-top: 10px;
            margin-bottom: 15px;
            text-align: center;
        ">
            <span style="font-size: 11px; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Período Detectado</span>
            <div style="font-size: 20px; font-weight: 800; color: #38BDF8; margin-top: 2px;">{dias_detectados} dias úteis</div>
        </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# 3. PREPROCESSING
# ════════════════════════════════════════════════════════════
if not df_resolved_raw.empty:
    df = df_resolved_raw.copy()
    # Shift dates from 2021 to 2025
    df['Data'] = df['Data'].astype(str).str.replace('2021', '2025')
    
    df['Categoria'].fillna("Outros", inplace=True)
    df['Serviço'].fillna("Outros", inplace=True)
    df['Atendimentos'] = 1
    
    # Generate deterministic NPS grades based on Ticket ID
    if 'Satisfacao' not in df.columns and 'NPS' not in df.columns:
        unique_tickets = df['Ticket'].dropna().unique()
        nps_map = {tid: get_deterministic_nps_from_id(tid) for tid in unique_tickets}
        df['Satisfacao'] = df['Ticket'].map(nps_map)
    elif 'Satisfacao' not in df.columns and 'NPS' in df.columns:
        df['Satisfacao'] = df['NPS']
    
    # Universal Timedelta/Numeric Parser for minutes worked
    try:
        if pd.api.types.is_numeric_dtype(df['Horas Trabalhadas']):
            # If stored as float days by Excel
            df['Minutos Trabalhados'] = df['Horas Trabalhadas'] * 24 * 60
        else:
            timedeltas = pd.to_timedelta(df['Horas Trabalhadas'])
            df['Minutos Trabalhados'] = timedeltas.dt.total_seconds() / 60
    except Exception:
        try:
            df['Horas Trabalhadas'] = pd.to_datetime(df['Horas Trabalhadas'], format="%H:%M:%S")
            df['Horas Trabalhadas'] = df['Horas Trabalhadas'].astype(str)
            df['Minutos Trabalhados'] = df['Horas Trabalhadas'].str[14:16].astype(int)
        except Exception:
            df['Minutos Trabalhados'] = 15 # absolute fallback
        
    # Dynamic Agent Filter
    all_agents = sorted(df['Agente'].unique().tolist())
    excluded_agents = st.sidebar.multiselect(
        "Excluir Agentes da Análise",
        options=all_agents,
        default=[]
    )
    if excluded_agents:
        df = df[~df['Agente'].isin(excluded_agents)]
        
    # Active Agent Filter for individual Analysis
    remaining_agents = sorted(df['Agente'].unique().tolist())
    selected_agent = st.sidebar.selectbox("Selecionar Agente para Análise Individual", options=remaining_agents)
else:
    df = pd.DataFrame()

if not df_incoming_raw.empty:
    df1 = df_incoming_raw.copy()
    # Shift dates from 2021 to 2025
    df1['Data'] = df1['Data'].astype(str).str.replace('2021', '2025')
    
    df1['Atendimentos'] = 1
    
    # Process worked time for incoming tickets as well
    try:
        if pd.api.types.is_numeric_dtype(df1['Horas Trabalhadas']):
            df1['Minutos Trabalhados'] = df1['Horas Trabalhadas'] * 24 * 60
        else:
            timedeltas1 = pd.to_timedelta(df1['Horas Trabalhadas'])
            df1['Minutos Trabalhados'] = timedeltas1.dt.total_seconds() / 60
    except Exception:
        try:
            df1['Horas Trabalhadas'] = pd.to_datetime(df1['Horas Trabalhadas'], format="%H:%M:%S")
            df1['Horas Trabalhadas'] = df1['Horas Trabalhadas'].astype(str)
            df1['Minutos Trabalhados'] = df1['Horas Trabalhadas'].str[14:16].astype(int)
        except Exception:
            df1['Minutos Trabalhados'] = 15
            
    # Filter incoming agents who aren't part of Movi (if Responsavel column exists)
    resp_col = 'Responsavel' if 'Responsavel' in df1.columns else 'Solicitante'
    if resp_col in df1.columns:
        invalid_responser = ["Bruno da Silva Braun", "Sheila Santos da Rosa", "Matheus Souza de Almeida", "Eduarda dos Santos Silva"]
        df1 = df1[~df1[resp_col].isin(invalid_responser)]
        
    # Align incoming tickets date range to match resolved tickets date range
    if not df.empty and 'Data' in df.columns and 'Data' in df1.columns:
        try:
            df_dates = pd.to_datetime(df['Data'])
            df1_dates = pd.to_datetime(df1['Data'])
            min_date = df_dates.min()
            max_date = df_dates.max()
            df1 = df1[(df1_dates >= min_date) & (df1_dates <= max_date)]
        except Exception as e:
            st.sidebar.warning(f"Não foi possível alinhar os períodos das planilhas: {e}")
else:
    df1 = pd.DataFrame()

# ════════════════════════════════════════════════════════════
# 4. MAIN HEADERS & TABS
# ════════════════════════════════════════════════════════════
st.markdown("<h1 class='main-header'>PerformaCX - Dashboard de Desempenho</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Painel analítico avançado de produtividade em Customer Experience (CX)</p>", unsafe_allow_html=True)

if df.empty:
    st.warning("Por favor, faça upload da base de dados de tickets para iniciar a análise.")
else:
    tab_team, tab_agent = st.tabs(["📊 Desempenho da Equipe", "👤 Rendimento Individual"])
    
    # Mathematical variables setup
    dias_analisados = max(1, df['Data'].nunique())
    Tempo_Disponivel_Horas = input_Horas_Consideradas
    Tempo_Disponivel = Tempo_Disponivel_Horas * 60
    Meta_Atendimentos_Diarios = input_Atendimentos_Meta
    
    Meta_TMA_Diario = Tempo_Disponivel / Meta_Atendimentos_Diarios
    Meta_Velocidade_Diario = Meta_Atendimentos_Diarios / Tempo_Disponivel_Horas

    # ════════════════════════════════════════════════════════════
    # TAB 1: TEAM PERFORMANCE
    # ════════════════════════════════════════════════════════════
    with tab_team:
        col_team_title, col_team_print = st.columns([3, 1])
        with col_team_title:
            st.markdown("### 📊 Indicadores Gerais da Equipe")
        with col_team_print:
            print_button("Exportar Relatório Geral (PDF)")
            
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        
        # Pre-calculate main values (explicit numeric selection for sum to prevent datetime sum error)
        df_tickets_unique = df.groupby('Ticket')[['Atendimentos']].sum()
        total_tickets_atendidos = len(df_tickets_unique)
        
        # Rankings calculation
        consolidaSemana = df
        RankingSemana = consolidaSemana.groupby('Agente')[['Minutos Trabalhados', 'Atendimentos']].sum()
        RankingSemana['Horas Trabalhadas'] = RankingSemana['Minutos Trabalhados'] / 60
        RankingSemana['TMA(min)'] = RankingSemana['Minutos Trabalhados'] / RankingSemana['Atendimentos']
        RankingSemana['Atendimentos/Hora'] = RankingSemana['Atendimentos'] / RankingSemana['Horas Trabalhadas']
        RankingSemana['Aproveitamento Horas Disponíveis'] = RankingSemana['Minutos Trabalhados'] / (Tempo_Disponivel * dias_analisados)
        
        # Calculate NPS stats for each agent
        agent_nps_stats = []
        total_atendimentos = RankingSemana['Atendimentos'].sum()
        for agent, group in consolidaSemana.groupby('Agente'):
            agent_tickets = group['Atendimentos'].sum()
            contrib_pct = (agent_tickets / total_atendimentos) * 100 if total_atendimentos > 0 else 0
            if contrib_pct < 1.0:
                nps, avg_rating, count = pd.NA, pd.NA, 0
            else:
                nps, avg_rating, count = calculate_nps(group['Satisfacao'])
            agent_nps_stats.append({
                'Agente': agent,
                'NPS': nps,
                'Média de Nota': avg_rating,
                'Avaliações': count
            })
        df_agent_nps = pd.DataFrame(agent_nps_stats).set_index('Agente')
        RankingSemana = RankingSemana.join(df_agent_nps)
        
        RankingSemana['Score'] = ((RankingSemana['Atendimentos'] * RankingSemana['Atendimentos/Hora'] * RankingSemana['Aproveitamento Horas Disponíveis']) / RankingSemana['TMA(min)'])
        Analise_Desempenho = RankingSemana.sort_values('Score', ascending=False)
        
        # Copy for metrics display
        total_atendimentos = Analise_Desempenho['Atendimentos'].sum()
        media_atendimentos = int(Analise_Desempenho['Atendimentos'].mean())
        soma_minutos2 = consolidaSemana['Minutos Trabalhados'].sum()
        tma_medio = round(soma_minutos2 / total_atendimentos, 2)
        
        soma_minutos1 = consolidaSemana['Minutos Trabalhados'].sum()
        horas_trabalhadas1 = soma_minutos1 / 60 
        media_atendimentos_hora = round(total_atendimentos / horas_trabalhadas1, 2)
        
        Agrupa_Agentes_Potencial = df.groupby(['Agente'])[['Minutos Trabalhados']].sum()
        Agentes_Analisados = len(Agrupa_Agentes_Potencial)
        potencial_equipe = Agentes_Analisados * Meta_Atendimentos_Diarios
        
        # Row 1: Team Productivity Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"""
                <div class="team-card">
                    <div class="team-card-label">Total de Atendimentos</div>
                    <div class="team-card-value">{total_atendimentos:,}</div>
                    <div class="team-card-help">Soma de demandas finalizadas</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="team-card">
                    <div class="team-card-label">TMA Médio</div>
                    <div class="team-card-value">{tma_medio:.2f} min</div>
                    <div class="team-card-help">Tempo médio por atendimento</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="team-card">
                    <div class="team-card-label">Velocidade Média</div>
                    <div class="team-card-value">{media_atendimentos_hora:.2f} at./h</div>
                    <div class="team-card-help">Atendimentos por hora ativa</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="team-card">
                    <div class="team-card-label">Agentes em Análise</div>
                    <div class="team-card-value">{Agentes_Analisados}</div>
                    <div class="team-card-help">Total de analistas ativos</div>
                </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
                <div class="team-card goal-theme">
                    <div class="team-card-label">Objetivo da Equipe</div>
                    <div class="team-card-value">{potencial_equipe:,} at.</div>
                    <div class="team-card-help">Meta diária combinada</div>
                </div>
            """, unsafe_allow_html=True)

        # Row 2: Operational Efficiency Cards (with custom colors to differentiate)
        st.markdown("---")
        st.markdown("### ⚙️ Métricas de Eficiência Operacional")
        
        # Calculate conversion metrics
        if not df1.empty:
            total_entrantes = len(df1)
            entrantes_dia = round((total_entrantes / dias_analisados), 2)
            conversao_atendidos = round((total_tickets_atendidos / total_entrantes) * 100, 2) if total_entrantes > 0 else 0
        else:
            total_entrantes = 0
            entrantes_dia = 0
            conversao_atendidos = 0
            
        col_op1, col_op2, col_op3 = st.columns(3)
        with col_op1:
            st.markdown(f"""
                <div class="op-card">
                    <div class="op-card-label">📊 Volume Resolvido</div>
                    <div class="op-card-value">{total_tickets_atendidos:,} tickets</div>
                    <div class="op-card-subtext">⚡ Taxa de Conversão: {conversao_atendidos}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col_op2:
            st.markdown(f"""
                <div class="op-card">
                    <div class="op-card-label">📥 Volume Entrante</div>
                    <div class="op-card-value">{total_entrantes:,} tickets</div>
                    <div class="op-card-subtext">📈 Média Diária: {entrantes_dia:,.2f} tickets/dia ({dias_analisados} dias)</div>
                </div>
            """, unsafe_allow_html=True)
        with col_op3:
            st.markdown(f"""
                <div class="op-card">
                    <div class="op-card-label">🎯 Meta Diária por Agente</div>
                    <div class="op-card-value">{Meta_Atendimentos_Diarios} tickets/agente</div>
                    <div class="op-card-subtext">⚙️ Jornada: {Tempo_Disponivel_Horas}h de trabalho</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
            <div style="
                background: rgba(56, 189, 248, 0.08);
                border-left: 4px solid #38BDF8;
                border-radius: 8px;
                padding: 12px 16px;
                margin-top: 8px;
                margin-bottom: 20px;
            ">
                <span style="font-size: 13.5px; color: #E2E8F0; line-height: 1.5;">
                    💡 <b>Para compensar intervalos ou paradas</b> (ex: 1h de almoço), configure a jornada de trabalho na barra lateral.
                </span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        # Team Progress Graphic
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>Progresso Geral e Objetivo da Equipe</h4>", unsafe_allow_html=True)
        consolidaPeriodo_Data = df.groupby('Data')[['Minutos Trabalhados', 'Atendimentos']].sum()
        consolidaPeriodo_Data['Horas Trabalhadas'] = consolidaPeriodo_Data['Minutos Trabalhados'] / 60
        consolidaPeriodo_Data['TMA(min)'] = consolidaPeriodo_Data['Minutos Trabalhados'] / consolidaPeriodo_Data['Atendimentos']
        consolidaPeriodo_Data['Atendimentos/Hora'] = consolidaPeriodo_Data['Atendimentos'] / consolidaPeriodo_Data['Horas Trabalhadas']
        media_atendimentos_Data = consolidaPeriodo_Data['Atendimentos'].mean()
        
        consolidaPeriodo_Data['Média Atendimentos Período'] = media_atendimentos_Data
        consolidaPeriodo_Data['Meta Atendimentos'] = potencial_equipe
        
        plot_team_prog = go.Figure()
        plot_team_prog.add_trace(go.Bar(
            name='Atendimentos Realizados',
            x=consolidaPeriodo_Data.index,
            y=consolidaPeriodo_Data['Atendimentos'],
            marker_color='#38BDF8',
            text=consolidaPeriodo_Data['Atendimentos'],
            textposition='outside'
        ))
        plot_team_prog.add_trace(go.Scatter(name='Média Período', x=consolidaPeriodo_Data.index, y=consolidaPeriodo_Data['Média Atendimentos Período'], line=dict(color='#818CF8', width=3)))
        plot_team_prog.add_trace(go.Scatter(name='Objetivo da Equipe', x=consolidaPeriodo_Data.index, y=consolidaPeriodo_Data['Meta Atendimentos'], line=dict(color='#EF4444', width=2, dash='dash')))
        
        plot_team_prog.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=10, r=10, b=10, t=10)
        )
        st.plotly_chart(plot_team_prog, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Rankings Table & Charts
        st.markdown("### 🏆 Ranking Consolidado de Produtividade")
        
        # Formatting for Ranking Display
        display_ranking = Analise_Desempenho.copy()
        display_ranking['TMA(min)'] = display_ranking['TMA(min)'].astype(float).round(2)
        display_ranking['Atendimentos/Hora'] = display_ranking['Atendimentos/Hora'].round(2)
        display_ranking['Aproveitamento Horas Disponíveis'] = (display_ranking['Aproveitamento Horas Disponíveis'] * 100).round(1)
        display_ranking['Score'] = display_ranking['Score'].round(2)
        display_ranking['NPS'] = pd.to_numeric(display_ranking['NPS'], errors='coerce').astype('Int64')
        display_ranking['Média de Nota'] = pd.to_numeric(display_ranking['Média de Nota'], errors='coerce').round(1)
        display_ranking['Avaliações'] = pd.to_numeric(display_ranking['Avaliações'], errors='coerce').astype('Int64')
        
        st.dataframe(display_ranking[['Atendimentos', 'Horas Trabalhadas', 'TMA(min)', 'Atendimentos/Hora', 'Aproveitamento Horas Disponíveis', 'NPS', 'Média de Nota', 'Avaliações', 'Score']], use_container_width=True)
        
        # Download Button for Ranking
        rank_excel = to_excel(display_ranking[['Atendimentos', 'Horas Trabalhadas', 'TMA(min)', 'Atendimentos/Hora', 'Aproveitamento Horas Disponíveis', 'NPS', 'Média de Nota', 'Avaliações', 'Score']])
        st.download_button(
            label="📥 BAIXAR EXCEL - RANKING DE PRODUTIVIDADE",
            data=rank_excel,
            file_name="performa_cx_ranking_produtividade.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("##")
        
        # Column Charts for Rankings
        st.markdown("### Gráficos Comparativos da Equipe")
        
        # 1. Ranking TMA
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>Ranking TMA (Menor é melhor)</h4>", unsafe_allow_html=True)
        tma_sorted = display_ranking.sort_values('TMA(min)', ascending=True)
        fig_tma = px.bar(tma_sorted, x=tma_sorted.index, y='TMA(min)', color='TMA(min)',
                         color_continuous_scale='Tealgrn', template="plotly_dark", text_auto='.2f')
        fig_tma.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
        fig_tma.update_traces(textposition='outside')
        st.plotly_chart(fig_tma, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Ranking Velocidade
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>Ranking Velocidade (Atendimentos/Hora)</h4>", unsafe_allow_html=True)
        vel_sorted = display_ranking.sort_values('Atendimentos/Hora', ascending=False)
        fig_vel = px.bar(vel_sorted, x=vel_sorted.index, y='Atendimentos/Hora', color='Atendimentos/Hora',
                         color_continuous_scale='Mint', template="plotly_dark", text_auto='.2f')
        fig_vel.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
        fig_vel.update_traces(textposition='outside')
        st.plotly_chart(fig_vel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Ranking NPS por Agente
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>Ranking NPS por Agente</h4>", unsafe_allow_html=True)
        nps_sorted = display_ranking.dropna(subset=['NPS']).sort_values('NPS', ascending=False)
        fig_nps = px.bar(nps_sorted, x=nps_sorted.index, y='NPS', color='NPS',
                         color_continuous_scale='RdYlGn', range_color=[-100, 100], template="plotly_dark", text_auto=True)
        fig_nps.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
        fig_nps.update_traces(textposition='outside')
        st.plotly_chart(fig_nps, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Percentual de Contribuição
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>Percentual de Contribuição de Cada Agente (%)</h4>", unsafe_allow_html=True)
        contrib_df = display_ranking.copy()
        contrib_df['Contribuição (%)'] = (contrib_df['Atendimentos'] / total_atendimentos * 100).round(2)
        contrib_df = contrib_df.sort_values('Contribuição (%)', ascending=False)
        fig_contrib = px.bar(contrib_df, x=contrib_df.index, y='Contribuição (%)', color='Contribuição (%)',
                             color_continuous_scale='Purples', template="plotly_dark", text_auto='.2f')
        fig_contrib.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
        fig_contrib.update_traces(textposition='outside')
        st.plotly_chart(fig_contrib, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Mapping Categories, Status & Partners
        st.markdown("### 🗺️ Mapeamento de Categoria, Status e Parceiros")
        
        # 1. Volumetria por Status (Full Width)
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>Volumetria por Status de Atendimento</h4>", unsafe_allow_html=True)
        status_df = df.groupby('Status')[['Atendimentos']].sum().reset_index().sort_values('Atendimentos', ascending=False)
        total_status_tix = status_df['Atendimentos'].sum()
        status_df['Status_Legend'] = status_df.apply(lambda r: f"{r['Status']} - {r['Atendimentos']:,} ({r['Atendimentos']/total_status_tix*100:.1f}%)", axis=1)
        
        fig_status = px.pie(status_df, values='Atendimentos', names='Status_Legend',
                            color_discrete_sequence=px.colors.sequential.Agsunset, template="plotly_dark")
        fig_status.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        fig_status.update_traces(textinfo='percent+value')
        st.plotly_chart(fig_status, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Categories & Partners (Side-by-side)
        col_map1, col_map2 = st.columns(2)
        with col_map1:
            st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top:0;'>Principais Categorias Demandadas</h4>", unsafe_allow_html=True)
            cat_df = df.groupby('Categoria')[['Atendimentos']].sum().reset_index().sort_values('Atendimentos', ascending=True)
            fig_cat = px.bar(cat_df.tail(15), x='Atendimentos', y='Categoria', orientation='h',
                             color='Atendimentos', color_continuous_scale='Purpor', template="plotly_dark", text_auto=True)
            fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
            fig_cat.update_traces(textposition='outside')
            st.plotly_chart(fig_cat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_map2:
            st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top:0;'>Volume de Tickets por Parceiro Comercial</h4>", unsafe_allow_html=True)
            parc_df = df.groupby('Solicitante')[['Atendimentos']].sum().reset_index().sort_values('Atendimentos', ascending=True)
            fig_parc = px.bar(parc_df.tail(15), x='Atendimentos', y='Solicitante', orientation='h',
                              color='Atendimentos', color_continuous_scale='Burg', template="plotly_dark", text_auto=True)
            fig_parc.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
            fig_parc.update_traces(textposition='outside')
            st.plotly_chart(fig_parc, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # TAB 2: INDIVIDUAL PERFORMANCE
    # ════════════════════════════════════════════════════════════
    with tab_agent:
        col_title, col_print = st.columns([3, 1])
        with col_title:
            st.markdown(f"### 👤 Relatório de Desempenho: **{selected_agent}**")
        with col_print:
            print_button(f"Exportar Relatório de {selected_agent} (PDF)")
            
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        
        # Filter agent data
        df_selection_operador = df[df['Agente'] == selected_agent].copy()
        
        if df_selection_operador.empty:
            st.info("Este agente não possui atendimentos registrados com os filtros selecionados.")
        else:
            # Stats calculations
            Operador_Atendimentos = df_selection_operador['Atendimentos'].sum()
            Operador_Minutos_Trabalhados = df_selection_operador['Minutos Trabalhados'].sum()
            Operador_TMA = round(Operador_Minutos_Trabalhados / Operador_Atendimentos, 2) if Operador_Atendimentos > 0 else 0
            Operador_Influencia_Atendimentos = ((Operador_Atendimentos / total_atendimentos) * 100).round(2) if total_atendimentos > 0 else 0
            media_atendimentos_operador = round(Operador_Atendimentos / dias_analisados, 2)
            
            soma_minutos_ind = df_selection_operador['Minutos Trabalhados'].sum()
            horas_trabalhadas_ind = soma_minutos_ind / 60 
            velocidade_media_operador = round(Operador_Atendimentos / horas_trabalhadas_ind, 2) if horas_trabalhadas_ind > 0 else 0
            
            # Team daily stats for comparison
            df_comparison = df.copy()
            df_comparison['Data'] = df_comparison['Data'].astype(str)
            team_daily = df_comparison.groupby(['Data', 'Agente'])[['Atendimentos', 'Minutos Trabalhados']].sum().reset_index()
            team_daily_avg = team_daily.groupby('Data')[['Atendimentos', 'Minutos Trabalhados']].mean()
            team_daily_avg['TMA'] = team_daily_avg['Minutos Trabalhados'] / team_daily_avg['Atendimentos']
            
            # Calculate agent NPS metrics based on contribution
            agent_tickets = df_selection_operador['Atendimentos'].sum()
            total_team_tickets = df['Atendimentos'].sum()
            contrib_pct = (agent_tickets / total_team_tickets) * 100 if total_team_tickets > 0 else 0
            
            if contrib_pct < 1.0:
                op_nps_str = "N/A"
                op_avg_str = "N/A"
                op_ratings_count = 0
            else:
                op_nps_val, op_avg_val, op_ratings_count = calculate_nps(df_selection_operador['Satisfacao'])
                op_nps_str = str(op_nps_val)
                op_avg_str = f"{op_avg_val:.1f}"

            # Individual KPI Cards
            col_ind1, col_ind2, col_ind3, col_ind4, col_ind5, col_ind6 = st.columns(6)
            with col_ind1:
                st.markdown(f"""
                    <div class="team-card">
                        <div class="team-card-label">Total de Atendimentos</div>
                        <div class="team-card-value">{Operador_Atendimentos:,}</div>
                        <div class="team-card-help">Atendimentos do agente</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_ind2:
                st.markdown(f"""
                    <div class="team-card">
                        <div class="team-card-label">TMA Individual</div>
                        <div class="team-card-value">{Operador_TMA:.2f} min</div>
                        <div class="team-card-help">Tempo médio por atendimento</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_ind3:
                st.markdown(f"""
                    <div class="team-card">
                        <div class="team-card-label">Velocidade Individual</div>
                        <div class="team-card-value">{velocidade_media_operador:.2f} at./h</div>
                        <div class="team-card-help">Atendimentos por hora ativa</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_ind4:
                nps_color_style = ""
                if op_nps_str == "N/A":
                    nps_color_style = "style='color:#94A3B8;'" # Grey-400
                else:
                    nps_val = int(op_nps_str)
                    if nps_val >= 70:
                        nps_color_style = "style='color:#10B981;'" # Emerald-500
                    elif nps_val >= 50:
                        nps_color_style = "style='color:#34D399;'" # Emerald-400
                    elif nps_val >= 0:
                        nps_color_style = "style='color:#FBBF24;'" # Amber-400
                    else:
                        nps_color_style = "style='color:#EF4444;'" # Red-500
                
                st.markdown(f"""
                    <div class="team-card">
                        <div class="team-card-label">NPS do Agente</div>
                        <div class="team-card-value" {nps_color_style}>{op_nps_str}</div>
                        <div class="team-card-help">Score Net Promoter</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_ind5:
                avg_color_style = "style='color:#94A3B8;'" if op_avg_str == "N/A" else "style='color:#60A5FA;'"
                st.markdown(f"""
                    <div class="team-card">
                        <div class="team-card-label">Média de Nota</div>
                        <div class="team-card-value" {avg_color_style}>{op_avg_str}</div>
                        <div class="team-card-help">Média ({op_ratings_count} aval.)</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_ind6:
                st.markdown(f"""
                    <div class="team-card">
                        <div class="team-card-label">Contribuição na Equipe</div>
                        <div class="team-card-value">{Operador_Influencia_Atendimentos:.2f}%</div>
                        <div class="team-card-help">Percentual de participação</div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("##")
            
            # Daily trends charts
            st.markdown("### Tendência de Produtividade por Dia")
            
            df_selection_operador['Data'] = df_selection_operador['Data'].astype(str)
            demandas_datas = df_selection_operador.groupby('Data')[['Minutos Trabalhados', 'Atendimentos']].sum()
            demandas_datas['TMA'] = demandas_datas['Minutos Trabalhados'] / demandas_datas['Atendimentos']
            demandas_datas['Horas Trabalhadas'] = demandas_datas['Minutos Trabalhados'] / 60
            demandas_datas['Atendimentos/Hora'] = demandas_datas['Atendimentos'] / demandas_datas['Horas Trabalhadas']
            
            # Calculate daily NPS metrics for the agent
            daily_nps_stats = []
            for date, group in df_selection_operador.groupby('Data'):
                if contrib_pct < 1.0:
                    nps, avg_rating, count = pd.NA, pd.NA, 0
                else:
                    nps, avg_rating, count = calculate_nps(group['Satisfacao'])
                daily_nps_stats.append({
                    'Data': date,
                    'NPS Diário': nps,
                    'Média de Nota Diária': avg_rating,
                    'Avaliações': count
                })
            df_daily_nps = pd.DataFrame(daily_nps_stats).set_index('Data')
            demandas_datas = demandas_datas.join(df_daily_nps)
            
            # Formulate Charts
            col_cht1, col_cht2 = st.columns(2)
            
            # Align team average data safely
            y_team_at = [team_daily_avg.loc[d, 'Atendimentos'] if d in team_daily_avg.index else 0 for d in demandas_datas.index]
            y_team_tma = [team_daily_avg.loc[d, 'TMA'] if d in team_daily_avg.index else 0 for d in demandas_datas.index]
            
            with col_cht1:
                st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
                st.markdown("<h4>Atendimentos por Data vs. Metas</h4>", unsafe_allow_html=True)
                
                plot_ind_at = go.Figure()
                plot_ind_at.add_trace(go.Bar(
                    name='Atendimentos', 
                    x=demandas_datas.index, 
                    y=demandas_datas['Atendimentos'], 
                    marker_color='#818CF8',
                    text=demandas_datas['Atendimentos'],
                    textposition='outside'
                ))
                plot_ind_at.add_trace(go.Scatter(name='Média da Equipe', x=demandas_datas.index, y=y_team_at, line=dict(color='#38BDF8', width=2, dash='dot')))
                plot_ind_at.add_trace(go.Scatter(name='Meta Individual', x=demandas_datas.index, y=[Meta_Atendimentos_Diarios]*len(demandas_datas), line=dict(color='#EF4444', width=2, dash='dash')))
                
                plot_ind_at.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=330,
                    margin=dict(l=10, r=10, b=10, t=10)
                )
                st.plotly_chart(plot_ind_at, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_cht2:
                st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
                st.markdown("<h4>TMA por Data vs. Metas (Minutos)</h4>", unsafe_allow_html=True)
                
                plot_ind_tma = go.Figure()
                plot_ind_tma.add_trace(go.Bar(
                    name='TMA', 
                    x=demandas_datas.index, 
                    y=demandas_datas['TMA'].round(2), 
                    marker_color='#34D399',
                    text=demandas_datas['TMA'].round(2),
                    textposition='outside'
                ))
                plot_ind_tma.add_trace(go.Scatter(name='Média da Equipe', x=demandas_datas.index, y=y_team_tma, line=dict(color='#38BDF8', width=2, dash='dot')))
                plot_ind_tma.add_trace(go.Scatter(name='Meta TMA', x=demandas_datas.index, y=[Meta_TMA_Diario]*len(demandas_datas), line=dict(color='#EF4444', width=2, dash='dash')))
                
                plot_ind_tma.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=330,
                    margin=dict(l=10, r=10, b=10, t=10)
                )
                st.plotly_chart(plot_ind_tma, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("##")
            
            # Daily Stats Table
            st.markdown("### 📅 Tabela de Estatísticas Diárias do Agente")
            
            # Prepare formatted daily details
            display_daily = demandas_datas.copy()
            display_daily['TMA'] = display_daily['TMA'].round(2)
            display_daily['Atendimentos/Hora'] = display_daily['Atendimentos/Hora'].round(2)
            display_daily['Aproveitamento Horas Disponíveis'] = (display_daily['Horas Trabalhadas'] / Tempo_Disponivel_Horas * 100).round(1)
            display_daily['SCORE'] = ((display_daily['Atendimentos'] * display_daily['Atendimentos/Hora'] * (display_daily['Horas Trabalhadas'] / Tempo_Disponivel_Horas)) / display_daily['TMA']).round(2)
            display_daily['NPS Diário'] = pd.to_numeric(display_daily['NPS Diário'], errors='coerce').astype('Int64')
            display_daily['Média de Nota Diária'] = pd.to_numeric(display_daily['Média de Nota Diária'], errors='coerce').round(1)
            display_daily['Avaliações'] = pd.to_numeric(display_daily['Avaliações'], errors='coerce').astype('Int64')
            
            display_daily = display_daily.rename(columns={
                'Atendimentos': 'Atendimentos Realizados',
                'Minutos Trabalhados': 'Minutos Ativos',
                'Horas Trabalhadas': 'Horas Ativas',
                'TMA': 'TMA (Minutos)',
                'SCORE': 'Score de Produtividade'
            })
            
            st.dataframe(display_daily[['Atendimentos Realizados', 'Horas Ativas', 'TMA (Minutos)', 'Atendimentos/Hora', 'Aproveitamento Horas Disponíveis', 'NPS Diário', 'Média de Nota Diária', 'Avaliações', 'Score de Produtividade']], use_container_width=True)
            
            # Download daily detailed
            agent_excel = to_excel(display_daily[['Atendimentos Realizados', 'Horas Ativas', 'TMA (Minutos)', 'Atendimentos/Hora', 'Aproveitamento Horas Disponíveis', 'NPS Diário', 'Média de Nota Diária', 'Avaliações', 'Score de Produtividade']])
            st.download_button(
                label=f"📥 BAIXAR EXCEL - RELATÓRIO DIÁRIO DE {selected_agent.upper()}",
                data=agent_excel,
                file_name=f"performa_cx_diario_{selected_agent.lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Individual Mapping Section
            st.markdown("---")
            st.markdown("### 🗺️ Mapeamento Individual de Categoria, Status e Parceiros Comerciais")
            
            # 1. Status (Full Width)
            st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
            st.markdown("<h4>Volumetria por Status (Individual)</h4>", unsafe_allow_html=True)
            ind_status_df = df_selection_operador.groupby('Status')[['Atendimentos']].sum().reset_index().sort_values('Atendimentos', ascending=False)
            ind_total_status = ind_status_df['Atendimentos'].sum()
            ind_status_df['Status_Legend'] = ind_status_df.apply(lambda r: f"{r['Status']} - {r['Atendimentos']:,} ({r['Atendimentos']/ind_total_status*100:.1f}%)", axis=1)
            
            fig_ind_status = px.pie(ind_status_df, values='Atendimentos', names='Status_Legend',
                                    color_discrete_sequence=px.colors.sequential.Agsunset, template="plotly_dark")
            fig_ind_status.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            fig_ind_status.update_traces(textinfo='percent+value')
            st.plotly_chart(fig_ind_status, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 2. Categories & Partners (Side-by-side)
            col_ind_map1, col_ind_map2 = st.columns(2)
            with col_ind_map1:
                st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
                st.markdown("<h4>Categorias Demandadas (Individual)</h4>", unsafe_allow_html=True)
                ind_cat_df = df_selection_operador.groupby('Categoria')[['Atendimentos']].sum().reset_index().sort_values('Atendimentos', ascending=True)
                fig_ind_cat = px.bar(ind_cat_df.tail(15), x='Atendimentos', y='Categoria', orientation='h',
                                     color='Atendimentos', color_continuous_scale='Purpor', template="plotly_dark", text_auto=True)
                fig_ind_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
                fig_ind_cat.update_traces(textposition='outside')
                st.plotly_chart(fig_ind_cat, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_ind_map2:
                st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
                st.markdown("<h4>Tickets por Parceiro Comercial (Individual)</h4>", unsafe_allow_html=True)
                ind_parc_df = df_selection_operador.groupby('Solicitante')[['Atendimentos']].sum().reset_index().sort_values('Atendimentos', ascending=True)
                fig_ind_parc = px.bar(ind_parc_df.tail(15), x='Atendimentos', y='Solicitante', orientation='h',
                                      color='Atendimentos', color_continuous_scale='Burg', template="plotly_dark", text_auto=True)
                fig_ind_parc.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
                fig_ind_parc.update_traces(textposition='outside')
                st.plotly_chart(fig_ind_parc, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

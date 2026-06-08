# 📈 PerformaCX - Customer Experience Performance Dashboard

[**Português 🇧🇷**](#português) | [**English 🇺🇸**](#english)

---

<a name="english"></a>
# English 🇺🇸

An advanced, interactive Customer Experience (CX) performance dashboard designed to analyze and rank agent productivity based on helpdesk ticket databases. Built with Streamlit and Plotly, **PerformaCX** replaces hardcoded business definitions with dynamic configurations, allowing managers to calculate complex, multi-variable performance metrics on the fly.

## 🚀 Key Features

*   **📊 Dynamic Team Progress Chart**: Compares current ticket completion rates against the team's overall capacity, target goals, and historical averages using interactive Plotly bar and line charts.
*   **🏆 Custom Productivity Ranking Algorithm**: Implements a custom mathematical formula to score agent performance fairly by combining volume, speed, and time utilization:
    $$\text{Score} = \frac{\text{Tickets Completed} \times \text{Tickets/Hour} \times \text{Capacity Utilization (\%)}}{\text{Average Handling Time (TMA)}}$$
*   **🎯 Dynamic Agent Filters**: A sidebar multi-select dropdown dynamically populated from the uploaded file, allowing managers to exclude or isolate specific agents from the analysis.
*   **📥 Excel Report Compilation**: Automatically compiles data and generates high-fidelity Excel download links for the Daily Agent metrics and Consolidated Productivity Rankings.
*   **💼 Comprehensive CX Metrics**: Tracks team metrics such as Total Tickets, Average Handling Time (TMA), worked hours, minimum/maximum scores, and category/service distributions.

---

## 🛠️ Tech Stack & Algorithms

*   **Dashboard UI**: [Streamlit](https://streamlit.io/) with a wide responsive layout.
*   **Data Analysis**: `Pandas`, `NumPy`, `BytesIO`.
*   **Data Visualization**: [Plotly Express](https://plotly.com/) & [Plotly Graph Objects](https://plotly.com/).
*   **Report Generation**: `xlsxwriter` for dynamic in-memory Excel generation.

---

## 💻 How to Run Locally

### Prerequisites
Make sure you have Python 3.8+ installed.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DigoRM/CX_performance_movi.git
   cd CX_performance_movi
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Dashboard**:
   ```bash
   streamlit run produtividade_movi_beta.py
   ```

---

## ☁️ Deployment

This dashboard is ready to deploy for free on the **Streamlit Community Cloud**:
1. Push this project to GitHub.
2. Link your repository on [Streamlit Share](https://share.streamlit.io/).
3. Set the entry point file to `produtividade_movi_beta.py` and deploy!

---

<br>

<a name="português"></a>
# Português 🇧🇷

Um dashboard avançado e interativo de análise de desempenho em Customer Experience (CX) desenvolvido para avaliar e ranquear a produtividade de analistas com base em históricos de tickets. Construído com Streamlit e Plotly, o **PerformaCX** substitui definições engessadas por parametrizações dinâmicas, permitindo a gestores calcularem métricas complexas de performance em tempo real.

## 🚀 Principais Funcionalidades

*   **📊 Gráfico Dinâmico de Progresso do Time**: Compara as taxas atuais de resolução de tickets com o potencial máximo de entrega da equipe, metas operacionais e médias históricas utilizando gráficos interativos de barra e linha do Plotly.
*   **🏆 Algoritmo de Ranking de Produtividade**: Implementa uma fórmula matemática balanceada para pontuar o desempenho individual dos agentes, ponderando volume de entregas, velocidade e aproveitamento de tempo de forma justa:
    $$\text{Score} = \frac{\text{Atendimentos Realizados} \times \text{Atendimentos/Hora} \times \text{Aproveitamento Horas Disponíveis (\%)}}{\text{Tempo Médio de Atendimento (TMA)}}$$
*   **🎯 Filtro Dinâmico de Agentes**: Menu lateral multiselect populado automaticamente a partir dos dados do arquivo carregado, permitindo excluir ou isolar analistas específicos da análise global instantaneamente.
*   **📥 Exportação Inteligente de Relatórios**: Gera links de download dinâmicos para arquivos Excel (.xlsx) estruturados contendo as Métricas Diárias por Agente e o Ranking Geral de Produtividade Consolidado.
*   **💼 Estatísticas Consolidadas de CX**: Consolida indicadores críticos como TMA Médio, Mínimo e Máximo, total de horas aplicadas em atendimento, aproveitamento da capacidade disponível e distribuição de volumetria por Categoria e Serviço.

---

## 🛠️ Stack Tecnológica e Algoritmos

*   **Interface/Dashboard**: [Streamlit](https://streamlit.io/) com layout responsivo e flexível.
*   **Processamento de Dados**: `Pandas`, `NumPy`, `BytesIO`.
*   **Visualizações**: [Plotly Express](https://plotly.com/) & [Plotly Graph Objects](https://plotly.com/).
*   **Geração de Relatórios**: `xlsxwriter` para compilação em memória de planilhas Excel estruturadas.

---

## 💻 Como Executar Localmente

### Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado.

1. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/DigoRM/CX_performance_movi.git
   cd CX_performance_movi
   ```

2. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o Dashboard Streamlit**:
   ```bash
   streamlit run produtividade_movi_beta.py
   ```

---

## ☁️ Implantação (Deployment)

Este dashboard está totalmente otimizado para deploy gratuito na **Streamlit Community Cloud**:
1. Faça o push do projeto para o GitHub.
2. Vincule seu repositório no [Streamlit Share](https://share.streamlit.io/).
3. Indique o arquivo `produtividade_movi_beta.py` como ponto de entrada e publique!

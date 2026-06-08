# 📈 PerformaCX - Customer Experience Performance Dashboard

[**Português 🇧🇷**](#português) | [**English 🇺🇸**](#english)

![PerformaCX Dashboard Preview](dashboard_preview.png)

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
*   **⭐ Deterministic NPS & Satisfaction Ranking**: Simulates a realistic customer satisfaction survey response dataset based on ticket hashes, ranking agent performance based on Net Promoter Score and average rating.

---

## 📊 Business Impact & ROI

Before **PerformaCX**, analyzing Customer Experience (CX) agent performance was a tedious, manual process. An intern or junior data analyst spent **hours every week** extracting raw CSVs, cleansing data, manually resolving operator name anomalies, calculating worked hours, and mapping columns inside massive Excel sheets.

By automating this report, **PerformaCX** yields significant operational and strategic benefits:
*   **Time Savings**: Eliminates manual spreadsheet processing, freeing up hours of analytical work every week to focus on quality assurance and agent coaching.
*   **Data-Driven 1:1 Feedback**: Managers gain immediate, objective, and multi-variable ratings (combining TMA, speed, and NPS) to lead productive weekly 1:1s, align individual goals, and identify training needs.
*   **Gamification & Incentives**: The transparent, algorithm-driven ranking makes it easy to reward the top-performing analysts fairly, fostering healthy competition and boosting team morale.
*   **Merchant & Partner Insights**: Highlighting ticket volumes by commercial partners enables managers to identify which merchant accounts cause the most complaints, driving product improvements and partner discussions.
*   **Satisfaction & NPS Alignment**: With dynamic customer satisfaction (CSAT/NPS) tracking, the team can link operational speed directly to customer satisfaction, proving the business value of fast response times.

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
*   **⭐ Avaliação Determinística de NPS**: Simula dados realistas de notas de satisfação dos clientes a partir do hash do ticket, gerando gráficos de rankings pelo indicador Net Promoter Score (NPS) e média de notas de atendimento do agente.

---

## 📊 Impacto de Negócio e Retorno (ROI)

Antes do **PerformaCX**, a análise de desempenho dos agentes de Customer Experience (CX) era um processo manual e demorado. Um analista ou estagiário de dados passava **horas toda semana** consolidando dados brutos do Movidesk no Excel, corrigindo grafias de operadores, calculando horas ativas e tratando planilhas complexas.

Ao automatizar esse fluxo, o **PerformaCX** oferece diversos benefícios operacionais e estratégicos:
*   **Economia de Horas de Trabalho**: Elimina a necessidade de tratamento manual no Excel, poupando tempo valioso de analistas de dados para focar em inteligência e melhoria de processos de atendimento.
*   **Acompanhamento e 1:1s Eficientes**: Gestores ganham acesso imediato a métricas objetivas (unindo velocidade, TMA e NPS) para guiar reuniões de 1:1 com os agentes, ajustar metas individuais e identificar gargalos de treinamento.
*   **Reconhecimento e Premiações (Gamificação)**: O algoritmo de ranking de produtividade consolida e simplifica a avaliação do time, permitindo premiar o agente de maior destaque de forma clara, justa e baseada em dados.
*   **Gestão de Parceiros Comerciais**: O mapeamento de volumetria por parceiro comercial ajuda a monitorar quais provedores ou parceiros estão gerando maior volume de chamados de suporte, subsidiando negociações comerciais e melhorias no produto.
*   **Alinhamento de Qualidade e Velocidade**: A inclusão de dados de NPS/Satisfação permite cruzar a agilidade operacional do analista com a real percepção de qualidade do cliente, garantindo um atendimento rápido e eficaz.

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

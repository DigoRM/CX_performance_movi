---
title: CX Performance Movi
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.58.0
app_file: produtividade_movi_beta.py
pinned: false
---

# PerformaCX · Enterprise Customer Experience (CX) Performance Analytics

PerformaCX is a high-performance, interactive analytics platform designed to analyze operational ticket databases and visualize productivity metrics, quality indicators, and throughput in Customer Experience (CX) environments. 

Rather than spending hours manually compiling spreadsheets, managers can upload support databases to **instantly generate standardized, professional insights** about team performance and individual rendering.

---

## ⚡ The Value Proposition

* **Automation of Reporting**: Weekly manual data consolidation tasks are completely eliminated, generating unified dashboards in **seconds**.
* **Objective-Goal Tracking**: Real-time comparisons of team productivity against custom resolution and Average Handling Time (TMA/AHT) targets.
* **Granular Quality Analytics**: Integrates Net Promoter Score (NPS) tracking per day, per agent, and across the entire team to monitor customer satisfaction trends.
* **Operational Flexibility**: Fully adjustable work hours and target parameters in the sidebar to simulate and scale operational setups.
* **Instant Export Suite**: Download fully compiled operational PDF performance sheets or consolidated raw Excel tables at any time.

---

## 🚀 Key Features

### 1. Interactive Team Dashboard
* **Macro Metrics**: Track total atendimentos, TMA médio (AHT), overall NPS, resolution velocity (tickets resolved per active hour), and active agents count.
* **Dynamic Visualization**: Beautiful, interactive charts showing daily productivity trends, daily NPS averages vs. target line, and category breakdown.
* **Operational Rankings**: Comparative leaderboards showcasing agents sorted by TMA, speed (resolutions/hour), NPS score, and team contribution percentage.

### 2. Individual Rendition Panel
* **Analyst Profile**: A dedicated tab for granular tracking of a specific agent.
* **Individual Trends**: View the agent's daily resolution trend vs. target, TMA fluctuations, and individual customer review distributions.
* **Categorical Mapping**: Inspect exactly which categories and commercial partners the agent spent most of their volume resolving.

### 3. Report Exporter
* **PDF Builder**: Compiles a highly styled, clean report PDF of the team or individual agent for immediate distribution.
* **Excel Exporter**: Compiles consolidated tables or individual logs into formatted Excel files.

---

## 🛠️ Technology Stack

* **Core Engine**: Python 3.9 / Streamlit (High-performance reactive frontend framework)
* **Data Processing**: Pandas / Openpyxl (Advanced file parsing and filtering)
* **Data Visualization**: Plotly / Plotly Graph Objects (Interactive web-based charts)
* **Exporting**: FPDF2 / Pillow (High-fidelity report layout construction)

---

## 📦 Local Installation & Run

### Prerequisites
* Python 3.9+

### Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/DigoRM/CX_performance_movi.git
   cd CX_performance_movi
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run produtividade_movi_beta.py
   ```
   Open your browser at the local address displayed (typically `http://localhost:8501`).

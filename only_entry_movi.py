import pandas as pd
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
import base64
from io import BytesIO

input_Dias_Analisados = st.number_input('Quantos dias úteis vou analisar?',min_value=1,max_value=60,value=1,step=1)
input_Agentes_Analisados = st.number_input('Quantos agentes estarão disponíveis?',min_value=1,max_value=60,value=1,step=1)

dias_analisados = input_Dias_Analisados
agentes_analisados = input_Agentes_Analisados
# Sidebar
st.sidebar.subheader("Entrantes")
	# Setup file upload
uploaded_file1 = st.sidebar.file_uploader(label="baixe o arquivo aqui", type=['csv','xlsx'])
global df1

try:
	df1 = pd.read_csv(uploaded_file1)
	# criando coluna para efetuar a contagem de atendimentos
	df1 ['Atendimentos']=1
	# processo para poder efetuar operações matematicas com o horario
	df1['Horas Trabalhadas'] = pd.to_datetime(df1['Horas Trabalhadas'],format="%H:%M:%S")
	df1['Horas Trabalhadas'] = df1['Horas Trabalhadas'].astype(str)
	df1['Minutos Trabalhados'] = df1['Horas Trabalhadas'].str[14:16]
	df1['Minutos Trabalhados'] = df1['Minutos Trabalhados'].astype(int)
           #agentes que não fazem parte do MoviDesk
	df1 = df1.drop(df1[df1.Responsavel == "Bruno da Silva Braun"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Sheila Santos da Rosa"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Matheus Souza de Almeida"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Eduarda dos Santos Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Marjorie Lima"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Natália M"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Isabelle da Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Ester Marques Plate da Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Heitor Francisco Pereira Netto"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Cátia Duarte Velleda"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Paola Fantinel"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Vanessa Lima"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Bruna Vasconcelos"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Bianca Moreira Scalcon"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Mariana Moreira Colombo"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Nathalia Bandarra Moreira"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Bruno Gonçalves Santin"].index)
	df1 = df1.drop(df1[df1.Responsavel == "fabiane barreto"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Matheus Vicente Cabral"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Isabel dos Santos Matos"].index)
	
	#####################
		
	df1 = df1.drop(df1[df1.Responsavel == "Pâmela Andressa dos Santos"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Julia de Cássia Rodrigues"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Douglas Bajon"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Larissa Muller"].index)
	df1 = df1.drop(df1[df1.Responsavel == "José Guilherme Ferreira Gonçalves"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Luan Gonçalves"].index)
except Exception as e:
	print(e)
	df1 = pd.read_excel(uploaded_file1)
	# criando coluna para efetuar a contagem de atendimentos
	df1 ['Atendimentos']=1
	# processo para poder efetuar operações matematicas com o horario
	df1['Aberto em'] = df1['Aberto em'].astype(str)
	df1['Aberto em'] = df1['Aberto em'].str[:10]
           #agentes que não fazem parte do MoviDesk
	df1 = df1.drop(df1[df1.Responsavel == "Bruno da Silva Braun"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Sheila Santos da Rosa"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Matheus Souza de Almeida"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Eduarda dos Santos Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Marjorie Lima"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Natália M"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Isabelle da Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Ester Marques Plate da Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Heitor Francisco Pereira Netto"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Cátia Duarte Velleda"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Paola Fantinel"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Vanessa Lima"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Bruna Vasconcelos"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Bianca Moreira Scalcon"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Mariana Moreira Colombo"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Nathalia Bandarra Moreira"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Bruno Gonçalves Santin"].index)
	df1 = df1.drop(df1[df1.Responsavel == "fabiane barreto"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Matheus Vicente Cabral"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Isabel dos Santos Matos"].index)
	
	#####################
	
	df1 = df1.drop(df1[df1.Responsavel == "Pâmela Andressa dos Santos"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Julia de Cássia Rodrigues"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Douglas Bajon"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Larissa Muller"].index)
	df1 = df1.drop(df1[df1.Responsavel == "José Guilherme Ferreira Gonçalves"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Luan Gonçalves"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Marcelo Böck"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Julia Dahm"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Yago Ayres Bednarck"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Leonardo Kosloski"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Larissa Carvalho Da Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Gabriel Paludo Fiorentin"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Gabrielly Ferreira"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Gisiane Miranda Martins"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Gustavo Gindri Werutsky"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Isabel Cristina Teixeira Dutra"].index)
	df1 = df1.drop(df1[df1.Responsavel == "João Vicente Uriarte"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Patrícia Rodrigues da Silva"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Samira Chagas Machado"].index)
	df1 = df1.drop(df1[df1.Responsavel == "Stephanie Kathreien Rodrigues Ribeiro"].index)
	
try:
	st.dataframe(data=df1,width=2000,height=150)
except Exception as e:
	print(e)
	st.write('Please upload your file...')
	st.markdown('##')


st.header('Volume de Tickets da Equipe')

A123, B123 = st.columns(2)
with A123:
	total_entrantes = len(df1)
	st.write(f"**Total Entrantes:** {total_entrantes} tickets")
	
	entrantes_dia = round((total_entrantes/dias_analisados),2)
	st.write(f"**Média de** {entrantes_dia} entrantes por dia")



with B123:
	responsaveis_entrantes_agrupa = df1.groupby('Responsavel').sum()
	responsaveis_analisados = len(responsaveis_entrantes_agrupa)
	
	entrantes_agente_dia = entrantes_dia/agentes_analisados
	
	st.write(f"**Quantidade de Responsáveis em análise:** {responsaveis_analisados} responsáveis")
	st.write(f"**Quantidade de Agentes:** {agentes_analisados} agentes")
	st.write(f"**Demandas esperadas:** {entrantes_agente_dia} tickets por agente")
	
	


# Gráficos
df1

df1_agrupa_data = df1.groupby('Aberto em').sum()
df1_agrupa_data = df1_agrupa_data.drop(columns='Número')
df1_agrupa_data['Aumento'] = df1_agrupa_data['Atendimentos'].diff()
df1_agrupa_data['Média Atendimentos/Dia'] = entrantes_dia

df1_agrupa_data['Média Aumento 20'] = df1_agrupa_data['Aumento']

df1_agrupa_data['Média Móvel'] = df1_agrupa_data['Atendimentos'].rolling(7).mean().round()

df1_agrupa_data['Média Móvel 10'] = df1_agrupa_data['Atendimentos'].rolling(10).mean().round()

df1_agrupa_data['Média Móvel 15'] = df1_agrupa_data['Atendimentos'].rolling(15).mean().round()

df1_agrupa_data['Média Móvel 20'] = df1_agrupa_data['Atendimentos'].rolling(20).mean().round()

df1_agrupa_data['Média Aumento 7'] = df1_agrupa_data['Aumento'].rolling(7).mean().round()

df1_agrupa_data['Média Aumento 10'] = df1_agrupa_data['Aumento'].rolling(10).mean().round()

df1_agrupa_data['Média Aumento 15'] = df1_agrupa_data['Aumento'].rolling(15).mean().round()

df1_agrupa_data['Média Aumento 20'] = df1_agrupa_data['Aumento'].rolling(20).mean().round()

df1_agrupa_data


st.title('Tickets')
st.markdown('#')

st.header('Tickets por dia')
plot = go.Figure(data=[go.Bar(name= 'Atendimentos',x=df1_agrupa_data.index,y=df1_agrupa_data['Atendimentos'],text=df1_agrupa_data['Atendimentos'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Atendimentos']),go.Line(name="Média Atendimentos/Dia",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Atendimentos/Dia'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Média de Tickets dos útimos 7 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Móvel',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel'],text=df1_agrupa_data['Média Móvel'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Média de Tickets dos útimos 10 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Móvel 10',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel 10'],text=df1_agrupa_data['Média Móvel 10'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel 10'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Média de Tickets dos útimos 15 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Móvel 15',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel 15'],text=df1_agrupa_data['Média Móvel 15'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel 15'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Média de Tickets dos útimos 20 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Móvel 2020',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel 20'],text=df1_agrupa_data['Média Móvel 20'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Móvel 20'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

#########
st.title('Variação')
st.markdown('#')
st.header('Variação de Tickets por dia')
plot = go.Figure(data=[go.Bar(name= 'Aumento',x=df1_agrupa_data.index,y=df1_agrupa_data['Aumento'],text=df1_agrupa_data['Aumento'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Aumento'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Variação média de Tickets a cada 7 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Aumento 7',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 7'],text=df1_agrupa_data['Média Aumento 7'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 7'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Variação média de Tickets a cada 10 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Aumento 10',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 10'],text=df1_agrupa_data['Média Aumento 10'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 10'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Variação média de Tickets a cada 15 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Aumento 15',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 15'],text=df1_agrupa_data['Média Aumento 15'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 15'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)

st.header('Variação média de Tickets a cada 20 dias')
plot = go.Figure(data=[go.Bar(name= 'Média Aumento 20',x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 20'],text=df1_agrupa_data['Média Aumento 20'],textposition='outside'),go.Line(name="Progress",x=df1_agrupa_data.index,y=df1_agrupa_data['Média Aumento 20'])])
plot.update_layout(height=800, width=1500)
st.plotly_chart(plot,use_container_width=False)


# Analise de Sazonalidade

# Sidebar
st.sidebar.subheader("Sazonalidade")
	# Setup file upload
uploaded_file2 = st.sidebar.file_uploader(label="Arraste o arquivo aqui", type=['csv','xlsx'])
global df2

try:
	df2 = pd.read_csv(uploaded_file2)

except Exception as e:
	print(e)
	df2 = pd.read_excel(uploaded_file2)
	
try:
	st.dataframe(data=df2,width=2000,height=150)
except Exception as e:
	print(e)
	st.write('Please upload your file...')
	st.markdown('##')

df2['Aberto em'] = pd.to_datetime(df2['Aberto em'])
df2['dia_da_semana'] = df2['Aberto em'].dt.strftime("%A")
traducao_dias = {'Monday':'Segunda', 'Tuesday':'Terça', 'Wednesday':'Quarta', 
	              'Thursday':'Quinta', 'Friday':'Sexta', 'Saturday':'Sábado',
	              'Sunday':'Domingo'}
df2['dia_da_semana'] = df2['dia_da_semana'].map(traducao_dias)

df2_sazonalidade = df2.groupby('dia_da_semana').mean().round()
df2_sazonalidade = df2_sazonalidade.sort_values('Atendimentos',ascending=False)
st.header('Média de Entrantes por dia da semana:')
plot = go.Figure(data=[go.Bar(name= 'Entrantes por dia da semana',x=df2_sazonalidade.index,y=df2_sazonalidade['Atendimentos'],text=df2_sazonalidade['Atendimentos'],textposition='outside')])
plot.update_layout(height=700, width=1000)
st.plotly_chart(plot,use_container_width=False)


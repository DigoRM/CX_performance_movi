import pandas as pd
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
import base64
from io import BytesIO


# Config Uploader
st.set_option('deprecation.showfileUploaderEncoding', False)


# Title of the app
st.set_page_config(page_title="PerformaCX", page_icon=":bar_chart:", layout="wide")
st.title('Analise de Desempenho CX - MOVI')
st.markdown('Bem vindo! Insira o arquivo das demandas no menu ao lado, e defina os seguintes parâmetros para minha análise:')

input_Dias_Analisados = st.number_input('Quantos dias úteis vou analisar?',min_value=1,max_value=30,value=1,step=1)
input_Horas_Consideradas = st.number_input('Quantas horas considero em 1 dia de trabalho',min_value=1.0,max_value=10.0,value=8.0,step=0.25)
input_TMA_Meta = st.number_input('Digite a meta TMA da equipe',min_value=1.0,max_value=10.0,value=3.0,step=0.25)

if input_Dias_Analisados is not None:


	# Sidebar
	st.sidebar.subheader("Settings")
	# Setup file upload
	uploaded_file = st.sidebar.file_uploader(label="Upload CSV or Excel file here", type=['csv','xlsx'])

	global df
	if uploaded_file is not None:

		print(uploaded_file)

		try:
			df = pd.read_csv(uploaded_file)
			df ['Categoria'].fillna("Outros", inplace=True)
			df ['Serviço'].fillna("Outros", inplace=True)
			# criando coluna para efetuar a contagem de atendimentos
			df ['Atendimentos']=1
			# processo para poder efetuar operações matematicas com o horario
			df['Horas Trabalhadas'] = pd.to_datetime(df['Horas Trabalhadas'],format="%H:%M:%S")
			df['Horas Trabalhadas'] = df['Horas Trabalhadas'].astype(str)
			df['Minutos Trabalhados'] = df['Horas Trabalhadas'].str[14:16]
			df['Minutos Trabalhados'] = df['Minutos Trabalhados'].astype(int)

		except Exception as e:
			print(e)
			df = pd.read_excel(uploaded_file)
			df.drop(df.columns[[0]], axis=1, inplace=True)

			df ['Categoria'].fillna("Outros", inplace=True)
			df ['Serviço'].fillna("Outros", inplace=True)
			# criando coluna para efetuar a contagem de atendimentos
			df ['Atendimentos']=1
			# processo para poder efetuar operações matematicas com o horario
			df['Horas Trabalhadas'] = pd.to_datetime(df['Horas Trabalhadas'],format="%H:%M:%S")
			df['Horas Trabalhadas'] = df['Horas Trabalhadas'].astype(str)
			df['Minutos Trabalhados'] = df['Horas Trabalhadas'].str[14:16]
			df['Minutos Trabalhados'] = df['Minutos Trabalhados'].astype(int)

	try:
		st.dataframe(data=df,width=2000,height=150)
	except Exception as e:
		print(e)
		st.write('Please upload your file...')

	

	
	st.markdown('##')
	dias_analisados = input_Dias_Analisados
	Tempo_Disponivel_Horas = input_Horas_Consideradas
	# aqui a conversao para minutos:
	Tempo_Disponivel = Tempo_Disponivel_Horas*60

	# Metas do time!!
	Meta_TMA_Diario = input_TMA_Meta
	Meta_Atendimentos_Diarios = Tempo_Disponivel/Meta_TMA_Diario
	Meta_Velocidade_Diario = Meta_Atendimentos_Diarios/Tempo_Disponivel_Horas

	st.header('Progresso Atendimentos CX')
	consolidaPeriodo_Data = df.groupby('Data').sum()
	consolidaPeriodo_Data = consolidaPeriodo_Data.drop(columns=['Ticket','Ação nº'])

	consolidaPeriodo_Data ['Horas Trabalhadas'] = consolidaPeriodo_Data['Minutos Trabalhados']/60
	consolidaPeriodo_Data ['TMA(min)'] = consolidaPeriodo_Data['Minutos Trabalhados']/consolidaPeriodo_Data['Atendimentos']
	consolidaPeriodo_Data ['Atendimentos/Hora']= consolidaPeriodo_Data['Atendimentos'] /consolidaPeriodo_Data['Horas Trabalhadas']

	consolidaPeriodo_Data['TMA(min)'] = consolidaPeriodo_Data['TMA(min)'].astype(str)
	consolidaPeriodo_Data ['Minutos'] = consolidaPeriodo_Data['TMA(min)'].str[0]
	consolidaPeriodo_Data ['Minutos'] = consolidaPeriodo_Data['Minutos'].astype(int)
	consolidaPeriodo_Data ['TMA(min)'] = consolidaPeriodo_Data['TMA(min)'].astype(float)
	consolidaPeriodo_Data['Segundos'] = consolidaPeriodo_Data['TMA(min)'] - consolidaPeriodo_Data['Minutos']
	consolidaPeriodo_Data['Segundos'] = (consolidaPeriodo_Data['Segundos'] * 60).astype(int)
	consolidaPeriodo_Data['Horas Trabalhadas'] = (consolidaPeriodo_Data['Horas Trabalhadas']).round(2)
	consolidaPeriodo_Data ['Aproveitamento Horas Disponíveis'] = consolidaPeriodo_Data ['Minutos Trabalhados']/(Tempo_Disponivel*dias_analisados)
	consolidaPeriodo_Data ['Aproveitamento Horas Disponíveis']=(consolidaPeriodo_Data ['Aproveitamento Horas Disponíveis'] * 100).round(1)

	#### --> Grafico do progresso de atendimentos por data
	Grafico_consolidaPeriodo_Data = px.bar(consolidaPeriodo_Data,y=consolidaPeriodo_Data.index,x='Atendimentos',orientation="v",title="<b>Progresso Atual</b>")
	# media de atendimentos atual (varia conforme periodo)
	media_atendimentos_Data = consolidaPeriodo_Data['Atendimentos'].mean()
	# potencial da equipe (varia conforme operador)
	Agrupa_Agentes_Potencial =  df.groupby(['Agente']).sum()
	Agentes_Analisados = len(Agrupa_Agentes_Potencial)
	potencial_equipe = Agentes_Analisados*Meta_Atendimentos_Diarios


	consolidaPeriodo_Data ['Média Atendimentos Período'] = media_atendimentos_Data
	consolidaPeriodo_Data ['Meta Atendimentos'] = potencial_equipe
	plot = go.Figure(data=[go.Bar(name= 'Atendimentos',x=consolidaPeriodo_Data.index,y=consolidaPeriodo_Data['Atendimentos']),go.Line(name="Média Atendimentos Atual",x=consolidaPeriodo_Data.index,y=consolidaPeriodo_Data['Média Atendimentos Período']),go.Line(name='Potencial Equipe',x=consolidaPeriodo_Data.index,y=consolidaPeriodo_Data['Meta Atendimentos']), go.Line(name='Progress',x=consolidaPeriodo_Data.index,y=consolidaPeriodo_Data['Atendimentos'])])
	plot.update_layout(height=1000, width=800)
	st.plotly_chart(plot,use_container_width=True)


	Agrupa_Agentes_Potencial =  df.groupby(['Data','Agente']).sum()
	Agrupa_Agentes_Potencial = Agrupa_Agentes_Potencial.drop(columns=['Ticket','Ação nº'])

	Agrupa_Agentes_Potencial ['Horas Trabalhadas'] = Agrupa_Agentes_Potencial['Minutos Trabalhados']/60
	Agrupa_Agentes_Potencial ['TMA(min)'] = Agrupa_Agentes_Potencial['Minutos Trabalhados']/Agrupa_Agentes_Potencial['Atendimentos']
	Agrupa_Agentes_Potencial ['Atendimentos/Hora']= Agrupa_Agentes_Potencial['Atendimentos'] /Agrupa_Agentes_Potencial['Horas Trabalhadas']

	Agrupa_Agentes_Potencial['TMA(min)'] = Agrupa_Agentes_Potencial['TMA(min)'].astype(str)
	Agrupa_Agentes_Potencial ['Minutos'] = Agrupa_Agentes_Potencial['TMA(min)'].str[0]
	Agrupa_Agentes_Potencial ['Minutos'] = Agrupa_Agentes_Potencial['Minutos'].astype(int)
	Agrupa_Agentes_Potencial ['TMA(min)'] = Agrupa_Agentes_Potencial['TMA(min)'].astype(float)
	Agrupa_Agentes_Potencial['Segundos'] = Agrupa_Agentes_Potencial['TMA(min)'] - Agrupa_Agentes_Potencial['Minutos']
	Agrupa_Agentes_Potencial['Segundos'] = (Agrupa_Agentes_Potencial['Segundos'] * 60).astype(int)
	Agrupa_Agentes_Potencial['Horas Trabalhadas'] = (Agrupa_Agentes_Potencial['Horas Trabalhadas']).round(2)
	Agrupa_Agentes_Potencial ['Aproveitamento Horas Disponíveis'] = Agrupa_Agentes_Potencial ['Minutos Trabalhados']/(Tempo_Disponivel*dias_analisados)
	Agrupa_Agentes_Potencial ['Aproveitamento Horas Disponíveis']=(Agrupa_Agentes_Potencial ['Aproveitamento Horas Disponíveis'] * 100).round(1)

	def to_excel(dataframe):
	    output = BytesIO()
	    writer = pd.ExcelWriter(output, engine='xlsxwriter')
	    dataframe.to_excel(writer, sheet_name='Sheet1')
	    writer.save()
	    processed_data = output.getvalue()
	    return processed_data

	def get_table_download_link(dataframe):
	    """Generates a link allowing the data in a given panda dataframe to be downloaded
	    in:  dataframe
	    out: href string
	    """
	    val = to_excel(dataframe)
	    b64 = base64.b64encode(val)  # val looks like b'...'
	    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Métricas individuais por Datas e por Atendentes</a>' # decode b'abc' => abc

	dataframe = Agrupa_Agentes_Potencial # your dataframe
	st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)

	st.markdown('#')
	st.markdown('#')


	st.header('**Ranking Produtividade**')
	consolidaSemana = df
	RankingSemana = consolidaSemana.groupby('Agente').sum()
	RankingSemana ['Horas Trabalhadas'] = RankingSemana['Minutos Trabalhados']/60
	RankingSemana ['TMA(min)'] = RankingSemana['Minutos Trabalhados']/RankingSemana['Atendimentos']
	RankingSemana ['Atendimentos/Hora']= RankingSemana['Atendimentos'] /RankingSemana['Horas Trabalhadas']
	RankingSemana ['Aproveitamento Horas Disponíveis'] = RankingSemana ['Minutos Trabalhados']/(Tempo_Disponivel*dias_analisados)

	# atribuindo uma nova coluna NOTA
	RankingSemana ['Score'] = ((RankingSemana['Atendimentos']*RankingSemana['Atendimentos/Hora']*RankingSemana['Aproveitamento Horas Disponíveis'])/RankingSemana['TMA(min)'])
	Analise_Desempenho = RankingSemana.sort_values('Score',ascending=False)

	# Primeiro vou add nova coluna para separar TMA(min) e TMA(s)
	Analise_Desempenho['TMA(min)'] = Analise_Desempenho['TMA(min)'].astype(str)
	Analise_Desempenho ['Minutos'] = Analise_Desempenho['TMA(min)'].str[0]
	Analise_Desempenho ['Minutos'] = Analise_Desempenho['Minutos'].astype(int)
	Analise_Desempenho ['TMA(min)'] = Analise_Desempenho['TMA(min)'].astype(float)
	Analise_Desempenho['Segundos'] = Analise_Desempenho['TMA(min)'] - Analise_Desempenho['Minutos']
	Analise_Desempenho['Segundos'] = (Analise_Desempenho['Segundos'] * 60).astype(int)
	Analise_Desempenho['Horas Trabalhadas'] = (Analise_Desempenho['Horas Trabalhadas']).round(2)
	Analise_Desempenho ['Aproveitamento Horas Disponíveis']=(Analise_Desempenho ['Aproveitamento Horas Disponíveis'] * 100).round(1)
	Analise_Desempenho = Analise_Desempenho.drop(columns=['Ticket','Ação nº'])

	st.dataframe(Analise_Desempenho)

	# Aqui o download Ranking Produtividade

	def to_excel(dataframe):
	    output = BytesIO()
	    writer = pd.ExcelWriter(output, engine='xlsxwriter')
	    dataframe.to_excel(writer, sheet_name='Sheet1')
	    writer.save()
	    processed_data = output.getvalue()
	    return processed_data

	def get_table_download_link(dataframe):
	    """Generates a link allowing the data in a given panda dataframe to be downloaded
	    in:  dataframe
	    out: href string
	    """
	    val = to_excel(dataframe)
	    b64 = base64.b64encode(val)  # val looks like b'...'
	    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Ranking Consolidade Produtividade</a>' # decode b'abc' => abc

	dataframe = Analise_Desempenho # your dataframe
	st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)

	st.title('Estatísticas gerais da equipe de CX ')
	columnA,  columnB = st.columns(2)
	with columnA:
		# Declarando as variaveis que representam indicadores relevantes:
		total_atendimentos = Analise_Desempenho['Atendimentos'].sum()
		media_atendimentos = int(Analise_Desempenho['Atendimentos'].mean())
		total_minutos = Analise_Desempenho['Minutos Trabalhados'].sum()
		media_minutos = int(Analise_Desempenho['Minutos Trabalhados'].mean())
		potencial_diario = int(Meta_Atendimentos_Diarios*dias_analisados)
		nota_minimo = Analise_Desempenho["Score"].min()
		nota_minimo = round(nota_minimo,2)
		nota_maxima = Analise_Desempenho["Score"].max()
		nota_maxima = round(nota_maxima,2)
		nota_media = Analise_Desempenho["Score"].mean()
		nota_media = round(nota_media,2)
		tma_maximo = Analise_Desempenho["TMA(min)"].max()
		tma_maximo = round(tma_maximo,2)
		tma_minimo = Analise_Desempenho["TMA(min)"].min()
		tma_minimo = round(tma_minimo,2)
		soma_atendimentos2 = consolidaSemana ['Atendimentos'].sum()
		soma_minutos2 = consolidaSemana ['Minutos Trabalhados'].sum()
		tma_medio = round(soma_minutos2/soma_atendimentos2,2) 


		# tma_medio = Analise_Desempenho["TMA(min)"].mean()
		# tma_medio = round(tma_medio,2)
	# criando a variavel velocidade
		soma_atendimentos1 = consolidaSemana ['Atendimentos'].sum()
		soma_minutos1 = consolidaSemana ['Minutos Trabalhados'].sum()
		horas_trabalhadas1 = soma_minutos1/60 
		media_atendimentos_hora = round(soma_atendimentos1/horas_trabalhadas1,2) 


		# media_atendimentos_hora = Analise_Desempenho['Atendimentos/Hora'].mean()
		# media_atendimentos_hora = round(media_atendimentos_hora,2)
		velocidade_minimo = Analise_Desempenho['Atendimentos/Hora'].min()
		velocidade_minimo = round(velocidade_minimo,2)
		velocidade_maximo = Analise_Desempenho['Atendimentos/Hora'].max()
		velocidade_maximo = round(velocidade_maximo,2)

		st.markdown('#')


		st.write(f"**Total de atendimentos:** {total_atendimentos}")
		st.write(f"**Potencial da Equipe:** {potencial_diario} atendimentos/dia")
		st.write(f"**Média de atendimentos da equipe:** {media_atendimentos} atendimentos por operador")

		st.markdown('#')	

		st.write(f"**TMA Médio:** {tma_medio} minutos")
		st.write(f"**Menor TMA:** {tma_minimo} minutos")
		st.write(f"**Maior TMA:** {tma_maximo} minutos")





		st.markdown('##')

	with columnB:


		st.markdown('#')
		st.write(f"**Velocidade Média da Equipe:** {media_atendimentos_hora} atendimentos/h")
		st.write(f"**Maior Velocidade da Equipe:** {velocidade_maximo} atendimentos/h")
		st.write(f"**Menor Velocidade da Equipe:** {velocidade_minimo} atendimentos/h")	

		st.markdown('##')

		st.write(f"**Score Médio:** {nota_media}")
		st.write(f"**Score Máximo:** {nota_maxima}")
		st.write(f"**Score Mínimo:** {nota_minimo}")

		st.markdown('##')

	st.subheader('KPIS CX')
	C1, C2, C3 = st.columns(3)
	with C1:
		Meta_Atendimentos_Diarios = round(Meta_Atendimentos_Diarios,2)
		st.write(f"**Atendimentos:** {Meta_Atendimentos_Diarios} atendimentos/dia")
	with C2:
		Meta_TMA_Diario = round(Meta_TMA_Diario,2)
		st.write(f"**TMA diário:** {Meta_TMA_Diario} minutos")
	with C3:
		Meta_Velocidade_Diario = round(Meta_Velocidade_Diario,2)
		st.write(f"**Velocidade:** {Meta_Velocidade_Diario} antendimentos/hora")

	st.markdown('##')
	st.markdown('##')

	st.subheader('Ranking Atendimentos')
	Analise_Desempenho_contrario = Analise_Desempenho.sort_values('Score',ascending=True)
	# Grafico_Analise_Desempenho = px.bar(Analise_Desempenho, x=Analise_Desempenho.index , y='Atendimentos' title='Ranking por atendimentos')
	Grafico_Analise_Desempenho = px.bar(Analise_Desempenho_contrario,y=Analise_Desempenho_contrario.index,x='Atendimentos',orientation="v",title="<b>Ranking Produtividade</b>",color_discrete_sequence=["#0083B8"] * len(Analise_Desempenho))
	Grafico_Analise_Desempenho.update_layout(height=1000)


	Analise_Desempenho ['Média Atendimentos Equipe'] = media_atendimentos

	Analise_Desempenho ['Meta Atendimentos'] = potencial_diario
	Grafico_Media_Atendimentos = px.line(Analise_Desempenho,y=Analise_Desempenho.index,x=['Média Atendimentos Equipe'])
	plot = go.Figure(data=[go.Bar(name= 'Atendimentos',x=Analise_Desempenho.index,y=Analise_Desempenho['Atendimentos']),go.Line(name="Média Atendimentos da Equipe",x=Analise_Desempenho.index,y=Analise_Desempenho['Média Atendimentos Equipe']),go.Line(name='Meta Atendimentos Individual',x=Analise_Desempenho.index,y=Analise_Desempenho['Meta Atendimentos'])])
	plot.update_layout(height=1000, width=800)


	st.plotly_chart(plot,use_container_width=True)

	columnS, columnT = st.columns(2)
	with columnS:
		st.subheader('Ranking TMA')
		# Grafico_Analise_Desempenho = px.bar(Analise_Desempenho, x=Analise_Desempenho.index , y='Atendimentos' title='Ranking por atendimentos')
		Grafico_Analise_Desempenho = px.bar(Analise_Desempenho,x=Analise_Desempenho.index,y='TMA(min)',orientation="v",title="<b>TMA</b>",color_discrete_sequence=["#0083B8"] * len(Analise_Desempenho))
		Grafico_Analise_Desempenho.update_layout(height=1000)


		Analise_Desempenho ['Média TMA Equipe'] = tma_medio
		Analise_Desempenho ['Meta TMA'] = Meta_TMA_Diario
		Grafico_Media_Atendimentos = px.line(Analise_Desempenho,y=Analise_Desempenho.index,x=['Média TMA Equipe'])
		plot1 = go.Figure(data=[go.Bar(name= 'TMA',x=Analise_Desempenho.index,y=Analise_Desempenho['TMA(min)']),go.Line(name="Média TMA da Equipe",x=Analise_Desempenho.index,y=Analise_Desempenho['Média TMA Equipe']),go.Line(name='Meta TMA',x=Analise_Desempenho.index,y=Analise_Desempenho['Meta TMA'])])
		plot1.update_layout(height=1000, width=800)
		st.plotly_chart(plot1,use_container_width=True)

	with columnT:
		st.subheader('Ranking Velocidade')
		# Grafico_Analise_Desempenho = px.bar(Analise_Desempenho, x=Analise_Desempenho.index , y='Atendimentos' title='Ranking por atendimentos')
		Grafico_Analise_Desempenho = px.bar(Analise_Desempenho,x=Analise_Desempenho.index,y='Atendimentos/Hora',orientation="v",title="<b>Velocidade</b>")
		Grafico_Analise_Desempenho.update_layout(height=1000)


		Analise_Desempenho ['Velocidade Média Equipe'] = media_atendimentos_hora
		Analise_Desempenho ['Meta Velocidade'] = Meta_Velocidade_Diario
		Grafico_Media_Atendimentos = px.line(Analise_Desempenho,y=Analise_Desempenho.index,x=['Velocidade Média Equipe'])
		plot1 = go.Figure(data=[go.Bar(name= 'Velocidade',x=Analise_Desempenho.index,y=Analise_Desempenho['Atendimentos/Hora']),go.Line(name="Velocidade Média Equipe",x=Analise_Desempenho.index,y=Analise_Desempenho['Velocidade Média Equipe']),go.Line(name='Meta Velocidade',x=Analise_Desempenho.index,y=Analise_Desempenho['Meta Velocidade'])])
		plot1.update_layout(height=1000, width=800)
		st.plotly_chart(plot1,use_container_width=True)



	st.header("Mapeando o **Status** das solicitações atendidas no dia")
	left_column,  right_column = st.columns(2)
	with left_column:
		# mapeando o status

		st.markdown('#')
		st.write('**Ranking STATUS**')
		st.markdown('#')
		Mapeando_Status = df.groupby('Status').sum()
		Mapeando_Status = Mapeando_Status.drop(columns=['Ticket','Ação nº','Minutos Trabalhados'])
		Ranking_Status = Mapeando_Status.sort_values('Atendimentos',ascending=False)
		st.dataframe(Ranking_Status)


	with right_column:
		# Grafico status
		Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
		Grafico_Status.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Grafico_Status.update_layout(title_font_size=20 ,legend_font_size=18, height=420)
		st.plotly_chart(Grafico_Status, use_container_width=True)

	st.header("Mapeando a **Categoria** das solicitações atendidas no dia")
	column1,  column2 = st.columns(2)
	with column1:
		# Ranking Categoria
		st.markdown('#')
		st.write('**Ranking CATEGORIA**')
		Mapeando_Categoria = df.groupby('Categoria').sum()
		Mapeando_Categoria = Mapeando_Categoria.drop(columns=['Ticket','Ação nº','Minutos Trabalhados'])
		Ranking_Categoria = Mapeando_Categoria.sort_values('Atendimentos',ascending=False)
		st.dataframe(Ranking_Categoria)

	with column2:
		# Grafico Categoria
		Ranking_Categoria = Mapeando_Categoria.sort_values('Atendimentos',ascending=True)
		Grafico_Categoria = px.bar(Ranking_Categoria, x='Atendimentos', y=Ranking_Categoria.index, title='Número de atendimentos por Categoria' )
		Grafico_Categoria.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Grafico_Categoria.update_layout(title_font_size=20 ,legend_font_size=18, height=420)
		st.plotly_chart(Grafico_Categoria, use_container_width=True)

	st.header("Mapeando o **Serviço** das solicitações atendidas no dia")
	column3,  column4 = st.columns(2)
	with column3:
		# Ranking Serviço
		st.markdown('#')
		st.markdown('#')
		st.write('**Ranking SERVIÇO**')
		st.markdown('#')

		Mapeando_Servico = df.groupby('Serviço').sum()
		Mapeando_Servico = Mapeando_Servico.drop(columns=['Ticket','Ação nº','Minutos Trabalhados'])
		Ranking_Servico = Mapeando_Servico.sort_values('Atendimentos',ascending=False)
		st.dataframe(Ranking_Servico)
	with column4:
		# Grafico
		Ranking_Servico = Mapeando_Servico.sort_values('Atendimentos',ascending=True)
		Grafico_Servico = px.bar(Ranking_Servico, x='Atendimentos', y=Ranking_Servico.index, title='Número de atendimentos por Categoria' )
		Grafico_Servico.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Grafico_Servico.update_layout(title_font_size=20 ,legend_font_size=5, height=600)
		st.plotly_chart(Grafico_Servico, use_container_width=True)

	st.header("Mapeando os **Parceiros** das solicitações atendidas no dia")
	column5,  column6 = st.columns(2)
	with column5:
		# Ranking Parceiros
		st.markdown('#')
		st.markdown('#')
		st.write('**Ranking PARCEIROS**')
		st.markdown('#')

		Mapeando_Parceiros = df.groupby('Solicitante').sum()
		Mapeando_Parceiros = Mapeando_Parceiros.drop(columns=['Ticket','Ação nº','Minutos Trabalhados'])
		Ranking_Parceiros = Mapeando_Parceiros.sort_values('Atendimentos',ascending=False)
		st.dataframe(Ranking_Parceiros)

	with column6:
		# Grafico
		Ranking_Parceiros = Ranking_Parceiros.sort_values('Atendimentos',ascending=False)
		Ranking_Parceiros = Ranking_Parceiros.head(25)
		Ranking_Parceiros = Ranking_Parceiros.sort_values('Atendimentos',ascending=True)
		Grafico_Parceiros = px.bar(Ranking_Parceiros, x='Atendimentos', y=Ranking_Parceiros.index, title='TOP 25 Parceiros CX' )
		Grafico_Parceiros.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Grafico_Parceiros.update_layout(title_font_size=20 ,legend_font_size=5, height=600)
		st.plotly_chart(Grafico_Parceiros, use_container_width=True)
	#####################################/#####################################################
	# Filter in SideBar
	operador = st.sidebar.multiselect ("Selecione o Agente", options=consolidaSemana['Agente'].unique())
	# squad = st.sidebar.multiselect ("Selecione o Squad", options=df['Squad'].unique(), default=df['Squad'].unique())
	# Resultado da Query
	st.title('Análise de Desempenho Individual')
	st.header('Lista de Atendimentos por Agente selecionado:')
	df_selection_operador = consolidaSemana.query("Agente == @operador")

	#################################################


	#################################################

	st.dataframe(df_selection_operador)

	# Rendimento Individual

	# declarando variaveis relevantes para analise de desempenho individual
	Operador_Atendimentos = df_selection_operador['Atendimentos'].sum()
	Operador_Minutos_Trabalhados = df_selection_operador['Minutos Trabalhados'].sum()
	Operador_TMA = round(Operador_Minutos_Trabalhados / Operador_Atendimentos,2)
	Operador_Influencia_Atendimentos = ((Operador_Atendimentos/total_atendimentos)*100).round(2)


	# Mostrando os indicadores individuais
	columnE , columnF = st.columns(2)
	with columnE:
		st.subheader('Métricas Equipe')
		st.write(f"**Demanda Total Equipe = ** {total_atendimentos} atendimentos")
		st.write(f"**Média de atendimentos da equipe:** {media_atendimentos}")
		st.write(f"**TMA da equipe:** {tma_medio} minutos ")
		st.write(f"**Velocidade Média CX:** {media_atendimentos_hora} atendimentos/h ")
	with columnF:
	# criando a variavel velocidade
		soma_atendimentos = df_selection_operador ['Atendimentos'].sum()
		soma_minutos = df_selection_operador ['Minutos Trabalhados'].sum()
		horas_trabalhadas = soma_minutos/60 
		velocidade_media_operador = round(soma_atendimentos/horas_trabalhadas,2) 



		st.subheader('Métricas Individuais')

		st.write(f"**TIckets:** {Operador_Atendimentos} solicitações atendidas")
		st.write(f"**Contribuição para a Equipe:** {Operador_Influencia_Atendimentos} %")
		st.write(f"**TMA do Agente:** {Operador_TMA} minutos")
		st.write(f"**Velocidade Média Agente:** {velocidade_media_operador} atendimentos/h ")

	# -> Mostrando os graficos PRINCIPAIS

	# Grafico Data Atendimentos
	df_selection_operador['Data']=df_selection_operador['Data'].astype(str)
	Operador_Atendimentos_Data = df_selection_operador.groupby('Data').sum()
	Operador_Atendimentos_Data ['Máximo Dia'] = Operador_Atendimentos_Data ['Atendimentos']
	Operador_Grafico_Atendimentos_Data = px.bar(Operador_Atendimentos_Data, y='Atendimentos', x=Operador_Atendimentos_Data.index, title='Número de atendimentos por Data' )
	# Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
	Operador_Grafico_Atendimentos_Data.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
	Operador_Grafico_Atendimentos_Data.update_layout(title_font_size=20 ,legend_font_size=18, height=420)
	#################--> Aqui vou realizar o processo de plotagem da reta Vermelha guia ( TMA , Atendimentos , Velocidade)
	Grafico_Analise_Desempenho = px.bar(Operador_Atendimentos_Data,y=Operador_Atendimentos_Data.index,x='Atendimentos',orientation="v",title="<b>Ranking Produtividade</b>")
	Grafico_Analise_Desempenho.update_layout(height=1000)

	Operador_Atendimentos_Data ['Média Atendimentos Equipe'] = media_atendimentos/dias_analisados
	############# Agora vou criar a variável Meta_Atendimentos_Diarios
	Operador_Atendimentos_Data ['Meta Atendimentos'] = Meta_Atendimentos_Diarios
	Agentes_Analisados = len(Analise_Desempenho)
	Operador_Atendimentos_Data['Meta Atendimentos Equipe'] = Meta_Atendimentos_Diarios*Agentes_Analisados

	plot = go.Figure(data=[go.Bar(name= 'Atendimentos',x=Operador_Atendimentos_Data.index,y=Operador_Atendimentos_Data['Atendimentos']),go.Line(name="Média Atendimentos Individual",x=Operador_Atendimentos_Data.index,y=Operador_Atendimentos_Data['Média Atendimentos Equipe']), go.Line(name="Meta Atendimentos Individual",x=Operador_Atendimentos_Data.index,y=Operador_Atendimentos_Data['Meta Atendimentos']), go.Line(name="Linha de Tendência",x=Operador_Atendimentos_Data.index,y=Operador_Atendimentos_Data['Atendimentos'])])
	plot.update_layout(title='Atendimentos', height=500)

	st.plotly_chart(plot, use_container_width=True)

	st.markdown('#')

	# Grafico Data TMA

	demandas_datas = df_selection_operador.groupby('Data').sum()

	demandas_datas ['TMA'] = demandas_datas ['Minutos Trabalhados'] / demandas_datas['Atendimentos']
	demandas_datas['Horas Trabalhadas'] = demandas_datas["Minutos Trabalhados"]/60
	demandas_datas ['Atendimentos/Hora'] = demandas_datas['Atendimentos']/demandas_datas['Horas Trabalhadas']

	grafico_atendimentos_Data = px.bar(demandas_datas, y='TMA', x=demandas_datas.index, title='TMA por Data' )
	# Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
	grafico_atendimentos_Data.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
	grafico_atendimentos_Data.update_layout(title_font_size=20 ,legend_font_size=18, height=420)
	#################--> Aqui vou realizar o processo de plotagem da reta Vermelha guia ( TMA , Atendimentos , Velocidade)
	demandas_datas ['Meta TMA'] = Meta_TMA_Diario
	demandas_datas ['TMA Equipe'] = tma_medio

	plot = go.Figure(data=[go.Bar(name= 'TMA',x=demandas_datas.index,y=demandas_datas['TMA']),go.Line(name="TMA Equipe",x=demandas_datas.index,y=demandas_datas['TMA Equipe']), go.Line(name="Meta TMA",x=demandas_datas.index,y=demandas_datas ['Meta TMA']), go.Line(name="Linha de Tendência",x=demandas_datas.index,y=demandas_datas['TMA'])])
	plot.update_layout(title='TMA', height=500)
	st.plotly_chart(plot, use_container_width=True)


	st.markdown('#')	
	# Grafico Data VELOCIDADE!!

	velocidade_datas = px.bar(demandas_datas, y='Atendimentos/Hora', x=demandas_datas.index, title='Atendimentos/Hora' )
		# Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
	velocidade_datas.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
	velocidade_datas.update_layout(title_font_size=20 ,legend_font_size=18, height=420)
		#################--> Aqui vou realizar o processo de plotagem da reta Vermelha guia ( TMA , Atendimentos , Velocidade)

	demandas_datas ['Meta Velocidade'] = Meta_Velocidade_Diario
	demandas_datas ['Velocidade Média Equipe'] = media_atendimentos_hora


	plot = go.Figure(data=[go.Bar(name= 'Velocidade',x=demandas_datas.index,y=demandas_datas['Atendimentos/Hora']),go.Line(name="Velocidade Média da Equipe",x=demandas_datas.index,y=demandas_datas['Velocidade Média Equipe']), go.Line(name="Meta Velocidade",x=demandas_datas.index,y=demandas_datas ['Meta Velocidade']),go.Line(name="Linha de Tendência",x=demandas_datas.index,y=demandas_datas['Atendimentos/Hora'])])
	plot.update_layout(title='Velocidade', height=500)
	st.plotly_chart(plot, use_container_width=True)


	st.subheader('Estatísticas Diárias')	
	# Primeiro vou add nova coluna para separar TMA(min) e TMA(s)
	demandas_datas['TMA'] = demandas_datas['TMA'].astype(str)
	demandas_datas ['Minutos'] = demandas_datas['TMA'].str[0]
	demandas_datas ['Minutos'] = demandas_datas['Minutos'].astype(int)
	demandas_datas ['TMA'] = demandas_datas['TMA'].astype(float)
	demandas_datas['Segundos'] = demandas_datas['TMA'] - demandas_datas['Minutos']
	demandas_datas['Segundos'] = (demandas_datas['Segundos'] * 60).astype(int)
	demandas_datas = demandas_datas.drop(columns=['Ticket','Ação nº','Minutos Trabalhados','Meta TMA','TMA Equipe','Meta Velocidade','Velocidade Média Equipe'])
	demandas_datas ['Aproveitamento Horas Disponíveis'] = demandas_datas ['Horas Trabalhadas']/(Tempo_Disponivel_Horas)

	# atribuindo uma nova coluna NOTA
	demandas_datas ['SCORE'] = ((demandas_datas['Atendimentos']*demandas_datas['Atendimentos/Hora']*demandas_datas['Aproveitamento Horas Disponíveis'])/demandas_datas['TMA'])
	Analise_Desempenho_Data = demandas_datas
	st.dataframe(Analise_Desempenho_Data)

	st.markdown('#')	
	st.write('Aqui vou colocar um botão para download do relatório de desempenho por Datas')
	def to_excel(dataframe):
	    output = BytesIO()
	    writer = pd.ExcelWriter(output, engine='xlsxwriter')
	    dataframe.to_excel(writer, sheet_name='Sheet1')
	    writer.save()
	    processed_data = output.getvalue()
	    return processed_data

	def get_table_download_link(dataframe):
	    """Generates a link allowing the data in a given panda dataframe to be downloaded
	    in:  dataframe
	    out: href string
	    """
	    val = to_excel(dataframe)
	    b64 = base64.b64encode(val)  # val looks like b'...'
	    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download Excel file</a>' # decode b'abc' => abc

	dataframe = demandas_datas # your dataframe
	st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)

	# Mostrando os graficos secundarios

	columnC, columnD = st.columns(2)
	with columnC:

		# Grafico Status
		Operador_Status = df_selection_operador.groupby('Status').sum()
		Operador_Grafico_Status = px.pie(Operador_Status, values='Atendimentos', names=Operador_Status.index, title='Número de atendimentos por Status')
		# Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
		Operador_Grafico_Status.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Operador_Grafico_Status.update_layout(title_font_size=20 ,legend_font_size=18, height=420)
		Operador_Grafico_Status.update_layout(legend_title_side="top left")
		st.plotly_chart(Operador_Grafico_Status, use_container_width=True)
		st.markdown('#')
		# Grafico Serviço
		Operador_Servico = df_selection_operador.groupby('Serviço').sum()
		Operador_Servico = Operador_Servico.sort_values('Atendimentos', ascending=True)
		Operador_Grafico_Servico = px.bar(Operador_Servico, x='Atendimentos', y=Operador_Servico.index, title='Número de atendimentos por Serviço' )
		# Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
		Operador_Grafico_Servico.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Operador_Grafico_Servico.update_layout(title_font_size=20 ,legend_font_size=18, height=600)
		st.plotly_chart(Operador_Grafico_Servico, use_container_width=True)

	with columnD:

		# Grafico Categoria
		Operador_Categoria = df_selection_operador.groupby('Categoria').sum()
		Operador_Categoria = Operador_Categoria.sort_values('Atendimentos',ascending=False)
		Operador_Grafico_Categoria = px.bar(Operador_Categoria, y='Atendimentos', x=Operador_Categoria.index, title='Número de atendimentos por Categoria' )
		# Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
		Operador_Grafico_Categoria.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Operador_Grafico_Categoria.update_layout(title_font_size=20 ,legend_font_size=18, height=420)
		st.plotly_chart(Operador_Grafico_Categoria, use_container_width=True)

		st.markdown('#')

	# Grafico Parceiros
		Mapeando_Parceiros = df_selection_operador.groupby('Solicitante').sum()
		Ranking_Parceiros = Mapeando_Parceiros.sort_values('Atendimentos',ascending=False)
		parceiros_top25 = Ranking_Parceiros.head(25)
		parceiros_top25 = parceiros_top25.sort_values('Atendimentos',ascending=True)
		Grafico_Parceiros = px.bar(parceiros_top25, x='Atendimentos', y=parceiros_top25.index, title='Número de atendimentos por Parceiros' )
		# Grafico_Status = px.pie(Ranking_Status, values='Atendimentos', names=Ranking_Status.index, title='Número de atendimentos por Status' )
		Grafico_Parceiros.update_layout(uniformtext_minsize=18, uniformtext_mode='show')
		Grafico_Parceiros.update_layout(title_font_size=20 ,legend_font_size=18, height=600)
		st.plotly_chart(Grafico_Parceiros, use_container_width=True)



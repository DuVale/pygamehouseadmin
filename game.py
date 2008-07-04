#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Sistema gerenciador de "casas de games"  PyGameHouseAdmin
# Projeto: http://code.google.com/p/pygamehouseadmin/
#
# Por: Carlos Henrique Marques da Cunha Filho
# Email: rickadt@gmail.com
# Site: http://codigobr.wordpress.com/
#
# Este é um software pequeno e simples, para ajudar no gerenciamento de
# casas de games ou fliperamas, escrito em PyGTK, pode ser facilmente
# modificado para outros tipos de estabelecimento que trabalhe com um
# seguimento parecido, como sinucas, boliches, ou qualquer tipo de jogo 
# ou equipamento alugado por tempo.
"""

import pygtk
pygtk.require("2.0")
import gtk, gtk.glade
import time
import datetime
import os.path
import commands
from pysqlite2 import dbapi2 as sqlite
import pango

##########
##########
class game:
	##########
	### Função construtora da classe
	def __init__(self):
		" Emcapsulando o .glade "
		self.itf = gtk.glade.XML('interface.glade')
		
		" Atribuindo os Widgets da interface a variaveis "
		self.janela = self.itf.get_widget('windowMain')
		self.itf.signal_autoconnect(self)
		self.treev = self.itf.get_widget('treeview')
		self.txtHora = self.itf.get_widget('txtHora')
		self.cbTempo = self.itf.get_widget('cbTempo')
		self.lbTermino = self.itf.get_widget('lbTermino')
		self.txtValor = self.itf.get_widget('txtValor')
		self.cbEquipamento = self.itf.get_widget('cbEquipamento')
		self.txtUsuario = self.itf.get_widget('txtUsuario')
		self.cbtPago = self.itf.get_widget('cbtPago')
				
		" chamando funções "
		self.modelAdd()
		self.janela.show_all()
		#self.janela.maximize()
		
		
		" SQLITE "
		" verifica se o banco de dados existe "
		if not os.path.exists('database.db'):
			self.sqlConnect = sqlite.connect('database.db')
			self.sqlCursor = self.sqlConnect.cursor()
			sql = """
		CREATE TABLE aluguel (
		  codigo   INT NOT NULL,
		  hora  CHAR(5),
		  valor   FLOAT,
		  tempo    CHAR(1),
		  equipamento   CHAR(50),
		  usuario   CHAR(50),
		  termino   CHAR(5),
		  pago   CHAR(3),
		  cancelado   CHAR(3),
		  data   DATE,
		  PRIMARY KEY ( codigo )
		)"""
			self.sqlCursor.execute(sql)
			self.sqlConnect.commit()
			
			sql = "INSERT INTO aluguel (codigo) VALUES (0)"
			self.sqlCursor.execute(sql)
			self.sqlConnect.commit()
		else:
			self.sqlConnect = sqlite.connect('database.db')
			self.sqlCursor = self.sqlConnect.cursor()
		
		self.selectRegistros()
		
		gtk.main()
	##########
	
	#########
	### Cria e adiciona um model ao Treeview
	def modelAdd(self):
		self.model = gtk.ListStore(str, str, str, str, str, str, str, str)
		self.treev.set_model(self.model)
		self.col0 = gtk.TreeViewColumn('Pago', gtk.CellRendererText(), text=0)
		self.col1 = gtk.TreeViewColumn('Hora', gtk.CellRendererText(), text=1)
		self.col2 = gtk.TreeViewColumn('Tempo', gtk.CellRendererText(), text=2)
		self.col3 = gtk.TreeViewColumn('Valor', gtk.CellRendererText(), text=3)
		self.col4 = gtk.TreeViewColumn('Equipamento', gtk.CellRendererText(), text=4)
		self.col5 = gtk.TreeViewColumn('Usuario', gtk.CellRendererText(), text=5)
		self.col6 = gtk.TreeViewColumn('Termino', gtk.CellRendererText(), text=6)
		self.col7 = gtk.TreeViewColumn('Código', gtk.CellRendererText(), text=7)
		self.col0.set_min_width(80)
		self.col1.set_min_width(90)
		self.col2.set_min_width(150)
		self.col3.set_min_width(90)
		self.col4.set_min_width(100)
		self.col5.set_min_width(150)
		self.col6.set_min_width(100)
		self.col7.set_min_width(100)
		self.treev.append_column(self.col0)
		self.treev.append_column(self.col1)
		self.treev.append_column(self.col2)
		self.treev.append_column(self.col3)
		self.treev.append_column(self.col4)
		self.treev.append_column(self.col5)
		self.treev.append_column(self.col6)
		self.treev.append_column(self.col7)
	##########
		
	
		
	
	##########
	### Função que cria as mensagens pop-up
	def mensagem(self, tipo, texto):
		if tipo == 'info':
			msg = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, texto)
			msg.set_position(gtk.WIN_POS_CENTER)
			msg.run()
			msg.destroy()
		elif tipo == 'erro':
			msg= gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, texto)
			msg.set_position(gtk.WIN_POS_CENTER)
			msg.run()
			msg.destroy()
		elif tipo == 'quest':
			msg = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, texto)
			msg.set_position(gtk.WIN_POS_CENTER)
			resposta = msg.run()
			msg.destroy()
			return resposta
	##########
	
	
	##########
	### Verifica se algum item do treeview foi selecionado
	def pegaSelecaoTreev(self):
		valor = self.treev.get_cursor()
		n = valor[0]
		if n == None:
			self.mensagem('info', 'Nenhum registro selecionado para Baixa')
			return None
		else:
			registro = self.treev.get_selection()
			registro.set_mode(gtk.SELECTION_MULTIPLE)
			" Pegando a linha selecionada "
			modelo, caminhos = registro.get_selected_rows()
			for caminho in caminhos:
				kiter = modelo.get_iter(caminho)
				cod = modelo.get_value(kiter, 7)
			return cod
	##########
	
	
	##########
	### Função que pega a hora de inicio e calcula a hora do termino
	def pegaTempo(self, widget):
		if self.txtHora.props.text == '':
			hora = time.strftime('%H:%M')
			self.txtHora.props.text = hora
			col = self.cbTempo.get_active()
		else:
			col = self.cbTempo.get_active()
		
		if col == 0:
			" 15 Minutos "
			self.txtValor.props.text = '0.50'
			self.tempTEMPO = '15 Minutos'
			self.horaTermino = self.calcTermino(15)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino),
		elif col == 1:
			" 30 Minutos "
			self.txtValor.props.text = '1.00'
			self.tempTEMPO = '30 Minutos'
			self.horaTermino = self.calcTermino(30)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 2:
			" 1 Hora "
			self.txtValor.props.text = '2.00'
			self.tempTEMPO = '1 Hora'
			self.horaTermino = self.calcTermino(60)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 3:
			" 1 Hora e 30 minutos "
			self.txtValor.props.text = '3.00'
			self.tempTEMPO = '1 Hora e 30 minutos'
			self.horaTermino = self.calcTermino(90)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 4:
			" 2 Horas "
			self.txtValor.props.text = '4.00'
			self.tempTEMPO = '2 Horas'
			self.horaTermino = self.calcTermino(120)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 5:
			" 2 Horas e 30 minutos "
			self.txtValor.props.text = '5.00'
			self.tempTEMPO = '2 Horas e 30 minutos'
			self.horaTermino = self.calcTermino(150)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 6:
			" 3 Horas "
			self.txtValor.props.text = '6.00'
			self.tempTEMPO = '3 Horas'
			self.horaTermino = self.calcTermino(180)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 7:
			" 4 Horas "
			self.txtValor.props.text = '8.00'
			self.tempTEMPO = '4 Horas'
			self.horaTermino = self.calcTermino(240)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 8:
			" 5 Horas "
			self.txtValor.props.text = '10.00'
			self.tempTEMPO = '5 Horas'
			self.horaTermino = self.calcTermino(300)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
		elif col == 9:
			" 6 Horas "
			self.txtValor.props.text = '12.00'
			self.tempTEMPO = '6 Horas'
			self.horaTermino = self.calcTermino(360)
			self.lbTermino.set_text('Hora do termino: '+self.horaTermino)
	##########
	
	
	#########
	### Verifica se o equipamento selecionado não esta em uso
	def pegaEquipamento(self):
		equipamento = self.cbEquipamento.get_active()
		if equipamento == -1:
			self.mensagem('erro', 'Selecione um equipamento')
			return 'cancelar'
		else:
			if equipamento == 0:
				return 'TV 1'
			elif equipamento == 1:
				return 'TV 2'
			elif equipamento == 2:
				return 'TV 3'
			elif equipamento == 3:
				return 'TV 4'
			elif equipamento == 4:
				return 'TV 5'
			elif equipamento == 5:
				return 'TV 6'
			elif equipamento == 6:
				return 'TV 7'
			elif equipamento == 7:
				return 'TV 8'
			elif equipamento == 8:
				return 'TV 9'
			elif equipamento == 9:
				return 'TV 10'
			elif equipamento == 10:
				return 'TV 11'
			elif equipamento == 11:
				return 'TV 12'
			elif equipamento == 12:
				return 'TV 13'
	##########
	
	
	##########
	### Calcula quando o tempo de jogo acabara
	def calcTermino(self, minutos):
		hora = time.strftime('%H:%M')
		h, m = hora.split(':')
		h = int(h)
		m = int(m)
		hora = str(datetime.timedelta(hours=h, minutes=m) + datetime.timedelta(minutes=minutos))
		h, m, s = hora.split(':')
		hora = h+':'+m
		return hora
	##########
	
	
	##########
	### Salva os dados no Banco de dados
	def salvaRegistro(self, widget):
		cod = self.pegaCodigo('aluguel', 'codigo')
		hora = self.txtHora.props.text
		valor = self.txtValor.props.text
		usuario = self.txtUsuario.props.text
		
		termino = self.horaTermino
		tempo = self.tempTEMPO
		
		
		if self.cbtPago.get_active() == True:
			pago = 'SIM'
		else:
			pago = 'NÃO'
		
		" Pega a data do dia "
		data = time.strftime('%Y-%m-%d')
		
		equipamento = self.pegaEquipamento()
		if equipamento != 'cancelar':
			sql = """INSERT INTO aluguel (codigo, hora, tempo, valor,
			equipamento, usuario, termino, pago, cancelado, data)
			VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'NÃO', '%s')
			""" % (cod, hora, tempo, valor, equipamento, usuario, termino, pago, data)
			self.sqlCursor.execute(sql)
			self.sqlConnect.commit()
			
			model = self.treev.get_model()
			model.append([pago, hora, tempo, valor, equipamento, usuario, termino, cod])
			
			" Limpando o formulário "
			self.cbTempo.set_active(-1)
			self.txtHora.props.text = ''
			self.lbTermino.set_text('')
			self.txtValor.props.text = ''
			self.cbEquipamento.set_active(-1)
			self.txtUsuario.props.text = ''
			self.cbtPago.set_active(False)
			" Limpando as Variaveis "
			cod = ''
			hora = ''
			tempo = ''
			self.tempTEMPO = ''
			valor = ''
			usuario = ''
			termino = ''
			pago = ''
	##########
	
	
	##########
	### Delete o registro
	def deleteRegistro(self, widget, data=None):
		cod = self.pegaSelecaoTreev()
		if cod == None:
			mensagem('info', 'Nenhum registro selecionado para Exclusão')
		else:
			resposta = self.mensagem('quest', 'Tem certeza que deseja excluir o registro?')
			if resposta == gtk.RESPONSE_YES:
				" Pegando os dados no DB "
				sql = """UPDATE aluguel SET cancelado = 'SIM' WHERE codigo = %s""" % (cod)
				self.sqlCursor.execute(sql)
				self.sqlConnect.commit()
				
				model = self.treev.get_model()
				model.clear()
				self.selectRegistros()				
	##########
	
	
	##########
	### Alterar o registro
	def baixar(self, widget, data=None):
		cod = self.pegaSelecaoTreev()
		if cod == None:
			self.mensagem('info', 'Nenhum registro selecionado para Baixa')
		else:
			resposta = self.mensagem('quest', 'Tem certeza que deseja baixar o registro?')
			if resposta == gtk.RESPONSE_YES:
				" Pegando os dados no DB "
				sql = """UPDATE aluguel SET pago = 'SIM' WHERE codigo = %s""" % (cod)
				self.sqlCursor.execute(sql)
				self.sqlConnect.commit()
				
				model = self.treev.get_model()
				model.clear()
				self.selectRegistros()	
	##########
	
	
	##########
	### Busca no DB os registros do dia
	def selectRegistros(self):
		data = time.strftime('%Y-%m-%d')
		sql = "SELECT * FROM aluguel WHERE data = '%s' AND cancelado = 'NÃO'" % (data)
		self.sqlCursor.execute(sql)
		dados = self.sqlCursor.fetchall()
		model = self.treev.get_model()
		for linha in dados:
			model.append([linha[7], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[0]])
	##########
	
	
	##########
	### Pega um código válido na tabela do DB
	def pegaCodigo(self, tabela, campo):
		sql = "SELECT max(%s) as cod FROM %s" % (campo, tabela)
		self.sqlCursor.execute(sql)
		result = self.sqlCursor.fetchall()
		cod = 1
		for i in result:
			cod = cod+i[0]
		return cod
	##########
	
	
	##########
	### Exibe o programa em tela cheia
	def setFullscreen(self, widget, data=None):
		self.janela.fullscreen()
	##########
	### Sai do modo Tela cheia
	def setUnfullscreen(self, widget, data=None):
		self.janela.unfullscreen()
	##########
	
	
	##########
	### Mostra a janela de relatórios
	def windowRelatoriosShow(self, widget):
		" Emcapsulando o .glade "
		self.itfRelatorios = gtk.glade.XML('interfaceRelatorios.glade')
		self.janelaRelatorios = self.itfRelatorios.get_widget('windowRelatorios')
		self.txtDataI = self.itfRelatorios.get_widget('txtDataI')
		self.txtDataF = self.itfRelatorios.get_widget('txtDataF')
		self.treevRelatorios = self.itfRelatorios.get_widget('treev')
		self.txtNaoPago = self.itfRelatorios.get_widget('txtNaoPagos')
		self.txtCancelado = self.itfRelatorios.get_widget('txtCancelados')
		self.txtLucroTotal = self.itfRelatorios.get_widget('txtLucroTotal')
		
		" Adicionando imagem ao botão calendario "
		btCalendarioI = self.itfRelatorios.get_widget('btCalendarioI')
		btCalendarioF = self.itfRelatorios.get_widget('btCalendarioF')
		imagem = gtk.Image()
		imagem.set_from_file('icones/calendario.png')
		btCalendarioI.add(imagem)
		imagem = gtk.Image()
		imagem.set_from_file('icones/calendario.png')
		btCalendarioF.add(imagem)
		
		
		" Adicionando um model ao TreeView "
		model = gtk.ListStore(str, str, str, str, str, str, str, str, str, str)
		self.treevRelatorios.set_model(model)
		col0 = gtk.TreeViewColumn('Código', gtk.CellRendererText(), text=0)
		col1 = gtk.TreeViewColumn('Hora', gtk.CellRendererText(), text=1)
		col2 = gtk.TreeViewColumn('Valor', gtk.CellRendererText(), text=2)
		col3 = gtk.TreeViewColumn('Tempo', gtk.CellRendererText(), text=3)
		col4 = gtk.TreeViewColumn('Equipamento', gtk.CellRendererText(), text=4)
		col5 = gtk.TreeViewColumn('Usuario', gtk.CellRendererText(), text=5)
		col6 = gtk.TreeViewColumn('Termino', gtk.CellRendererText(), text=6)
		col7 = gtk.TreeViewColumn('Pago', gtk.CellRendererText(), text=7)
		col8 = gtk.TreeViewColumn('Cancelado', gtk.CellRendererText(), text=8)
		col9 = gtk.TreeViewColumn('Data', gtk.CellRendererText(), text=9)
		col0.set_min_width(80)
		col1.set_min_width(90)
		col2.set_min_width(150)
		col3.set_min_width(90)
		col4.set_min_width(100)
		col5.set_min_width(150)
		col6.set_min_width(100)
		col7.set_min_width(100)
		col8.set_min_width(100)
		col9.set_min_width(100)
		self.treevRelatorios.append_column(col0)
		self.treevRelatorios.append_column(col1)
		self.treevRelatorios.append_column(col2)
		self.treevRelatorios.append_column(col3)
		self.treevRelatorios.append_column(col4)
		self.treevRelatorios.append_column(col5)
		self.treevRelatorios.append_column(col6)
		self.treevRelatorios.append_column(col7)
		self.treevRelatorios.append_column(col8)
		self.treevRelatorios.append_column(col9)
		
		
		self.itfRelatorios.signal_autoconnect(self)
		self.janelaRelatorios.show_all()
	##########
	
	
	##########
	### Mostra a janela de calendario para seleção de data
	def windowCalendarioIShow(self, widget):
		" Emcapsulando o .glade "
		self.itfCalendarioI = gtk.glade.XML('interfaceCalendarioI.glade')
		self.janelaCalendarioI = self.itfCalendarioI.get_widget('windowCalendarioI')
		self.itfCalendarioI.signal_autoconnect(self)
		
		self.calendarioI = self.itfCalendarioI.get_widget('calendarioI')
		
		self.janelaCalendarioI.show_all()
	#########
	#########
	### Pega a dara da janela de calendario e adiciona ao txtData
	def pegaDataInicio(self, widget):
		data = self.calendarioI.get_date()
		ano = data[0]
		mes = data[1]+1
		if mes < 10:
			mes = "0%s" % (mes)
		dia = data[2]
		if dia < 10:
			dia = "0%s" % (dia)
		data = "%s/%s/%s" % (dia, mes, ano)
		self.txtDataI.props.text = data
		self.janelaCalendarioI.destroy()
	#########
	
	
	#########
	### Mostra a janela de calendario para seleção de data
	def windowCalendarioFShow(self, widget):
		" Emcapsulando o .glade "
		self.itfCalendarioF = gtk.glade.XML('interfaceCalendarioF.glade')
		self.janelaCalendarioF = self.itfCalendarioF.get_widget('windowCalendarioF')
		self.itfCalendarioF.signal_autoconnect(self)
		
		self.calendarioF = self.itfCalendarioF.get_widget('calendarioF')
		
		self.janelaCalendarioF.show_all()
	#########
	#########
	### Pega a dara da janela de calendario e adiciona ao txtData
	def pegaDataFim(self, widget):
		data = self.calendarioF.get_date()
		ano = data[0]
		mes = data[1]+1
		if mes < 10:
			mes = "0%s" % (mes)
		dia = data[2]
		if dia < 10:
			dia = "0%s" % (dia)
		data = "%s/%s/%s" % (dia, mes, ano)
		self.txtDataF.props.text = data
		self.janelaCalendarioF.destroy()
	#########
	
	
	#########
	### Gera o relatório de locações de um determinado periodo
	def gerarRelatorio(self, widget):
		" Pegando e preparando as datas "
		dataI = self.txtDataI.props.text
		dia, mes, ano = dataI.split('/')
		dataI = ano+'-'+mes+'-'+dia
		dataF = self.txtDataF.props.text
		dia, mes, ano = dataF.split('/')
		dataF = ano+'-'+mes+'-'+dia
		
		sql = "SELECT * FROM aluguel WHERE data >= '%s' AND data <= '%s'" % (dataI, dataF)
		self.sqlCursor.execute(sql)
		dados = self.sqlCursor.fetchall()
		
		model = self.treevRelatorios.get_model()
		model.clear()
		naoPagos = 0
		cancelados = 0
		lucro = .0
		for linha in dados:
			if linha[7] == 'NÃO':
				naoPagos += 1
			else:
				lucro = lucro + float(linha[2])
			
			if linha[8] == 'SIM':
				cancelados += 1
			
			ano, mes, dia = linha[9].split('-')
			data = dia+'/'+mes+'/'+ano
			model.append([linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7], linha[8], data])
		self.txtNaoPago.props.text = naoPagos
		self.txtCancelado.props.text = cancelados
		self.txtLucroTotal.props.text = lucro
	##########
	
	
	##########
	### Exibe a janea de ajuda
	def windowAjudaShow(self, widget):
		if(os.name == "posix"):
			os.system('firefox ajuda.html')
		elif(os.name == "nt"):
			os.system('iexplorer.exe ajuda.html')
	##########
	
	
	#########
	### Função que Mostra o About do programa
	def windowAboutShow(self, widget):
		" Emcapsulando o .glade "
		self.itfAbout = gtk.glade.XML('interfaceAbout.glade')
		self.janelaAbout = self.itfAbout.get_widget('windowAbout')
		self.itfAbout.signal_autoconnect(self)
		self.janelaAbout.show_all()
	##########
	#########
	### Função que encerra a janela de about
	def sairAbout(self, widget):
		self.janelaAbout.quit()
	##########
	
	
	
	#########
	### Função que encerra o programa
	def sair(self, widget):
		gtk.main_quit()
	##########
		
##########

" Instanciando a classe "
if __name__ == "__main__":
	game = game()

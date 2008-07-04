#!/usr/bin/env python
# -*- coding: utf-8 -*-

class addTempo:
	
	### Adiciona mais tempo de jogo a um registro
	def addTempo(self, widget):
		cod = self.tempCod
		
		tempo = self.self.addTempoTxtTempo.props.text
		tempo = tempo+
		horaTermino = self.addTempoTxtHoraTermino.props.text
		valor = self.valorAddTempo
		pago = self.addTempoCbtPago.get_active()
		
		sql = """UPDATE aluguel SET 
		tempo = '%s', valor = '%s', pago = '%s', termino = '%s'
		WHERE codigo = %s
		"""  % (tempo, valor, pago, horaTermino, cod)
	##########
	
	##########
	### Calcula quando o tempo de jogo acabara para Add tempo
	def calcTerminoAddTempo(self, minutos, hora):
		print '---------------'
		print hora
		print '---------------'
		h, m = hora.split(':')
		h = int(h)
		m = int(m)
		hora = str(datetime.timedelta(hours=h, minutes=m) + datetime.timedelta(minutes=minutos))
		h, m, s = hora.split(':')
		hora = h+':'+m
		print hora
		return hora
	##########
	
	
	##########
	### Pega o tempo do para adicionar mais tempo ao registro
	def pegaTempo(self, widget):
		col = self.addTempoCbTempo.get_active()
		hora = self.tempHora
		if col == 0:
			" 15 Minutos "
			horaTermino = self.calcTerminoAddTempo(15, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '0.50'
		elif col == 1:
			" 30 Minutos "
			horaTermino = self.calcTerminoAddTempo(30, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '1.00'
		elif col == 2:
			" 1 Hora "
			horaTermino = self.calcTerminoAddTempo(60, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '2.00'
		elif col == 3:
			" 1 Hora e 30 minutos"
			horaTermino = self.calcTerminoAddTempo(90, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '3.00'
		elif col == 4:
			" 2 Horas "
			horaTermino = self.calcTerminoAddTempo(120, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '4.00'
		elif col == 5:
			" 2 horas e 30 minutos "
			horaTermino = self.calcTerminoAddTempo(150, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '5.00'
		elif col == 6:
			" 3 Horas "
			horaTermino = self.calcTerminoAddTempo(180, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '6.00'
		elif col == 7:
			" 4 Horas "
			horaTermino = self.calcTerminoAddTempo(240, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '8.00'
		elif col == 8:
			" 5 Horas "
			horaTermino = self.calcTerminoAddTempo(300, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '10.00'
		elif col == 9:
			" 6 Horas "
			horaTermino = self.calcTerminoAddTempo(360, hora)
			self.addTempoTxtHoraTermino.props.text = horaTermino
			self.valorAddTempo = '12.00'
	##########
	
	
	##########
	### mostra a janela para adicionar mais tempo de jogo a um registro
	def windowAddTempoShow(self, widget):
		cod = self.pegaSelecaoTreev()
		self.tempCod = cod
		if cod == None:
			self.mensagem('info', 'Nenhum registro selecionado')
		else:
			" Emcapsulando o .glade "
			self.itfAddTempo = gtk.glade.XML('interfaceAddTempo.glade')
			self.janelaAddTempo = self.itfAddTempo.get_widget('windowAddTempo')
			txtUsuario = self.itfAddTempo.get_widget('txtUsuario')
			txtTempo = self.itfAddTempo.get_widget('txtTempo')
			txtEquipamento = self.itfAddTempo.get_widget('txtEquipamento')
			self.addTempoTxtHora = self.itfAddTempo.get_widget('txtHora')
			self.addTempoTxtHoraTermino = self.itfAddTempo.get_widget('txtHoraTermino')
			self.addTempoCbTempo = self.itfAddTempo.get_widget('cbTempo')
			self.addTempoCbtPago = self.itfAddTempo.get_widget('cbtPago')
			
			self.itfAddTempo.signal_autoconnect(self)
			self.janelaAddTempo.show_all()
			
			" Pegando os dados no DB "
			
			sql = "SELECT * from aluguel WHERE codigo = %s" % (cod)
			self.sqlCursor.execute(sql)
			dados = self.sqlCursor.fetchall()
			for linha in dados:
				txtUsuario.props.text = linha[5]
				self.addTempoTxtHora.props.text = linha[1]
				txtTempo.props.text = linha[3]
				txtEquipamento.props.text = linha[4]
				self.addTempoTxtHoraTermino.props.text = linha[6]
				self.tempHora = linha[6]
				if linha[7] == 'SIM':
					self.addTempoCbtPago.set_active(True)
				else:
					self.addTempoCbtPago.set_active(False)
	##########
	
	


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk, gtk.glade
import time
import datetime
import os.path
import commands
from pysqlite2 import dbapi2 as sqlite
import pango

class addTempo:
	
	def __init__(self):
		self.sqlConnect = sqlite.connect('database.db')
		self.sqlCursor = self.sqlConnect.cursor()
	
	
	### Adiciona mais tempo de jogo a um registro
	def addTempo(self ):
		tempo = self.self.addTempoTxtTempo.props.text
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
	def addTempoCalcTermino(self, minutos, hora):
		h, m = hora.split(':')
		h = int(h)
		m = int(m)
		hora = str(datetime.timedelta(hours=h, minutes=m) + datetime.timedelta(minutes=minutos))
		h, m, s = hora.split(':')
		hora = h+':'+m
		return hora
	##########
	
	
	##########
	### Pega o tempo do para adicionar mais tempo ao registro
	def addTempoPegaTempo(self, hora, tempo):
		if tempo == 0:
			" 15 Minutos "
			horaTermino = self.calcTerminoAddTempo(15, hora)
			valor = 0.50
		elif tempo == 1:
			" 30 Minutos "
			horaTermino = self.calcTerminoAddTempo(30, hora)
			valor = 1.00
		elif tempo == 2:
			" 1 Hora "
			horaTermino = self.calcTerminoAddTempo(60, hora)
			valor = 2.00
		elif tempo == 3:
			" 1 Hora e 30 minutos"
			horaTermino = self.calcTerminoAddTempo(90, hora)
			valor = 3.00
		elif tempo == 4:
			" 2 Horas "
			horaTermino = self.calcTerminoAddTempo(120, hora)
			valor = 4.00
		elif tempo == 5:
			" 2 horas e 30 minutos "
			horaTermino = self.calcTerminoAddTempo(150, hora)
			valor = 5.00
		elif tempo == 6:
			" 3 Horas "
			horaTermino = self.calcTerminoAddTempo(180, hora)
			valor = 6.00
		elif tempo == 7:
			" 4 Horas "
			horaTermino = self.calcTerminoAddTempo(240, hora)
			valor = 8.00
		elif tempo == 8:
			" 5 Horas "
			horaTermino = self.calcTerminoAddTempo(300, hora)
			valor = 10.00
		elif tempo == 9:
			" 6 Horas "
			horaTermino = self.calcTerminoAddTempo(360, hora)
			valor = 12.00
		return horaTermino
		return valor
	##########

import sys, re
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDate, Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage

import numpy as np
import matplotlib.pyplot as plt

import time
import os

from EnergyConfigurations import *


current_time = lambda : time.time()

dir_principal = os.getcwd()

data_folder = dir_principal + '/Data' #.ui files and temporal .png files
file_folder = os.getcwd() + '/Files' #.dat files

if not os.path.exists(data_folder): os.mkdir(data_folder)
if not os.path.exists(file_folder): os.mkdir(file_folder)


class Window(QMainWindow): 
	def __init__(self):
		QMainWindow.__init__(self)
		os.chdir(data_folder)
		uic.loadUi('MagChainConfigEnergy.ui', self)
		os.chdir(dir_principal)

		self.showMaximized()

		#Make plots
		self.plot.clicked.connect(self.make_plots)
		

	def E_barrier_vs_dipole_frac(self, m, d, adimensionalised, N0, Nf, points, dipole_fractions):
	
		E_barrier = []

		file = open('Energy_barrier_vs_dipole_fraction.dat', 'w')
		file.write('#E barrier\tDipole fraction\n')

		for dipole_frac in dipole_fractions:

			energies = EnergyConfigs_AB(m, dipole_frac, d, adimensionalised)

			r, E = energies.energy_barrier(N0, Nf, points)

			times = len(E.shape)

			E_barrier.append(np.amax(E))

			file.write(str(dipole_frac) + '\t' + str(np.amax(E)) + '\n')

		file.close()

		return dipole_fractions, np.array(E_barrier)


	#Make plots
	def make_plots(self):

		#System parameters
		adimensionalised = self.adimensionalise.isChecked()
		dipole_fraction = self.dipole_fraction.value()

		if adimensionalised == True:
			d = 1
			m = 1

		else:

			try:
				m = float(self.m.text())
				d = float(self.m.text())

			except:
				QMessageBox.warning(self, 'Warning!', 'Not dipole moment or diamteter selected. Automatically adimensionalization')
				m = 1
				d = 1

				adimensionalised = True

		
		#Config parameters
		N0 = self.N0.value()
		Nf = self.Nf.value()
		points = self.points.value()

		#Energy barrier vas dipole frac parameters

		init_dipole = self.init_dipole.value()
		final_dipole = self.final_dipole.value()
		points_dipole = self.points_dipole.value()

		#Plot settings
		title = self.title.text()
		xlabel = self.xlabel.text()
		ylabel = self.ylabel.text()
		data_labels = self.data_labels.text().split()
		avg_labels = self.avg_labels.text().split()
		grid = self.grid.isChecked()

		data_linestyles = self.data_ls.text().split()
		avg_linestyles = self.avg_ls.text().split()
		data_colors = self.data_colors.text().split()
		avg_colors = self.avg_colors.text().split()
		data_markers=self.data_markers.text().split()

		plot_avg = self.plot_avg.isChecked()
		default = self.default_2.isChecked()
		legend = self.legend.isChecked()
		inverse_xlim = self.inverse_xlim.isChecked()

		equil = self.equil.value()

		#Customize figure
		right = self.right.value()
		left = self.left.value()
		top = self.top.value()
		bottom = self.bottom.value()
		wspace = self.wspace.value()
		hspace = self.hspace.value()

		width = self.width.value()
		height = self.height.value()

		background = self.background.text()
		borders = self.borders.text()

		#Obtain the arrays
		config_energy = EnergyConfigs_AB(m, dipole_fraction, d, adimensionalised)

		x_array = 0
		y_array = 0

		#First plot

		if self.plot_type.currentText() == 'Head to tail aggregation':

			os.chdir(file_folder)
			x_array, y_array = config_energy.add_dipole_chain(N0, Nf)

		elif self.plot_type.currentText() == 'Lateral aggregation':

			os.chdir(file_folder)
			x_array, y_array = config_energy.add_dipole_laterally(N0, Nf)

		elif self.plot_type.currentText() == 'Add dipole progression':

			os.chdir(file_folder)
			x_array, y_array = config_energy.add_progressive_laterally(N0, Nf, points)


		elif self.plot_type.currentText() == 'Energy barrier':

			os.chdir(file_folder)

			x_array, y_array = config_energy.energy_barrier(N0, Nf, points)

		elif self.plot_type.currentText() == 'Two identical head to tail':

			os.chdir(file_folder)

			x_array, y_array = config_energy.two_identical_chains_linear(N0, Nf)

		elif self.plot_type.currentText() == 'Zippering configuration':

			os.chdir(file_folder)

			x_array, y_array = config_energy.zippering_config(N0, Nf)

		elif self.plot_type.currentText() == 'Energy barrier vs dipole frac':

			os.chdir(file_folder)

			dipole_fractions = np.linspace(init_dipole, final_dipole, points_dipole)

			x_array, y_array = self.E_barrier_vs_dipole_frac(m, d, adimensionalised, N0, Nf, points, dipole_fractions)

		elif self.plot_type.currentText() == 'Add dipole middle chain':

			os.chdir(file_folder)
			x_array, y_array = config_energy.add_dipole_chain_middle(N0, Nf)

		else:
			QMessageBox.warning(self, 'Warning!', 'Unexpected error!')


		#Second plot

		if self.plot_type_2.currentText() == self.plot_type.currentText():

			QMessageBox.warning(self, 'Warning!', 'You are plotting the same plot twice! Set the second plot to "None" or choose a different plot.')

		elif self.plot_type.currentText() == 'Add dipole progression' and self.plot_type_2.currentText() != 'None':

			QMessageBox.warning(self, 'Warning!', 'Unfortunatelly "Add dipole progression" can not be compared.')

		else:


			if self.plot_type_2.currentText() == 'None':

				#Plot the arrays
				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot(x_array, y_array)

				plt.show()

			elif self.plot_type_2.currentText() == 'Head to tail aggregation':

				os.chdir(file_folder)

				x_array_2, y_array_2 = config_energy.add_dipole_chain(N0, Nf)

				new_x_array = [x_array, x_array_2]
				new_y_array = [y_array, y_array_2]

				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot_comparison(new_x_array, new_y_array)

				plt.show()

			elif self.plot_type_2.currentText() == 'Lateral aggregation':

				os.chdir(file_folder)

				x_array_2, y_array_2 = config_energy.add_dipole_laterally(N0, Nf)

				new_x_array = [x_array, x_array_2]
				new_y_array = [y_array, y_array_2]

				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot_comparison(new_x_array, new_y_array)

				plt.show()

			elif self.plot_type_2.currentText() == 'Energy barrier':

				os.chdir(file_folder)

				x_array_2, y_array_2 = config_energy.energy_barrier(N0, Nf, points)

				new_x_array = [x_array, x_array_2]
				new_y_array = [y_array, y_array_2]

				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot_comparison(new_x_array, new_y_array)

				plt.show()

			elif self.plot_type_2.currentText() == 'Two identical head to tail':

				os.chdir(file_folder)

				x_array_2, y_array_2 = config_energy.two_identical_chains_linear(N0, Nf)

				new_x_array = [x_array, x_array_2]
				new_y_array = [y_array, y_array_2]

				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot_comparison(new_x_array, new_y_array)

				plt.show()

			elif self.plot_type_2.currentText() == 'Zippering configuration':

				os.chdir(file_folder)

				x_array_2, y_array_2 = config_energy.zippering_config(N0, Nf)

				new_x_array = [x_array, x_array_2]
				new_y_array = [y_array, y_array_2]

				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot_comparison(new_x_array, new_y_array)

				plt.show()

			elif self.plot_type.currentText() == 'Energy barrier vs dipole frac':

				os.chdir(file_folder)

				dipole_fractions = np.linspace(init_dipole, final_dipole, points_dipole)

				x_array_2, y_array_2 = self.E_barrier_vs_dipole_frac(m, d, adimensionalised, N0, Nf, points, dipole_fractions)

				new_x_array = [x_array, x_array_2]
				new_y_array = [y_array, y_array_2]

				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot_comparison(new_x_array, new_y_array)

				plt.show()

			elif self.plot_type_2.currentText() == 'Add dipole middle chain':

				os.chdir(file_folder)

				x_array_2, y_array_2 = config_energy.add_dipole_chain_middle(N0, Nf)

				new_x_array = [x_array, x_array_2]
				new_y_array = [y_array, y_array_2]

				make_plot = MakePlot(title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders)
				plt = make_plot.plot_comparison(new_x_array, new_y_array)

				plt.show()

	#close event
	def closeEvent(self, event):
		result = QMessageBox.question(self, 'Leaving...','Do you want to exit?', QMessageBox.Yes | QMessageBox.No)
		if result == QMessageBox.Yes:
			event.accept()	
		else:
			event.ignore()

		
app = QApplication(sys.argv)
_window=Window()
_window.show()
app.exec_()
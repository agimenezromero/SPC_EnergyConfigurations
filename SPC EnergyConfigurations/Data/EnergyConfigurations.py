import numpy as np
import matplotlib.pyplot as plt

class EnergyConfigs(object):
	"""docstring for EnergyConfigs"""
	def __init__(self, m, d, adimensionalised):
		
		self.m = m #Magnetic dipole moment
		self.d = d #Particle diameter

		self._mu_0 = 4 * np.pi * 1e-7

		self.U_max = (self._mu_0 * self.m**2) / (2 * np.pi * self.d**2)

		if adimensionalised == True:
			self.d = 1
			self.U_max = 1

	def U(self, r, theta):
		return -self.U_max * (self.d / r)**3 * (1 - 1.5 * np.sin(theta)**2)

	def add_dipole_chain(self, N0, N):
		"""
			Calculates the energy when adding a dipole to linear chains of different sizes
		"""

		E_configs = []
		r = []

		file = open('Head_to_tail_aggregation.dat', 'w')
		file.write('#Particles in chain\tChange in energy\n')

		for i in range(N0, N + 1): #Loop over different chain lenght

			E = 0 #Energy of the configuration

			for j in range(1, i+1): #Loop for particles in current chain

				r_j = j * self.d
				theta_j = 0

				E += self.U(r_j, theta_j)

			file.write(str(i) + '\t' + str(E) + '\n')

			E_configs.append(E)
			r.append(i)

		file.close()

		return np.array(r), np.array(E_configs)

	def add_dipole_laterally(self, N0, N):

		E_configs = []
		r = []

		file = open('Lateral_aggregation.dat', 'w')
		file.write('#Particles in chain\tChange in energy\n')

		for i in range(N0, N+2, 2):
			
			E = 0 #Energy of the configuration

			for j in range(int(i/2)):

				r_j = self.d * np.sqrt((0.75 + (0.5 + j)**2))
				theta_j = np.arctan(np.sqrt(3) / (1 + 2*j))

				E += 2 * self.U(r_j, theta_j)

			file.write(str(i) + '\t' + str(E) + '\n')

			E_configs.append(E)
			r.append(i)

		file.close()

		return np.array(r), np.array(E_configs)

	def add_progressive_laterally(self, N0, Nf, points): #Use even N for simplicity
		'''
			Calculate the energy between the 2 chains depending on de separation of the chains
 			and between the added particle and both chains
 		'''

		h_0 = self.d * np.sqrt(3)/2 #Initial h
		hs = np.linspace(h_0, 0, points) #Array of h

		Energy_N = [] #list to store the energy of each configuration

		file = open('Ad_dipole_progression.dat', 'w')
		file.write('#Relative height\tChange in energy\n')

		for N in range(N0, Nf + 2, 2):

			Energy = []

			file.write('\nN=' + str(N) + '\n')

			for h in hs: #Loop over different configs
				s = 2 * np.sqrt(self.d**2 - h**2) #Separation between chains to let the colloid insert
				E = 0 #Energy for the current configuration

				for i in range(int(N/2)): #Loop over chain particles

					#Energy between the colloid inserting and the rest of chains
					r_i = np.sqrt((np.sqrt(self.d**2 - h**2) + i * self.d)**2 + h**2) #Geometrical considerations (Pitagoras)
					theta_i = np.arctan(h / (np.sqrt(self.d**2 - h**2) + i * self.d)) 

					E += 2*self.U(r_i, theta_i)

					for j in range(int(N/2)):

						#Energy between chains
						r = s + j * self.d + i * self.d
						theta = 0

						E += self.U(r, theta)

				if h == h_0:
					E0 = E

				file.write(str(h) + '\t' + str(E - E0) + '\n')

				Energy.append(E - E0)

			Energy_N.append(Energy)

		return hs, np.array(Energy_N)

	def energy_barrier(self, N0, Nf, points):

		r, E = self.add_progressive_laterally(N0, Nf, points)

		E_barrier = []
		r = np.arange(N0, Nf + 2, 2)

		file = open('Energy_barrier.dat', 'w')
		file.write('#N particles\tEnergy\n')

		for i in range(len(E)):
			E_barrier.append(np.amax(E[i]))

			file.write(str(r[i]) + '\t' + str(np.amax(E[i])) + '\n')

		r = np.arange(N0, Nf + 2, 2)

		return r, np.array(E_barrier)

	def two_identical_chains_linear(self, N0, Nf):

		E_N = []
		r_N = []

		file = open('two_idetical_head_to_tail.dat', 'w')
		file.write('#Number of particles\tChange in energy\n')

		for N in range(N0, Nf + 1): #Loop over all considered chain lengths

			E = 0

			for i in range(N): #Loop over chain particles

				for j in range(N): #Loop over the other chain particles

					#Energy between chains
					r = self.d * (i + j + 1)
					theta = 0

					E += self.U(r, theta)

			E_N.append(E)
			r_N.append(N)

			file.write(str(N) + '\t' + str(E) + '\n')

		return r_N, np.array(E_N)

	def zippering_config(self, N0, Nf):

		h = self.d * np.sqrt(3) / 2
		R = self.d / 2

		E_N = []
		r = []

		file = open('zippering_configuration.dat', 'w')
		file.write('#Number of particles\tChange in energy\n')

		for N in range(N0, Nf + 1):

			E = 0

			for i in range(N):
				for j in range(N):

					if j <= i:
						r_xij = (R + (i-j)*self.d)
					
					else:
						r_xij = (R + (j-i-1)*self.d)
					
					r_ij = np.sqrt(h**2 + r_xij**2)
					theta_ij = np.arctan(h / (R + (i-j)*self.d))

					E += self.U(r_ij, theta_ij)

			E_N.append(E)
			r.append(N)

			file.write(str(N) + '\t' + str(E) + '\n')

		return r, np.array(E_N)

class MakePlot(object):
	def __init__(self, title, xlabel, ylabel, data_labels, avg_labels, grid, data_linestyles, avg_linestyles, data_colors, avg_colors, data_markers, plot_avg, default, legend, inverse_xlim, equil, right, left, top, bottom, wspace, hspace, width, height, background, borders):

		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.data_labels = data_labels
		self.avg_labels = avg_labels
		self.grid = grid

		self.data_linestyles = data_linestyles
		self.avg_linestyles = avg_linestyles
		self.data_colors = data_colors
		self.avg_colors = avg_colors
		self.data_markers = data_markers

		self.plot_avg = plot_avg
		self.default = default
		self.legend = legend
		self.inverse_xlim = inverse_xlim

		self.equil = equil

		#Customize figure
		self.right = right
		self.left = left
		self.top = top
		self.bottom = bottom
		self.wspace = wspace
		self.hspace = hspace

		self.x = width
		self.y = height

		self.background = background
		self.borders = borders

	#Plot analysed data
	def plot(self, x_array, y_array):

		if self.default == False:
			plt.figure(figsize=(self.x, self.y), facecolor=self.background, edgecolor=self.borders)

		if len(y_array.shape) == 1 :

			avg = np.mean(y_array[self.equil :])

			if self.default == True:
				plt.plot(x_array, y_array)

				if self.plot_avg == True:
					plt.plot(x_array, np.linspace(avg, avg, len(x_array)))

			else:
				plt.plot(x_array, y_array, ls=self.data_linestyles[0], marker=self.data_markers[0] , color=self.data_colors[0], label=self.data_labels[0])

				if self.plot_avg == True:
					plt.plot(x_array, np.linspace(avg, avg, len(x_array)), ls=self.avg_linestyles[0], color=self.avg_colors[0], label=self.avg_labels[0] + ' ' + str(round(avg, 3)))

		else:

			if len(self.data_labels) == len(y_array) and len(self.data_colors) == len(y_array) and len(self.data_linestyles) == len(y_array):
				for i in range(len(y_array)):

					avg = np.mean(y_array[i][self.equil :])

					if self.default == True:

						plt.plot(x_array, y_array[i])

						if self.plot_avg == True:
							plt.plot(x_array, np.linspace(avg, avg, len(x_array)))

					else:
						plt.plot(x_array, y_array[i], ls=self.data_linestyles[i], marker=self.data_markers[i], color=self.data_colors[i], label=self.data_labels[i])

						if self.plot_avg == True:
							plt.plot(x_array, np.linspace(avg, avg, len(x_array)), ls='--', color='k', label='Average' + ' ' + str(round(avg, 3)))	

			else:			

				for i in range(len(y_array)):

					avg = np.mean(y_array[i][self.equil :])

					if self.default == True:

						plt.plot(x_array, y_array[i])

						if self.plot_avg == True:
							plt.plot(x_array, np.linspace(avg, avg, len(x_array)))

					else:
						plt.plot(x_array, y_array[i], ls=self.data_linestyles[0], marker=self.data_markers[0], color=self.data_colors[0], label=self.data_labels[0])

						if self.plot_avg == True:
							plt.plot(x_array, np.linspace(avg, avg, len(x_array)), ls='--', color='k', label='Average' + ' ' + str(round(avg, 3)))
							

		plt.title(self.title)
		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)

		if self.inverse_xlim == True:
			plt.xlim(x_array[0], x_array[-1])


		if self.default == False:
			plt.subplots_adjust(right=self.right, left=self.left, top=self.top, bottom=self.bottom, wspace=self.wspace, hspace=self.hspace)
			self.legend == False

		if self.legend == True:
			plt.legend()

		plt.grid(self.grid)
		#plt.show()

		return plt

	def plot_comparison(self, x_array, y_array):

		if self.default == False:
			plt.figure(figsize=(self.x, self.y), facecolor=self.background, edgecolor=self.borders)

		for i in range(2):

			avg = np.mean(y_array[i][self.equil :])

			if self.default == True:
				plt.plot(x_array[i], y_array[i])

				if self.plot_avg == True:
					plt.plot(x_array[i], np.linspace(avg, avg, len(x_array[i])))

			else:
				plt.plot(x_array[i], y_array[i], ls=self.data_linestyles[i], marker=self.data_markers[i] , color=self.data_colors[i], label=self.data_labels[i])

				if self.plot_avg == True:
					plt.plot(x_array[i], np.linspace(avg, avg, len(x_array[i])), ls=self.avg_linestyles[i], color=self.avg_colors[i], label=self.avg_labels[i] + ' ' + str(round(avg, 3)))


			plt.title(self.title)
			plt.xlabel(self.xlabel)
			plt.ylabel(self.ylabel)

			if self.inverse_xlim == True:
				plt.xlim(x_array[-1], x_array[0])

			if self.default == False:
				plt.subplots_adjust(right=self.right, left=self.left, top=self.top, bottom=self.bottom, wspace=self.wspace, hspace=self.hspace)
				self.legend == False

			if self.legend == True:
				plt.legend()

			plt.grid(self.grid)

		return plt



		
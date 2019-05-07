# MagneticChain EnergyConfigurations
A simple graphical interface built in PyQt5 to calculate and analyse the energy of different magnetic configurations.

# Overview
The aim of this program is to simplify and automate the energetic analysis of the different structures formed in colloidal dispersions of superparamagnetic particles under magnetic fields. With this graphical interface the energetic analysis of different kinds of aggregation, including chain formation among others, can be done simply and easily, so anyone with basic or even null programming notions will be able to use all the software features. Although the software use is quite intuitive, a documentation has been written to assure its properly use, so we strongly recommend having a look on it.

Table of contents
=================

<!--ts-->
   * [MagneticChain EnergyConfigurations](#MagneticChain-EnergyConfigurations)
   * [Table of contents](#table-of-contents)
   * [Installation](#installation)
   * [Usage](#usage)
      * [Setting system parameters](#Setting-system-parameters)
      * [Setting configuration parameters](#Setting-configurations-parameters)
      * [Ploting data](#Ploting-data)
      * [Customizing plots](#Customizing-plots)
   * [Examples](#Examples)
   * [Authors](#Authors)
   * [License](#License)
   * [Acknowledgments](#Acknowledgements)
<!--te-->

# Installation
1. Download the project and copy in your prefered directory.
2. You must have the following *python3* packages installed:
   - NumPy
   - Matplotlib
   - PyQt5
3. To run the program simply double-click the MagChain_EnergyConfigurations.pyw file or execute via cmd as `python3 MagChain_EnergyConfigurations.pyw` in the corresponding directory.

# Usage

## Setting system parameters 
First of all the studied system parameters must be set. This are the characteristic parameters of superparamagnetic particles, that is to say their `diameter` and `magnetic dipole moment`. One may prefer to make an adimensionalised study, in order to see more clearly how the energy changes within different configurations compared with the typical energy scale of the system (U*). This adimensionalisation has been implemented so that the user just has to check the `Adimensionalise`checkbox in the interface.

## Setting configuration parameters
This software calculates the energy for different superparamagnetic aggregate configurations or the change of energy when moving from one configuration to another, in order to determine if the studied configurations are possible, stable, or more probable than others. The different configurations implemented are the following:

- `Add dipole linear chains`: Computes the change of energy due the  head-to-tail aggregation of a particle to a linear chain as a function of the number of particles in the chain.
- `Add dipole lateral chains`: Computes the change of energy due the lateral aggregation of a particle to a linear chain as a function of the number of particles in the chain
- `Add dipole progression`: Computes the change of energy due the lateral insertion of a particle in a linear chain as a function of the differents configurations reached and the number of particles in the chain. The initial configuration corresponds to a lateral aggregated and we compute the change of energy respect to this configuration untill we have a linear chain because of the particle insertion. This proces shows an energy barrier that can be studied with the following option.
- `Energy barrier`: Computes the previously mentioned energy barrier.



### Parameters

- `N initial`: Initial length of the chains
- `N final`: Final length of the chains
- `Points`: Number of points reached in `Add dipole progression` method between being a lateral aggregate ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20h%3Dd%5Cfrac%7B%5Csqrt%7B3%7D%7D%7B2%7D) until being a linear one ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20h%3D0)
- `Equil`: This number is used to plot the average from an equilibrium value.




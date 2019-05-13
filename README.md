# Superparamagnetic Chain EnergyConfigurations
A simple graphical interface built in PyQt5 to calculate and analyse the energy of different superparamangetic particle configurations.

# Overview
The aim of this program is to simplify and automate the energetic analysis of the different structures formed in colloidal dispersions of superparamagnetic particles under magnetic fields. With this graphical interface the energetic analysis of different kinds of aggregation, including chain formation among others, can be done simply and easily, so anyone with basic or even null programming notions will be able to use all the software features. Although the software use is quite intuitive, a documentation has been written to assure its properly use, so we strongly recommend having a look on it.

Table of contents
=================

<!--ts-->
   * [Overview](#Overview)
   * [Table of contents](#table-of-contents)
   * [Installation](#installation)
   * [Usage](#usage)
      * [Setting system parameters](#Setting-system-parameters)
      * [Setting configuration parameters](#Setting-configurations-parameters)
      * [Ploting data](#Ploting-data)
      * [Plot customization](#Plot-customization)
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
3. To run the program simply double-click the MagChain_EnergyConfigurations.pyw file or execute via cmd as `python3 SPC_EnergyConfigurations.pyw` in the corresponding directory.

# Usage

## Setting system parameters 
First of all the studied system parameters must be set. This are the characteristic parameters of superparamagnetic particles, that is to say their `diameter` and `magnetic dipole moment`. One may prefer to make an adimensionalised study, in order to see more clearly how the energy changes within different configurations compared with the typical energy scale of the system (U*). This adimensionalisation has been implemented so that the user just has to check the `Adimensionalise`checkbox in the interface.

## Setting configuration parameters
This software calculates the energy for different superparamagnetic aggregate configurations or the change of energy when moving from one configuration to another, in order to determine if the studied configurations are possible, stable, or more probable than others. The different configurations implemented are the following:

- `Head to tail aggregation`: Computes the change of energy due the  head-to-tail aggregation of a particle to a linear chain as a function of the number of particles in the chain.
- `Lateral aggregation`: Computes the change of energy due the lateral aggregation of a particle to a linear chain as a function of the number of particles in the chain. Number of particles in chains should be even for a properly study!
- `Add dipole progression`: Computes the change of energy due the lateral insertion of a particle in a linear chain as a function of the separation between the center of the inserted particle and the line crossing the chain from head to tail. By setting `N final` greater than `N initial` one can study this process for different chain length in the same plot. The initial configuration corresponds to a lateral aggregated and we compute the change of energy respect to this configuration untill we have a linear chain because of the particle insertion. Number of particles in chains should be even for a properly study! This proces shows an energy barrier that can be studied with the following option.
- `Energy barrier`: Computes the previously mentioned energy barrier as a function of the number of particles in the chain. Number of particles in chains should be even for a properly study!
- `Two identical head to tail`: Computes the change of energy due the head-to-tail aggregation of a chain with another of the same length.
- `Zippering configuration`: Computes the change of energy due the lateral aggregation of a chain with another of the same length.

### Parameters
- `N initial`: Initial length of the chains
- `N final`: Final length of the chains
- `Points`: Number of points reached in `Add dipole progression` method between being a lateral aggregate ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20h%3Dd%5Cfrac%7B%5Csqrt%7B3%7D%7D%7B2%7D) until being a linear one ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20h%3D0)
- `Equil`: This number is used to plot the average from an equilibrium value.

## Plotting data
Select the desired plot to visualize in the dropdown menue and click the `plot` button. Automatically a matplotlib.pyplot will be generated.

Some configurations can also be compared, select a different plot in each of the dropdown menues available and click the `plot`button to do it.

## Plot customization
Almost all matplotlib.pyplot parameters can be changed in an easy way by the user. The available ones are the following:

**IMPORTANT**: In order to customize several lines, separe the parameters by a space.

- `Title`: Write here the plot title.
- `xlabel`: Write here the label for the x axis.
- `ylabel`: Write here the label for the y axis.
- `Data labels`: Write here the labels for the different lines that will be set in the legend.
- `Data linestyles`: Write here the linestyles for the different lines ploted following the matplotlib.pyplot [syntax](https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html).
- `Data colors`: Write here the colors for the different lines ploted following the matplotlib.pyplot [syntax](https://matplotlib.org/2.0.2/examples/color/named_colors.html).
- `Data markers`: Write here the markers for the different lines ploted following the matplotlib.pyplot [syntax](https://matplotlib.org/api/markers_api.html).

*The same is applied to the average lines.*

In the line below some checkbox are available:

- `Default`: Set default matplotlib.pyplots settings.
- `Grid`: Plot a background grid.
- `Plot average`: Plot an average computed from the equilibrium value.
- `Legend`: Show the written labels in a legend.
- `Inverse xlim`: Inverse the x axis limits (Use it to plot `add dipole progression` graph)

Finally, you can also customize the ploted figure by changing it's shape, background color or other parameters.

# Authors
* **Àlex Giménez**
* **Jordi Faraudo** - *ICMAB-CSIC, Barcelona*
* **Juan Camacho** - *Universitat Autònoma de Barcelona*

# License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/alexeltsar/SPC_EnergyConfigurations/blob/master/LICENSE) file for details

# Acknowledgments



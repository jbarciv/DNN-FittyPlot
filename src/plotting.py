#!/usr/bin/env python
# coding: utf-8

print("------------------------------------------")
print("Starting to plot... please wait")

######################################################################################################

### basic stuff
import os
from typing import final
import numpy as np
import sys
 
### matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

### for vtk import
# import vtk
# from vtk.util.numpy_support import vtk_to_numpy

### for files
from pathlib import Path

### for globbing (using * for search some pattern)
import glob

######################################################################################################

pgf_with_latex = {                      # setup matplotlib to use latex for output
    'pgf.texsystem': 'pdflatex',        # change this if using xetex or lautex
    'text.usetex': True,                # use LaTeX to write all text
    'font.size' : 10,
    #'font.family': 'sans-serif',
    'font.family': 'serif',
    #'font.serif': ['Computer Modern Roman'],  # blank entries should cause plots
    'font.serif': [],                          # blank entries should cause plots 
    'font.sans-serif': [],                     # to inherit fonts from the document
    'font.monospace': [],
    'text.latex.preamble':r'\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage[detect-all]{siunitx}\usepackage{amsmath}\usepackage{bm}\usepackage{color}'
    #'text.latex.preamble':r'\usepackage{sansmath}\sansmath\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage[detect-all]{siunitx}\usepackage{amsmath}\usepackage{bm}'
    }
mpl.rcParams.update(pgf_with_latex)
plt.rcParams["axes.axisbelow"] = False ### draw axes, ticks and labels always above everything else

######################################################################################################

what_axis = {
    0: r'$\text{Iteration}$',
    1: r'$\text{Time}\quad t\cdot V_S / R_S$',
    2: r'$\text{Time}\quad t / s$',
    3: r'$\text{Needle}\quad$',
    4: r'$\text{Undelcooling}\quad \Delta $' ,
    5: r'$\text{Undercooling}\quad \Delta S$',
    6: r'$\text{Supersaturation}\quad \Omega$',
    7: r'$\text{Supersaturation}\quad \Omega$',
    8: r'$\text{Length}\quad L / R_s$',
    9: r'$\text{Length}\quad$',
    10: r'$\text{Velocity}\quad V / V_s$',
    11: r'$\text{Velocity}\quad V$',
    12: r'$\text{Radius}\quad R / R_s$',
    13: r'$\text{Radius}\quad$',
    14: r'$\text{Péclet}\quad Pe$',
    15: r'$\text{Péclet Iv.}\quad $',
    16: r'$\text{X_tip}\quad V / V_s$',
    17: r'$\text{Y_tip}$',
    18: r'$\text{r_x}\quad$',
    19: r'$\text{r_y}\quad$',
    20: r'$\text{r}\quad$',
    21: r'$\text{Theta}\quad \theta / rad$',
    22: r'$\text{dl[0]}\quad$',
    23: r'$\text{dl[1]}\quad$',
    24: r'$\text{X-offset}\quad$',
    25: r'$\text{X-offset}\quad$',
    26: r'$\text{Num. Needles}\quad$',
    27: r'$\text{Needles\' size}\quad$',
    28: r'$\text{Computation}\quad t/ s$',
    29: r'$\text{max. fluid vel. comp.}\quad$',
    30: r'$\text{Order}\quad$',
    31: r'$\text{X_tip_max}\quad$',
    32: r'$\text{Y_tip_max}\quad$',
    33: r'$\text{X_tip_PB}\quad$',
    34: r'$\text{Y_tip_PB}\quad$',
    35: r'$\text{Dir. X}\quad V / V_s$',
    36: r'$\text{Dir. Y}\quad V / V_s$',
    37: r'$\text{Undercooling ind.}\quad$',
    38: r'$\text{Oversaturation ind.}\quad$'
}
######################################################################################################
##################################################
### column numbers in the needle output files ####
##################################################
LENGTH_RS = 8
LENGTH_SI = 9
VELOCITY_VS = 10
VELOCITY_SI = 11
RADIUS_RS = 12
RADIUS_SI = 13
DELTA = 4
DELTA_IND = 37
OMEGA_IND = 38
OMEGA = 6
PECLET = 14
Y_OFFSET = 25
ACTIVE_NEEDLES = 26
SIZE_NEEDLES = 27
COMPT_TIME = 28
VEL_MAX = 29
ORDER = 30

X_TIP = 16
Y_TIP = 17
RX = 18
RY = 19

X_TIP_MAX = 31
Y_TIP_MAX = 32
X_TIP_PB = 33
Y_TIP_PB = 34

# time_idx = time_s  # WHAT IS THAT?
TIME_RSVS = 1
TIME_S = 2
######################################################################################################

## PLOTTING GENERAL INFO - 'SMALL' GRID PLOT
def plot_small_grid(test_data, plot_name, dimensions):
    print("\t\t Plotting the small grid")
    if dimensions == 0:
        TIME = TIME_RSVS
        VELOCITY = VELOCITY_VS
        LENGTH = LENGTH_RS
        RADIUS = RADIUS_RS
    else:
        TIME = TIME_S
        VELOCITY = VELOCITY_SI
        LENGTH = LENGTH_SI
        RADIUS = RADIUS_SI
    ###########################################################
    # Color setting
    ###########################################################
    ### colors
    color_smooth = 'k'

    ### markers
    marker_smooth = '-'
    ###########################################################
    # Graph labels selection
    ###########################################################
    col_0_1 = TIME_S #ax0
    col_0_2 = DELTA

    col_1_1 = TIME #ax1
    col_1_2 = LENGTH

    col_2_1 = TIME #ax2
    col_2_2 = RADIUS

    col_3_1 = TIME_S #ax3
    col_3_2 = COMPT_TIME

    col_4_1 = TIME  #ax4
    col_4_2 = VELOCITY
    ###########################################################
    fig = plt.figure(figsize = (6.47699,4.7))
    fig.suptitle(plot_name)
    gs = gridspec.GridSpec(nrows = 2, ncols = 3, wspace = .6, hspace = .5)
    ###########################################################
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.tick_params(direction = 'in', which = 'both', bottom = True, top = True, left = True, right = True)
    ax0.minorticks_on()
    #ax0.set_title(r'')

    ###################### 
    ax0.plot(test_data[:, col_0_1], test_data[:, col_0_2]);
    ######################

    #ax0.set_xlabel(r'$\text{Time}\quad t / s$')
    #ax0.set_ylabel(r'$\text{Undercooling}\quad \Delta$')
    ax0.set_xlabel(what_axis[col_0_1])
    ax0.set_ylabel(what_axis[col_0_2])

    ax0.set_ybound(lower = 0, upper = None)
    ax0.set_xbound(lower = 0, upper = None)
    #ax0.legend(ncol = 2, borderpad = 1, borderaxespad = 0.)

    ###########################################################
    ax1 = fig.add_subplot(gs[0, 1])#, sharex=ax0)
    ax1.tick_params(direction = 'in', which = 'both', bottom = True, top = True, left = True, right = True)
    ax1.minorticks_on()
    #ax1.set_title(r'')

    ###################### 
    ax1.plot(test_data[:, col_1_1], test_data[:, col_1_2]);
    ######################

    ax1.set_xlabel(what_axis[col_1_1])
    ax1.set_ylabel(what_axis[col_1_2])

    ax1.set_ybound(lower = 0, upper = None)
    ax1.set_xbound(lower=0, upper=None)
    #ax1.legend(ncol = 2, borderpad = 1, borderaxespad = 0.)

    ###########################################################
    ax2 = fig.add_subplot(gs[0, 2])#, sharex = ax0)
    ax2.tick_params(direction = 'in', which = 'both', bottom = True, top = True, left = True, right = True)
    ax2.minorticks_on()
    #ax2.set_title(r'')

    ###################### 
    ax2.plot(test_data[:, col_2_1], test_data[:, col_2_2]);
    ######################

    ax2.set_xlabel(what_axis[col_2_1])
    ax2.set_ylabel(what_axis[col_2_2])

    radius = list(test_data[:,RADIUS])
    rad_max = np.max(radius)
    rad_mean = np.mean(radius)
        
    if (rad_max / rad_mean) > 7:
            ax2.set_ybound(lower = 0, upper = 5*rad_mean)
    else:
        ax2.set_ybound(lower = 0, upper = None)
    ax2.set_xbound(lower = 0, upper = None)
    #ax2.legend(ncol = 2, borderpad = 1, borderaxespad = 0.)
    ###########################################################
    ax3 = fig.add_subplot(gs[1,0])#, sharex=ax0)
    ax3.tick_params(direction='in', which='both', bottom=True, top=True, left=True, right=True)
    ax3.minorticks_on()
    #ax3.set_title(r'')

    ###################### 
    ax3.plot(test_data[:,col_3_1], test_data[:,col_3_2]);
    ######################

    ax3.set_xlabel(what_axis[col_3_1])
    ax3.set_ylabel(what_axis[col_3_2])

    ax3.set_ybound(lower=0., upper=None)
    ax3.set_xbound(lower=0, upper=None)
    #ax3.legend(ncol=1, borderpad=1, borderaxespad=0.)
    #ax3.legend()
    ###########################################################
    ax4 = fig.add_subplot(gs[1, 1:])#, sharex = ax0)
    ax4.tick_params(direction = 'in', which = 'both', bottom = True, top = True, left = True, right = True)
    ax4.minorticks_on()
    #ax4.set_title(r'')
    ##################################################################
    ### calculate velocity as derivative of the length (smoother) ####
    ##################################################################
    n = 50 #smoothness
    data_time_collapsed = test_data[::n, TIME]
    data_length_collapsed = test_data[::n, LENGTH]
    data_dLdt = np.gradient(data_length_collapsed, data_time_collapsed)
    ###################### NORMAL PLOT (BLUE, NOISY)
    ax4.plot(test_data[:, col_4_1], test_data[:, col_4_2]);
    ###################### SMOOTH PLOT (BLACK, SMOOTH)
    ax4.plot(data_time_collapsed, data_dLdt, marker_smooth, color = color_smooth)
    ######################
    ax4.set_xlabel(what_axis[col_4_1])
    ax4.set_ylabel(what_axis[col_4_2])

    velocity = list(test_data[:,VELOCITY])
    vel_max = np.max(velocity)
    vel_mean = np.mean(velocity)
        
    if (vel_max / vel_mean) > 7:
            ax4.set_ybound(lower = 0, upper = 5*vel_mean)
    else:
        ax4.set_ybound(lower = 0, upper = None)
    ax4.set_xbound(lower = 0, upper = None)
    #ax4.legend(ncol = 1, borderpad = 1, borderaxespad = 0.)
    #ax4.legend()

    ###########################################################
    plt.subplots_adjust(left = .085, right = .975, top = .9, bottom = .1)
    fig.savefig('./' + plot_name + '.pdf', transparent = True, dpi = 600)
######################################################################################################

######################################################################################################
## PLOTTING EACH NEEDLE VELOCITY INFO - 'BIG' GRID
######################################################################################################
def plot_big_grid(survival_needles, needle_list, plot_name, folder_wd, dimensions):
    print("\t\t Plotting the big plots grid")
    if dimensions == 0:
        TIME = TIME_RSVS
        VELOCITY = VELOCITY_VS
        LENGTH = LENGTH_RS
    else:
        TIME = TIME_S
        VELOCITY = VELOCITY_SI
        LENGTH = LENGTH_SI
    ###########################################################
    # Color setting
    ###########################################################
    ### colors
    color_smooth = 'k'

    ### markers
    marker_smooth = '-'
    ###########################################################
    # Setting Grid dimensions
    ###########################################################
    Tot = len(survival_needles) # Number of subplots desired
    Cols = int(Tot ** 0.5)
    Rows = Tot // Cols
    Rows += Tot % Cols
    #Position = range(1, Tot + 1)
    ###########################################################
    # Preparing indexes in wich iterate & removing indexes of empty plots
    ###########################################################
    Row_list = list(range(Rows))
    Col_list = list(range(Cols))
    subplots = []
    for i in Row_list:
        for j in Col_list:
            subplots.append((i,j))
    while Tot < len(subplots):
        subplots.pop()
    ###########################################################
    # Getting data of all the needles before plotting the current needle velocity
    ###########################################################
    needles_vel_max = []
    k = 0
    for i, j in subplots:
        needle_file_path = folder_wd + '/' + needle_list[survival_needles[k]]
        test_data = np.loadtxt(needle_file_path, skiprows = 1)
        velocities = list(test_data[:,VELOCITY])
        vel_max = np.max(velocities)
        needles_vel_max.append(vel_max)
        
    needles_max_mean = np.mean(needles_vel_max)
    ###########################################################
    fig = plt.figure(figsize = (float(Cols*6),float(Rows*3)))
    fig.suptitle(plot_name)
    gs = gridspec.GridSpec(nrows = Rows, ncols = Cols, wspace = .55, hspace = .5)
    ###########################################################
    k = 0
    for i, j in subplots:
        needle_file_path = folder_wd + '/' + needle_list[survival_needles[k]]
        test_data = np.loadtxt(needle_file_path, skiprows = 1)
        ##################################################################
        ### calculate velocity as derivative of the length (smoother) ####
        ##################################################################
        n = 20 #smoothness
        data_time_collapsed = test_data[::n, TIME]
        data_length_collapsed = test_data[::n, LENGTH]
        data_dLdt = np.gradient(data_length_collapsed, data_time_collapsed)
        ##################################################################
        ax = fig.add_subplot(gs[i, j])
        ax.tick_params(direction = 'in', which = 'both', bottom = True, top = True, left = True, right = True)
        ax.minorticks_on()
        ax.set_title(r'$\text{Needle}$ %d' %survival_needles[k])
        ###################### 
        ax.plot(test_data[:, TIME], test_data[:, VELOCITY])
        ax.plot(data_time_collapsed, data_dLdt, marker_smooth, color=color_smooth)
        ######################

        ax.set_xlabel(what_axis[TIME])
        ax.set_ylabel(what_axis[VELOCITY])
        
        velocity = list(test_data[:,VELOCITY])
        vel_max = np.max(velocity)
        vel_mean = np.mean(velocity)
        
        if (vel_max / vel_mean) > 7:
            if (5 * vel_mean) > needles_max_mean:
                ax.set_ybound(lower = 0, upper = (needles_max_mean + vel_mean))
            else:
                ax.set_ybound(lower = 0, upper = 5*vel_mean)
        else:
            ax.set_ybound(lower = 0, upper = None)
        ax.set_xbound(lower = 0, upper = None)
        #print(needles_max_mean, vel_max, vel_mean, vel_max/vel_mean, 5*vel_mean)
        #ax.legend(ncol = 2, borderpad = 1, borderaxespad = 0.)
        ###########################################################
        plt.subplots_adjust(left = .09, right = .975, top = .95, bottom = .1)
        fig.savefig('./' + plot_name + '.pdf', transparent = True, dpi = 600)
        plt.close(fig)
        k = k + 1
        
######################################################################################################
# FUNCTION FOR REACHING THE LAST LINE IN THE FILE (AND OTHER MINOR CHANGES)
def last_line_from_file(path_to_file):
    with open(path_to_file, "r") as f:
        last_line = f.readlines()[-1]
        last_line = list(last_line.split(" \t"))   # converting from string to list
        last_line = last_line[:-1]                 # removing the last element (/n) of the list
    return last_line

######################################################################################################
# FUNCTION FOR CHECKING FOR AN ALREADY DONE PLOT
def already_plotted(initial_cwd, folder):
    os.chdir(initial_cwd + '/' + folder)
    folder_wd = os.getcwd()

    file_needleYmax = glob.glob("**needleYmax.dat")
    file_Ymax = str(file_needleYmax[0])
    last_line_Ymax = last_line_from_file(folder_wd + '/' + file_Ymax)
    current_time = float(last_line_Ymax[TIME_RSVS])

    file_Param = glob.glob("**_Param.txt")
    file_Param = str(file_Param[0])
    with open(file_Param,"r") as lines:
        for line in lines:
            if " Time = " in line:
                this_line = line.lstrip(" Time = ")
                pos = this_line.find(".")
                final_time = float(this_line[:pos])
    current_time = round(current_time) + 1
    final_time = round (final_time)
    if current_time >= final_time:
        return 1
    else:
        return 0

######################################################################################################
### PLOT WHATEVER SIMULATION FOLDER -> DOING ALL THE REQUIRED PLOTS
######################################################################################################
def plot_for_this_folder(initial_cwd, work_path, PLOT_ALL):
    
    os.chdir(initial_cwd)
    simulation_plots = initial_cwd + '/simulation_plots'
    small_plots = simulation_plots + '/small_grid'

    if os.path.exists(simulation_plots):
        pass
    else:
        os.mkdir(simulation_plots)
        print("\n ... creating /simulation_plots directory!")

    folders_list = glob.glob("v**_**_**_**_**_**_**_**")
    for folder in folders_list:
        os.chdir(initial_cwd + '/' + folder)
        folder_wd = os.getcwd()
        print("\t", folder_wd)
        if PLOT_ALL == 0:
            if already_plotted(initial_cwd, folder):
                print("Skipping plot...")
                continue
        # Data for small plot
        file_needleYmax = glob.glob("**needleYmax.dat")
        needleYmax_file_path = folder_wd + '/' + str(file_needleYmax[0])
        test_data = np.loadtxt(needleYmax_file_path, skiprows = 1)
        # Data for big plot
        needle_list = glob.glob("**needle0**.dat")
        needle_list.sort()
        y_tip = []
        for file in needle_list:
            last_line = last_line_from_file(folder_wd + '/' + file)
            y_tip.append(float(last_line[Y_TIP]))
        i = 0
        survival_needles = list(range(len(y_tip)))
        for tip in y_tip:
            if tip < (0.1*np.max(y_tip)):
                survival_needles.remove(i)
            i = i + 1

        os.chdir(simulation_plots)
        plot_name = folder[: folder.rfind('_G')]
        ## Plotting small and big plots
        # 0: dimensionless; 1: with dimensions

        if os.path.exists(small_plots):
            pass
        else:
            os.mkdir(small_plots)

        os.chdir(small_plots)
        plot_small_grid(test_data, plot_name, 1)

        os.chdir(simulation_plots) 
        plot_big_grid(survival_needles, needle_list, plot_name, folder_wd, 1)
        
    os.chdir(work_path)



def main():
    # If you are at home use: plotting 1; if at Imdea: plotting 0 is fine of whatever other number
    n = int(sys.argv[1])
    if n == 0:
        work_path = '/home/josep/Documents/IMDEA/Simulations'
        PLOT_ALL = 0
    elif n == 1:
        work_path = '/home/josepbarbera/Documents/Simulations'
        PLOT_ALL = 0
    elif n == 2:
        print("Plotting the lastest simulations performed (all the folder)")
        PLOT_ALL = 1
        work_path = '/home/josepbarbera/Documents/Simulations'
        folder_directory = '/home/josepbarbera/Documents/Simulations/Partition_coefficient_0.2'
        plot_for_this_folder(folder_directory, work_path, PLOT_ALL)
        exit(1)
    elif n == 3:
        print("Plotting the Partition_coefficient folder")
        PLOT_ALL = 1
        work_path = '/home/josepbarbera/Documents/Simulations'
        folder_directory = '/home/josepbarbera/Documents/Simulations/Partition_coefficient_0.7'
        plot_for_this_folder(folder_directory, work_path, PLOT_ALL)
        exit(1)
    elif n == 99:
        work_path = '/home/josepbarbera/Documents/Simulations'
        PLOT_ALL = 1
    
    os.chdir(work_path)
    folders = os.listdir()
    for folder in folders:
        if os.path.isdir(folder):
            folder_directory = work_path + '/' + folder
            print("\nI'm in this folder: ", folder)
            plot_for_this_folder(folder_directory, work_path, PLOT_ALL)

main()

print("------------------------------------------")



from os.path import join as filejoin
import glob
import numpy as np
import matplotlib.pyplot as plt
import functions as f

from scipy import optimize

### ----------File Path -----------###
directory = 'A:\Programming\Data\EMFC5'
file_path = glob.glob(filejoin(directory, '*.dat'))
##For Testing###
# directory1 = 'A:\Programming\dataTest'
# file_path = glob.glob(filejoin(directory1, '*.dat'))

### ------------ Calling dict_files functions to make a dictionary that is sorted by timestamps ------------###
dictionary_of_files = f.dict_files(file_path)
ID = {'TIME': 0,'RESISTANCE':1,'TRANSVERSAL RESISTANCE': 16,}

## ---------- Moving Average to Smooth slightly the data ---------##
moving_average = [f.do_movingaverage(file)for file in dictionary_of_files.values()]

## ---------- Means of all columns for all files -----------##
mean_of_all_columns = f.meansofallcolumns(moving_average)

##------List of name files = hCools_list --------##
hCools_list = dictionary_of_files.keys()
hCools_list = f.findHcools(hCools_list)

## ------------ List of Data to be Evaluated ---------##
time_list_values       = [value_[ID['TIME']]for value_ in mean_of_all_columns]
transversal_resistance = [value_[ID['TRANSVERSAL RESISTANCE']] for value_ in mean_of_all_columns]

## ----------- Time in units for Plotting ------------##
time_lst_in_secs = f.timeinsecs(moving_average,time_list_values)

## ------------ Human Readable Timing ----------------##
date = f.timestamps(time_list_values)
print(date)

## ----------- Frequency Rate of the Test ------------##
frequency = f.frequencysample(time_list_values)
cutoff = 0.1

## ------------ Filtering y-axis ---------------------##
ydrift = f.butter_lowpass_filter(transversal_resistance,cutoff,order=8)

final = moving_average[1][0,0]
initial = moving_average[0][0,0]
print('Final: {}, Initial: {}',final, initial)




''' ************ Plotting ******************'''

########## Figures for Plotting ##########
fig1, (ax1) = plt.subplots(1)
fig2, (ax2) = plt.subplots(1)
fig3, (ax3) = plt.subplots(1)
fig4, (ax4) = plt.subplots(1)

labellist = ['Non-Filtered Data','Filtered Data','Subtracted']

f.dolineplot(time_lst_in_secs,ydrift,labellist[1],ax1)
f.dolineplot(time_lst_in_secs,transversal_resistance,labellist[0],ax1)

subtractedaxis = f.subtract_yaxis(ydrift,transversal_resistance)
subtractedaxis1 = f._removeoutlayers(subtractedaxis)

f.doscatterplot(hCools_list,transversal_resistance,labellist[0],ax3)
f.doscatterplot(hCools_list,ydrift,labellist[1],ax3)

f.doscatterplot(hCools_list,subtractedaxis,labellist[2],ax2)
#f.doscatterplot(hCools_list[:len(subtractedaxis1)],subtractedaxis1,labellist[2],ax2)

#p1,pcov = optimize.curve_fit(f.hyperbolic(transversal_resistance),hCools_list,transversal_resistance,p0=[2,2])

#plt.plot(hCools_list, f.hyperbolic(hCools_list, p1[0], p1[1]),label='Fitted function')
#f.doscatterplot(transversal_resistance,f.hyperbolic(transversal_resistance),labellist[0],ax4)

plt.show()


##TEST###
# first2pairs = {k: dictionary_of_files[k] for k in list(dictionary_of_files)[:2]}
# print(first2pairs)
# print(moving_average[:5])





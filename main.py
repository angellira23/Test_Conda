from os.path import join as filejoin
import glob
import numpy as np
import matplotlib.pyplot as plt
import functions as f
import operator


directory = 'A:\Programming\Data\EMFC5'
#directory = 'A:\Programming\dataTest'
file_path = glob.glob(filejoin(directory, '*.dat'))

dictionary_of_files = f.dict_files(file_path)
ID = {'TIME': 0,'RESISTANCE':1,'TRANSVERSAL RESISTANCE': 16,}

moving_average = [f.do_movingaverage(file)for file in dictionary_of_files.values()]
##TEST###
# first2pairs = {k: dictionary_of_files[k] for k in list(dictionary_of_files)[:2]}
# print(first2pairs)
# print(moving_average[:5])

hCools_list = f.findHcools(file_path)
mean_of_all_columns = f.meansofallcolumns(moving_average)

frequency = f.frequencysample(mean_of_all_columns[0])

time_list_values       = [value_of[0]for value_of in mean_of_all_columns]
transversal_resistance = [value_of[16] for value_of in mean_of_all_columns]
#print(list(dictionary_of_files.items())[])
time_lst_in_secs = f.timeinsecs(moving_average,time_list_values)

frequency = f.frequencysample(time_list_values)
cutoff = 0.1

y_filtered = f.butter_lowpass_filter(transversal_resistance,cutoff,frequency,order=8)
########## Variables for Plotting ##########
fig1, (ax1) = plt.subplots(1)
fig2, (ax2) = plt.subplots(1)



labellist = ['Non-Filtered Data','Filtered Data','Subtracted']

f.dolineplot(time_lst_in_secs,y_filtered,labellist[1],ax1)
f.dolineplot(time_lst_in_secs,transversal_resistance,labellist[0],ax1)

final_yaxis = f.subtract_yaxis(transversal_resistance,y_filtered)

f.doscatterplot(time_lst_in_secs,final_yaxis,labellist[2],ax2)

plt.show()








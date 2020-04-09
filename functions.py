import numpy as np
import re
from scipy.signal import butter,filtfilt


def dict_files(filepath_lst):
    dictoffiles = {}
    for namefile in filepath_lst:
        content_file = np.loadtxt(namefile)
        dictoffiles[namefile] = content_file
    ## Sorting files according to content array
    sorted_dictoffiles = {keys: values for keys, values in sorted(dictoffiles.items(), key=lambda item: item[1][0, 0])}
    return sorted_dictoffiles

def do_movingaverage(arr):
    result = (arr[:-1, :] + arr[1:, :]) * 0.5
    return result

def findHcools(filename_lst):
    values_filelst = []
    for strings in filename_lst:
        lst_numberStr = re.findall(r'[*+-]?\d+\.\d+', strings)
        values_filelst.append(float(lst_numberStr[0]))
    return values_filelst

def meansofallcolumns(lst):            # Averages of all columns => axis =0. Averages of all rows => axis = 1
    meansvalues = [i.mean(axis=0) for i in lst]
    return meansvalues

def timeinsecs(lstofarrays,axislist):
    reference_time = lstofarrays[0][0, 0]
    print('Try to put the date as human reading',reference_time)
    axistoplot = [(x - reference_time) * 1e-4 for x in axislist]
    return axistoplot

# def difference(lst):
# #     for i in range(len(lst) - 1):
# #         subtraction = lst[i + 1] - lst[i]
# #     return subtraction

def frequencysample(timelst):
    dt = np.mean(np.diff(timelst))
    frequency = 1/dt
    return frequency

def butter_lowpass_filter(data, cutoff, fs, order):
    #Get the filter coefficients
    coef1, coef2 = butter(order, cutoff, btype='low', analog=False)
    filtered_yaxis = filtfilt(coef1, coef2, data)
    return filtered_yaxis


def coherence_plot(y1coord, y2coord, freq, ax=None):
    ax = ax
    cxy, f = ax.cohere(y1coord, y2coord, NFFT=10)
    ax.set_ylabel('Coherence between \n Original Data - Filtered Data \n [Transversal Resistance]')
    return cxy, f

def doscatterplot(xcoord,ycoord,labellist,ax=None):
    ax = ax
    ax.scatter(xcoord, ycoord,label=labellist)
    # ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
    ax.legend()
    ax.grid('On')
    ax.set_ylabel('Transversal Resistance [\u03A9]')
    ax.set_xlabel('HCools [T]')
    ax.set_title('Transversal Resistance [\u03A9] vs HCools [T]' )
    return

def dolineplot(xcoord,ycoord,labellist,ax=None):
    ax=ax
    ax.plot(xcoord,ycoord, label= labellist)
    ax.legend()
    ax.grid('On')
    ax.set_ylabel('Transversal Resistance [\u03A9]')
    ax.set_xlabel('Time [s]')
    ax.set_title('Transversal Resistance [\u03A9] vs Time [s]' )
    return

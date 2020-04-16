from os.path import join as filejoin
import glob
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.signal import butter,filtfilt
# A = [np.array([[1, 2, 3],[1, 2, 3],[1, 2, 3]]),np.array([[50,6,7],[5,6,7],[5,6,7]]),np.array([[7,8,9],[7,8,9],[7,8,9]])]
IDaxis ={'TIME':0,'RESISTANCE':16}

# directory1 = 'A:\Programming\dataTest'
# file_path = glob.glob(filejoin(directory1, '*.txt'))
directory = 'A:\Programming\Data\EMFC5'
file_path = glob.glob(filejoin(directory, '*.dat'))

class DoAnalysis:
    def __init__(self,filepath,IDxaxis,IDyaxis):
        self.filepath = filepath
        self.IDxaxis = IDxaxis
        self.IDyaxis = IDyaxis

    ## Constants ##
    CUTTOFF = 0.1
    ORDER = 8
    AXISNAMES_DICT = {'TIME [ts]':0,'TRANSVERSAL RESISTANCE [\u03A9]':16}###After do a list with all the column names
    AXISNAMES_LST = list(AXISNAMES_DICT.keys())


    def dict_files(self):
        dictoffiles = {}
        for namefile in self.filepath:
            content_file = np.loadtxt(namefile)
            dictoffiles[namefile] = content_file
        ## Sorting files according to content array
        sorted_dictoffiles = {keys: values for keys, values in
                              sorted(dictoffiles.items(), key=lambda item: item[1][0, 0])}
        return sorted_dictoffiles

    def do_movingaverage(self):
        result = []
        for i in self.dict_files().values():
            result.append((i[:-1, :] + i[1:, :]) * 0.5)
        return result

    def meanvalues(self):
        meanvals = [i.mean(axis=0) for i in self.do_movingaverage()]
        return meanvals

    def _getAxis(self):
        xaxis = [item[self.IDxaxis] for item in self.meanvalues()]
        yaxis = [item[self.IDyaxis] for item in self.meanvalues()]
        return (xaxis,yaxis)

    def timeinsecs(self):
        reference_time = self.do_movingaverage()[0][0, 0]
        #print('Try to put the date as human reading', reference_time)
        axistoplot = [(x - reference_time) *1e-4 for x in self._getAxis()[0]]
        return axistoplot

    def _removeoutlayers(self):
        elements = np.array(self._getAxis()[1])
        mean = np.mean(elements,axis=0)
        st   = np.std(elements,axis=0)
        upperBond = [ x for x in elements if (x > mean - 2*st)]
        final     = [ x for x in upperBond if (x < mean + 2*st)]
        print('Tamanho Initial',len(self._getAxis()[1]))
        print('Tamanho do Final',len(final))
        return final

    def frequencysample(self):
        dt = [item[self.IDxaxis]for item in self.meanvalues()]
        dt = np.mean(np.diff(dt))
        frequency = 1 / dt
        return frequency


    def _butterlowfilter(self):
        y_tofilter = self._getAxis()[1]
        coef1, coef2 = butter(self.ORDER, self.CUTTOFF, btype='low', analog=False)
        filtered_yaxis = filtfilt(coef1, coef2, y_tofilter)
        return filtered_yaxis

    def _dolinePlot(self):
        plt.plot(self.timeinsecs(),self._getAxis()[1])
        plt.plot(self.timeinsecs(),self._butterlowfilter())
        plt.xlabel(str(self.AXISNAMES_LST[0]))
        plt.ylabel(str(self.AXISNAMES_LST[1]))
        plt.show()
        return

    def findHcools(self):
        values_filelst = []
        for strings in self.dict_files().keys():
            lst_numberStr = re.findall(r'[*+-]?\d+\.\d+', strings)
            values_filelst.append(float(lst_numberStr[0]))
        return values_filelst

    def _doscatterplot(self):
        plt.scatter(self.findHcools(), self._getAxis()[1])
        plt.scatter(self.findHcools(), self._butterlowfilter())
        plt.xlabel('Hcools [T]')
        plt.ylabel(self.AXISNAMES_LST[1])
        plt.show()
        return

    def subtract_yaxis(self):
        # Subtract the filtered data - Original Data
        y_result = np.array(self._butterlowfilter()) - np.array(self._getAxis()[1])
        return y_result

    def _scatterplotsub(self):
        plt.scatter(self.findHcools(), self.subtract_yaxis())
        plt.show()


    # def _scatterplotsub(self):
    #     newxaxis = self.findHcools()[:len(self._removeoutlayers())]
    #     plt.scatter(newxaxis,self._removeoutlayers())
    #     plt.show()

    # def stddeviation(self):
    #     stddev = [i.std(axis=0)for i in self.arr]
    #     stdref = np.mean(stddev)
    #     for i in stddev:
    #         if i > stdref:
    #             stddev.remove(i)
    #     return stddev



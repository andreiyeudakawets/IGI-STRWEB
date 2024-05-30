from math import fabs
from inputs import input_float
import math
from statistics import mean, median, mode, variance
import matplotlib.pyplot as plt
import numpy as np

class SeriesPlotBuilder:
    def __init__(self, series, iterations):
        self._series = series
        self._iterations = iterations

    def showPlot(self):
        x = np.linspace(-0.99, 0.99, 200)
        y1 = np.arcsin(x)
        y2 = sum((fact(2*n)*np.power(x,2*n+1)) / np.power(4,n)/np.power(fact(n), 2)/(2*n+1) for n in range(self._iterations))
        #plt.style.use('_mpl-gallery')
        plt.plot(x, y1, label='arcsin(x)', color='r')
        plt.plot(x, y2, label='Series', color='g')
        plt.subplots_adjust(bottom=0.05, left=0.05)

        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Plots')
        plt.text(-1.05, 85, 'There are two plots:\nred is our math function\ngreen is our series ')
        #plt.annotate('Annotation', (-1.05, 80))

        plt.annotate("Пересечение графика с Oy/Ox", 
                     xy=(0, 0), 
                     xytext=(0, -1),
                     arrowprops=dict(facecolor="blue", shrink=0.04, width = 0.5))

        plt.grid(True)
        figure = plt.gcf()
        figure.set_size_inches(16, 9)
        plt.savefig(r'C:\Users\Andrei\PycharmProjects\IGI4\plots.png', dpi=300)
        plt.show()

class Series:
    def __init__(self, x, eps):
        self._series = []
        self._x = x
        self._eps = eps
        #self._attribute_calculator = SeriesAttributesCalculator()

    def calculateSeries(self):
        """function for calculating sum of series with given accuracy"""
        n = 0
        series = []
        seriesResult = 0.0
        while True:
            try:
                series.append((fact(2*n)*math.pow(self._x,2*n+1)) / math.pow(4,n)/math.pow(fact(n), 2)/(2*n+1))
                seriesResult += (fact(2*n)*math.pow(self._x,2*n+1))/math.pow(4,n)/math.pow(fact(n), 2)/(2*n+1)    
            except Exception:
                print("Argumement for factorial is too big. Try decreasing the precision")
                seriesResult = None
                break
            
            if fabs(series[int(n)]) <= self._eps:
                print(f"x = {self._x}, n = {n}, F(x) = {round(seriesResult, 10)}, Math F(x) = {math.asin(self._x)}"
                      f", eps = {self._eps}")
                
                print(f"average of series elements: {mean(series)}\n"
                      f"median: {median(series)}\n"
                      f"mode: {mode(series)}\n"
                      f"dispersion: {variance(series)} {np.var(series)}\n"
                      f"mean deviation: {np.std(series)}\n")
                return series, n

            n += 1.0

        print("max count of iterations")
        return

def fact(a):
    res = 1.0
    while True:
        if a != 0:
            res *= a
        a-=1
        if a <= 0.0:
            break

    return res 


def task3():
        """function for performing third task"""
        while True:
            x = input_float('input x (-1 < x < 1)')
            if fabs(x) >= 1:
                print("incorrect input.")
                continue
            eps = input_float('please, input eps')
            series = Series(x, eps)
            series_lst, n = series.calculateSeries()

            seriesPlotBuilder = SeriesPlotBuilder(series_lst, int(n))
            seriesPlotBuilder.showPlot()
            return
        


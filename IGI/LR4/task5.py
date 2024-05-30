
import numpy as np
from inputs import try_input_int as input_int

class NumerPy():
    
    def create_array(self, size):
        if size > 0:
            arr = np.random.randint(-20, 20, size)
        return arr

    def create_matrix(self, n, m):
        """
        Initialization of our matrix
        """
        matrix = np.empty((n, m))
        while True:
            option = input_int("1 - random\n2 - by user")
            
            if option == 1:
                for i in range(n):
                    for j in range(m):
                        matrix[i, j] = np.random.randint(-20, 20)
                return matrix
            if option == 2:
                for i in range(n):
                    for j in range(m):
                        value = input_int(f"Value of matrix[{i}, {j}]")
                        matrix[i, j] = value
                return matrix
        
    
    def show_create(self):
        """
        shows init
        """
        print(f"Создание массива:")
        arr = np.array([1,2,3,4,5,6,7,8,9])
        print(arr)
        arr2 = np.asarray((1,2,3))
        print(arr2)

        print(f"Создание массива нулей:")
        arr2 = np.zeros((3, 3))
        print(arr2) 

        print(f"Создание массива заданного числа(5.0):")
        arr5 = np.full(4, 5.0)
        print(arr5)

    def show_index(self, arr):
        """Shows by index"""
        # Индексирование элемента по индексам строки и столбца
        print(arr)
        print(f"Индексирование в думерном массиве [0, 1]: {arr[0, 1]}")
        print(f"Индексирование [1] строки {arr[1]}")

    def show_slice(self, arr):
        """
        Shows the work of slices
        """
        #arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        print(arr)
        print("Срез строк с индексами 1-2")
        print(arr[1:3, :])
        print("Срез столбцов с индексами 0-1")
        print(arr[:, 0:2])

    def show_operations(self, arr):
        """
        Shows NumPy operations 
        """
        print("Операции с массивами. Универсальные (поэлементные) функции:")
        print("Возведение элементов массива в экспоненту:")
        result2 = np.exp(arr)
        print(result2)
        print("Квадратный корень:")
        result2 = np.sqrt(arr)
        print(result2)
        print("Умножение на 3:")
        result2 = np.multiply(arr, 3)
        print(result2)

    def show_other(self, arr):
        """
        shows functions from np
        """
        print("Функция mean():")
        print(arr)
        print("Вычисление среднего значения по всем элементам:")
        mean_value = np.mean(arr)
        print(mean_value)
        print("Вычисление среднего значения по столбцам (ось 0 - столбцы, ось 1 - строки):")
        mean_value_axis0 = np.mean(arr, axis=0)
        print(mean_value_axis0)
        print("Функция median():")
        median_value = np.median(arr)
        print(median_value)
        print(arr)
        print("Функция corrcoef:")
        print(np.corrcoef(arr))
        print("Функция var по строкам:")
        print(np.var(arr, axis= 1))
        print("Стандартное отклонение std() по столбцам")
        print(np.std(arr, axis= 0))

    def sort_array(self, array):
        """
        prints our sorted array
        """
        #: после запятой (array[:, -1]) означает, что мы выбираем все строки (: в первой позиции) и последний столбец (-1 во второй позиции) в матрице array.
        # Получение индексов элементов последнего столбца в отсортированном порядке
        #sorted_indices = np.argsort(matrix[:, -1])[::-1]

        # Переупорядочивание матрицы в соответствии с сортировкой
        #sorted_matrix = matrix[sorted_indices]
        print(f"по убыванию элементов последнего столбца:\n{array[np.argsort(array[:, -1])[::-1]]}")

    def med(self, array):
        """
        mean from np
        """
        last_column = array[:, -1]
        mean_last_column = np.mean(last_column)
        print(f"среднее значение элементов последнего столбца mean() {mean_last_column:.2f}")
    
    
def task5():
        """
        performs the fifth task
        """
        a = NumerPy()

        print(f"Random array: {a.create_array(10)}")

        a.show_create()

        arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        print(arr)
        
        a.show_index(arr)
        a.show_operations(arr)
        a.show_other(arr)

        n = input_int("rows")
        m = input_int("columns")

        matrix = a.create_matrix(n, m)
        print(matrix)

        print(f"{a.sort_array(matrix)}")

        # Вычисление среднего значения элементов последнего столбца
        a.med(matrix)
        last_column_sum = 0
        for i in range(n):
            last_column_sum += matrix[i][-1]
        print(f"среднее значение элементов последнего столбца {last_column_sum/n:.2f}")


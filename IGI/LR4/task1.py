from abc import ABC, abstractmethod
import csv
import pickle

class Serial(ABC):
    @abstractmethod
    def read(self, filename):
        pass

    @abstractmethod
    def write(self, filename, data):
        pass

class For_CSV(Serial):
    def read(self, filename):
        products = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, old_price, new_price = row
                products.append(Product(name, old_price, new_price))
        return products
    
    def write(self, filename, data):
        with open(filename, 'w', newline='') as csvfile:
            writer2 = csv.writer(csvfile)
            for fruit, prices in data.items():
                writer2.writerow([fruit, prices[0], prices[1]])

class For_Pickle(Serial):
    def read(self, filename):
        products = []
        with open(filename, 'rb') as picklefile:
            data = pickle.load(picklefile)
            for fruit, prices in data.items():
                name = fruit
                old_price, new_price = prices
                products.append(Product(name, old_price, new_price))
        return products
    
    def write(self, filename, data):
        with open(filename, 'wb') as picklefile:
            pickle.dump(data, picklefile)


class Shop:
    """
    The Shop class represents a shop that can save and load product information.
    """
    def __init__(self,  products):
        """
        Initializes the shop with products.
        """
        self.products = products

    def show_difference(self):
        """
        Displays the price difference between old and new prices for each product.
        Args:
            products (list): List of Product objects.
        """
        for product in self.products:
            if product.difference() > 0:
                Product.calculate(product)

    def search(self, request):
        """
        Searches for a product by name and displays its details.
        """
        for product in self.products:
            if request == product.name:
                print(product)
                break
        else:
            print("Not found")

    def sort(self):
        """
        Sorts our products by new price        
        """

        sorted_list = sorted(self.products, key=lambda product: product.new_price)

        index = 1
        for product in sorted_list:
            print(f"{index}. Name: {product.name}, old: {product.old_price}, new: {product.new_price}\n")
            index += 1


    def __str__(self):
        """
        For print(obj)
        """
        output = ""
        index = 1
        for product in self.products:
            output += (f"{index}. Name: {product.name}, old: {product.old_price}, new: {product.new_price}\n")
            index += 1
        return output
    

class Product:
    
    def __init__(self, name, old_price, new_price):
        """
        Initialize with name old price and new price
        """ 
        self.name = name    
        self.old_price = old_price
        self.new_price = new_price


    def __str__(self):
        return (f"Name: {self.name}, old: {self.old_price}, new: {self.new_price}, difference: {(self.difference() / float(self.old_price) * 100):.4f}%")

    
    def difference(self):
        return float(self.new_price) - float(self.old_price)


    @staticmethod
    def calculate(product):
        increase = product.difference() / float(product.old_price) * 100
        print(f"Product: {product.name}, increase: {increase:.4f}%")
    
   
    


def task1():
    """
    performs the first task
    """

    #переделать мб

    apple = Product("apple", 12.5, 14.0)
    orange = Product("orange", 17.0, 17.6)
    banana = Product("banana", 11.62, 11.4)
    tomato = Product("tomatoe", 7.62, 8.19)


    dict = {
        apple.name: (apple.old_price, apple.new_price),
        orange.name: (orange.old_price, orange.new_price),
        banana.name: (banana.old_price, banana.new_price),
        tomato.name: (tomato.old_price, tomato.new_price)
    }


    csvf = For_CSV()
    picklef = For_Pickle()
    # Вызов функции для записи данных в файл
    csvf.write("fruits.csv", dict)
    print("data has been written(in csv format)")
    
    picklef.write("fruits2.pkl", dict)
    print("data has been written(in pickle format)\n")

    csv_list = csvf.read("fruits.csv")
    pkl_list = picklef.read("fruits2.pkl")

    shop1 = Shop(pkl_list)
    shop2 = Shop(csv_list)

    print(shop1)
    print(shop2)

    shop1.show_difference()
    shop1.sort()
    prod = input("search: ")
    shop1.search(prod)





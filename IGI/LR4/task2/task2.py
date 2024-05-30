import re
from collections import Counter
import zipfile

class Analyzer:
    def __init__(self, text):
        self.text = text

    def count_sentences(self):
        """
        Используем регулярное выражение для поиска предложений
        """
        sentence_pattern = r"[^.!?]+[\w\s][.!?]"
        sentences = re.findall(sentence_pattern, self.text)

        info = (f"All sentences - {len(sentences)}\n")
        return info
    
    def count_sentences_categories(self):
    # Используем регулярное выражение для поиска предложений
    # Предложения отделяются точкой, восклицательным или вопросительным знаком
        sentence_pattern1 = r"[^.!?]+[\w\s][+.]"
        sentences1 = re.findall(sentence_pattern1, self.text)

        pattern = r"\b[^.!?]*\.{3}\b"
        sentences4 = re.findall(pattern, self.text)

        sentence_pattern2 = r"[^.!?]+[\w\s][?]"
        sentences2 = re.findall(sentence_pattern2, self.text)
    
        sentence_pattern3 = r"[^.!?]+[\w\s][!]"
        sentences3 = re.findall(sentence_pattern3, self.text)
    
        info = (f". - {len(sentences1) + len(sentences4)}, ? - {len(sentences2)}, ! - {len(sentences3)}\n")
        return info
    
    def average_sentence_length(self):
        # Используем регулярное выражение для поиска слов
        word_pattern = r"\b\w+\b"
        words = re.findall(word_pattern, self.text)
    
        # Считаем общее количество символов в словах
        total_characters = sum(len(word) for word in words)
    
        # Считаем количество предложений
        num_sentences = len(self.count_sentences())
    
        # Вычисляем среднюю длину предложения в символах
        if num_sentences > 0:
            average_length = total_characters / num_sentences
            return (f"Avarage length of sentence = {average_length}\n")
        else:
            return (f"Avarage length of sentence not defined\n")

    def average_word_length(self):
        # Используем регулярное выражение для поиска слов
        word_pattern = r"\b\w+\b"
        words = re.findall(word_pattern, self.text)
    
        # Считаем общее количество символов в словах
        total_characters = sum(len(word) for word in words)
    
        # Считаем количество предложений
        num_words = len(words)
    
        # Вычисляем среднюю длину предложения в символах
        if num_words > 0:
            average_length = total_characters / num_words
            return (f"Avarage length of words = {average_length}\n")
        else:
            return 0

    def count_smileys(self):
        # Поиск смайликов с помощью регулярного выражения
        pattern = r'([:;]-*([()\[\]])\2*)'
        smiley_matches = re.findall(pattern, self.text)
    
        count = len(smiley_matches)
        return (f"Smiles: {count}\n")


class AnalyzerSpec(Analyzer):
    
    def __init__(self, text):
        super().__init__(text)

    def upper_number(self):
        #pattern = r'\b(?=\w*\d)(?=[^\W\d_]*[A-Z])\w+\b' #
        pattern = r'\b[A-Z]+\d+\b'
        matched_words = re.findall(pattern, self.text)
        if len(matched_words) != 0:
            return (f"Upper+number words: {matched_words}\n")
        else:
            return ("No words with Upper+number pattern\n")

    def count_upper(self):
        # Поиск слов, состоящих только из прописных букв с помощью регулярного выражения
        pattern = r'\b[A-Z]+\b'
        matches = re.findall(pattern, self.text)
        
        # Возвращаем количество найденных слов
        return (f"A-Z words: {len(matches)}\n")

    def find_longest_word_starting_with_l(self):
        # Поиск слов, начинающихся на 'l' с помощью регулярного выражения
        pattern = r'\bl\w+\b'
        matches = re.findall(pattern, self.text)
        
        # Находим самое длинное слово
        longest_word = max(matches, key=len)
        
        return (f"Longest word starting with l: {longest_word}\n")

    def find_duplicate_words(self):
        # Поиск повторяющихся слов с помощью регулярного выражения
        pattern = r'\b(\w+)\b(?=.*\b\1\b)' #
        duplicate_words = re.findall(pattern, self.text)
        
        return (f"Duplicate words: {duplicate_words}\n")

    def find_duplicate_words2(self):
        # Разделение текста на слова
        words = self.text.split()
        
        # Использование Counter для подсчета повторяющихся слов
        word_counts = Counter(words)
        
        # Фильтрация слов, у которых количество повторений больше 1
        duplicate_words = [word for word, count in word_counts.items() if count > 1]
        
        return duplicate_words

    def check_password(self, password):
        if len(password) >= 8:
            # Проверка наличия только допустимых символов
            if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)', password): #
                return True
        return False    

class FileProsessor:
    def __init__(self, read, write):
        self.read = read
        self.write = write

    def read_file(self):
        with open(self.read, "r", encoding="utf-8") as file:
            content = file.read()
            print(content)

        return content

    def write_info(self, info):
        """
        writes results in file
        """
        with open(self.write, "w", encoding="utf-8") as file:
            file.write(f"{info}")


def task2():

        """function for performing second task"""   
        f = FileProsessor(r"C:\Users\Andrei\PycharmProjects\IGI4\task2\text2.txt", r"C:\Users\Andrei\PycharmProjects\IGI4\task2\result.txt")
        text = f.read_file()
        a = AnalyzerSpec(text)    

        info = a.count_sentences()
        info += a.count_sentences_categories()
        info += a.average_sentence_length()
        info += a.average_word_length()
        info += a.count_smileys()
        info += a.count_upper()
        info += a.find_longest_word_starting_with_l()
        info += a.upper_number()
        try:
            password = input("Password: ")
        except Exception as e:
            print(f"Error: {e}")

        info += (f"Password {password} ")

        if(a.check_password(password)):
            info += (f"is reliable\n")
        else:
            info += (f"is not reliable\n")

         
        info += a.find_duplicate_words()
        f.write_info(info)

        file_to = r"C:\Users\Andrei\PycharmProjects\IGI4\task2\result.txt"
        archive = r"C:\Users\Andrei\PycharmProjects\IGI4\task2\rarchive.zip"
        with zipfile.ZipFile(archive, 'w') as zipf:
            zipf.write(file_to)

        with zipfile.ZipFile(archive, "r") as myzip:
            for item in myzip.infolist():
                print(f"File Name: {item.filename}, Date: {item.date_time}, Size: {item.file_size}")
                


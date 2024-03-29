def decorator_for4th(func):
    def wrapper():
        print("\nillustration of a decorator working:")
        print("\nthe 4th task has started...")
        func()
        print("\n... has ended.")
    return wrapper
    

@decorator_for4th
def task4():

    """
    Analyzes a given string by performing the following tasks:
    1. Splits the string into words, removes punctuation, and converts to lowercase.
    2. Removes duplicates and sorts the words by length in descending order.
    3. Identifies words with an equal number of vowels and consonants.
    4. Counts the number of words consisting of exactly 3 letters (with and without repetitions).
    """

    #maybe decorator
    string = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

    # Разбиваем строку на слова, удаляем знаки препинания и приводим к нижнему регистру
    words = [x.strip('.,').lower() for x in string.split(' ')]
    # Удаляем дубликаты и сортируем по длине в убывающем порядке
    sorted_words = sorted(set(words), key= len, reverse=True)

    print("\nЧетных == нечетных")

    index = 0
    list = []
    
    for word in words:
        index += 1
        count1 = 0
        count2 = 0
        for char in word:
            if char in "aeoui":
                count1 += 1
            else:
                count2 += 1
    
        if len(word)==3:
            list.append(word)

        if count1 == count2:
            print(f"{word} - {index}")

    print(f"\nNumber of words that consit of 3 letters(with repetitions) {len(list)}")
    print(f"\nNumber of words that consit of 3 letters(without repetitions) {len(set(list))}")

    # Выводим отсортированные слова
    print("\nin descending order of their lengths:\n")
    print("\n".join(sorted_words))

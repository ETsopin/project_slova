import os
import random
import sys


#константы
clear = lambda: os.system('cls')
rules = "Правила игры в слова:\n\
Компьютер выбирает случайное слово из заданной тематики.\n\
Игроку необходимо придумать слово из той же тематики, при этом это слово должно начинаться с той же буквы, которой заканчивается слово, загаданное комьютером.\n\
Далее компьютер загадывает слово, начинающееся на последнюю букву слова, загаданного игроком и так далее.\n\
Если загаданное слово кончается на й, Ъ или ь, последней буквой считается буква, стоящая перед й, ъ или ь" 
special_letters = ["й","ъ","ь"]


#модель
class GameModel:
    current_word_to_guess = ""
    current_theme = ""
    current_record = 0
    theme_words = []
    theme_dict = {}
    used_words = []
    record = 0
gameModel = GameModel()


#работа с файлами и вспомогательные функции 
def read_record():
    with open('data/record.txt','r', encoding='utf-8') as f:
        for line in f:
            gameModel.record = int(line)
def update_record(new_record):
    with open('data/record.txt', "w", encoding='utf-8') as f:
        gameModel.record = new_record
        f.write(str(new_record))
def read_theme(file_name):
    print(file_name)
    with open(file_name,'r', encoding='utf-8') as file: 
        for line in file:    
            if len(line.split())==1:
                for word in line.split():
                    gameModel.theme_words.append(word.lower())
                    if word[0].lower() in list(gameModel.theme_dict.keys()):       
                        gameModel.theme_dict[word[0].lower()].append(word)
                    else:
                        gameModel.theme_dict[word[0].lower()] = [] 
                        gameModel.theme_dict[word[0].lower()].append(word)
def add_word(filename, word):
    with open(filename, "a", encoding='utf-8') as f:
        f.write("\n" + word)
def del_if_special(word):
    if len(word)>1:
        if word[len(word)-1] in special_letters:
            return word[0:len(word)-1]
    return word


#меню
def show_menu():
    clear()
    read_record()
    gameModel.current_record = 0
    print("1. Начать игру\n2. Правила\n3. Рекорды\n4. Выйти из игры")
    key = 0
    while key not in ["1","2","3","4"]:
        key = input()
    if key == "1":
        show_theme_menu()
    if key == "2":
        show_rules()
    if key == "3":
        show_record()
    if key == "4":
        sys.exit()
def show_rules():
    clear()
    print(rules)
    print("Введите любое значение чтобы вернуться в меню")  
    input()
    show_menu()
def show_record():
    clear()
    print("Ваш рекорд: "+str(gameModel.record))
    print("Введите любое значение чтобы вернуться в меню")  
    input()
    show_menu()
def show_theme_menu():
    clear()
    print("1. Города России\n2. Страны мира\n3. Столицы стран мира")
    key = 0
    while key not in ["1","2","3"]:
        key = input()
    if key == "1":
        gameModel.current_theme = "data/cities.txt"
    if key == "2":
        gameModel.current_theme = "data/countries.txt"
    if key == "3":
        gameModel.current_theme = "data/capitals.txt"
    read_theme(gameModel.current_theme)
    gameplay(gameModel.theme_words[random.randint(0,len(gameModel.theme_words)-1)])




#игровая логика
def gameplay(word_to_guess):
    clear()
    #print(gameModel.theme_dict)
    gameModel.current_word_to_guess = word_to_guess
    print("Очки: "+str(gameModel.current_record))
    print("Слово компьютера: "+word_to_guess.lower().title())
    print("Введите ваше слово:")
    print('(Для просмотра правил введите "r", для вызова меню - "m")')
    player_word = input()
    if (player_word == "r"):
        clear()
        print(rules)
        print("Введите любой символ для продолжения")
        input()
        gameplay(word_to_guess)
    if (player_word == "m"):
        show_menu()
    #Проверка
    while len(player_word)<2 or player_word in gameModel.used_words or " " in player_word:
        if len(player_word)<2:
            print("Слово не должно быть короче 2 символов!")
        if player_word.lower() in gameModel.used_words:
            print("Вы уже использовали это слово!")
        if " " in player_word:
            print("Вы можете ввести только одно слово!")
        print("Введите любой символ, чтобы попробовать еще раз")
        input()
        gameplay(word_to_guess)
    p_last_letter = del_if_special(player_word)[len(del_if_special(player_word))-1].lower()

    #Проверка наличия слова в словаре 
    if player_word.lower() not in gameModel.theme_words:
        print("Данного слова нет в словаре, вы уверены, что оно существует? y/n")
        choice = ""
        while choice not in ["y", "n"]:
            choice = input()
        if choice == "n":
            print("Введите любой символ, чтобы попробовать еще раз")
            input()
            gameplay(word_to_guess)
        else:
            add_word(gameModel.current_theme, player_word.lower().title())
            print("Слово было добавлено в словарь по данной теме! (Введите любой символ для продолжения)")
            input()
        
    c_last_letter = del_if_special(word_to_guess)[len(del_if_special(word_to_guess))-1].lower()
    p_first_letter = player_word[0].lower()
    if c_last_letter == p_first_letter:
        gameModel.used_words.append(player_word.lower())
        gameModel.current_record+=1
        if gameModel.current_record > gameModel.record:
            update_record(gameModel.current_record)
        if p_last_letter not in list(gameModel.theme_dict.keys()):
            clear()
            print("В словаре игры нет слов, начинающихся на букву " + del_if_special(player_word)[len(del_if_special(player_word))-1]+", поэтому будет загадано случайно слово")
            print("Введите любой символ, чтобы продолжить")
            input()
            gameplay(gameModel.theme_words[random.randint(0,len(gameModel.theme_words)-1)])
        else:
            new_word_to_guess = gameModel.theme_dict[p_last_letter][random.randint(0,len(gameModel.theme_dict[p_last_letter])-1)]
            gameplay(new_word_to_guess)
    else:
        print("Слово не подходит, попробуйте еще раз!")
        print("Введите любой символ, чтобы попробовать еще раз")
        input()
        gameplay(word_to_guess)



show_menu() 
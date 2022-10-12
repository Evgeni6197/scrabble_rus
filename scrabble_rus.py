#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Вариант известной игры Скрабл, где нужно из случайного набора букв составлять
слова и набирать очки.
Игроку выдается набор из  HAND_SIZE букв, из которых HAND_SIZE//3 гласныe.

Переменная RARE составлена из "редких" букв. Алгоритм следит за тем, 
чтобы в выдаваемом игроку случайном наборе было не более RARE_VOW 
"редких" гласных и не более RARE_CON "редких" согласных.  

"""
import random
import sys

VOWELS = 'аеиоуыэюя'  # русские гласные
CONSONANTS = 'бвгджзйклмнпрстфхцчшщъь' # русские согласные
HAND_SIZE = 12 # общее количество букв в наборе
RARE = 'уыэюяйжзфхцчшщъь'  # "редкие" буквы
RARE_VOW = 1 # Квота на "редкие" гласные в наборе
RARE_CON = 2 # Квота на "редкие" согласные в наборе

# значения для рассчета очков
SCRABBLE_LETTER_VALUES = {
    'а': 1, 'б': 3, 'в': 2, 'г': 3, 'д': 2, 
    'е': 1, 'ж': 5, 'з': 5, 'и': 1, 'й': 2,
    'к': 2, 'л': 2, 'м': 2, 'н': 1, 'о': 1,
    'п': 2, 'р': 2, 'с': 2, 'т': 2, 'у': 3,
    'ф': 10,'х': 5, 'ц':10, 'ч': 5, 'ш': 10,
    'щ': 10,'ъ':10, 'ы':5,  'ь':5,   'э':10,
    'ю':10,'я':3
}



def read_words_file(filename):
    
    '''
    Reads dictionary from filename
    
    input : str,  valid filename
    Returns list of str  - valid lowercase words including only alphabetic characters
            which were read from input file 
    '''
    words=[]
    count=0
    assert type(filename)==str
    print('загружает словарь...')
    try:
        with open(filename) as f:
            for element in f:
                count+=1
                try: 
                    assert type(element)==str 
                except AssertionError:
                    print (f'Not alphabetic element in  line {count} of reference  file {filename}')
                else:
                    words.append(element.rstrip('\n').lower())
    except IOError:
        print(f"Can not open {filename}")
        sys.exit()
    
    else:
        print(f'   загрузилось  {len(words)}  слов')
        return words
    
def get_initial_hand():
    '''
    return  str:   HAND_SIZE random uppercase letters separated 
                by whitespaces with trailing whitespace
    HAND_SIZE//3 vowels, the other - consonants
 
    '''
    vow= HAND_SIZE // 3    # количество гласных в наборе
    conson = HAND_SIZE - vow  # количество согласных в наборе    
    hand_list=[] # переменная для фиксации составляемого набора в виде list
    rare_vow=0  # переменная для отслеживания количества редких гласных в наборе
    rare_con=0  # переменная для отслеживания количества редких согласных в наборе
    
    for i in range(vow):
        while True:
            
            # выбираем случайную гласную
            v=random.choice(VOWELS)
            
            # если гласная редкая и она уже в наборе, 
            # возвращаемся к выбору новой гласной
            if v in RARE and v in hand_list:
                continue
            
            # если гласная редкая и в наборе
            # уже выбрана квота редких гласных,
            # возвращаемся к выбору новой гласной           
            if v in RARE and rare_vow >= RARE_VOW:
                continue
            
            
            hand_list.append(v)  # вставляем гласную в набор
            
            # если вставленная гласная редкая, учитываем это, чтобы
            # в дальнейшем не превысить количество редких гласных  в наборе
            if v in RARE:
                rare_vow += 1
                
            break
        
    
    # Аналогично с согласными
    for i in range(conson):
        while True:
            c=random.choice(CONSONANTS)
            if c in RARE and c in hand_list:
                continue
            if c in RARE and rare_con >= RARE_CON:
                continue           
            hand_list.append(c)
            if c in RARE:
                rare_con += 1          
            break        
    
    hand = ''  # переменная для вывода набора на экран in  str type
    for ch in hand_list:
        hand += ch + ' '
        
    assert type(hand)==str
    assert hand[-1]==' '   # проверка наличия пробела в конце набора
    return hand
    

def game_action_choice(last_hand):
    '''
    game action choice depending on user input
        Parameters
    ----------
    last_hand : TYPE str : letters separated by whitespaces
                        with trailing whitespace

    Returns
    -------
    TYPE str
        hand chosen - the new one or the last one
        OR
    None - if user has chosen  to quit the game

    '''
    assert type(last_hand)==str
    while True:
        game_action=input('Введите "н" для нового набора букв, "с" - переиграть со старым набором, "в" выйти из игры: ').lower().strip() 
        
        if not game_action in ('н','с','в'):
            print ('неверная команда, попробуйте еще раз ')
            continue
        
        if not last_hand and game_action=='с':  # если игрок выбрал старый набор в начале игры
            print('Вы играете первый раз')
            continue 
        
        else:
            break
            
    if game_action =='н':
         return get_initial_hand()
    elif game_action=='с':
        return last_hand 
    sys.exit()
    
def word_score(word):
    
    '''
    Counts the score, got by the word according to the scrabble rules
    Parameters
    ----------
    word : TYPE str, alphabetic  characters only
        DESCRIPTION. evaluate input word's score by game rules 
    Returns
    -------
    int - word's score

    '''
    score=0
    assert word.isalpha()==True 
    for ch in word.lower():
        score+=SCRABBLE_LETTER_VALUES[ch]
    score *= len(word)
    if len(word) >= 7:
        score+=50
    
    return score
            
def word_composing(remaining_hand) :
           
    '''
    composing valid word using letters of remaining hand
    Parameters
    ----------
    remaining_hand : TYPE str - letters separated by whitespaces 
                     with one trailing whitespace  - to compose a word

    Returns
    -------
    str - word_composed
    OR
    int 1 - if user can not compose a word and input '.'
    '''
    
    assert type(remaining_hand)==str
    
    while True:
        print('Ваш набор букв               ' +remaining_hand )
        valid=True
        word=input('введите слово или точку, если нет подходящего слова: ').lower().strip()
        
        # если слово не удалось составить
        if word =='.':
            return 1
        
        # если составленного слова нет в прочитанном файле - словаре
        # пробуем составить снова
        if not word in dictionary_words:
            print('Такого слова нет в словаре, или это не существительное в единственном числе')
            continue 
       
        # проверяем  есть ли в наборе буквы, из которых составлено слово
        testing_hand=remaining_hand
        for ch in word:
            if not ch in testing_hand   : 
                valid=False
                
            # удаляем проверенную букву слова из набора, на тот случай, если 
            # в слове буква встречается дважды, а в наборе она только одна        
            testing_hand =testing_hand.replace(ch+' ','',1) 
        
        # если в наборе нет букв, из которых составлено 
        # слово - пробуем составить снова
        if valid==False:
            print('Таких букв нет в наборе')
            continue
        break
    return word

def internal_cycle(start_cycle_hand): 
    '''
    The essence of the game. One single set of   words composing 
    starting with HAND_SIZE letters (a new one hand or the last one) , 
    several trying of composing with intermediate and final score.   
    Parameters
    ----------
    start_cycle_hand : TYPE str - letters separated by whitespaces
                                    with one trailing whitespace. 

    Returns None
    '''
    score=0
    current_hand=start_cycle_hand # начинаем цикл с полного количества букв в наборе
    while True:
        
        # Составляем новое слово из оставшихся букв набора
        word=word_composing(current_hand)
        
        # Если слово не удалось составить
        if word==1:
            print(f'Общий счет: {score}')
            return
        
        # считаем сколько слово получает очков
        current_score=word_score(word)
        score+= current_score
        print(f'"{word}" получает {current_score} очков. Счет {score} очков. ')
        
        # удаляем из набора использованные в слове буквы
        for ch in word:
            current_hand=current_hand.replace(ch+' ','',1)
            
        # Если в наборе не осталось букв    
        if not current_hand:
            print(f'Буквы кончились. Общий счет: {score} очков.')
            return
        
def main():
    hand=''
    while True:
        print()
        # выбираем как продолжится игра
        hand=game_action_choice(hand)
        
        # переходим к сути игры - составлять слова из букв набора
        internal_cycle(hand)
        
if __name__=='__main__':
    dictionary_words=read_words_file('russian_nouns_singular.txt')
    main()    
    

    
    
    
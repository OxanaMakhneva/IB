import re
import json
import csv

#Отчищает строку от лишних символов и приводит ее к строчному виду
def norm_sentence(soft_name):
    #Строчные буквы
    soft_name = soft_name.lower()
    #Исключаем кавычки, переводы строки
    soft_name = re.sub("""^\s+|'|"|\n|\r|\s+$""", '', soft_name)
    #Исключаем повторяющиеся пробелы
    soft_name = " ".join(soft_name.split())
    return soft_name

#Разделяет строку на кусочкис наложением
def get_tokens(soft_name):
    words = soft_name.split(' ')
    tokens = [word for word in words if len(word) > 2]
    return tokens

#Проверяет похожесть двух кусочков
def is_tokens_equal(first_token, second_token, subtoken_len, true_limit):
    first_number = len(first_token) - subtoken_len + 1
    second_number = len(second_token) - subtoken_len + 1
    used_tokens = [False for ind in range(second_number)]
    equal_count = 0
    for first_ind in range(first_number):
        subtoken_first = first_token[first_ind : first_ind + subtoken_len]
        for second_ind in range(second_number):
            if not used_tokens[second_ind]:
                subtoken_second = second_token[first_ind : first_ind + subtoken_len]
                if subtoken_first == subtoken_second:
                    equal_count = equal_count + 1
                    used_tokens[second_ind] = True
                    break
    subtoken_first_count = len(first_token) - subtoken_len + 1
    subtoken_second_count = len(second_token) - subtoken_len + 1
    tanimoto = (1.0 * equal_count) / (subtoken_first_count + subtoken_second_count - equal_count)
    return tanimoto > true_limit

#Перевирает все кусочки из двух строк и собирает только одинаковые в отдельный список
def get_equals_tokens(tokens_first, tokens_second, subtoken_len, true_limit):
    equals_tokens = []
    used_token = [False for ind in range(len(tokens_second))]
    for first_ind in range(len(tokens_first)):
        for second_ind in range(len(tokens_second)):
            if not used_token[second_ind]:
                if is_tokens_equal(tokens_first[first_ind], tokens_second[second_ind], subtoken_len, true_limit):
                    equals_tokens.append(tokens_first[first_ind])
                    used_token[second_ind] = True
                    break
    return equals_tokens

#Определяет степень одинаковости строк
def calc_equal(first_word, second_word, subtoken_len, true_limit):
    tokens_first = get_tokens(norm_sentence(first_word))
    tokens_second = get_tokens(norm_sentence(second_word))
    equals_tokens = get_equals_tokens(tokens_first, tokens_second, subtoken_len, true_limit)
    equals_count = len(equals_tokens)
    first_count = len(tokens_first)
    second_count = len(tokens_second)
    result_value = (1.0 * equals_count) / (first_count + second_count - equals_count)
    #print(result_value)
    return result_value

#Подбирает для записи по с пк несколько (количество = top) самых подходящих вариантов название из БД ПО
def siblins_soft_for_one_rec(soft_rec, all_bd_soft, column_bd, top = 10):
    #Длина сегментов дляразделениякаждого слова
    subtoken_len = 3
    #Граница, прикоторой принимается решение о совпадении слова со словом
    true_limit = 0.6
    #Расчет коэффициентасвязностидля каждой пары soft_rec - soft_bd
    rvalues = {index_bd: calc_equal(soft_rec, soft_bd[column_bd], subtoken_len, true_limit) for index_bd, soft_bd in enumerate(all_bd_soft)}
    sorted_rvalues = {}
    #Делаем словарь, где ключами являются коэфф. связи, а значениями индексы из бд.
    #Сортируем его в порядке возрастания
    sorted_keys = sorted(rvalues, key = rvalues.get)
    #Берем последние top значений и переделываем их вобратный словарь
    for w in sorted_keys[-top:]:
        sorted_rvalues[w] =  rvalues[w]
    #Вычисляем индекс наиболее подходящей записи в БД
    best_index = list(sorted_rvalues.keys())[top-1]
    #Возвращаем индекс, rvalue и список 10 индексов для наиболее близких строк
    return (best_index, sorted_rvalues[best_index], list(sorted_rvalues.keys()))

from typing import Dict
from typing import List


def filter_by_currency (list|dict)
'''
Функция filter_by_currency принимает список словарей на вход
и возвращает итератор, который поочередно выдает транзакции, 
где валюта операции соответствует заданной (например, USD)
'''
    pass
    '''
    Создайте функцию filter_by_currency
    , которая принимает на вход список словарей, представляющих транзакции.
    Функция должна возвращать итератор, который поочередно выдает транзакции, 
    где валюта операции соответствует заданной (например, USD).
        Пример использования функции
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))
    
    >>> {
              "id": 939719570,
              "state": "EXECUTED",
              "date": "2018-06-30T02:08:58.425572",
              "operationAmount": {
                  "amount": "9824.07",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод организации",
              "from": "Счет 75106830613657916952",
              "to": "Счет 11776614605963066702"
          }
          {
                  "id": 142264268,
                  "state": "EXECUTED",
                  "date": "2019-04-04T23:20:05.206878",
                  "operationAmount": {
                      "amount": "79114.93",
                      "currency": {
                          "name": "USD",
                          "code": "USD"
                      }
                  },
                  "description": "Перевод со счета на счет",
                  "from": "Счет 19708645243227258542",
                  "to": "Счет 75651667383060284188"
           }
    '''


def transaction_descriptions (list|dict)
'''
Функция-генератор transaction_descriptions
принимает на вход список словарей и использует 
yield для генерации значений по запросу
'''
    pass
    '''
    Напишите генератор transaction_descriptions
    , который принимает список словарей с транзакциями и 
    возвращает описание каждой операции по очереди.
    
    Пример использования функции
    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))
    
    >>> Перевод организации
        Перевод со счета на счет
        Перевод со счета на счет
        Перевод с карты на карту
        Перевод организации
    '''



def card_number_generator (start, stop)
'''
Генератор card_number_generator принимает значения 
start и stop в качестве аргумента
'''
    pass
    '''
Создайте генератор card_number_generator, который выдает номера банковских карт в формате 
XXXX XXXX XXXX XXXX , где X
 — цифра номера карты. Генератор может сгенерировать номера карт 
 в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.
Генератор должен принимать начальное и конечное значения для генерации диапазона номеров.

Пример использования функции
for card_number in card_number_generator(1, 5):
    print(card_number)

>>> 0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005
    '''
"""
Классы игроков, в т.ч. крупье
"""

from time import sleep
from random import randrange

from ErrorsClasses import *
from card_class import *


class Player:
    def __init__(self, pl_name, chips):
        self.points = 0
        self.name = pl_name
        self.own_cards = []
        self.bet = None
        if chips >= 100:
            self.chips_count = chips
        else:
            raise ChipsCountError

    def ask_move(self):
        pass

    def betting(self):
        pass

    @property
    def check_blackjack(self):
        if self.points == 21:
            print(f"************************************\n"
                  f"{self.name} набрал 21 с двух карт, браво!\n"
                  f"************************************")
            self.own_cards = []
            return True
        return False


class Croupier(Player):
    @property
    def ask_move(self):
        if not (self.points == 17 or self.points == 18 or self.points == 19 or self.points == 20 or self.points == 21):
            return True
        print("Крупье завершил свой ход.")
        self.own_cards = []
        return False


class User(Player):
    @property
    def ask_move(self):
        print("************************************\n"
              "Ваши карты:")
        for card in range(len(self.own_cards)):
            print(f"{self.own_cards[card].__str__()}")
        print("************************************")
        input("Нажмите Enter, чтобы продолжить...")
        try:
            ask_variants_no = ["Нет", "нет", "No", "no"]
            ask_variants_yes = ["Да", "да", "Yes", "yes"]
            ask = input("""Дать еще карту (Да/Нет)?: """)
            if ask in ask_variants_yes:
                return True
            if ask in ask_variants_no:
                print(f"{self.name} завершил свой ход.")
                self.own_cards = []
                return False
            else:
                raise WrongInputError
        except WrongInputError as error:
            print(error)
            return self.ask_move

    def betting(self):
        if self.chips_count <= 100:
            self.bet = self.chips_count
            self.chips_count -= self.bet
            self.own_cards.append(Card)
            print("У Вас меньше 100 фишек! Вы вынуждены идти all-in!")
            return
        bet = input("Введите величину вашей ставки: ")
        try:
            bet = int(bet)
            if bet > self.chips_count or bet < 100:
                raise WrongBetError
        except WrongBetError as error:
            print(error)
            return self.betting()
        except ValueError:
            print(WrongBetError())
            return self.betting()
        else:
            self.bet = bet
            self.chips_count -= self.bet
            return


class AI(Player):
    @property
    def ask_move(self):
        ai_points_to_stop = [18, 19, 20, 21]
        if self.points in ai_points_to_stop:
            print("ИИ завершил свой ход.")
            self.own_cards = []
            sleep(1)
            return False
        return True

    def betting(self):
        print("ИИ думает, сколько поставить...")
        sleep(2)
        all_in_chance = randrange(1, 100)
        if all_in_chance >= 95:
            self.bet = self.chips_count
            print(f"{self.name} решает идти all-in, ставя {self.bet} фишек!")
        elif 300 <= self.chips_count <= 500:
            self.bet = randrange(100, (self.chips_count + 1) // 3, 10)
            print(f"{self.name} ставит {self.bet} фишек.")
        elif 200 <= self.chips_count < 300:
            self.bet = self.chips_count // 2
            print(f"{self.name} ставит {self.bet} фишек.")
        elif 100 < self.chips_count < 200:
            self.bet = self.chips_count
            print(f"{self.name} решает идти all-in, ставя {self.bet} фишек!")
        elif self.chips_count <= 100:
            self.bet = self.chips_count
            print(f"У {self.name} слишком мало фишек, он вынужден идти all-in, ставя {self.bet} фишек!")
        else:
            self.bet = randrange(100, (self.chips_count + 1) // randrange(4, 5), 10)
            print(f"{self.name} ставит {self.bet} фишек.")
        self.chips_count -= self.bet
        return

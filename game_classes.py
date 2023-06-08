"""
Класс игры
"""

from os import system, name
from random import choice

from Players import *

class Game:
    def __init__(self):
        self.deck = []
        self.user = User(self.input_username(), 1000)
        self.ai = AI('ИИ', 1000)
        self.croupier = Croupier('Крупье', (self.user.chips_count + self.ai.chips_count) * 100)
        self.dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
                     "K": 10, "A": 11}
        self.flag_user = True
        self.flag_ai = True

    def input_username(self):
        try:
            username = input('Пожалуйста, введите Ваше имя: ')
            if (not username.isalpha()) or len(username) < 2:
                raise WrongInputError
        except WrongInputError as error:
            print(error)
            return self.input_username()
        else:
            return username

    def hello(self):
        print(f"""Здравствуйте, {self.user.name}.
    Добро пожаловать в игру "BlackJack".
    ************************************
    В игре принимают участие 2 игрока: пользователь и ИИ.
    Каждый из них играет против крупье.
    Цель игры: выиграть у крупье.
    ************************************
    На старте число фишек у пользователя: {self.user.chips_count}
    На старте число фишек у ИИ: {self.ai.chips_count}
    ************************************
    Минимальная ставка: 100 фишек.
    ************************************
    Начало игры.""")
        input("Нажмите Enter, чтобы продолжить...")
        return

    def initialize_deck(self):
        print(f"************************************\n"
              f"Новый кон игры.")
        suit_list = ["Черви", "Бубны", "Треф", "Пик"]
        card_value_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        sleep(1)
        print("Крупье перемешивает колоду...", end=" ")
        for suit in suit_list:
            for value in card_value_list:
                self.deck.append(Card(suit, value))
        sleep(3)
        print("Колода перемешана.")
        sleep(1)
        return

    def initialize_new_con(self):
        self.user.points = 0
        self.ai.points = 0
        self.croupier.points = 0
        if self.flag_user:
            print(f"Текущее число фишек {self.user.name}: {self.user.chips_count}")
        if self.flag_ai:
            print(f"Текущее число фишек ИИ: {self.ai.chips_count}")
        sleep(1)
        return

    def place_bets(self):
        if self.flag_user:
            self.user.betting()
        if self.flag_ai:
            self.ai.betting()
        return

    def get_card(self, player):
        print("Крупье выдает карту...", end=" ")
        sleep(1)
        card = choice(self.deck)
        player.own_cards.append(card)
        print(f"выдается карта {player.name}: {card.__str__()}")
        sleep(1)
        self.deck.remove(card)
        if card.value == "A" and player.points > 10:
            player.points += 1
            print(f"При набранных очках {player.name} выданный туз считается за 1 очко.")
        else:
            player.points += self.dict.get(card.value)
        return card

    def cards_distribution(self):
        if self.flag_user and self.flag_ai:
            self.get_card(self.user)
            self.get_card(self.ai)
            self.get_card(self.user)
            self.get_card(self.ai)
        elif self.flag_user:
            self.get_card(self.user)
            self.get_card(self.user)
        elif self.flag_ai:
            self.get_card(self.ai)
            self.get_card(self.ai)
        self.get_card(self.croupier)
        return

    def check_blackjack_game_end(self, player):
        if player.points == 21 and self.croupier.points == 21:
            player.chips_count += player.bet
            print(f"У {player.name} и крупье блек-джек, ничья.")
            return True
        elif self.croupier.points == 21:
            print(f"У крупье блек-джек, {player.name} проиграл.")
            return True
        elif player.points == 21:
            player.chips_count += player.bet * 2
            print(f"У {player.name} блек-джек, {player.name} выиграл!")
            return True
        return False

    def check_winner(self):
        print("************************************\n"
              "Игра подошла к концу. Величина очков:\n")
        if self.flag_user:
            print(f"у {self.user.name}: {self.user.points}")
        if self.flag_ai:
            print(f"у ИИ: {self.ai.points}")
        print(f"у крупье: {self.croupier.points}\n\n"
              f"************************************")
        if self.flag_user:
            sleep(1)
            print(f"Определение победителя в паре {self.user.name}--крупье:")
            sleep(3)
            if self.check_blackjack_game_end(self.user):
                pass
            elif self.user.points < 21 and self.croupier.points < 21:
                if self.user.points > self.croupier.points:
                    self.user.chips_count += self.user.bet * 2
                    print(f"По итогам игры у {self.user.name} больше очков, чем у крупье. Вы победили!")
                elif self.user.points == self.croupier.points:
                    self.user.chips_count += self.user.bet
                    print(f"Ничья. У {self.user.name} и крупье одинаковое число очков по итогам игры.")
                else:
                    self.croupier.chips_count += self.user.bet
                    print("Победа крупье, поскольку у него больше очков.")
            elif self.user.points > 21 and self.croupier.points > 21:
                self.user.chips_count += self.user.bet
                print("Ничья, поскольку у обоих игроков перебор.")
            elif self.user.points > 21:
                print(f"Победа крупье, поскольку у {self.user.name} перебор.")
            elif self.croupier.points > 21:
                self.user.chips_count += self.user.bet * 2
                print(f"Победа {self.user.name}, поскольку у крупье перебор!")
        if self.flag_ai:
            sleep(1)
            print(f"Определение победителя в паре {self.ai.name}--крупье:")
            sleep(3)
            if self.check_blackjack_game_end(self.ai):
                pass
            elif self.ai.points < 21 and self.croupier.points < 21:
                if self.ai.points > self.croupier.points:
                    self.ai.chips_count += self.ai.bet * 2
                    print("По итогам игры у ИИ больше очков, чем у крупье. ИИ победил!")
                elif self.ai.points == self.croupier.points:
                    self.ai.chips_count += self.ai.bet
                    print("Ничья. У ИИ и крупье одинаковое число очков по итогам игры.")
                else:
                    self.croupier.chips_count += self.ai.bet
                    print("Победа крупье, поскольку у него больше очков.")
            elif self.ai.points > 21 and self.croupier.points > 21:
                self.ai.chips_count += self.ai.bet
                print("Ничья, поскольку у обоих игроков перебор.")
            elif self.ai.points > 21:
                print("Победа крупье, поскольку у ИИ перебор.")
            elif self.croupier.points > 21:
                self.ai.chips_count += self.ai.bet * 2
                print("Победа ИИ, поскольку у крупье перебор.")
            sleep(1)
        input("Нажмите Enter, чтобы продолжить...")
        return

    def ask_user_to_continue(self):
        try:
            ask = input(f"Желаете ли Вы продолжить наблюдать за игрой {self.ai.name}? ")
            ask_variants_no = ["Нет", "нет", "No", "no"]
            ask_variants_yes = ["Да", "да", "Yes", "yes"]
            if ask in ask_variants_yes:
                print("Игра продолжается между ИИ и крупье.")
                sleep(2)
                return True
            elif ask in ask_variants_no:
                print("Игра окончена.")
                return False
            else:
                raise WrongInputError
        except WrongInputError as error:
            print(error)
            return self.ask_user_to_continue()

    def start_game(self):
        self.hello()
        while self.flag_user or self.flag_ai:
            system('cls') if name == 'nt' else system('clear')
            flag_bj_user = False
            flag_bj_ai = False
            self.initialize_deck()
            self.initialize_new_con()
            self.place_bets()
            self.cards_distribution()
            if self.flag_user and self.user.check_blackjack:
                flag_bj_user = True
            if self.flag_ai and self.ai.check_blackjack:
                flag_bj_ai = True
            if self.flag_user:
                print(f"Начинается ход {self.user.name}.")
                sleep(0.5)
                while True:
                    if flag_bj_user:
                        sleep(1)
                        print(f"Карты {self.user.name} не нужны, поскольку у него (неё) блек-джек.")
                        break
                    else:
                        sleep(1)
                        if self.user.ask_move:
                            self.get_card(self.user)
                            if self.user.points == 21:
                                print(f"У {self.user.name} блек-джек!")
                                break
                            elif self.user.points > 21:
                                print(f"У {self.user.name} перебор.")
                                break
                        else:
                            break
                self.user.own_cards = []
            input("Нажмите Enter, чтобы продолжить...")
            if self.flag_ai:
                print(f"Начинается ход {self.ai.name}.")
                sleep(1)
                while True:
                    if flag_bj_ai:
                        print("Карты ИИ не нужны, поскольку у него блек-джек.")
                        break
                    else:
                        sleep(1)
                        if self.ai.ask_move:
                            self.get_card(self.ai)
                            if self.ai.points == 21:
                                print("У ИИ блек-джек!")
                                break
                            elif self.ai.points > 21:
                                print("У ИИ перебор.")
                                break
                        else:
                            break
                self.ai.own_cards = []
            input("Нажмите Enter, чтобы продолжить...")
            print("Начинается ход крупье.")
            sleep(1)
            while self.croupier.ask_move:
                self.get_card(self.croupier)
                if self.croupier.points == 21:
                    print("У крупье блек-джек!")
                    break
                elif self.croupier.points > 21:
                    print("У крупье перебор.")
                    break
            input("Нажмите Enter, чтобы продолжить...")
            self.check_winner()
            if self.user.chips_count == 0 and self.flag_user:
                print("\n"
                      "************************************\n"
                      "************************************\n"
                      f"Фишки {self.user.name} закончились!\n"
                      "************************************\n"
                      "************************************\n")
                sleep(2)
                self.flag_user = False
            if self.ai.chips_count == 0 and self.flag_ai:
                print("\n"
                      "************************************\n"
                      "************************************\n"
                      f"Фишки {self.ai.name} закончились!\n"
                      "************************************\n"
                      "************************************\n")
                sleep(2)
                self.flag_ai = False
            if self.flag_ai and not self.flag_user and not self.ask_user_to_continue():
                break
            if not (self.flag_ai and self.flag_user):
                print("Игра окончена, у всех игроков кончились фишки! Крупье победил!")
                break

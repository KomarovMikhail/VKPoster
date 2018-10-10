import random


class Wishes:
    def __init__(self):
        self._common = [
            'огромного счастья',
            'крепкого здоровья',
            'верных друзей'
        ]
        self._study = [
            'отличных оценок',
            'успешной учебы',
            'легких экзаменов'
        ]
        self._camp = [
            'незабываемых смен',
            'послушных детей',
            'отзывчивых коллег-вожатых'
        ]
        self._from = [
            'Фотона',
            'нашего вожатского отряда'
        ]
        self._state = [
            'Пусть каждый твой день будет наполнен радостью и теплом.',
            'Пусть сбываются все твои мечты и достигаются поставленные цели.',
            'Пусть тебя всегда окружают люди, готовые прийти на помощь в любую минуту.'
        ]
        self._hb = 'С Днем Рождения!'

    def get_common(self):
        return random.choice(self._common)

    def get_study(self):
        return random.choice(self._study)

    def get_camp(self):
        return random.choice(self._camp)

    def get_from(self):
        return random.choice(self._from)

    def get_state(self):
        return random.choice(self._state)

    def get_hb(self):
        return self._hb

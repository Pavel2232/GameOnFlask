
from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    match_start = False
    battle_result = ""

    def start(self, player: BaseUnit, player2: BaseUnit):
        self.player = player
        self.enemy = player2
        self.match_start = True

    def next_round(self):
        result = self.health_check()
        if result is not None:
            return result
        if self.match_start:
            self.regeneration_stamina()
            return self.enemy.deal_damage(self.player)

        self.enemy.class_person.skill.use(self.enemy, self.player)
        self.enemy.deal_damage(self.player)

    def regeneration_stamina(self):

        players = [self.player, self.enemy]

        for stamina in players:
            if stamina.stamina_point + self.STAMINA_PER_ROUND >= stamina.class_person.max_stamina:
                stamina.stamina_point = stamina.class_person.max_stamina
            else:
                stamina.stamina_point += self.STAMINA_PER_ROUND

    def health_check(self):
        if self.player.health_point and self.enemy.health_point > 0:
            return None

        if self.player.health_point and self.enemy.health_point <= 0:
            self.battle_result = "Ничья"

        if self.player.health_point <= 0:
            self.battle_result = "Игрок потерпел поражение"

        if self.enemy.health_point <= 0:
            self.battle_result = "Компьютер проиграл"

        return self.game_over()

    def game_over(self):
        self._instances = {}
        self.match_start = False
        return self.battle_result

    def hit_player(self) -> str:
        if self.match_start:
            result = self.player.deal_damage(self.enemy)
            enemy_result = self.next_round()
            return f"{result}\<br>{enemy_result}"
        result = self.health_check()
        if result is not None:
            return result

    def use_skill(self) -> str:
        if self.match_start:
            result = self.player.skill_use(self.enemy)
            enemy_result = self.next_round()
            return f"{result}\<br>{enemy_result}"
        result = self.health_check()
        if result is not None:
            return result

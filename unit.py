import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

from classes import Unit
from equipment import Weapon, Armor


@dataclass
class DataBaseUnit:
    nickname: str
    class_person: Unit
    health_point: float
    stamina_point: float
    attack: float
    weapon: Weapon
    armor: Armor


class BaseUnit(ABC, DataBaseUnit):
    _use_skill = False

    def set_weapon(self, weapon) -> str:
        self.weapon = weapon

        return f"{self.nickname} экипирован оружием {self.weapon.name}"

    def set_armor(self, armor) -> str:
        self.armor = armor

        return f"{self.nickname} экипирован броней {self.weapon.name}"

    def _count_damage(self, target) -> int:

        self.stamina_point -= self.weapon.stamina_per_hit

        self.attack += self.class_person.attack + self.weapon.random_damage
        damage = int(self.attack)

        if target.stamina_point >= target.armor.stamina_per_turn:
            damage_down = target.armor.defence + target.armor.stamina_per_turn
            damage -= damage_down
            target.stamina_point -= target.armor.stamina_per_turn

        target.damage_received(damage)

        return damage

    def damage_received(self, damage):
        if damage > 0:
            self.health_point -= damage

    def skill_use(self, target) -> str:
        if self._use_skill:
            return "Навык уже использован."

        self._use_skill = True
        return self.class_person.skill.use(self, target)

    @abstractmethod
    def deal_damage(self, target):
        pass


class Player(BaseUnit):

    def deal_damage(self, target) -> str:

        if self.stamina_point < self.weapon.stamina_per_hit:
            return f" {self.nickname} попытался использовать {self.weapon.name}, но у него не хватило {self.stamina_point} выносливости{self.weapon.stamina_per_hit}."

        damage = self._count_damage(target)

        if damage > 0:
            return f"{self.nickname} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

        return f"{self.nickname} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class Enemy(BaseUnit):

    def deal_damage(self, target) -> str:
        if self._use_skill:

            if self.stamina_point < self.weapon.stamina_per_hit:
                return f" {self.nickname} попытался использовать {self.weapon.name}, но у него не хватило {self.stamina_point} выносливости{self.weapon.stamina_per_hit}."

            damage = self._count_damage(target)

            if damage > 0:
                return f"{self.nickname} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

            return f"{self.nickname} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        return self.skill_use(target)


    def skill_use(self, target) -> str:
        if self._use_skill:
            return "Навык уже использован."

        self._use_skill = True
        chance = (random.randint(1, 100))
        if chance <= 10:
            return self.class_person.skill.use(self, target)

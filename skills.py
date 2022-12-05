from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class SkillData:
    name: str
    damage: float
    required_stamina: float
    user = None
    target = None


class Skill(ABC, SkillData):

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def use(self, user, target) -> str:
        self.user = user
        self.target = target
        if user.stamina_point >= self.required_stamina:
            return self.skill_effect()
        return f"{self.user.nickname} попытался использовать {self.name}, но у него не хватило выносливости."


class PierceThrough(Skill, ABC):

    def skill_effect(self) -> str:
        self.target.damage_received(self.damage)
        self.user.stamina_point -= self.required_stamina

        return f"{self.user.nickname} использует {self.name} и наносит {self.damage} урона сопернику."


class StealingLife(Skill):

    def skill_effect(self) -> str:
        self.target.damage_received(self.damage)
        self.user.stamina_point -= self.required_stamina

        return f"{self.user.nickname} использует {self.name} и наносит {self.damage} урона сопернику."


class HitBack(Skill):

    def skill_effect(self) -> str:
        self.target.damage_received(self.damage)
        self.user.stamina_point -= self.required_stamina

        return f"{self.user.nickname} использует {self.name} и наносит {self.damage} урона сопернику."


Warriorskill = PierceThrough("Пронзающий клинок", 15, 2)
Warlockkill = StealingLife("Похищение жизни", 30, 6)
Thiefskill = HitBack("Удар в спину", 20, 3)

skills = {
    Warriorskill.name: Warriorskill,
    Warlockkill.name: Warlockkill,
    Thiefskill.name: Thiefskill
}

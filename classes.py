from dataclasses import dataclass,fields

from skills import Warriorskill, Warlockkill, Thiefskill, Skill

@dataclass
class Unit:
    name: str
    max_health: int
    max_stamina: int
    attack: float
    mod_stamina: float
    mod_armor: float
    skill: Skill



WarriorClass = Unit("Воин Князь Калаврат",100,30,5,12,1.2,Warriorskill)
WarlockClass = Unit("Чернокнижник Черная змея",100,30,7,5,0.3,Warlockkill)
ThiefClass = Unit("Вор ловкий Владимир",100,30,1.3,7,5,Thiefskill)

unit_classes = {
    ThiefClass.name : ThiefClass,
    WarriorClass.name: WarlockClass,
    WarlockClass.name: WarlockClass

}



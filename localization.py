from enum import Enum

class StartDialogue(Enum):
    welcome: str = "Добро пожаловать абитуриент...!\nВведи свое имя:"
    direction: str = "Отлично, на какую кафедру ты планируешь подавать документы?"
    
class Map(Enum):
    start: str = "Выберите корпус"
    selected: str = "Отправляем вам геолокацию: "
    map: str = "Вы просматриваете карту корпусов НИТУ МИСИС"
    
class Club(Enum):
    select: str = "Выбери клуб о коротором хотите узнать"
from collections import namedtuple

Person = namedtuple('Person', [
    'name',
    'loan',
    'chips'
])

persons = [Person("Oleg", [150, 150], 0),
           Person("Dima", [300], 100),
           Person("Evgeniy", [450], 2000)]

all_chips = sum(map(lambda person: person.chips, persons))
all_money = sum(map(lambda person: sum(person.loan), persons))
chip_price = all_money / all_chips


def print_info(person: Person):
    money = person.chips * chip_price - sum(person.loan)
    if money >= 0:
        print(f"{person.name} earned {money}")
    else:
        print(f"{person.name} lost {money}")


[print_info(person) for person in persons]

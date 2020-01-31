from collections import namedtuple

Person = namedtuple(
    typename='Person',
    field_names=['name', 'loan', 'chips', 'sold'],
    defaults=("noname", [], 0, 0)
)

persons = [Person("Oleg", [150], 0),
           Person("Dima", [150], 0),
           Person("Serega", [150], 0),
           Person("Misha", [150], 0),
           Person("Andrey", [150], 0),
           Person("Sasha", [150], 0),
           Person("Evgeniy", [150], 0)
           ]

all_chips = sum(map(lambda person: person.chips + person.sold, persons))
all_money = sum(map(lambda person: sum(person.loan), persons))
chip_price = all_money / all_chips


def print_info(person: Person):
    money = (person.chips + person.sold) * chip_price - sum(person.loan)
    if money >= 0:
        print(f"{person.name} earned {money}")
    else:
        print(f"{person.name} lost {money}")


[print_info(person) for person in persons]

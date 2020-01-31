from sqlalchemy.util import namedtuple

ChiptSet = namedtuple(
    typename='chips_set',
    field_names=[
        'amount',
        'nominal'
    ]
)

chips = [ChiptSet(100, 5),
         ChiptSet(100, 25),
         ChiptSet(50, 50),
         ChiptSet(50, 100)]

total_chips_amount = sum([chips_set.amount * chips_set.nominal for chips_set in chips])
print(f"Total amount of chips {total_chips_amount}")
chips_per_person = 650
persons_amount = 7
rebuys = 3
persons_to_count = persons_amount + rebuys

max_chips_per_person = [ChiptSet(int(chip_set.amount / persons_to_count), chip_set.nominal) for chip_set in chips]


def calc_single_set(chip_set, sum_left):
    if sum_left - chip_set.amount * chip_set.nominal >= 0:
        return (chip_set,), sum_left - chip_set.amount * chip_set.nominal
    else:
        chips_amount = int(sum_left / chip_set.nominal)
        return (ChiptSet(chips_amount, chip_set.nominal),), sum_left - chips_amount * chip_set.nominal


def calculate(chips, sum_left) -> tuple:
    if sum_left == 0:
        return ()
    elif not chips:
        print(f"There are some uncalculated chips {sum_left}")
        return ()
    elif sum_left < 0:
        raise ArithmeticError("Bullshit calc. The sum is below 0")
    else:
        calc_chip_set, new_sum_left = calc_single_set(chips[0], sum_left)
        return calc_chip_set + calculate(chips[1:], new_sum_left)


result = calculate(max_chips_per_person, chips_per_person)

[print(f"{chips_set.amount} of {chips_set.nominal}") for chips_set in result]

from sqlalchemy.util import namedtuple

ChiptSet = namedtuple('chips_set', [
    'amount',
    'nominal'
])

chips = [ChiptSet(100, 5),
         ChiptSet(100, 25),
         ChiptSet(50, 50),
         ChiptSet(50, 100)]

total_chips_amount = sum([chips_set.amount * chips_set.nominal for chips_set in chips])
chips_per_person = 600
persons_amount = 7
rebuys = 3
persons_to_count = persons_amount + rebuys

max_chips_per_person = [ChiptSet(int(chip_set.amount / persons_to_count), chip_set.nominal) for chip_set in chips]

#
# def balanced_calc_chips(chip_set, sum_left):
#     new_sum_left = sum_left - chip_set.amount * chip_set.nominal
#     if len(chip_set) == 1:
#         return (chip_set,), new_sum_left
#     else:





def calc_chips(chip_set, sum_left):
    if sum_left - chip_set.amount * chip_set.nominal >= 0:
        return (chip_set,), sum_left - chip_set.amount * chip_set.nominal
    else:
        chips_amount = int(sum_left / chip_set.nominal)
        return (ChiptSet(chips_amount, chip_set.nominal),), sum_left - chips_amount * chip_set.nominal


def take_more(chips, sum_left) -> tuple:
    if sum_left == 0:
        return ()
    elif not chips:
        print(f"There are some uncalculated chips {sum_left}")
        return ()
    elif sum_left < 0:
        raise ArithmeticError("Bullshit calc. The sum is below 0")
    else:
        calc_chip_set, new_sum_left = calc_chips(chips[0], sum_left)
        return calc_chip_set + take_more(chips[1:], new_sum_left)


result = take_more(max_chips_per_person, chips_per_person)

[print(f"{chips_set.amount} of {chips_set.nominal}") for chips_set in result]

from sqlalchemy.util import namedtuple
from functools import reduce
import operator

ChipSet = namedtuple(
    typename='chips_set',
    field_names=[
        'nominal',
        'amount'
    ]
)


chips_sets = [ChipSet(5, 100),
              ChipSet(25, 100),
              ChipSet(50, 50),
              ChipSet(100, 50)]

total_chips_amount = sum([chips_set.amount * chips_set.nominal for chips_set in chips_sets])
chips_per_person = 650

print(f"Total amount of chips {total_chips_amount}")

persons_amount = 7
rebuys = 3
persons_to_count = persons_amount + rebuys


def calc_single_set(chip_set, sum_left):
    if sum_left - chip_set.amount * chip_set.nominal >= 0:
        return (chip_set,), sum_left - chip_set.amount * chip_set.nominal
    else:
        chips_amount = int(sum_left / chip_set.nominal)
        return (ChipSet(chip_set.nominal, chips_amount),), sum_left - chips_amount * chip_set.nominal


def calculate(chips, sum_left) -> tuple:
    if sum_left == 0 and chips:
        return tuple(ChipSet(chip_set.nominal, 0) for chip_set in chips)
    elif sum_left == 0:
        return ()
    elif not chips:
        print(f"There are some uncalculated chips {sum_left}")
        return ()
    elif sum_left < 0:
        raise ArithmeticError("Bullshit calc. The sum is below 0")
    else:
        calc_chip_set, new_sum_left = calc_single_set(chips[0], sum_left)
        return calc_chip_set + calculate(chips[1:], new_sum_left)


def substitute_chip_sets(sets_from, sets_to_substitute):
    return tuple(ChipSet(total.nominal, total.amount - occupied.amount)
                 for occupied, total
                 in zip(sorted(sets_to_substitute), sorted(sets_from))
                 )


def rebalance_lower_pair(chips_set, chips_left):
    sum = chips_set.nominal * chips_set.amount

    chips_left_with_returned = [left_chip_set
                                if chips_set.nominal != left_chip_set.nominal
                                else ChipSet(left_chip_set.nominal, left_chip_set.amount + chips_set.amount)
                                for left_chip_set
                                in chips_left]

    rebalanced_chip_set = calculate(chips_left_with_returned, sum)
    new_chips_left = substitute_chip_sets(chips_left_with_returned, rebalanced_chip_set)

    return rebalanced_chip_set, new_chips_left


def get_rebalanced_chip_sets(raw_result, chips_left):
    if not raw_result:
        return (),
    else:
        rebalanced_chip_set, new_chips_left = rebalance_lower_pair(raw_result[-1:][0], chips_left)
        return (rebalanced_chip_set,) + get_rebalanced_chip_sets(raw_result[:-1], new_chips_left)

max_chips_per_person = sorted(
    tuple(ChipSet(chip_set.nominal, int(chip_set.amount / persons_to_count)) for chip_set in chips_sets),
    reverse=True
)

raw_result = calculate(max_chips_per_person, chips_per_person)
chips_left = substitute_chip_sets(max_chips_per_person, raw_result)
result_sets = list(filter(lambda value: value, get_rebalanced_chip_sets(raw_result, chips_left)))

result = reduce(lambda l1, l2: [ChipSet(ch_set1.nominal, ch_set1.amount + ch_set2.amount)
                                for ch_set1, ch_set2
                                in zip(l1, l2)],
                result_sets
                )


print(result)

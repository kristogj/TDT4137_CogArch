import datasets

DISTANCE = 3.75
DELTA = 1.2

DISTANCE_SET = datasets.distance_set
DELTA_SET = datasets.delta_set
ACTIONS_SET = datasets.actions


def fuzzy_and(a, b):
    return min(a, b)


def fuzzy_or(a, b):
    return max(a, b)


def fuzzy_not(a):
    return 1 - a


# 1 Fuzzyfication
def get_value(fuzzy_set, set_key, x):
    """

    :param fuzzy_set: Dict - DISTANCE_SET, DELTA_SET or ACTIONS_SET
    :param set_key: String - example "VerySmall"
    :param x: Float
    :return: Float
    """
    # Get the possible key-values in set
    key_set = fuzzy_set["keys"][set_key]

    # Check if the ends is at the top
    if fuzzy_set["start"] == key_set[0] and x <= key_set[1]:
        return 1
    if fuzzy_set["end"] == key_set[3] and x >= key_set[2]:
        return 1

    # The check if x is outside the definition value
    if x <= key_set[0] or x >= key_set[3]:
        return 0

    # Then check if x is at a top
    if key_set[1] <= x <= key_set[2]:
        return 1

    # Last case is if x matches on of the slopes
    if key_set[0] < x < key_set[1]:
        return (x - key_set[0]) / (key_set[1] - key_set[0])
    if key_set[2] < x < key_set[3]:
        return 1 - (x - key_set[2]) / (key_set[3] - key_set[2])

    return 0

# 2 Rule evaluation
# Takes care of the spesific reasoning logic in the program
def rule_evaluation():
    """

    :return: dict[String] = Float
    """
    global DISTANCE, DELTA, DISTANCE_SET, DELTA_SET
    weights = dict()
    # Evaluate all the given rules
    weights["None"] = fuzzy_and(get_value(DISTANCE_SET, "Small", DISTANCE), get_value(DELTA_SET, "Growing", DELTA))
    weights["SlowDown"] = fuzzy_and(get_value(DISTANCE_SET, "Small", DISTANCE), get_value(DELTA_SET, "Stable", DELTA))
    weights["SpeedUp"] = fuzzy_and(get_value(DISTANCE_SET, "Perfect", DISTANCE), get_value(DELTA_SET, "Growing", DELTA))
    weights["FloorIt"] = fuzzy_and(get_value(DISTANCE_SET, "VeryBig", DISTANCE),
                                   fuzzy_or(
                                       fuzzy_not(get_value(DELTA_SET, "Growing", DELTA)),
                                       fuzzy_not(get_value(DELTA_SET, "GrowingFast", DELTA))))
    weights["BrakeHard"] = get_value(DISTANCE_SET, "VerySmall", DISTANCE)
    return weights


# 3 Aggregation
def aggreagation(weights):
    """

    :param weights: dict[String] = Float
    :return: List[Float]
    """
    global ACTIONS_SET
    clipping = []
    for x in range(ACTIONS_SET["start"], ACTIONS_SET["end"] + 1):
        val = 0
        for (action, value_set) in ACTIONS_SET["keys"].items():
            if weights[action] > 0:
                if value_set[0] < x < value_set[3]:
                    val = max(val, min(get_value(ACTIONS_SET, action, x), weights[action]))
        clipping.append(val)
    return clipping


# 4 Defuzzyfication
def defuzzyfication(values):
    """

    :param values: List[Float]
    :return: Float
    """
    global ACTIONS_SET
    weights_times_x = [(x + ACTIONS_SET["start"])*val for x, val in enumerate(values)]
    return sum(weights_times_x) / sum(values)


def main():
    weights = rule_evaluation()
    values = aggreagation(weights)
    cog = defuzzyfication(values)
    print(cog)


main()












import random


def cost_for_countries(countries):
    """
    Returns calling costs for a list of countries
    :param countries: list
        "landline" or "mobile"
    :return: dict
        A dictionaru with the format:
            {
                "country_1": "cost_for_country_1",
                "country_2": "cost_for_country_2",
                ...,
                "country_N": "cost_for_country_N"
            }
    """
    result = dict()
    for country in countries:
        result[country] = "{cost} pounds".format(cost=random.randint(1,20))

    return result

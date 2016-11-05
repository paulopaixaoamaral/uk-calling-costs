from . import repository


def calling_cost_for_countries(countries):
    """
    Returns calling costs for a list of countries
    :param countries: list
    :return: dict
        A dictionaru with the format:
            {
                "country_1": "cost_for_country_1",
                "country_2": "cost_for_country_2",
                ...,
                "country_N": "cost_for_country_N"
            }
    """
    return repository.cost_for_countries(countries)

import json

from pprint import pprint

from src import calling_cost_for_countries


if __name__ == "__main__":
    with open("countries.json") as countries_file:
        countries_list = json.load(countries_file)

    cost_type = "landline"
    costs = calling_cost_for_countries(countries=countries_list, cost_type=cost_type)
    print("Costs for calling", cost_type, "from the UK:")
    pprint(costs)

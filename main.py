import json

from pprint import pprint

from src import calling_cost_for_countries


if __name__ == "__main__":
    countries = ["Canada", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"]
    cost_type = "landline"
    costs = calling_cost_for_countries(countries=countries, cost_type=cost_type)
    print("Costs for calling", cost_type, "from the UK:")
    pprint(costs)

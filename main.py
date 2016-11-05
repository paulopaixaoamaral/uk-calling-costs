from src import calling_cost_for_countries


if __name__ == "__main__":
    costs = calling_cost_for_countries(
        countries=["Canada", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"]
    )
    print(costs)

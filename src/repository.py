from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from .config import CALLING_COSTS_URL
from .config import SELENIUM_CHROME_DRIVER


from .exceptions import InvalidCostType
from .exceptions import UnknownCountry
from .exceptions import MissingCountryData


COST_TYPE_MAPPING = {"landline": "Landline", "mobile": "Mobiles"}
DOM_ELEMENT_WAITING_TIME = 5


def cost_for_countries(countries, cost_type="landline"):
    """
    Returns calling costs for a list of countries
    :param countries: list
    :param cost_type: str
        "landline" or "mobile"
    :return: dict
        A dictionaru with the format:
            {
                "country_1": "cost_for_country_1",
                "country_2": "cost_for_country_2",
                ...,
                "country_N": "cost_for_country_N"
            }
    :raises: InvalidCostType
    :raises: RepositoryException
    """
    _validate_calling_cost_type(cost_type=cost_type)

    driver = _init_web_driver()
    try:
        result = dict()
        for country in countries:
            cost = _cost_for_country(driver=driver, country=country, cost_type=cost_type)
            result[country] = cost
    except Exception as e:
        _close_web_driver(driver=driver)
        raise e

    _close_web_driver(driver=driver)
    return result


def _validate_calling_cost_type(cost_type):
    """
    Validates a given calling cost type
    :param cost_type: str
    :raises: InvalidCostType
    """
    if not COST_TYPE_MAPPING.get(cost_type):
        raise InvalidCostType(
            "Cost type '{cost_type} is invalid. Valid cost types: {cost_types}'".format(
                cost_type=cost_type,
                cost_types=",".join(COST_TYPE_MAPPING)
            )
        )


def _init_web_driver():
    """
    Initiates a web drivers
    :return: WebDriver
    """
    return webdriver.Chrome(SELENIUM_CHROME_DRIVER)


def _close_web_driver(driver):
    """
    Closes a Web Driver
    :param driver: WebDriver
    """
    driver.quit()


def _cost_for_country(driver, country, cost_type):
    """
    Returns a cost for a country
    :param driver: WebDriver
    :param country: str
    :param cost_type: cost_type
    :return: str
    """
    driver.get(CALLING_COSTS_URL)
    _search_for_country(driver=driver, country=country)

    try:
        cost_element = _get_cost_element(driver=driver, cost_type=cost_type)
    except Exception:
        raise MissingCountryData(
            "Missing data for country '{country}' and type '{cost_type}'".format(
                country=country,
                cost_type=cost_type
            )
        )

    return cost_element.text


def _search_for_country(driver, country):
    """
    Searches costs for a given country
    :param driver: WebDriver
    :param country: str
    :return: str
    :raises: UnknownCountry
    """
    countries_name_input = driver.find_element_by_id("countryName")
    countries_name_input.clear()
    countries_name_input.send_keys(country)
    countries_name_input.send_keys(Keys.RETURN)

    if _element_has_class(element=countries_name_input, class_name="error"):
        raise UnknownCountry(
            "Cannot fetch costs for country '{country}'.".format(country=country)
        )

    cost_button = WebDriverWait(driver, DOM_ELEMENT_WAITING_TIME).until(
        expected_conditions.element_to_be_clickable(
            (By.ID, "paymonthly")
        )
    )
    cost_button.click()


def _element_has_class(element, class_name):
    """
    Checks if a WebElement has a given class
    :param element: WebElement
    :param class_name: str
    :return:bool
    """
    element_classes = element.get_attribute("class").split(" ")
    return class_name in element_classes


def _get_cost_element(driver, cost_type):
    """
    Returns the DOM cost element
    :param driver: WebDriver
    :param cost_type: str
    :return: WebElement
    """
    cost_type_text = COST_TYPE_MAPPING.get(cost_type)
    x_path = "//table[@id='standardRatesTable']//td[text()='{cost_type_text}']/following-sibling::td".format(
        cost_type_text=cost_type_text
    )
    return WebDriverWait(driver, DOM_ELEMENT_WAITING_TIME).until(
        expected_conditions.visibility_of_element_located((By.XPATH, x_path))
    )

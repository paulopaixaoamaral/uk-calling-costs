from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

from src.repository import cost_for_countries
from src.exceptions import InvalidCostType, UnknownCountry, MissingCountryData


class RepositoryTest(TestCase):
    def test_invalid_cost_type(self):
        self.assertRaises(
            InvalidCostType,
            cost_for_countries,
            ["country A", "country B"],
            "invalid_cost_type"
        )

    @patch("src.repository._init_web_driver")
    def test_unknown_country(self, init_web_driver_mock):
        driver_mock = Mock()
        countries_name_input_mock = Mock()
        countries_name_input_mock.get_attribute.return_value = "some_class error"

        driver_mock.find_element_by_id.return_value = countries_name_input_mock

        init_web_driver_mock.return_value = driver_mock
        self.assertRaises(
            UnknownCountry,
            cost_for_countries,
            ["country A", "country B"],
            "landline"
        )

    @patch("src.repository._init_web_driver")
    def test_unknown_country(self, init_web_driver_mock):
        init_web_driver_mock.return_value = self.__get_webdriver_mock(countries_name_input_class="some_class error")

        self.assertRaises(
            UnknownCountry,
            cost_for_countries,
            ["country A", "country B"],
            "landline"
        )

    @patch("src.repository.WebDriverWait")
    @patch("src.repository._get_cost_element")
    @patch("src.repository._init_web_driver")
    def test_missing_country_data(self, init_web_driver_mock, get_cost_element_mock, webdriver_wait_mock):
        init_web_driver_mock.return_value = self.__get_webdriver_mock(countries_name_input_class="some_class")
        get_cost_element_mock.side_effect = Exception

        self.assertRaises(
            MissingCountryData,
            cost_for_countries,
            ["country A", "country B"],
            "landline"
        )

    def __get_webdriver_mock(self, countries_name_input_class):
        driver_mock = Mock()
        countries_name_input_mock = Mock()
        countries_name_input_mock.get_attribute.return_value = countries_name_input_class
        driver_mock.find_element_by_id.return_value = countries_name_input_mock
        return driver_mock

    @patch("src.repository.WebDriverWait")
    @patch("src.repository._get_cost_element")
    @patch("src.repository._init_web_driver")
    def test_cost_for_countries_success(self, init_web_driver_mock, get_cost_element_mock, webdriver_wait_mock):
        init_web_driver_mock.return_value = self.__get_webdriver_mock(countries_name_input_class="some_class")
        get_cost_element_mock.return_value = Mock(
            text="1.5 pounds"
        )

        costs = cost_for_countries(countries=["country A", "country B"], cost_type="landline")
        self.assertEqual(
            {
                "country A": "1.5 pounds",
                "country B": "1.5 pounds"
            },
            costs
        )

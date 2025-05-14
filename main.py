import time
from selenium import webdriver
from pages import UrbanRoutesPage
import data
import helpers

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.routes_page = UrbanRoutesPage(cls.driver)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.routes_page.get_from() == data.ADDRESS_FROM
        assert self.routes_page.get_to() == data.ADDRESS_TO


    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        assert self.routes_page.get_selected_plan() == 'Supportive'


    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.fill_phone_number(data.PHONE_NUMBER)
        assert self.routes_page.get_entered_phone_number() == data.PHONE_NUMBER


    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.routes_page.get_entered_card_number() == data.CARD_NUMBER
        assert self.routes_page.get_entered_card_code() == data.CARD_CODE


    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.comment_for_driver(data.MESSAGE_FOR_DRIVER)
        assert self.routes_page.get_entered_driver_comment() == data.MESSAGE_FOR_DRIVER



    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.order_blanket_and_handkerchiefs()
        assert self.routes_page.is_blanket_and_handkerchiefs_selected() is True

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(1)
        self.routes_page.select_supportive_plan()
        time.sleep(3)
        number_of_ice_creams = 2
        for count in range(number_of_ice_creams):
            self.routes_page.order_ice_cream()
            time.sleep(1)
        assert int(self.routes_page.verify_ice_cream_order()) == 2


    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        time.sleep(1)
        self.routes_page.select_supportive_plan()
        time.sleep(1)
        self.routes_page.comment_for_driver(data.MESSAGE_FOR_DRIVER)
        self.routes_page.click_order_taxi_button()
        time.sleep(3)
        assert self.routes_page.is_car_search_model_visible(), "Car search model did not appear as expected."


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
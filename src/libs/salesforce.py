import uuid
import logging
from typing import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from models.screenshot import Screenshot
from settings import Settings


logger = logging.getLogger(__name__)
conf = Settings()

class SalesforceCommunityPortalSeleniumTester:

    def __init__(self) -> None:

        logger.info(f'Connecting to Selenium Hub @ {conf.SELENIUM_HUB_URL}')

        self.driver = webdriver.Remote(
            command_executor=conf.SELENIUM_HUB_URL,
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.driver.maximize_window()

        logger.info(f'Connected to Selenium Hub')

    def __del__(self) -> None:

        logger.info('Quitting')

        self.driver.close()
        self.driver.quit()

        logger.info('Done')

    def login_to_salesforce_portal(self) -> None:

        login_url = f'https://{conf.SALESFORCE_ORG_DOMAIN}.my.salesforce.com/'

        logger.info(f'Logging into Salesforce as {conf.SALESFORCE_USERNAME} at {login_url}')

        self.driver.get(login_url)

        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")

        username.send_keys(conf.SALESFORCE_USERNAME)
        password.send_keys(conf.SALESFORCE_PASSWORD)

        self.driver.find_element_by_name("Login").click()

        WebDriverWait(self.driver, conf.SELENIUM_WAIT_TIME).until(
            expected_conditions.url_changes(login_url)
        )        
        
        logger.info('Logged into Salesforce')

    def login_to_community_portal(self) -> None:

        contact_detail_url = f'https://{conf.SALESFORCE_ORG_DOMAIN}.lightning.force.com/{conf.SALESFORCE_CONTACT_ID}'

        logger.info(f'Logging into Community Portal @ {conf.COMMUNITY_PORTAL_URL}')

        self.driver.get(contact_detail_url)

        WebDriverWait(self.driver, conf.SELENIUM_WAIT_TIME).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//runtime_platform_actions-action-renderer[@title="Log in to Community as User"]')
            )
        )

        self.driver.find_element_by_xpath('//button[@name="LoginToNetworkAsUser"]').click()

        WebDriverWait(self.driver, conf.SELENIUM_WAIT_TIME).until(
            expected_conditions.url_to_be(conf.COMMUNITY_PORTAL_URL)
        )            

        logger.info('Logged into Community Portal')

    def collect_screenshot_from_community_portal(self, url: str, wait_time : int = conf.SELENIUM_WAIT_TIME) -> Screenshot:

        logger.info(f'Collecting screenshot from {url}')

        self.driver.get(url)
        
        WebDriverWait(self.driver, wait_time)

        ss = self.driver.find_element_by_tag_name("body").screenshot_as_base64
        
        logger.info('Collected screenshot')

        return Screenshot(url=url, b64png=ss, cid=str(uuid.uuid4()))


    def get_screenshots(self) -> List[Screenshot]:

        self.login_to_salesforce_portal()
        self.login_to_community_portal()

        return [self.collect_screenshot_from_community_portal(url) for url in conf.COMMUNITY_PORTAL_URLS_TO_SCREENSHOT]


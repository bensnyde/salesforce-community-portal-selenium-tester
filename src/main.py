import logging
from datetime import datetime
from jinja2 import Template

from libs.salesforce import SalesforceCommunityPortalSeleniumTester
from libs.email import EmailHtmlMessage
from settings import Settings


if __name__ == '__main__':

    conf = Settings()

    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers = [
            logging.StreamHandler()
        ]
    )

    start_time = datetime.now()
    screenshots = SalesforceCommunityPortalSeleniumTester().get_screenshots()
    execution_time = datetime.now() - start_time

    with open(conf.EMAIL_TEMPLATE) as file_:
        template = Template(file_.read())
        EmailHtmlMessage(conf.SMTP_SERVER, conf.SMTP_PORT, conf.SMTP_USER, conf.SMTP_PASS).send_email(
            conf.EMAIL_TO,
            conf.EMAIL_FROM,
            conf.EMAIL_SUBJECT,
            template.render(
                screenshots=screenshots, 
                execution_time=execution_time
            ),
            screenshots
        )


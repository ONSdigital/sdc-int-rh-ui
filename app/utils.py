from pytz import timezone

from structlog import get_logger

logger = get_logger('respondent-home')

uk_zone = timezone('Europe/London')


class View:
    valid_display_regions = r'{display_region:\ben|cy\b}'
    valid_display_regions_en_only = r'{display_region:\ben\b}'
    valid_user_journeys = r'{user_journey:\bstart|request\b}'
    page_title_error_prefix_en = 'Error: '
    page_title_error_prefix_cy = 'Gwall: '

    @staticmethod
    def log_entry(request, endpoint):
        method = request.method
        logger.info(f"received {method} on endpoint '{endpoint}'",
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    method=request.method,
                    path=request.path)

    @staticmethod
    def gen_page_url(request):
        full_url = str(request.rel_url)
        if full_url[:3] == '/en' or full_url[:3] == '/cy':
            generic_url = full_url[3:]
        else:
            generic_url = full_url
        return generic_url

    @staticmethod
    def get_contact_centre_number(display_region):
        if display_region == 'cy':
            contact_centre_number = '0800 169 2021'
        else:
            contact_centre_number = '0800 141 2021'
        return contact_centre_number

    @staticmethod
    def get_campaign_site_link(request, display_region, requested_link):
        link = '/'

        if requested_link == 'contact-us':
            if display_region == 'cy':
                link = 'https://cy.ons.gov.uk/aboutus/contactus/surveyenquiries'
            else:
                link = 'https://www.ons.gov.uk/aboutus/contactus/surveyenquiries'
        elif requested_link == 'access_to_research_link':
            if display_region == 'cy':
                link = "https://cy.ons.gov.uk/aboutus/whatwedo/statistics/requestingstatistics" \
                       "/accesstounpublishedonsresearchdatabygovernmentorganisationsforstatisticalresearch "
            else:
                link = "https://www.ons.gov.uk/aboutus/whatwedo/statistics/requestingstatistics" \
                       "/accesstounpublishedonsresearchdatabygovernmentorganisationsforstatisticalresearch "
        elif requested_link == 'approved_researchers_link':
            if display_region == 'cy':
                link = "https://cy.ons.gov.uk/aboutus/whatwedo/statistics/requestingstatistics/approvedresearcherscheme"
            else:
                link = "https://www.ons.gov.uk/aboutus/whatwedo/statistics/requestingstatistics" \
                       "/approvedresearcherscheme "
        elif requested_link == 'ons_data_protection_link':
            if display_region == 'cy':
                link = "https://cy.ons.gov.uk/aboutus/transparencyandgovernance/dataprotection"
            else:
                link = "https://www.ons.gov.uk/aboutus/transparencyandgovernance/dataprotection"
        elif requested_link == 'code_of_practice_link':
            link = "https://code.statisticsauthority.gov.uk/"

        return link


class FlashMessage:
    @staticmethod
    def generate_flash_message(text, level, message_type, field):
        json_return = {'text': text, 'level': level, 'type': message_type, 'field': field}
        return json_return

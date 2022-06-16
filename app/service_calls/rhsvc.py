from structlog import get_logger
from app.service_calls import ServiceCalls

logger = get_logger('respondent-home')


class RHSvc:
    @staticmethod
    async def get_uac_details(request):
        uac_hash = request['uac_hash']
        logger.info('making get request for uac',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    uac_hash=uac_hash)
        rhsvc_url = request.app['RHSVC_URL']
        return await ServiceCalls.make_request(request,
                                               'GET',
                                               f'{rhsvc_url}/uacs/{uac_hash}',
                                               auth=request.app['RHSVC_AUTH'],
                                               return_type="json")

    @staticmethod
    async def get_eq_launch_token(request, url_path):
        rhsvc_url = request.app['RHSVC_URL']
        client_ip = request['client_ip']
        url = f'{rhsvc_url}{url_path}&clientIP={client_ip}'
        return await ServiceCalls.make_request(request,
                                               'GET',
                                               url,
                                               auth=request.app['RHSVC_AUTH'],
                                               return_type="text")

    @staticmethod
    async def get_cases_by_attribute(request, attribute_key, attribute_value):
        rhsvc_url = request.app['RHSVC_URL']
        return await ServiceCalls.make_request(request,
                                               'GET',
                                               f'{rhsvc_url}/cases/attribute/{attribute_key}/{attribute_value}',
                                               return_type="json")

    @staticmethod
    async def register_new_case(request, data):
        new_case_json = {
            'schoolId': '1',  # Dummy value - no way to source currently
            'schoolName': data['school_name'],
            'consentGivenTest': 'true',  # Fixed value
            'consentGivenSurvey': 'true',  # Fixed value
            'firstName': data['parent_first_name'],
            # Unable to submit parent_middle_names
            'lastName': data['parent_last_name'],
            'childFirstName': data['child_first_name'],
            'childMiddleNames': data['child_middle_names'],
            'childLastName': data['child_last_name'],
            'childDob': data['child_dob'],
            'mobileNumber': data['mobile_number'],
            'emailAddress': 'a.b@c.com'  # Dummy value - not required to be captured currently
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await ServiceCalls.make_request(request,
                                               'POST',
                                               f'{rhsvc_url}/cases/new',
                                               auth=request.app['RHSVC_AUTH'],
                                               request_json=new_case_json)

    @staticmethod
    async def post_web_form(request, form_data):
        form_json = {
            'category': form_data['category'],
            'region': form_data['region'],
            'language': form_data['language'],
            'name': form_data['name'],
            'description': form_data['description'],
            'email': form_data['email'],
            'clientIP': ServiceCalls.single_client_ip(request)
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await ServiceCalls.make_request(request,
                                               'POST',
                                               f'{rhsvc_url}/webform',
                                               auth=request.app['RHSVC_AUTH'],
                                               request_json=form_json)

from structlog import get_logger
from app.service_calls import MakeRequest, SingleClientIP
from datetime import datetime
from pytz import utc

logger = get_logger('respondent-home')


class Authentication:
    @staticmethod
    async def get_uac_details(request):
        uac_hash = request['uac_hash']
        logger.info('making get request for uac',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    uac_hash=uac_hash)
        rhsvc_url = request.app['RHSVC_URL']
        return await MakeRequest.make_request(request,
                                              'GET',
                                              f'{rhsvc_url}/uacs/{uac_hash}',
                                              auth=request.app['RHSVC_AUTH'],
                                              return_json=True)


class Cases:
    @staticmethod
    async def get_cases_by_uprn(request, uprn):
        rhsvc_url = request.app['RHSVC_URL']
        return await MakeRequest.make_request(request,
                                              'GET',
                                              f'{rhsvc_url}/cases/uprn/{uprn}',
                                              return_json=True)


class EQLaunch:
    @staticmethod
    async def post_surveylaunched(request, case, adlocation):
        if not adlocation:
            adlocation = ''
        launch_json = {
            'questionnaireId': case['qid'],
            'caseId': case['collectionCase']['caseId'],
            'agentId': adlocation,
            'clientIP': SingleClientIP.single_client_ip(request)
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await MakeRequest.make_request(request,
                                              'POST',
                                              f'{rhsvc_url}/surveyLaunched',
                                              auth=request.app['RHSVC_AUTH'],
                                              request_json=launch_json)


class Fulfilments:
    @staticmethod
    async def request_fulfilment_sms(request, case_id, tel_no, fulfilment_code_array):
        rhsvc_url = request.app['RHSVC_URL']
        fulfilment_json = {
            'caseId': case_id,
            'telNo': tel_no,
            'fulfilmentCodes': fulfilment_code_array,
            'dateTime': datetime.now(utc).isoformat(),
            'clientIP': SingleClientIP.single_client_ip(request)
        }
        url = f'{rhsvc_url}/cases/{case_id}/fulfilments/sms'
        return await MakeRequest.make_request(request,
                                              'POST',
                                              url,
                                              auth=request.app['RHSVC_AUTH'],
                                              request_json=fulfilment_json)

    @staticmethod
    async def request_fulfilment_post(request, case_id, first_name, last_name, fulfilment_code_array, title=None):
        rhsvc_url = request.app['RHSVC_URL']
        fulfilment_json = {
            'caseId': case_id,
            'title': title,
            'forename': first_name,
            'surname': last_name,
            'fulfilmentCodes': fulfilment_code_array,
            'dateTime': datetime.now(utc).isoformat(),
            'clientIP': SingleClientIP.single_client_ip(request)
        }
        url = f'{rhsvc_url}/cases/{case_id}/fulfilments/post'
        return await MakeRequest.make_request(request,
                                              'POST',
                                              url,
                                              auth=request.app['RHSVC_AUTH'],
                                              request_json=fulfilment_json)

    @staticmethod
    async def request_fulfilment_email(request, case_id, email, fulfilment_code_array):
        rhsvc_url = request.app['RHSVC_URL']
        fulfilment_json = {
            'caseId': case_id,
            'email': email,
            'fulfilmentCodes': fulfilment_code_array,
            'dateTime': datetime.now(utc).isoformat(),
            'clientIP': SingleClientIP.single_client_ip(request)
        }
        url = f'{rhsvc_url}/cases/{case_id}/fulfilments/email'
        return await MakeRequest.make_request(request,
                                              'POST',
                                              url,
                                              auth=request.app['RHSVC_AUTH'],
                                              request_json=fulfilment_json)


class RegisterCase:
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
        return await MakeRequest.make_request(request,
                                              'POST',
                                              f'{rhsvc_url}/cases/new',
                                              auth=request.app['RHSVC_AUTH'],
                                              request_json=new_case_json)


class Surveys:
    @staticmethod
    async def get_survey_details(request, survey_id):
        rhsvc_url = request.app['RHSVC_URL']
        return await MakeRequest.make_request(request,
                                              'GET',
                                              f'{rhsvc_url}/surveys/{survey_id}',
                                              auth=request.app['RHSVC_AUTH'],
                                              return_json=True)

    @staticmethod
    async def survey_fulfilments_by_type(request, method, survey_id, language):
        survey_data = await Surveys.get_survey_details(request, survey_id)
        method_data = {}
        pack_code = ''
        if method == 'sms':
            method_data = survey_data['allowedSmsFulfilments']
        elif method == 'post':
            method_data = survey_data['allowedPrintFulfilments']
        elif method == 'email':
            method_data = survey_data['allowedEmailFulfilments']

        for fulfilment in method_data:
            for region in fulfilment['metadata']['suitableRegions']:
                if region == language:
                    pack_code = fulfilment['packCode']

        return pack_code


class RHSvcWebForm:
    @staticmethod
    async def post_webform(request, form_data):
        form_json = {
            'category': form_data['category'],
            'region': form_data['region'],
            'language': form_data['language'],
            'name': form_data['name'],
            'description': form_data['description'],
            'email': form_data['email'],
            'clientIP': SingleClientIP.single_client_ip(request)
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await MakeRequest.make_request(request,
                                              'POST',
                                              f'{rhsvc_url}/webform',
                                              auth=request.app['RHSVC_AUTH'],
                                              request_json=form_json)

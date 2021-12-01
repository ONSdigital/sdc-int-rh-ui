import time
import hashlib
from collections import namedtuple
from uuid import uuid4
from aiohttp.web import Application
from structlog import get_logger

from .exceptions import InvalidEqPayLoad

logger = get_logger('respondent-home')

Request = namedtuple('Request', ['method', 'path', 'auth', 'func'])


class EqPayloadConstructor(object):
    def __init__(self, uac_claim_ctx: dict, attributes: dict, app: Application):
        """
        Creates the payload needed to communicate with EQ, built from the RH service
        """

        self._app = app

        self._tx_id = str(uuid4())

        if not attributes:
            raise InvalidEqPayLoad('Attributes is empty')

        self._sample_attributes = attributes

        salt = app['EQ_SALT']
        domain_url_protocol = app['DOMAIN_URL_PROTOCOL']
        domain_url = app['DOMAIN_URL_EN']
        url_path_prefix = app['URL_PATH_PREFIX']
        url_display_region = '/' + self._sample_attributes['display_region']
        save_and_exit_url = '/signed-out/'
        start_url = '/start/'
        self._account_service_url = \
            f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{start_url}'
        self._account_service_log_out_url = \
            f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{save_and_exit_url}'

        self._channel = 'rh'

        try:
            self._case_id = uac_claim_ctx['collectionCase']['caseId']
        except KeyError:
            raise InvalidEqPayLoad('No case id in supplied case JSON')

        try:
            self._collex_id = uac_claim_ctx['collectionExercise']['collectionExerciseId']
        except KeyError:
            raise InvalidEqPayLoad('No collection id in supplied case JSON')

        try:
            self._questionnaire_id = uac_claim_ctx['qid']
        except KeyError:
            raise InvalidEqPayLoad('No questionnaireId in supplied case JSON')

        self._response_id = self.hash_qid(self._questionnaire_id, salt)

        try:
            self._uprn = uac_claim_ctx['collectionCase']['address']['uprn']
        except KeyError:
            raise InvalidEqPayLoad('Could not retrieve address uprn from case JSON')

        try:
            self._region = uac_claim_ctx['collectionCase']['address']['region'][0]
        except KeyError:
            raise InvalidEqPayLoad('Could not retrieve region from case JSON')

        if self._region == 'E':
            self._language_code = 'en'
        else:
            self._language_code = self._sample_attributes['language']

        #   The following are put in as part of SOCINT-258 - temporary for use with POC
        try:
            self._collex_name = uac_claim_ctx['collectionExercise']['name']
        except KeyError:
            raise InvalidEqPayLoad('No collection name supplied in case JSON')

        try:
            self._case_ref = uac_claim_ctx['collectionCase']['caseRef']
        except KeyError:
            raise InvalidEqPayLoad('No caseRef supplied in case JSON')

        try:
            self._survey_url = uac_claim_ctx['collectionInstrumentUrl']
        except KeyError:
            raise InvalidEqPayLoad('No collectionInstrumentUrl in case JSON')

    async def build(self):
        """__init__ is not a coroutine function, so I/O needs to go here"""

        logger.debug('creating payload for jwt',
                     case_id=self._case_id,
                     tx_id=self._tx_id)

        payload = {
            'jti': str(uuid4()),
            'tx_id': self._tx_id,
            'iat': int(time.time()),
            'exp': int(time.time() + (5 * 60)),
            'collection_exercise_sid': self._collex_id,
            'region_code': self.convert_region_code(self._region),
            'ru_ref': self._questionnaire_id,   # SOCINT-258 - temporary for use with POC
            'user_id': '1234567890',            # SOCINT-258 - temporary for use with POC
            'case_id': self._case_id,
            'language_code': self._language_code,
            'display_address': self.build_display_address(self._sample_attributes),
            'response_id': self._response_id,
            'account_service_url': self._account_service_url,
            'account_service_log_out_url': self._account_service_log_out_url,
            'channel': self._channel,
            'questionnaire_id': self._questionnaire_id,
            'eq_id': '9999',  # originally 'census' changed for SOCINT-258
            'period_id': self._collex_id,  # SOCINT-258 - temporary for use with POC
            'form_type': 'zzz',  # Was originally 'H' but changed for SOCINT-258
            # The following are put in as part of SOCINT-258 - temporary for use with POC
            'schema_name': 'zzz_9999',
            'period_str': self._collex_name,
            'survey_url': self._survey_url,
            'case_ref': self._case_ref,
            # ru_name is a temp harcoded value for a show and tell. It will likely be removed or reference another field
            'ru_name': 'Hercule Poirot'
        }
        return payload

    @staticmethod
    def hash_qid(qid, salt):
        hashed = hashlib.sha256(salt.encode() + qid.encode()).hexdigest()
        return qid + hashed[0:16]

    @staticmethod
    def build_display_address(sample_attributes):
        """
        Build `display_address` value by appending not-None (in order) values of sample attributes

        :param sample_attributes: dictionary of address attributes
        :return: string of a single address attribute or a combination of two
        """
        display_address = ''

        try:
            transient_town_name = sample_attributes['transientTownName']
            transient_accommodation_type = sample_attributes['transientAccommodationType']
            if sample_attributes['language'] == 'cy':
                display_address = transient_accommodation_type + ' gerllaw ' + transient_town_name
            else:
                display_address = transient_accommodation_type + ' near ' + transient_town_name

        except KeyError:
            for key in [
                'addressLine1', 'addressLine2', 'addressLine3', 'townName',
                'postcode'
            ]:  # retain order of address attributes
                val = sample_attributes.get(key)
                if val:
                    prev_display = display_address
                    display_address = f'{prev_display}, {val}' if prev_display else val
                    if prev_display:
                        break  # break once two address attributes have been added

        if not display_address:
            raise InvalidEqPayLoad(
                'Displayable address not in sample attributes')
        return display_address

    @staticmethod
    def convert_region_code(case_region):
        if case_region == 'N':
            region_value = 'GB-NIR'
        elif case_region == 'W':
            region_value = 'GB-WLS'
        else:
            region_value = 'GB-ENG'
        return region_value

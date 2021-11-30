import jwt
from app.service_calls import MakeRequest


class JWT:
    @staticmethod
    def generate_jwt(request):
        key = request.app['ADDRESS_INDEX_SVC_KEY']
        token = jwt.encode({}, key, algorithm="HS256")
        return token


class Postcode:
    @staticmethod
    async def get_postcode_return(request, postcode, display_region):
        postcode_return = await Postcode.get_ai_postcode(request, postcode)

        address_options = []

        if display_region == 'cy':
            cannot_find_text = 'Ni allaf ddod o hyd i fy nghyfeiriad'
        else:
            cannot_find_text = 'I cannot find my address'

        for singleAddress in postcode_return['response']['addresses']:
            address_options.append({
                'value': singleAddress['uprn'],
                'label': {
                    'text': singleAddress['formattedAddress']
                },
                'id': singleAddress['uprn']
            })

        address_options.append({
            'value': 'xxxx',
            'label': {
                'text': cannot_find_text
            },
            'id': 'xxxx'
        })

        address_content = {
            'postcode': postcode,
            'addresses': address_options,
            'total_matches': postcode_return['response']['total']
        }

        return address_content

    @staticmethod
    async def get_ai_postcode(request, postcode):
        ai_svc_url = request.app['ADDRESS_INDEX_SVC_URL']
        ai_epoch = request.app['ADDRESS_INDEX_EPOCH']
        token = JWT.generate_jwt(request)
        url = f'{ai_svc_url}/addresses/rh/postcode/{postcode}?limit=5000&epoch={ai_epoch}'
        headers = {'Authorization': 'Bearer ' + token}
        return await MakeRequest.make_request(request,
                                              'GET',
                                              url,
                                              headers=headers,
                                              return_json=True)
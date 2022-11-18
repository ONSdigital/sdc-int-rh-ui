async def domain_processor(request):
    domain_protocol = request.app['DOMAIN_URL_PROTOCOL']
    domain_en = request.app['DOMAIN_URL_EN']
    return {'domain_url_en': domain_protocol + domain_en,
            'site_name_en': request.app['SITE_NAME_EN'],
            'site_name_cy': request.app['SITE_NAME_CY']}

async def domain_processor(request):
    domain_protocol = request.app['DOMAIN_URL_PROTOCOL']
    domain_en = request.app['DOMAIN_URL_EN']
    domain_cy = request.app['DOMAIN_URL_CY']
    return {'domain_url_en': domain_protocol + domain_en,
            'domain_url_cy': domain_protocol + domain_cy,
            'site_name_en': request.app['SITE_NAME_EN'],
            'site_name_cy': request.app['SITE_NAME_CY']}

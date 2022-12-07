async def domain_processor(request):
    domain_protocol = request.app['DOMAIN_URL_PROTOCOL']
    domain = request.app['DOMAIN_URL']
    return {'domain_url': domain_protocol + domain,
            'site_name_en': request.app['SITE_NAME_EN'],
            'site_name_cy': request.app['SITE_NAME_CY']}

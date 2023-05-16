async def ga_ua_id_processor(request):
    return {'gtm_cont_id': request.app['GTM_CONTAINER_ID'], 'gtm_tag_id': request.app['GTM_TAG_ID']}

from .swissmeteowarningsclient import SwissMeteoWarningsClient
from .geodata import GeoData

geoData = GeoData(46.6261212,8.0269831, None)
geoData.init_geo_data()
place = geoData.get_place()
post_code = geoData.get_post_code()

'''  language_code = f"{hass.config.language}-{hass.config.country}"'''

swissMeteoWarningsClient = SwissMeteoWarningsClient(place, 2826, "fr", "ch")
swissMeteoWarningsClient.update()
warnings = swissMeteoWarningsClient.get_typed_data()
'''
for i in range(2000, 9700):
    swissMeteoWarningsClient = SwissMeteoWarningsClient(place, i, "fr", "ch")
    swissMeteoWarningsClient.update()
    warnings = swissMeteoWarningsClient.get_typed_data()
    if (warnings is None):
        print(str(i) + " - None")
    else:
        print(str(i), " - ", [warning.type.name for warning in warnings])
'''
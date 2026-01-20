FEED_URL = 'https://qgisfeed.envirosolutions.pl/'


INDUSTRIES = {
    "999": "Nie wybrano",
    "e": "Energetyka/OZE",
    "u": "Urząd",
    "td": "Transport/Drogi",
    "pg": "Planowanie/Geodezja",
    "wk": "WodKan",
    "s": "Środowisko",
    "rl": "Rolnictwo/Leśnictwo",
    "tk": "Telkom",
    "edu": "Edukacja",
    "i": "Inne",
    "it": "IT",
    "n": "Nieruchomości"
}


OLDEST_ORTO_YEAR = 1957

QT_VER = {
    6: "6."
}

ORTO_SERVICE_URL = "https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/StandardResolutionTime"
WMS_BASE_PARAMS = "IgnoreGetFeatureInfoUrl=1&IgnoreGetMapUrl=1&contextualWMSLegend=0&crs=EPSG:2180&format=image/jpeg&layers=Raster&styles=&url="
WMS_TIME_SUFFIX = "-01-01T00%3A00%3A00.000%2B01%3A00"

SRS_CODE = "2180"
# Coordinates of Warsaw in EPSG:2180
POINT_COORDINATES = (637420, 487755)
# Empirically determined initial scale for Warsaw
INITIAL_SCALE = 37147

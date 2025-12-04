import unittest
import sys
import os
from qgis.PyQt.QtCore import QObject, QEventLoop, QTimer, QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import (
    QgsApplication,
    QgsRasterLayer,
    QgsNetworkAccessManager,
    QgsProject
)
from qgis.PyQt.QtWidgets import QApplication

class NetworkLogger(QObject):
    """
    Logger sieciowy odporny na zmiany API w QGIS 4.
    """
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.last_status = None
        self.last_error = None
        self.last_url = "Nieznany URL"
        self.reply_received = False 

    def on_finished(self, reply):
        """
        Ta metoda obsługuje zarówno stare QNetworkReply (Qt5) 
        jak i nowe QgsNetworkReplyContent (Qt6/QGIS4).
        """

        self.last_status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        self.last_error = reply.error()

        # pobranie url z obiektu reply w zaleznosci od wersji QGIS
        try:
            if hasattr(reply, 'request'):
                req = reply.request()
                self.last_url = req.url().toString()
            elif hasattr(reply, 'url'):
                self.last_url = reply.url().toString()
            else:
                self.last_url = "Brak dostępu do URL w obiekcie reply"
        except Exception as e:
            self.last_url = f"Błąd parsowania URL: {e}"
            
        self.reply_received = True

class TestGeoportalFutureProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''
        Inicjalizacja QGISa i podlaczenie Loggera do sygnału finished.
        Wykonywane jest to tylko raz na poczatku testow.
        '''
        cls.qgs = QgsApplication([], False)
        cls.qgs.initQgis()
        
        cls.nam = QgsNetworkAccessManager.instance()
        
        cls.logger = NetworkLogger()
        
        # podlaczenie loggera do sygnału finished
        cls.nam.finished.connect(cls.logger.on_finished)

    @classmethod
    def tearDownClass(cls):
        # usuniecie QGISa
        cls.qgs.exitQgis()

    def testYearsAvailability(self):

        with open(os.path.join(os.path.dirname(__file__), 'data', 'years.txt')) as f:
            content = f.read()
            years = [line.strip() for line in content.split(",") if line.strip()]

        print(f"Uruchamiam testy (QGIS 4 Ready) dla lat: {years}")

        base_url = (
            "IgnoreGetFeatureInfoUrl=1&IgnoreGetMapUrl=1&crs=EPSG:2180&format=image/jpeg"
            "&layers=Raster&styles=&url=https://mapy.geoportal.gov.pl/wss/service/"
            "PZGIK/ORTO/WMS/StandardResolutionTime?TIME="
        )

        for year in years:
            with self.subTest(year=year):
                self.logger.reset()

                time_param = f"{year}-01-01T00%3A00%3A00.000%2B01%3A00"
                uri = base_url + time_param

                # Tworzymy warstwę
                layer = QgsRasterLayer(uri, f"orto_{year}", "wms")

                # petla czekajaca na odpowiedz maksymalnie 5s
                loop = QEventLoop()

                # podlaczenie loggera
                self.nam.finished.connect(loop.quit)
                
                timer = QTimer()
                timer.setSingleShot(True)
                timer.timeout.connect(loop.quit)
                timer.start(5000) 
                
                if not self.logger.reply_received:
                    loop.exec_()
                
                # odlaczenie loggera
                self.nam.finished.disconnect(loop.quit)

                status = self.logger.last_status

                if status is None:
                    print(f"Rok {year}: Timeout.")
                else:
                    print(f"Rok {year}: Status {status}")
                    self.assertEqual(status, 200, f"Oczekiwano 200, jest {status}")
                    
                    if not layer.isValid():
                        print(f"Rok {year}: Status 200, ale layer.isValid() == False. Błąd: {layer.error().message()}")

if __name__ == "__main__":
    unittest.main()
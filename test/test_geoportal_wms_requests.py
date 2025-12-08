import unittest
import sys
import os
from qgis.PyQt.QtCore import QObject, QEventLoop, QTimer
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import (
    QgsApplication,
    QgsRasterLayer,
    QgsNetworkAccessManager
)

class NetworkLogger(QObject):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.last_status = None
        self.last_error = None
        self.last_url = "Nieznany URL"
        self.reply_received = False 

    def on_finished(self, reply):
        self.last_status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        self.last_error = reply.error()
        self.reply_received = True

class TestGeoportalFutureProof(unittest.TestCase):
    
    qgs = None
    nam = None
    logger = None
    test_results = []

    @classmethod
    def setUpClass(cls):
        """
        Uruchamia się RAZ przed startem testów w tym pliku.
        Inicjuje QGIS i przygotowuje środowisko.
        """
        if QgsApplication.instance() is None:
            cls.qgs = QgsApplication([], False)
            cls.qgs.initQgis()
        else:
            cls.qgs = QgsApplication.instance()
        
        cls.nam = QgsNetworkAccessManager.instance()
        cls.logger = NetworkLogger()
        cls.nam.finished.connect(cls.logger.on_finished)
        
        cls.test_results = []

    @classmethod
    def tearDownClass(cls):
        """
        Uruchamia się RAZ po zakończeniu wszystkich testów w tym pliku.
        Generuje raport i sprząta.
        """
        print("\n" + "="*60)
        print(f"RAPORT PODSUMOWUJĄCY ({len(cls.test_results)} przypadków)")
        print("="*60)
        
        passed = [r for r in cls.test_results if r['status'] == 'OK']
        failed = [r for r in cls.test_results if r['status'] != 'OK']
        
        print(f"SUKCES: {len(passed)}")
        print(f"BŁĄD:   {len(failed)}")
        
        if failed:
            print("-" * 60)
            print("Szczegóły błędów:")
            for item in failed:
                print(f" -> Rok {item['year']}: {item['reason']}")
        print("="*60 + "\n")

        if cls.qgs:
            cls.qgs.exitQgis()

    def testYearsAvailability(self):
        """
        Główny test sprawdzający dostępność lat.
        """
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'years.txt')
        
        if not os.path.exists(file_path):
            self.fail(f"Brak pliku konfiguracyjnego: {file_path}")

        with open(file_path) as f:
            years = [line.strip() for line in f.read().split(",") if line.strip()]

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

                layer = QgsRasterLayer(uri, f"orto_{year}", "wms")

                loop = QEventLoop()
                conn = self.nam.finished.connect(loop.quit)
                
                timer = QTimer()
                timer.setSingleShot(True)
                timer.timeout.connect(loop.quit)
                timer.start(5000) # 5 sekund timeout
                
                if not self.logger.reply_received:
                    loop.exec_()
                
                self.nam.finished.disconnect(conn)
                timer.stop()

                status = self.logger.last_status
                result_entry = {'year': year, 'status': 'FAIL', 'reason': ''}

                if status is None:
                    result_entry['reason'] = "Timeout (5s)"
                elif status != 200:
                    result_entry['reason'] = f"Kod HTTP {status}"
                elif not layer.isValid():
                    result_entry['reason'] = f"HTTP 200, ale warstwa Invalid: {layer.error().message()}"
                else:
                    result_entry['status'] = 'OK'
                    result_entry['reason'] = "OK"

                self.test_results.append(result_entry)

                self.assertEqual(
                    result_entry['status'], 
                    'OK', 
                    f"Rok {year}: {result_entry['reason']}"
                )

if __name__ == "__main__":
    unittest.main()
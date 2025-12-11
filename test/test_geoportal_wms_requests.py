import unittest
import sys
import os
import importlib 
from unittest.mock import MagicMock, patch
from .constans import YEARS 

# Dynamiczne ustalanie ścieżek i nazwy pakietu
current_dir = os.path.dirname(os.path.abspath(__file__))
plugin_dir = os.path.dirname(current_dir)
plugins_dir = os.path.dirname(plugin_dir)
sys.path.append(plugins_dir)

   

# Pobieramy nazwę folderu wtyczki
plugin_package_name = os.path.basename(plugin_dir)

from qgis.PyQt.QtCore import QObject, QEventLoop, QTimer
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import (
    QgsApplication,
    QgsRasterLayer,
    QgsNetworkAccessManager
)

module_name = f"{plugin_package_name}.archiwalna_ortofotomapa"
plugin_module = importlib.import_module(module_name)
ArchiwalnaOrtofotomapa = plugin_module.ArchiwalnaOrtofotomapa

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
    plugin = None

    @classmethod
    def setUpClass(cls):
        if QgsApplication.instance() is None:
            cls.qgs = QgsApplication([], False)
            cls.qgs.initQgis()
        else:
            cls.qgs = QgsApplication.instance()
        
        cls.nam = QgsNetworkAccessManager.instance()
        cls.logger = NetworkLogger()
        cls.nam.finished.connect(cls.logger.on_finished)
        
        cls.test_results = []

        # Dynamiczne mockowanie qgis_feed
        feed_mock = MagicMock()
        sys.modules[f'{plugin_package_name}.qgis_feed'] = feed_mock
        
        feed_mock.QgisFeed.return_value.initFeed = MagicMock()
        feed_mock.QgisFeedDialog.return_value.exec_.return_value = 0 

        # Mockowanie QgsSettings i QSettings
        plugin_module_name = ArchiwalnaOrtofotomapa.__module__
        
        cls.settings_patcher = patch(f'{plugin_module_name}.QgsSettings')
        MockQgsSettings = cls.settings_patcher.start()
        MockQgsSettings.return_value.value.return_value = "geodezja" 

        cls.qsettings_patcher = patch(f'{plugin_module_name}.QSettings')
        MockQSettings = cls.qsettings_patcher.start()
        MockQSettings.return_value.value.return_value = "pl_PL"

        cls.iface_mock = MagicMock()
        cls.iface_mock.mainWindow.return_value.findChild.return_value = None
        
        cls.plugin = ArchiwalnaOrtofotomapa(cls.iface_mock)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'settings_patcher'):
            cls.settings_patcher.stop()
        if hasattr(cls, 'qsettings_patcher'):
            cls.qsettings_patcher.stop()

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

        for year in YEARS:
            with self.subTest(year=year):
                self.logger.reset()
                
                uri = self.plugin.makeDataSourceUri(year)

                layer = QgsRasterLayer(uri, f"orto_{year}", "wms")
                
                status = self.logger.last_status
                result_entry = {'year': year, 'status': 'FAIL', 'reason': ''}

                if status is None:
                    result_entry['reason'] = "Timeout"
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
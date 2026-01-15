from .constants import QT_VER 
from qgis.core import Qgis, QgsMessageLog
from . import PLUGIN_NAME

class Utils:
    @staticmethod
    def isCompatibleQtVersion(cur_version, tar_version):
        return cur_version.startswith(QT_VER[tar_version])

    @staticmethod
    def pushLogInfo(message: str) -> None:
        QgsMessageLog.logMessage(
            message,
            tag=PLUGIN_NAME,
            level=Qgis.Info
        )
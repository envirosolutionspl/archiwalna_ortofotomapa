import os
from .constants import QT_VER
from qgis.core import Qgis, QgsMessageLog, QgsApplication
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QPainter, QPalette, QPixmap
from qgis.PyQt.QtWidgets import QWidget
from . import PLUGIN_NAME

PLUGIN_DIR = os.path.dirname(__file__)

class MessageUtils:

    @staticmethod
    def pushLogInfo(message: str) -> None:
        QgsMessageLog.logMessage(
            message,
            tag=PLUGIN_NAME,
            level=Qgis.MessageLevel.Info
        )

    @staticmethod
    def pushLogWarning(message: str) -> None:
        QgsMessageLog.logMessage(
            message,
            tag=PLUGIN_NAME,
            level=Qgis.MessageLevel.Warning
        )

    @staticmethod
    def pushLogCritical(message: str) -> None:
        QgsMessageLog.logMessage(
            message,
            tag=PLUGIN_NAME,
            level=Qgis.MessageLevel.Critical
        )

class ThemeUtils:
    """
    Motyw jasny/ciemny i logo dla okna wtyczki
    """

    @staticmethod
    def isDarkTheme():
        """
        Ciemny motyw QGIS (np. Night Mapping) albo ciemna paleta systemu
        """
        name = ''
        try:
            theme_name = (QgsApplication.themeName() or '').lower()
            if theme_name:
                name = theme_name.lower()
        except AttributeError as e:
            MessageUtils.pushLogCritical(f"Atrybut motywu jest niedostępny (AttributeError): {e}")
        except RuntimeError as e:
            MessageUtils.pushLogCritical(f"Aplikacja QGIS nie jest w pełni zainicjalizowana (RuntimeError): {e}")
        except TypeError as e:
            MessageUtils.pushLogCritical(f"Nieoczekiwany typ danych przy pobieraniu motywu (TypeError): {e}")
        except Exception as e:
            MessageUtils.pushLogCritical(f"Nieoczekiwany błąd: {e}")

        if 'night' in name or 'dark' in name:
            return True
        return QgsApplication.palette().color(QPalette.ColorRole.Window).lightness() < 128

    @staticmethod
    def repolishAll(window):
        for widget in [window] + window.findChildren(QWidget):
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

    @staticmethod
    def themedIcon(path, size=48, disabledOpacity=0.35):
        icon = QIcon(path)
        dimmed = QPixmap(size, size)
        dimmed.fill(Qt.GlobalColor.transparent)
        painter = QPainter(dimmed)
        painter.setOpacity(disabledOpacity)
        painter.drawPixmap(0, 0, icon.pixmap(size, size))
        painter.end()
        icon.addPixmap(dimmed, QIcon.Mode.Disabled)
        return icon

    @staticmethod
    def setLogo(label, filename, height):
        pix = QPixmap(os.path.join(PLUGIN_DIR, 'icons', filename))
        if pix.isNull():
            return
        dpr = label.devicePixelRatioF()
        pix = pix.scaledToHeight(int(height * dpr), Qt.TransformationMode.SmoothTransformation)
        pix.setDevicePixelRatio(dpr)
        label.setScaledContents(False)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setPixmap(pix)

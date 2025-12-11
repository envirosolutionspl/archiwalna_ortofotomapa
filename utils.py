from .constants import QT_VER   

def getQtVersion(version):
    if version in QT_VER:
        return QT_VER[version]
    return None
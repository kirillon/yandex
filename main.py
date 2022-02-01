import pygame, requests, sys, os

# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication


class MapParams(object):
    def __init__(self,lon,lat,zoom):
        self.lat = lon  # Координаты центра карты на старте. Задал координаты университета
        self.lon = lat
        self.zoom = zoom  # Масштаб карты на старте. Изменяется от 1 до 19
        self.type = "map"  # Другие значения "sat", "sat,skl"

    # Преобразование координат в параметр ll, требуется без пробелов, через запятую и без скобок
    def ll(self):
        return str(self.lon) + "," + str(self.lat)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./main.ui", self)
        self.mp = MapParams(61, 50,16)
        self.load_map()

    def load_map(self):

        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=self.mp.ll(), z=self.mp.zoom,
                                                                                        type=self.mp.type)
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запись полученного изображения в файл.

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        pixmap = QPixmap(map_file)
        self.label.setPixmap(pixmap)
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Left:
            self.mp.lon-=0.001
            self.load_map()

        if event.key() == Qt.Key_Right:
            self.mp.lon+=0.001
            self.load_map()
        if event.key() == Qt.Key_Up:
            self.mp.lat+=0.001
            self.load_map()
        if event.key() == Qt.Key_Down:
            self.mp.lat-=0.001
            self.load_map()
        if event.key() == Qt.Key_PageUp:
            if self.mp.zoom <= 20:
                self.mp.zoom += 1
                self.load_map()
        if event.key() == Qt.Key_PageDown:
            if self.mp.zoom >= 5:
                self.mp.zoom -= 1
                self.load_map()





def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    # создание таблиц

    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

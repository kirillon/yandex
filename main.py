import pygame, requests, sys, os

# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication


class MapParams(object):
    def __init__(self):
        self.lat = 61.665279  # Координаты центра карты на старте. Задал координаты университета
        self.lon = 50.813492
        self.zoom = 16  # Масштаб карты на старте. Изменяется от 1 до 19
        self.type = "map"  # Другие значения "sat", "sat,skl"

    # Преобразование координат в параметр ll, требуется без пробелов, через запятую и без скобок
    def ll(self):
        return str(self.lon) + "," + str(self.lat)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./main.ui", self)
        self.load_map()

    def load_map(self):
        mp = MapParams()
        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom,
                                                                                        type=mp.type)
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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    # создание таблиц

    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

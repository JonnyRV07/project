import sys

from PyQt5 import uic
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QHeaderView, QComboBox, QWidget, \
    QLabel
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap


class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('window.ui', self)

    #Чтение файла с информацией

    def get_info(self, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            return [i.split('; ') for i in f.read().split('\n')]


    def resize_img(self, f):
        img = Image.open(f)
        new_img = img.resize((241, 191))
        new_img.save(f)


    #Наполнение формы информацией

    def get_content(self, name):
        #Выбор списка для распаковки
        for i in self.get_info('main_inf_country.txt'):
            if name == i[0]:
                self.list_ = i
        #Заголовок и название виджета
        self.name_lbl.setText(self.list_[0])
        self.setWindowTitle(f'Easy Trip. {self.list_[0]}')
        #Основные характеристики
        y = 364
        lst = self.list_[::-1]
        for i in range(0, 9):
            self.res_lbl = QLabel('res_lbl{}'.format(i), self)
            self.res_lbl.setText(lst[i])
            if len(lst[i]) > 40 and len(lst[i]) < 100:
                self.res_lbl.setGeometry(300, y, len(lst[i]) * 5, 30)
            if len(lst[i]) >= 100:
                self.res_lbl.setGeometry(300, y, len(lst[i]) * 6, 30)
            else:
                self.res_lbl.setGeometry(300, y, len(lst[i]) * 7, 30)
            y -= 30
            self.res_lbl.setStyleSheet('font: 75 7pt "Perpetua"; background-color: rgb(255, 255, 255); border-radius: \
            5px; border: 1.5px solid #000000;')
        #Информация для отдыхающих
        for i in self.get_info('inf_country.txt'):
            if name == i[0]:
                self.list_ = i
        lst = self.list_[::-1]
        y2 = 543
        for i in range(0, 4):
            self.res_lbl1 = QLabel('res_lbl{}'.format(i), self)
            self.res_lbl1.setText(lst[i])
            if len(lst[i]) > 100:
                self.res_lbl1.setWordWrap(True)
                self.res_lbl1.setGeometry(295, y2, len(lst[i]) * 2.8, 30)
            else:
                self.res_lbl1.setGeometry(295, y2, len(lst[i]) * 6, 30)
            y2 -= 30
            self.res_lbl1.setStyleSheet('font: 75 7pt "Perpetua"; background-color: rgb(255, 255, 255); border-radius: \
            5px; border: 1.5px solid #000000;')
        #Подгрузка jpg
        self.background.setPixmap(QPixmap(f'jpg//{self.list_[0]}//фон.jpg'))
        self.resize_img(f'jpg//{self.list_[0]}//флаг.jpg')
        self.flag_lbl.setPixmap(QPixmap(f'jpg//{self.list_[0]}//флаг.jpg'))
        self.resize_img(f'jpg//{self.list_[0]}//герб.png')
        self.gerb_lbl.setPixmap(QPixmap(f'jpg//{self.list_[0]}//герб.png'))


class WorldMap(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('world_map.ui', self)

        self.setWindowTitle('Easy Trip')

        #Фильтр

        self.filter = QComboBox(self)
        self.filter.addItems(['Страны', 'Страны Мира', 'Страны СНГ', 'Страны ООН', 'Страны НАТО', 'Страны ЕС',
                              'Страны Шенгенского соглашения'])
        self.filter.setGeometry(1090, 60, 251, 21)
        self.filter.activated[str].connect(self.onActivated)

        #Кнопки на карте и создание таблицы для вывода данных

        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.mainBtn_australia)
        self.btn_group.addButton(self.mainBtn_brazil)
        self.btn_group.addButton(self.mainBtn_canada)
        self.btn_group.addButton(self.mainBtn_china)
        self.btn_group.addButton(self.mainBtn_germany)
        self.btn_group.addButton(self.mainBtn_india)
        self.btn_group.addButton(self.mainBtn_japan)
        self.btn_group.addButton(self.mainBtn_russia)
        self.btn_group.addButton(self.mainBtn_spain)
        self.btn_group.addButton(self.mainBtn_sweden)

        self.lst_countries = []
        self.lst_countries.append('Страны'), self.lst_countries.append(sorted([i.text() for i in
                                                                               self.btn_group.buttons()]))
        self.lst_val = ['Страны']

        self.create_result_field(self.lst_countries)

        #Подключение к кнопкам, открытие информационных окон по каждой стране

        self.mainBtn_australia.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_australia.text()))
        self.mainBtn_brazil.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_brazil.text()))
        self.mainBtn_canada.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_canada.text()))
        self.mainBtn_germany.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_germany.text()))
        self.mainBtn_spain.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_spain.text()))
        self.mainBtn_sweden.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_sweden.text()))
        self.mainBtn_russia.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_russia.text()))
        self.mainBtn_japan.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_japan.text()))
        self.mainBtn_china.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_china.text()))
        self.mainBtn_india.clicked.connect(lambda: self.open_infoWindow(self.mainBtn_india.text()))

        print(self.mainBtn_sweden.text())

    def open_infoWindow(self, btn_name):
        global iw
        iw = InfoWindow()
        iw.get_content(btn_name)
        iw.show()

    # Поисковая строка (детализация и её backend)

    def create_result_field(self, lst):
        countries = tuple(sorted(lst[1]))
        model = QStandardItemModel(len(countries), 1)
        model.setHorizontalHeaderLabels([lst[0]])

        for row, country in enumerate(countries):
            item = QStandardItem(country)
            model.setItem(row, 0, item)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterKeyColumn(0)

        self.search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)

        self.result_field.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_field.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_field.setModel(filter_proxy_model)

    # Работа фильтра

    def get_list_(self, p):
        with open('international_organizations.txt', 'r', encoding='UTF-8') as f:
            lst = [[i[:i.find(':')].strip(), i[i.find(':') + 1:].strip().split(', ')] for i in f.readlines()]
            for i in lst:
                if ''.join(p) == i[0]:
                    res = lst[lst.index(i)]
                    return res

    def onActivated(self, text):
        self.lst_val[0] = text
        print(self.lst_val)
        self.parameter_selection()

    def parameter_selection(self):
        if ''.join(self.lst_val) == 'Страны':
            self.create_result_field(self.lst_countries)
        else:
            self.create_result_field(self.get_list_(self.lst_val))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WorldMap()
    ex.show()
    sys.exit(app.exec_())
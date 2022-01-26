from PyQt5.QtWidgets import *
from PyQt5.QtGUI import *
import PyQt5.QtCore as qt
from random import randint
import sys
import os

class PyQtLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.__width = int(1300)
        self.__height = int(700)
        self.__ax = 0
        self.__ay = 0

        self.loc_label = []
        self.current_location = None

        self.locations = QLabel(self)
        self.current_loc_label = QLabel(self)
        self.results = QLabel(self)

        self.loc_select = QComboBox(self)
        
        self.add_loc = QPushButton("Add New Location")
        self.add_res = QPushButton("Add New Restaurant")
        self.update_loc = QPushButton("Select Location")
        self.quit_button = QPushButton("Quit")
        self.select_random_restaurant = QPushButton("Choose for me!")

        self.square = QPainter(self)
        
        self.UI()

    def UI(self):
        self.init_locations()

        self.locations.setText(self.build_location_label())
        self.current_loc_label.setText(self.selected_location_label())

        self.results.setText('')
        self.square.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        self.square.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        self.square.draw

        self.add_loc.resize(100,20)
        self.add_loc.clicked.connect(self.add_location)

        self.add_res.resize(100,20)
        self.add_res.clicked.connect(self.add_restaurant)

        self.update_loc.clicked.connect(self.set_selected_location)

        self.quit_button.clicked.connect(self.close)

        self.select_random_restaurant.clicked.connect(self.get_rand_res)

        self.set_total_layout()

        grid = QGridLayout()
        grid.addWidget(self.add_loc, 0, 6)
        grid.addWidget(self.add_res, 1, 6)
        grid.addWidget(self.locations, 2, 6)
        grid.addWidget(self.quit_button, 3, 6)

        grid.addWidget(self.loc_select, 1, 0)
        grid.addWidget(self.update_loc, 0, 0)
    
        grid.addWidget(self.select_random_restaurant, 1, 4)
        grid.addWidget(self.results, 2, 4)
        grid.addWidget(self.current_loc_label, 0, 4)
        
        self.setLayout(grid)
        self.setGeometry(self.__ax, self.__ay, self.__width, self.__height)
        self.setWindowTitle("Kaia's Restaurant Picker")

    def set_total_layout(self):
        #Color Pallet
        #light purple = 9a82b0
        #dark purple = 4f2262
        #grey = 3f3b3b
        #light blue = d4eced
        self.setStyleSheet("background-color: #9a82b0;"
                            "font-weight: bold;"
                            "color: #4f2262;"
                            )

        self.add_loc.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )
        self.add_res.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )
        self.update_loc.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )
        self.quit_button.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )        
        self.select_random_restaurant.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )        
        self.loc_select.setStyleSheet("color: #4f2262;"
                                   "background: #92d8e3;"
                                   )
  
    def add_location(self):
        text , pressed = QInputDialog.getText(self, "Add New Location", "Location Name: ", QLineEdit.Normal, "")

        if pressed:
            # TODO: verify that location doesnt exist already
            if text != '':
                new_loc = open(f"restaurants\\{text}.csv", "w")
                new_loc.close()
                self.update_current_locations(text)
                self.locations.setText(self.build_location_label())
                self.locations.adjustSize()
            else:
                msg_empty_loc = QMessageBox(self)
                msg_empty_loc.setWindowTitle("ERROR")
                msg_empty_loc.setText("Enter a location name")
                msg_empty_loc.setIcon(QMessageBox.Warning)
                empty_loc_ret = msg_empty_loc.exec_()

    # TODO: Make path better
    def init_locations(self):
        init = False
        for file in os.listdir("restaurants"):
            if file[-4:] == ".csv":
                    self.update_current_locations(file[:-4])
            if init == False:
                self.current_location = file[:-4]
                init = True

    def update_current_locations(self, new_loc): 
        if len(new_loc) != 0:
            self.loc_select.addItem(new_loc)
            self.loc_label.append(new_loc)

    def set_selected_location(self):
        self.current_location = self.loc_select.currentText()
        self.locations.setText(self.build_location_label())
        self.locations.adjustSize()

    def build_location_label(self):
        return "\n\nLocations:\n\n" + '\n'.join(self.loc_label)

    def selected_location_label(self):
        return "Selected Location: " + self.current_location 

    def add_restaurant(self):
        data = []
        display_text = [ "Restaurant Name:", "Restaurant Genre", "Price 0($) to 10($$)", "Short Description" ]

        for index in range(4):
            text, pressed = QInputDialog.getText(self, "Add New Restaurant", display_text[index], QLineEdit.Normal, "")

            if pressed:
                if text == '':
                    data.append(None)
                else:
                    data.append(text)

        new_res = open(f"restaurants\\{self.current_location}.csv", "a")
        new_res.write(','.join(data) + '\n')
        new_res.close()

    def get_rand_res(self):
        available_restaurants = []
        random_choices = []
    
        current_file = open(f"restaurants\\{self.current_location}.csv", "r")
        for line in current_file:
            available_restaurants.append(line.split(','))
        current_file.close()
        for _ in range(5):
            random_num = randint(0, len(available_restaurants)-1)
            random_choices.append(available_restaurants[random_num])
            available_restaurants.pop(random_num)
        self.build_results(random_choices)
        
    def build_results(self, choices):
        results_label = f"Here\'s 5 random restaurants in {self.current_location}\nName:\tGenre\tPrice 0($) to 10($$)\tDescription\n\n"
        for index in range(5):
            results_label += '\t'.join(choices[index]) + '\n'
        self.results.setText(results_label)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = PyQtLayout()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

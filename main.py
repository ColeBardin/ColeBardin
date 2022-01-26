from PyQt5.QtWidgets import *
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

        self.location_text = []
        self.restaurant_text = ''
        self.current_location = None

        self.label_locations = QLabel(self)
        self.label_current_location = QLabel(self)
        self.label_results = QLabel(self)

        self.list_current_restaurants = QListWidget(self)

        self.combo_location_select = QComboBox(self)
        
        self.button_add_location = QPushButton("Add New Location")
        self.button_add_restaurant = QPushButton("Add New Restaurant")
        self.button_update_location = QPushButton("Select Location")
        self.button_quit = QPushButton("Quit")
        self.button_random_restaurants = QPushButton("Choose for me!")

        self.UI()

    def UI(self):
        self.init_locations()
        self.update_restaurants()

        self.list_current_restaurants.setMaximumWidth(int(self.__width/3))

        self.label_locations.setText(self.build_location_label())
        self.label_current_location.setText(self.selected_location_label())
        self.label_results.setText('')

        self.button_add_location.clicked.connect(self.add_location)
        self.button_add_restaurant.clicked.connect(self.add_restaurant)
        self.button_update_location.clicked.connect(self.set_selected_location)
        self.button_quit.clicked.connect(self.close)
        self.button_random_restaurants.clicked.connect(self.get_rand_res)

        self.set_total_layout()

        grid = QGridLayout()
        grid.addWidget(self.button_add_location, 0, 6)
        grid.addWidget(self.button_add_restaurant, 1, 6)
        grid.addWidget(self.label_locations, 2, 6)
        grid.addWidget(self.button_quit, 3, 6)

        grid.addWidget(self.combo_location_select, 1, 0)
        grid.addWidget(self.button_update_location, 0, 0)
        grid.addWidget(self.list_current_restaurants, 2, 0)
    
        grid.addWidget(self.button_random_restaurants, 1, 4)
        grid.addWidget(self.label_results, 2, 4)
        grid.addWidget(self.label_current_location, 0, 4)
        
        self.setLayout(grid)
        self.setGeometry(self.__ax, self.__ay, self.__width, self.__height)
        self.setWindowTitle("Kaia's Restaurant Picker")

    def set_total_layout(self):
        #Color Pallet
        #light purple = 9a82b0
        #dark purple = 4f2262
        #grey = 3f3b3b
        #dark_grey = #6a6383
        #light blue = 92d8e3
        #off_black = #553b5e
        self.setStyleSheet("background-color: #9a82b0;"
                            "font-weight: bold;"
                            "color: #4f2262;"
                            )

        self.button_add_location.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )
        self.button_add_restaurant.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )
        self.button_update_location.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )
        self.button_quit.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )        
        self.button_random_restaurants.setStyleSheet("color: #4f2262;"
                                   "background-color: #92d8e3;"
                                   )        
        self.combo_location_select.setStyleSheet("color: #4f2262;"
                                   "background: #92d8e3;"
                                   )
        self.label_locations.setStyleSheet("background-color: #6a6383;"
                                     "border: 5px solid #553b5e;"
                                     "color: #c2e9f0;"
                                     )
        self.label_results.setStyleSheet("background-color: #6a6383;"
                                     "border: 5px solid #553b5e;"
                                     "color: #c2e9f0;"
                                     )
        self.label_current_location.setStyleSheet("background-color: #6a6383;"
                                     "border: 5px solid #553b5e;"
                                     "color: #c2e9f0;"
                                     )

    def add_location(self):
        text , pressed = QInputDialog.getText(self, "Add New Location", "Location Name: ", QLineEdit.Normal, "")

        if pressed:
            # TODO: verify that location doesnt exist already
            if text != '':
                new_loc = open(f"restaurants\\{text}.csv", "w")
                new_loc.close()
                self.update_current_locations(text)
                self.label_locations.setText(self.build_location_label())
                self.label_locations.adjustSize()
            else:
                msg_empty_loc = QMessageBox(self)
                msg_empty_loc.setWindowTitle("ERROR")
                msg_empty_loc.setText("Enter a location name")
                msg_empty_loc.setIcon(QMessageBox.Warning)
                empty_loc_ret = msg_empty_loc.exec_()

    def update_restaurants(self):
        self.list_current_restaurants.addItem(QListWidgetItem("Full Restaurant List:\n"))
        file = open(f"restaurants\\{self.current_location}.csv", "r")
        for line in file:
            self.list_current_restaurants.addItem(QListWidgetItem(f"{line.split(',')[0]}"))
        file.close()


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
            self.combo_location_select.addItem(new_loc)
            self.location_text.append(new_loc)

    def set_selected_location(self):
        self.current_location = self.combo_location_select.currentText()
        self.label_locations.setText(self.build_location_label())
        self.label_locations.adjustSize()

    def build_location_label(self):
        return "\n\nLocations:\n\n" + '\n'.join(self.location_text)

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
        update_restaurants()

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
        self.label_results.setText(results_label)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = PyQtLayout()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

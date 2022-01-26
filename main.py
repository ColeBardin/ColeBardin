from PyQt5.QtWidgets import *
from random import randint
import sys
import os

# Layout class
class PyQtLayout(QWidget):
    # Class initialization method
    def __init__(self):
        super().__init__()

        # Set main window size and location
        self.__width = int(1500)
        self.__height = int(800)
        self.__ax = 0
        self.__ay = 0

        # Variable to store current location
        self.current_location = None

        # Initialize all Widgets ons creen
        self.label_current_location = QLabel(self)
        self.table_results = QTableWidget(self)
        self.list_current_restaurants = QListWidget(self)
        self.list_locations = QListWidget(self)
        self.combo_location_select = QComboBox(self)
        self.button_add_location = QPushButton("Add New Location")
        self.button_add_restaurant = QPushButton("Add New Restaurant")
        self.button_update_location = QPushButton("Select Location")
        self.button_quit = QPushButton("Quit")
        self.button_random_restaurants = QPushButton("Choose for me!")

        # Run UI Method
        self.init_gui()
    
    # Generate UI layout specifications
    def init_gui(self):
        # Build all text packets
        self.init_locations_table()
        self.update_restaurants()
        self.init_results_table()
        self.build_locations()

        # Set max width for list objects
        self.list_current_restaurants.setMaximumWidth(int(self.__width/3))
        self.list_locations.setMaximumWidth(int(self.__width/3))

        # Display text on current locations list
        self.label_current_location.setText(self.get_selected_location_label())

        # Connect all the buttons to their action methods
        self.button_add_location.clicked.connect(self.add_location)
        self.button_add_restaurant.clicked.connect(self.add_restaurant)
        self.button_update_location.clicked.connect(self.update_selected_location)
        self.button_quit.clicked.connect(self.close)
        self.button_random_restaurants.clicked.connect(self.generate_random_restaurant)
        
        # Adjust CSS for this project
        self.set_css()

        # Create grid layout of Widget objects
        grid = QGridLayout()
        #Add Widgets to the grid:
        # Left Column
        grid.addWidget(self.combo_location_select, 1, 0)
        grid.addWidget(self.button_update_location, 0, 0)
        grid.addWidget(self.list_current_restaurants, 2, 0)  
        # Middle Column
        grid.addWidget(self.button_random_restaurants, 1, 1)
        grid.addWidget(self.table_results, 2, 1)
        grid.addWidget(self.label_current_location, 0, 1)
        # Right Column
        grid.addWidget(self.button_add_location, 0, 2)
        grid.addWidget(self.button_add_restaurant, 1, 2)
        grid.addWidget(self.list_locations, 2, 2)
        grid.addWidget(self.button_quit, 3, 2)

        # Apply grid layout
        self.setLayout(grid)
        # Format window
        self.setGeometry(self.__ax, self.__ay, self.__width, self.__height)
        self.setWindowTitle("Kaia's Restaurant Picker")

    # Initialize the locations for the table
    def init_locations_table(self):
        # Bool used to set first file as current location on startup
        init = False
        # Iterate over all files in restaurants directory
        for file in os.listdir("restaurants"):
            # Only cound .CSV files for locations
            if file[-4:] == ".csv":
                    # Add new location to table
                    self.update_available_locations(file[:-4])
            # Set current location as first file
            if init == False:
                self.current_location = file[:-4]
                # Do not run again
                init = True

    # Initialize results table on startup
    def init_results_table(self):
        # Set table size and formatting
        self.table_results.setRowCount(5)
        self.table_results.setColumnCount(4)
        self.table_results.setHorizontalHeaderLabels(["Name","Genre","Price","Description"])
        # Fill table with blank values until get_random_restaurant() is called
        for row in range(5):
            for col in range(4):
                # For each row and column, fill with blank item
                self.table_results.setItem(row, col, QTableWidgetItem(''))

    # Adjusts the CSS elements
    def set_css(self):
        #Color Pallet:
        #light purple = 9a82b0
        #dark purple = 4f2262
        #grey = 3f3b3b
        #dark_grey = #6a6383
        #light blue = 92d8e3
        #off_black = #553b5e

        # Adjust CSS of Main Window
        self.setStyleSheet("background-color: #9a82b0;"
                            "font-weight: bold;"
                            "color: #4f2262;"
                            )
        # Add Location Button
        self.button_add_location.setStyleSheet("color: #4f2262;"
                                               "background-color: #92d8e3;"
                                               )
        # Add Restaurant Button
        self.button_add_restaurant.setStyleSheet("color: #4f2262;"
                                                 "background-color: #92d8e3;"
                                                 )
        # Update Location Button
        self.button_update_location.setStyleSheet("color: #4f2262;"
                                                  "background-color: #92d8e3;"
                                                  )
        # Quit Button
        self.button_quit.setStyleSheet("color: #4f2262;"
                                       "background-color: #92d8e3;"
                                       )       
        # Get Random Restaurant Button
        self.button_random_restaurants.setStyleSheet("color: #4f2262;"
                                                     "background-color: #92d8e3;"
                                                     )      
        # Location Select Dropdown
        self.combo_location_select.setStyleSheet("color: #4f2262;"
                                                 "background: #92d8e3;"
                                                 )
        # Locations List
        self.list_locations.setStyleSheet("background-color: #6a6383;"
                                          "border: 5px solid #553b5e;"
                                          "color: #c2e9f0;"
                                          )
        # Current Restaurants List
        self.list_current_restaurants.setStyleSheet("background-color: #6a6383;"
                                                    "border: 5px solid #553b5e;"
                                                    "color: #c2e9f0;"
                                                    )

        # Results Table
        self.table_results.setStyleSheet("background-color: #6a6383;"
                                         "border: 5px solid #553b5e;"
                                         "color: #c2e9f0;"
                                         )
        # Current Locations Label
        self.label_current_location.setStyleSheet("background-color: #6a6383;"
                                                  "border: 5px solid #553b5e;"
                                                  "color: #c2e9f0;"
                                                  )

    # Action method for button_add_location
    def add_location(self):
        new_location = self.get_user_input("Add New Location", "Enter a new location name:")
        # If blank entry is submitted
        if new_location == '':
            # Display error message for empty input
            self.generate_display_msg("Warning", "Enter a valid location name", QMessageBox.Warning)
            # Recurse
            self.add_location()
        # If cancel button is pressed, NoneType is passed
        elif type(new_location) == type(None):
            self.generate_display_msg("Warning", "New location entry cancelled", QMessageBox.Information)
        # Else result is valid
        else:
            # Check to see if file exists before writing a new one
            if os.path.isfile(f"restaurants\\{new_location}.csv"):\
                # Display error message
                self.generate_display_msg("Warning", "A file for this location already exists", QMessageBox.Warning)
                # Recurse
                self.add_location()
            else:
                # Create a .CSV file with the input as the name
                new_file = open(f"restaurants\\{new_location}.csv", "w")
                new_file.close()
                # Update the current available locations table
                self.update_available_locations(new_location)
                self.generate_display_msg("Succes", f"Successfully created new location: {new_location}", QMessageBox.Information)

   # Action method to add a new restaurant to current location
    def add_restaurant(self):
        # Make empty list to hold input values
        data = ['','','','']
        # List of prompts for line edits
        messages = [ "Restaurant Name:", "Restaurant Genre", "Price 0($) to 10($$)", "Short Description" ]
        # Use iterator to determine data type
        iterator = 0
        # Repeat until all data is collected
        while iterator < 4:
            # Prompt user for input
            input_data = self.get_user_input("Add restaurant to f{self.current_location}", messages[iterator])
            # If blank entry is submitted
            if input_data == '':
                # Only error if blank name is submitted
                if iterator == 0:
                    # Display error message
                    self.generate_display_msg("Error", "Restaurants must at least have a name", QMessageBox.Critical)
                # If empty input is given for other fields
                else:
                    # Leave data entry blank and move on
                    iterator += 1
            # If cancel button is pressed at any time
            elif type(input_data) == type(None):
                # Generate error message
                self.generate_display_msg("Warning", "Restaurant entry cancelled", QMessageBox.Information)
                # End process
                iterator = 10
                break;
            # If a filled submission is given
            else:
                data[iterator] = temp_data
                iterator += 1
        if iterator == 4:                    
            # Add new restaurant packet to current location file
            new_res = open(f"restaurants\\{self.current_location}.csv", "a")
            # Join data with a newline and write
            new_res.write(','.join(data) + '\n')
            # Close current location file
            new_res.close()
            # Update available restaurants list
            self.update_restaurants()

    # Method to call when the list of resaurants or current location is changed
    def update_restaurants(self):
        # Clear all elements from the list
        self.list_current_restaurants.clear()
        # Add first title element
        self.list_current_restaurants.addItem(QListWidgetItem(f"All Restaurants in {self.current_location}:\n"))
        # Get available restaurants from current location file
        file = open(f"restaurants\\{self.current_location}.csv", "r")
        # Iterate over each restaurant packet
        for line in file:
            # Parse out the name of the restaurant from the packet
            self.list_current_restaurants.addItem(QListWidgetItem(f"{line.split(',')[0]}"))
        # Close the current location file
        file.close()
    
    # Method to update the location table with a new location
    def update_available_locations(self, new_loc): 
        # TODO: Input error handle
        # Make sure new location is valid
        if len(new_loc) != 0:
            # Add the item to the drop down menu
            self.combo_location_select.addItem(new_loc)
            # Build the available locations table
            self.build_locations()

    # Action method to set the selected location from the drop down as the current location
    def update_selected_location(self):
        # Setting current location
        self.current_location = self.combo_location_select.currentText()
        # Update current location label
        self.label_current_location.setText(self.get_selected_location_label())
        # Update the list of available restaurants from this new location
        self.update_restaurants()

    # Method to build the location table
    def build_locations(self):
        # First, clear the table
        self.list_locations.clear()
        # Add first title element
        self.list_locations.addItem(QListWidgetItem("Full Location List:\n"))
        # Iterate for all the files in \restaurants subdirectory
        for file in os.listdir('restaurants'):
            # Add filename to list of available locations
            self.list_locations.addItem(QListWidgetItem(file[:-4]))

    # Method to build results table with given choices
    def build_results(self, choices):
        # Clear the table from previous choices
        self.table_results.clear()
        # Reset horizontal header labels
        self.table_results.setHorizontalHeaderLabels(["Name","Genre","Price","Description"])
        # Iterate for each row index
        for row in range(5):
            # Iterate for each column index
            for col in range(4):
                # Parese choices based on current row and column and add them as items to results table
                self.table_results.setItem(row, col, QTableWidgetItem(choices[row][col]))

    # Method to generate new location label with current location
    def get_selected_location_label(self):
        # Returns complete string
        return "Selected Location: " + self.current_location 

    # Action method to display random restaurants
    def generate_random_restaurant(self):
        # List to hold all available restaurants
        available_restaurants = []
        # List to hold chose restaurants
        random_choices = []
    
        # Read from current location file
        current_file = open(f"restaurants\\{self.current_location}.csv", "r")
        # Iterate over each line in .CSV
        for line in current_file:
            # Add restaurants to list to choose from
            available_restaurants.append(line.split(','))
        # Close the current location file
        current_file.close()
        # Repeat 5 times
        for _ in range(5):
            # Choose random number
            random_num = randint(0, len(available_restaurants)-1)
            # Use random number as index to select restaurant and add to list of choices
            random_choices.append(available_restaurants[random_num])
            # Stop current restaurant from beign displayed twice
            available_restaurants.pop(random_num)
        # Build results table with random choices
        self.build_results(random_choices)  

    # Method to prompt user for a text input
    def get_user_input(self, title, msg):
        # Generate input text box for user
        text , pressed =  text , pressed = QInputDialog.getText(self, title, msg, QLineEdit.Normal, "")
        
        # Check for submission
        if pressed:
            # Return user input
            return text

    # Method to make error messages pop up
    def generate_display_msg(self, title, msg, err_type):
        # Generate message box object
        error_msg = QMessageBox(self)
        # Set the window title
        error_msg.setWindowTitle(title)
        # Set the message box text to be msg parameter
        error_msg.setText(msg)
        #QMessageBox.Warning, Question, Information, Critical
        # Set error type from parameter
        error_msg.setIcon(err_type)
        # Execute error message and save return value
        err_msg_ret_val = error_msg.exec_()


# Main body function
def main():
    # Crate PyQt Application
    app = QApplication(sys.argv)
    # Set style to be 'fusion'
    app.setStyle("fusion")
    # Create main window of PyQtLayout class
    window = PyQtLayout()
    # Display window
    window.show()
    # Close window when python program is closed
    sys.exit(app.exec_())

if __name__ == "__main__":
    # TODO: Make directory paths OS friendly
    # Call upon main function
    main()

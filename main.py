from PyQt5.QtWidgets import *
from PyQt5 import QtCore
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

        # Variable to store current selected items
        self.current_location = None
        self.current_restaurant = None

        # Buffer to hold current restaurant information
        self.info_current_restaurants = None

        # Welcome informating string
        line1 = "<h2>Welcome to Kaia's Restaurant Picker</h2><hr>"
        line2 = "<h3><font color=#553b5e>~ </font color=#553b5e>Hit <i><font color=#66CADA>Choose for me!</font color=#66CADA></i> to display 5 random <i><font color=#4f2262>restaurants</font color=#4f2262></i> from the <i><font color=#3f3857>current location</font color=#3f3857></i><br>"
        line3 = "<font color=#553b5e>~ </font color=#553b5e>Click on a <i><font color=#3f3857>location</font color=#3f3857></i> to select and display its <i><font color=#4f2262>restaurants</font color=#4f2262></i><br>"
        line4 = "<font color=#553b5e>~ </font color=#553b5e>Use the <i><font color=#66CADA>Add Restaurant</font color=#66CADA></i> button to add a <i><font color=#4f2262>restaurant</font color=#4f2262></i> to the <i><font color=#3f3857>current location</font color=#3f3857></i><br>"
        line5 = "<font color=#553b5e>~ </font color=#553b5e>Use <i><font color=#66CADA>Add Location</font color=#66CADA></i> button to make a new <i><font color=#3f3857>location</font color=#3f3857></i> file<br>"
        line6 = "<font color=#553b5e>~ </font color=#553b5e>To edit an existing restaurant, select it and hit <i><font color=#66CADA>Edit Restaurant</font color=#66CADA></i></h3><br>"
        line7 = "<h2>Enjoy!</h2>"
        # Format string
        self.welcome_str = line1+line2+line3+line4+line5+line6+line7

        # Initialize QLabels
        self.label_current_location = QLabel(self)
        self.label_welcome_info = QLabel(self)
        self.label_welcome_info.setTextFormat(1)
        self.label_restaurants = QLabel(self)
        self.label_locations = QLabel("Your Locations:")

        # Initialize QTable
        self.table_results = QTableWidget(self)

        # Initialize QLists
        self.list_current_restaurants = QListWidget(self)
        self.list_locations = QListWidget(self)

        # Initialize QPushButtons
        self.button_add_location = QPushButton("Add New Location")
        self.button_add_restaurant = QPushButton("Add New Restaurant")
        self.button_quit = QPushButton("Quit")
        self.button_random_restaurants = QPushButton("Choose for me!")
        self.button_edit_restaurant = QPushButton("Edit Restaurant")

        # Run UI Method
        self.init_gui()
    
    # Generate UI layout specifications
    def init_gui(self):
        # Build all text packets
        self.init_locations_table()
        self.build_restaurants()
        self.init_results_table()

        # Set max width for list objects
        self.list_current_restaurants.setMaximumWidth(int(self.__width/4))
        self.list_locations.setMaximumWidth(int(self.__width/4))

        # Display on label objects
        self.label_current_location.setText(self.get_selected_location_label())
        self.label_welcome_info.setText(self.welcome_str)

        # Connect all the buttons to their action methods
        self.button_add_location.clicked.connect(self.add_location)
        self.button_add_restaurant.clicked.connect(self.add_restaurant)
        self.button_quit.clicked.connect(self.close)
        self.button_random_restaurants.clicked.connect(self.generate_random_restaurant)
        self.button_edit_restaurant.clicked.connect(self.edit_restaurant)

        # Connect list objects to their action methods
        self.list_current_restaurants.itemClicked.connect(self.set_current_restaurant)
        self.list_locations.itemClicked.connect(self.set_current_location)

        # Connect the table items to generate info QDialog boxes
        self.table_results.itemClicked.connect(self.generate_restaurant_info)
        
        # Adjust CSS for this project
        self.set_css()

        # Create grid layout of Widget objects
        grid = QGridLayout()
        #Add Widgets to the grid:
        # Left Column
        grid.addWidget(self.button_add_restaurant, 0, 0)
        grid.addWidget(self.label_restaurants, 1, 0)
        grid.addWidget(self.list_current_restaurants, 2, 0) 
        grid.addWidget(self.button_edit_restaurant, 3, 0)
        # Middle Column
        grid.addWidget(self.button_random_restaurants, 1, 1)
        grid.addWidget(self.label_welcome_info, 2, 1)
        grid.addWidget(self.table_results, 2, 1)
        grid.addWidget(self.label_current_location, 0, 1)
        # Right Column
        grid.addWidget(self.button_add_location, 0, 2)
        grid.addWidget(self.label_locations, 1, 2)
        grid.addWidget(self.list_locations, 2, 2)
        grid.addWidget(self.button_quit, 3, 2)

        # Apply grid layout
        self.setLayout(grid)
        # Format window size
        self.setGeometry(self.__ax, self.__ay, self.__width, self.__height)
        # Add window title to the app
        self.setWindowTitle("Kaia's Restaurant Picker")

    # Initialize the locations for the table
    def init_locations_table(self):
        # Bool used to set first file as current location on startup
        init = False
        # Test to see if there are location files in directory
        if len(os.listdir("restaurants")) == 0:
            # Set current location string to be empty
            self.current_location = ''
        # If files do exist in directory
        else:
        # Iterate over all files in restaurants directory
            for file in os.listdir("restaurants"):
                # Only cound .CSV files for locations
                if file[-4:] == ".csv" and len(file) != 0:
                    # Set the first file to the current location
                    self.current_location = file[:-4]
                    # Stop loop
                    break
            # Build the available locations table
            self.build_locations()

    # Initialize results table on startup
    def init_results_table(self):
        # Set table size and formatting
        self.table_results.setRowCount(5)
        self.table_results.setColumnCount(1)
        # Set horizontal header of table
        self.table_results.setHorizontalHeaderLabels([f"Five Random Restaurants in {self.current_location}"])
        # Fill table with blank values until get_random_restaurant() is called
        for row in range(5):
            # For each row and column, fill with blank item
            self.table_results.setItem(row, 0, QTableWidgetItem(''))
        # Hide the results table until it is needed
        self.table_results.hide()

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
                # Close the file
                new_file.close()
                # Rebuild the locations table 
                self.build_locations()
                # Display success message
                self.generate_display_msg("Succes", f"Successfully created new location: {new_location}", QMessageBox.Information)

    # Action method to add a new restaurant to current location
    def add_restaurant(self):
        # Call method to get restaurant info from user with new_restaurant paramater True
        new_restaurant_data, iterator = self.get_restaurant_info(True)
        # Once full data collection has occured
        if iterator == 4:                    
            # Add new restaurant packet to current location file
            new_res = open(os.path.join("restaurants",f"{self.current_location}.csv"), "a")
            # Join data with a newline and write
            new_res.write(','.join(new_restaurant_data) + '\n')
            # Close current location file
            new_res.close()
            # Update available restaurants list
            self.build_restaurants()
            # Display success message once completed
            self.generate_display_msg("Success",f"Successfully added new restaurant to {self.current_location}", QMessageBox.Information)

    # Method to build the location table
    def build_locations(self):
        # First, clear the table
        self.list_locations.clear()
        # Iterate for all the files in \restaurants subdirectory
        for file in os.listdir('restaurants'):
            # Only add locations of .CSV file
            if file[-4:].lower() == ".csv":
                # Add filename to list of available locations
                self.list_locations.addItem(QListWidgetItem(file[:-4]))

    # Method to call when the list of resaurants or current location is changed
    def build_restaurants(self):
        # Clear all elements from the list
        self.list_current_restaurants.clear()
        # Clear buffer of current restaurant info
        self.info_current_restaurants = []
        # Adjust label with with current location
        self.label_restaurants.setText(f"Your Restaurants in {self.current_location}:")
        # Get available restaurants from current location file
        file = open(os.path.join("restaurants",f"{self.current_location}.csv"), "r")
        # Iterate over each restaurant packet
        for line in file:
            # Parse out the name of the restaurant from the packet
            self.list_current_restaurants.addItem(QListWidgetItem(f"{line.split(',')[0]}"))
            # Add current restaurant information to info buffer
            self.info_current_restaurants.append(line.split(','))
        # Close the current location file
        file.close()
        # Set current restaurant to None since list is deselected
        self.current_restaurant = None

    # Method to build results table with given choices
    def build_results(self, choices):
        # Hide the welcome info message
        self.label_welcome_info.hide()
        # Clear the table from previous choices
        self.table_results.clear()
        # Reset horizontal header labels
        self.table_results.setHorizontalHeaderLabels([f"Five Random Restaurants in {self.current_location}"])
        # Iterate for each row index
        for row in range(5):
            # Create variable to hold instance of QTableWidgetItem so the flags can be adjusted
            current_item = QTableWidgetItem(choices[row][0])
            # Make cell static and not editable by the user
            current_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            # Parese choices based on current row and column and add them as items to results table
            self.table_results.setItem(row, 0, current_item)
            # Resize column height
            self.table_results.setRowHeight(row, int(self.__height/8))
        # Resize the table by stretching to fit
        self.table_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Display the table on the screen
        self.table_results.show()

    # Method to generate new location label with current location
    def get_selected_location_label(self):
        # Returns complete string
        return "Selected Location: " + self.current_location 

    # Method to prompt user for a text input
    def get_user_input(self, title, msg):
        # Create InputDialog object
        dialog = QInputDialog(self)
        # Resize the window
        dialog.resize(QtCore.QSize(500, 100))
        # Set window title to passed parameter
        dialog.setWindowTitle(title)
        # Set dialog message to passed parameter
        dialog.setLabelText(msg)
        # Set Echo mode to normal
        dialog.setTextEchoMode(QLineEdit.Normal)
        # Wait for response
        if dialog.exec_() == QDialog.Accepted:
            # Return submitted value
            return dialog.textValue()

    # Method to get and return new restaurant info packet and iterator from user
    def get_restaurant_info(self, new_restaurant):
        # Make empty list to hold input values
        new_restaurant_data = ['','','','']
        # List of prompts for line edits
        messages = [ "Restaurant Name:", "Restaurant Genre", "Price 0($) to 10($$)", "Short Description" ]
        # Title for prompts selection determined by new_restaurant parameter
        if new_restaurant == True:
            # New restaurant title
            title = f"Add Restaurant to {self.current_location}"
        else:
            # Editing restaurant title
            title = f"Edit {self.current_restaurant} in {self.current_location}"
        # Use iterator to determine data type
        iterator = 0
        # Repeat until all data is collected
        while iterator < 4:
            # Prompt user for input
            input_data = self.get_user_input(title, messages[iterator])
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
                # Set most recent input
                new_restaurant_data[iterator] = input_data
                # Increment after successful data acquisition
                iterator += 1
        # Return the given data and the end status of the iterator
        return new_restaurant_data, iterator

    # Action method to display random restaurants
    def generate_random_restaurant(self):
        # List to hold all available restaurants
        available_restaurants = []
        # List to hold chose restaurants
        random_choices = []
    
        # Read from current location file
        current_file = open(os.path.join("restaurants",f"{self.current_location}.csv"), "r")
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

    # Method to make error messages pop up
    def generate_display_msg(self, title, msg, err_type):
        # Generate message box object
        disp_msg = QMessageBox(self)
        # Set the window title
        disp_msg.setWindowTitle(title)
        # Set the message box text to be msg parameter
        disp_msg.setText(msg)
        #QMessageBox.Warning, Question, Information, Critical
        # Set error type from parameter
        disp_msg.setIcon(err_type)
        # Execute error message and save return value
        disp_msg_ret_val = disp_msg.exec_()

    # Method to display a restaurant's information
    def generate_restaurant_info(self, restaurant):
        # Variable to hold incoming full information
        restaurant_info = None
        # Iterate over known restaurant data in buffer
        for i_restaurant in self.info_current_restaurants:
            # Match restaurant name from QTable to restaurant data in the buffer
            if i_restaurant[0] == restaurant.text():
                # Retain the current restaurant information
                restaurant_info = i_restaurant
                # No need to execute more iterations
                break
        # Initialize QDialog box winodw
        info_window = QMessageBox(self)
        # Set the title to be the restaurant and location
        info_window.setWindowTitle(f"{restaurant_info[0]}")
        # Display the restaurant's information
        info_window.setText(
            f"<h2>{restaurant_info[0]},<br>{self.current_location}</h2><h3><font color=#66CADA>Genre:</font color=#66CADA></h3><h4><font color=#9a82b0>{restaurant_info[1]}</font color=#9a82b0></h4><h3><font color=#66CADA>Price 0($) to 10($$):</font color=#66CADA></h3><h4><font color=#9a82b0>{restaurant_info[2]}</font color=#9a82b0></h4><h3><font color=#66CADA>Description:</font color=#66CADA></h4><h3><font color=#9a82b0>{restaurant_info[3]}</font color=#9a82b0></h3>")
        # Set text format to rich text
        info_window.setTextFormat(1)
        # Change the styling of the window
        info_window.setStyleSheet("color: #c2e9f0;"
                                  "padding: 10px;"
                                  "background-color: #3f3857;"
                                  )
        # Execute the window build operation
        result = info_window.exec()
        # Reset current restaurant to be None
        self.current_restaurant = None

    # Method to update current restaurant
    def set_current_restaurant(self, item):
        # Update current_restaurant variable with selected item
        self.current_restaurant = item.text()

    # Action method to set the selected location from the drop down as the current location
    def set_current_location(self, item):
        # Setting current location
        self.current_location = item.text()
        # Update current location label
        self.label_current_location.setText(self.get_selected_location_label())
        # Update the list of available restaurants from this new location
        self.build_restaurants()

    # Adjusts the CSS elements
    def set_css(self):
        #Color Pallet:
        # Window baground: light purple =   9a82b0
        # Button font: dark purple =        4f2262
        # Table and CL BG: dark_grey =      6a6383
        # Button Background: light blue =   92d8e3
        # Object border: off_black =        553b5e
        # List BG: super dark grey =        3f3857
        # Button indicator: blue =          66CADA

        # Adjust CSS of Main Window
        self.setStyleSheet("background-color: #9a82b0;"
                            "font: 20px bold;"
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
        # Quit Button
        self.button_quit.setStyleSheet("color: #4f2262;"
                                       "background-color: #92d8e3;"
                                       )       
        # Get Random Restaurant Button
        self.button_random_restaurants.setStyleSheet("color: #4f2262;"
                                                     "background-color: #92d8e3;"
                                                     "padding-top: 10px;"
                                                     "padding-bottom: 10px;"
                                                     )  
        # Edit restaurant button
        self.button_edit_restaurant.setStyleSheet("color: #4f2262;"
                                                  "background-color: #92d8e3;"
                                                  )  
        # Locations List
        self.list_locations.setStyleSheet("background-color: #3f3857;"
                                          "border: 5px solid #553b5e;"
                                          "color: #c2e9f0;"
                                          "padding: 10px;"
                                          )
        # Current Restaurants List
        self.list_current_restaurants.setStyleSheet("background-color: #3f3857;"
                                                    "border: 5px solid #553b5e;"
                                                    "color: #c2e9f0;"
                                                    "padding: 10px;"
                                                    )
        # Results Table
        self.table_results.setStyleSheet("background-color: #6a6383;"
                                         "border: 5px solid #553b5e;"
                                         "color: #c2e9f0;"
                                         "font: 30px bold;"
                                         )
        # Current Locations Label
        self.label_current_location.setStyleSheet("background-color: #6a6383;"
                                                  "border: 5px solid #553b5e;"
                                                  "color: #c2e9f0;"
                                                  "padding: 5px;"
                                                  )
        # Welcome info label
        self.label_welcome_info.setStyleSheet("background-color: #6a6383;"
                                              "border: 5px solid #553b5e;"
                                              "color: #c2e9f0;"
                                              "padding: 5px;"
                                              "alignment: center;"
                                              "font: 20px bold;"
                                              )
        # Welcome info label
        self.label_restaurants.setStyleSheet("background-color: #3f3857;"
                                             "border: 5px solid #553b5e;"
                                             "color: #c2e9f0;"
                                             "padding: 5px;"
                                             )
        # Welcome info label
        self.label_locations.setStyleSheet("background-color: #3f3857;"
                                           "border: 5px solid #553b5e;"
                                           "color: #c2e9f0;"
                                           )

    # Method to edit the current restaurant
    def edit_restaurant(self):
        # Check to see if current restaurant is selected
        if self.current_restaurant == None:
            # Display error message
            self.generate_display_msg("Error","Select a restaurant to edit",QMessageBox.Warning)
        # Current restaurant selection is valid
        else:
            # Collect new restaurant data with new_restaurant parameter False to signify editing a restaurant
            new_restaurant_data, iterator = self.get_restaurant_info(False)
            # Make an empty string to store contents of new file
            new_file = ''
            # Open the location file
            current_location_file = open(os.path.join("restaurants",f"{self.current_location}.csv"), "r+")
            # Iterate over each line in the file
            for line in current_location_file:
                # Validate that line beings with current restaurant name
                if line[:len(self.current_restaurant)] == self.current_restaurant:
                    # Append the new data to the buffer instead
                    new_file += ','.join(new_restaurant_data) + '\n'
                # Current line entry does not being with current restaurant name
                else:
                    # Add previous unedited lines to new file
                    new_file += line
            # Set absolute file position
            current_location_file.seek(0)
            # Delete all contents of file
            current_location_file.truncate()
            # Write new data to file
            current_location_file.write(new_file)
            # Close the file
            current_location_file.close()
            # Display a success message once rewriting file
            self.generate_display_msg("Success",f"Successfully edited {self.current_restaurant}", QMessageBox.Information)
            # Rebuild the list of restaurants
            self.build_restaurants()

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
    # Call upon main function
    main()

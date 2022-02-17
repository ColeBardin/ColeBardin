# PyQt5 Restaurant Decider Application V1.2.1

PyQt5 based GUI to interact with a source of restaurants sorted by location to produce random decision

Interfaces with PyQt5 application to add location files and restaurant entries stored in .CSV files

Includes a compiled desktop application and installer

Shell script `builddmg.sh` takes desktop application built by PyInstaller and created DMG installer for MacOS

## Compililation, Packaging and Bundling

Use PyInstaller to create desktop application

Run command within  `./gui` directory

``pyinstaller -n "Amongus" --windowed --add-data='locations:locations' kaia_app.py``

Use shell script to create Disk Image installer for the application

``./builddmg.sh``

## Dependencies

### kaia_app.py:

[PyQt5](https://pypi.org/project/PyQt5/)

### Create Desktop Application:

[PyInstaller](https://pypi.org/project/pyinstaller/)

### Create MacOS Disk Image:

[Brew Create-DMG](https://formulae.brew.sh/formula/create-dmg)

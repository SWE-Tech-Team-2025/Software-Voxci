# Voxci Testing Software

## About the project
This is a desktop application to communicate with the testing device provided by the hardware team. This application meets specifics as set by Voxci. Code is mostly complete but does need some work before it is completely ready for use. 

## Getting Started

### Prerequisites

Both npm and poetry are required to run this application. Poetry is the Python package manager in use for this program, while npm installs all the frontend packages. For the ESP32, installing the Arduino IDE is needed to flash the code to the ESP32, and the CP210x USB drivers to be able to enable the ESP32 in the Arduino IDE. 

#### Installation

##### Poetry:

With Windows Subsystem for Linux, Linux, and MacOS, you can install poetry with this command: 

```
curl -sSL https://install.python-poetry.org | python3 -
```

The install command for Windows Powershell is 

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content py -
```

The PATH variable should be set after this install, but it can be set if not setup automatically. The installation guide linked below shows more detailed steps

https://python-poetry.org/docs/#installing-with-the-official-installer

##### npm:

An installer for npm for Windows and MacOS can be found here: https://nodejs.org/en/download/

If you are using this on Linux, please consult your distro documentation to find the package with your package manager. For example, on Arch Linux:

```
pacman -S npm
```

##### Arduino IDE

The Windows and MacOS installation can be found at the Arduino website here: https://www.arduino.cc/en/software/

On Linux, this can be installed at the same website with an AppImage or you can find the package in your distro package manager and install it that way. 

The CP210x USB drivers need to be installed in order for the IDE to find the ESP32 once plugged in. The install for Windows and MacOS can be found and installed here:

https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads

Along with that, in the Arduino IDE, manage libraries by going to Tools/Board/Board Manager and search for the esp32 package by Espressif and install it. 

 In many distros of Linux, the package already exists and doesn't require more packages to install. If the IDE can find the port the board is plugged into, then all you need is the esp32 package in the board manager.

### Poetry packages

This is the list of required poetry packages for the code: 

```
annotated-types
anyio
cffi
click
cryptography
dnspython
fastapi
h11
idna
jwt
pycparser
pydantic
pydantic-core
pymongo
python-dotenv
services
sniffio
starlette
typing-extensions
typing-inspection
uvicorn
xlsxwriter
```

The base packages needed are these packages, which will install some of the above as dependencies
```
python-dotenv
pymongo
fastapi(standard)
pydantic
pymongo
python-dotenv
xlsxwriter
```

### Npm packages

The following npm packages are necessary for the code:

```
eslint
tailwindcss
react
vite
autoprefixer
chart
```

Once npm, poetry, and their respective packages are installed, the application can be started in the project directory with the command

```
poetry run python run.py
```

This will start up everything and launch the GUI in a new browser window. 

## Usage

The GUI is pretty self explanitory with the buttons, but there are a couple things to mention. 

### Voltage and Frequency Inputs

These need to be set before the start button is clicked. Changing of values mid test is not supported and will lead to incorrect behavior. 

Once you set these values, click start, and the software will relay this info to the hardware and start the test as expected. I think we were supposed to give a overall testing time that the tests run for, but this functionality can be added without too much issue on the software side. The stop button, which should be implemented before this code is relayed to Voxci, will stop the test. 

Functionality is missing in the frontend to be able to change the die out and get a new die ID so that dies can be differentiated, but this functionality exists on the backend and should be able to be added in later versions. When this is added, if the die isn't swapped out and a new test is run, the die test number will increment to show a new die test and differentiate it in the database.

The graph in the GUI will show the live data during the test, but with the export button, this data will be exported to an Excel file that can be used for calculations for pass/fail.

All of this functionality is untested as of 11/27/2025, but should be mostly working by 12/03/25. 

## Contact

Samantha Raby: sraby4723@proton.me

Please contact me with any questions, I can also work on this with your team/developer if they need any help understanding parts of the code. Good luck, and I hope this code and the hardware helps!

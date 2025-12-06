# Voxci Testing Software

## About the project
This is a desktop application to communicate with the testing device provided by the hardware team. This application meets specifics as set by Voxci. Code is mostly complete but does need some work before it is completely ready for use. 

## Getting Started

### Prerequisites

Both npm and poetry are required to run this application. Poetry is the Python package manager in use for this program, while npm installs all the frontend packages. For the ESP32, installing the Arduino IDE is needed to flash the code to the ESP32, and the CP210x USB drivers to be able to enable the ESP32 in the Arduino IDE. The data for the application is stored in a MongoDB instance, either an online Atlas instance or a local run instance on the host machine. All of these need to be set up for the application to fully do the job. 

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

On Linux, this can be installed at the same website with an AppImage or you can find the package in your distro package manager and install it that way. It may also already be included in the kernel, and to check, just see if the board shows up in the Arduino IDE when you plug it in.

The CP210x USB drivers need to be installed in order for the IDE to find the ESP32 once plugged in. The install for Windows and MacOS can be found and installed here:

https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads

Along with that, in the Arduino IDE, manage libraries by going to Tools/Board/Board Manager and search for the esp32 package by Espressif and install it. 

 In many distros of Linux, the package already exists and doesn't require more packages to install. If the IDE can find the port the board is plugged into, then all you need is the esp32 package in the board manager.

##### MongoDB

To install MongoDB on the local host, follow installation instructions here: 

https://www.mongodb.com/docs/manual/installation/  

If local host isn't what you choose, just create an Atlas database on their website and follow the next steps. 

For both of these options, all that needs to be done is the edition of the .env file, which contains the API key for the MongoDB instance. This must go in the src/backend folder in order for the database_comm.py to find the key. This should not be uploaded to the repository, as this is a security hole. 

The .env contains the key in this format: 

```
MONGODB_URI=mongodb+srv://myUser:myPass123@mongodb0.example.com/
```

For the local install, you can find the key with the MongoDB Shell after starting the server. Just paste this key into the .env, and the code will find the database.

For the Atlas instance, the key can be found in the management portal for the instance. This can be found by logging into the dashboard with your MongoDB user account.


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

All of this functionality is untested as of 11/27/2025. 

## File Structure

The code is organized into the following structure: 

```
src
    backend
        .env
        backend files
    frontend
        frontend files
esp32
    esp32 files
index.html
run.py
```

The .env needs to be added after the MongoDB instance is set up. The routes are already set in the coding files, so all that needs to be done to run the program is to run  run.py. 

### Backend

The backend has these files: 

```
__init__.py
database_comm.py
esp_32_wifi_communicator.py
excel_export.py
main.py
routes.py
shared_shutdown.py
```

#### init.py:

Used for routing for files. Can be ignored, but has to stay put.

#### database_comm.py

Manages all operations to and from the database. Adds die sweeps, dies, and can recall them for Excel exporting. 

#### esp_32_wifi_communicator.py

Manages the ESP32 connections and allows for messages to be sent by the code and received from the ESP32.  

Outgoing messages come in two flavors:
- OutMessage  
    Every parameter sent to the hardware device such as the voltage range and the frequency  

- StartStopTestMsg  
    Sends the start/stop message to the hardware, when stop is called during a test, the test will halt in its tracks

There is only one version of the incoming message, we are mostly dealing with incoming sweeps, and all this data is handled by the InMessage class.

Along with that we also have encoding for each, and two handler methods,listener_thread and sender_thread. Both of these handle live messages and place them into the respective queues, which the code then dequeues and handles. 

The buffer contains the text and data sent to the computer. It is set to 256 characters but can be changed for larger messages lengths.

#### excel_export.py

Takes input and finds every sweep associated with the unique die ID# and the test number, then adds it to an Excel file to export.

#### main.py

Runs the program after being called by run.py. Initializes the database communication and the ESP32 communucation. Also handles interrupts from routes.py and FastAPI

#### routes.py

Manages all the FastAPI routes, including stopping the test when the stop button is pressed, parsing input from the text boxes, and more.

#### shared_shutdown.py

Adds the shutdown implementation to shutdown the application when the UI calls the shutdown route in routes.py

#### run.py

Manages starting all services for the program. Starts FastAPI and React, opens the GUI in a new browser, and calls the backend code. Works across all platforms as it changes the executed code depending on the operating system.

### Frontend

The frontend has these files:

```
index.html
main.jsx
App.jsx
App.css
style.css
assets/
```

#### index.html

The main HTML file that serves as the entry point for the web application. Contains the basic HTML structure with:
- Meta tags for character encoding and responsive viewport settings
- Link to the global CSS file (index.css)
- A root div element where the React application mounts
- Script tag that loads the React application from main.jsx

#### main.jsx

Entry point for the React application. Initializes the React root, renders the App component within React's StrictMode, and attaches it to the DOM element with id "root". This file sets up the entire frontend application.

#### App.jsx

Main React component that contains all the application logic and UI. Manages the state for frequency, voltage, graph data, and test run history. Implements the following functionality:
- Input handling for voltage and frequency parameters with slider and text inputs
- Start button to initiate tests and generate capacitance vs voltage data
- Live graph rendering using Chart.js to display test results
- Data history tracking for all test runs with timestamps
- Excel export functionality to save test data to a spreadsheet file
- Clear graph function to reset the display
- Shutdown button to close the application via backend API call
- Displays the Vocxi logo in the top navigation bar
- Data history table showing run number, timestamp, frequency, and voltage for each test

#### App.css

Primary stylesheet for the application. Defines all the visual styling including:
- Layout structure with flexbox for left panel (controls) and right panel (graph)
- Blue top navigation bar with logo positioning
- Light blue input boxes and graph containers with rounded corners and shadows
- Input styling for frequency slider, voltage text input, and number inputs
- Button styling with hover effects and consistent sizing
- Graph container with responsive sizing and overflow handling
- Data history table styling with alternating row colors and hover effects
- Responsive design to maintain proper layout across different screen sizes

#### style.css

Contains Tailwind CSS imports. While Tailwind is installed and configured in the project, the current implementation uses custom CSS classes defined in App.css rather than Tailwind utility classes.

#### assets/

Directory containing static assets used by the frontend, primarily the Vocxi logo image (vocxi_logo.png) that appears in the top navigation bar.



## Contact

Samantha Raby  

Email: jraby@wisc.edu  
Personal Email: sraby4723@proton.me  

Sasha Nikitin
Email: anikitin@wisc.edu
Personal Email: volshebnik2014@gmail.com

Please contact me with any questions, I can also work on this with your team/developer if they need any help understanding parts of the code. Good luck, and I hope this code and the hardware helps!

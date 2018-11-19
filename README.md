# temp_reader
temp_reader is an app that displays an auto-updating web page with the current room temperatue read from a raspberry pi.

### Installation
First install a python 3.7 virtual environment using whatever way you want and activate it.
    
    git clone https://github.com/xkal36/temp_reader
    pip install -r requirements.txt
   
### Running
    python app.py

### Tasks
* Hook up temperature sensor to raspberry pi and test
* Have the pause between temperature reads be passed in from command line args (currently hardcoded)
* Replace random number generator with code that reads temperature from raspberry pi temperature sensor
* Style webpage
* Display current temperatue in an easily visible manner
* Display chart of temperatures

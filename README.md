# temp_reader
temp_reader is an app that displays an auto-updating web page with the current room temperatue read from a raspberry pi.

### Installation
First install a python 3.7 virtual environment using whatever way you want and activate it.
    
    git clone https://github.com/xkal36/temp_reader
    pip install -r requirements.txt
   
### Running
    python app.py 10


In the above example, the temperature will be read and sent to the browser every 10 seconds.
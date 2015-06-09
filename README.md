# ODR-EncoderManager
OpenDigitalRadio Encoder Manager is a tools to run and configure ODR Encoder easly with a WebGUI.

The first script 'encoder.py' launch dabplus-enc and mot-encoder according config.ini and expose a JSONRPC api
The second script 'api.py' provide a web server

ODR-EncoderManager is currently in developpement and is not yet ready to use in production.

![Screenshot] (https://raw.github.com/YoannQueret/ODR-EncoderManager/master/ODR-Encoder_Manager.png)

# INSTALLATION

Run install-python-dependency.sh to install all python dependency.

  * ./encoder.py -c /absolute_path/config.ini -l /absolute_path/logs/
  * ./api.py -s /absolute_path/static/ -l /absolute_path/logs/

# IN PRODUCTION

  See doc/supervisor/README.md
  
# Warning
This program has been tested only on GNU/Linux Debian Jessie (8.x)

No access protection has been implemented yet instead IP binding configuration. So, unless the network is protected otherwise, anyone can access and modify your encoder settings.


# TODO LIST

  * Create help content on help page
  * Add documentation about API and how to update automaticly DLS from different automation software.




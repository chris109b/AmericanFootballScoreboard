# AmericanFootballScoreboard

An application to display, manage and distribute scoreboard data for American Football games in various ways.

## Key features

* Remote Control Interface - A simple web interface to change the information shown on the board (optimized for smart phones and tablets).
* Display Interface - A simple web site, showing a full featured scoreboard on almost any screen (640x360 - 3840x2160 pixel size).
* Plugins - To share data with other applications or devices.
  * OBS Studio Plugin - Writes data to separate text files within one folder. Those files can be used to display the information within an video live stream created with OBS Studio.
  * Logfile Plugin - Writes data to log file with time stamps to document the course of the game and help with writing statistics.
  * Test Plugin - A simple example for you to learn how to develop your own plugin.
* Bonjour/Avahi/Zeroconf Service Announcement - Allowing you to find the service easily.

## Technology

* Python - https://en.wikipedia.org/wiki/Python_(programming_language)
* HTML - https://en.wikipedia.org/wiki/HTML
* CSS - https://en.wikipedia.org/wiki/Cascading_Style_Sheets
* JavaScript - https://en.wikipedia.org/wiki/JavaScript
* Tornado - https://en.wikipedia.org/wiki/Tornado_(web_server)

## Other applications that can be useful along with this software:

* Zentri Discovery - https://play.google.com/store/apps/details?id=discovery.ack.me.ackme_discovery
* Pea Finder - https://play.google.com/store/apps/details?id=com.ersteheimat.peafinder

## Installation on Microsoft Windows

* You need to install Python 3.x. You can download it here: https://www.python.org/
* You need to install the Python packages listet in "requirements.txt", here is how you do it: https://docs.python.org/3/installing/index.html
* For some of the packages a compiler is needed for installation: http://landinghub.visualstudio.com/visual-cpp-build-tools
* If you want to keep on track with the latest development install Git and clone the repsitory: https://git-scm.com/downloads
* If you want to be able to alter the code yourself Notepad++ is a nice editor to do so: https://notepad-plus-plus.org/

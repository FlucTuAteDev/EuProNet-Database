### Welcome to the EU PRONET database github repository!

Here we are creating tools to transport data from the workstations of the different countries to the central database. We also provide an empty database skeleton for local testing if you need. 


The _queries _table is where all the information about what's going on at each country's workstations will flow in. We will write server-side programs to process this data and update other database tables and views accordingly.

In the _states _table each country will define the different states of their operation and assign code numbers to them. The codes don't have to be globally unique, they only have to be unique within the specific country's state codes. 

The _countrycodes_ table keeps each country's name, two letter code and an id number we'll use inside the database. Here's how that looks: 

![(Based on ISO 3166 and logo order)](https://i.imgur.com/IHHQ0Yl.png)

The _colors_ table defines an id number for each color for use inside the database.
***
We do not know what data your workstations can generate and we do not know what protocols your workstations use to connect to your computers. We also don't know exactly all the different steps of each country's operations. Therefore, we have intentionally designed our framework to be as flexible and expandable as possible.

![Diagram](https://imgur.com/2osiNLM.png)

Currently we have a NodeMCU board that simulates a workstation, an imagined 3D printer. When you press a colored button it starts to “print” a chip of that color. It also has a button to discard the chip (e.g. the print failed) and another button to indicate that the print has finished. 

_collector.py_ communicates with the workstation through WiFi/Serial and writes the incoming data into a buffer file in the correct format. You do not necessarily have to use _collecor.py_, you can expand it or you can use your own tool. That's why we seperated the data collection and upload process into two seperate scripts. <br>
_filetosql.py_ monitors the buffer file and uploads its contents to the database. It attaches your country code automatically based on your login information. The date will also be added if it's not specified already.

***

We plan on providing compiled executable files so you do not need to install a python environment on your machine to run these tools.

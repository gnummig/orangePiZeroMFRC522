#! /bin/bash
#Start with fresh  5.25 jessie server image.
sudo apt-get --yes update
sudo apt-get --yes upgrade 
sudo apt-get --yes install python-dev python-pip
pip install spidev --user
#python setup.py install
pip install --upgrade pip --user
pip install setuptools --user
pip install pip --user
#apt install python-dev --user
# change owndership of the python library folder to be able to run librarys as user door
#sudo chown -R door /usr/local/lib/
# get gpio library
git clone https://github.com/duxingkei33/orangepi_PC_gpio_pyH3
cd orangepi_PC_gpio_pyH3/
python setup.py install
cd ..
#get SPI library
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py/
python setup.py install
cd ..
#get MFRC533 library
git clone https://github.com/gnummig/MFRC522-python
sudo sed -i "/exit 0/c\ exec sudo python \/home\/door\/orangePiZeroMFRC522\/door.py & \n exit 0" /etc/rc.local 

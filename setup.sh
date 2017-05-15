#! /bin/bash
#Start with fresh  5.14 jessie server image. Bring it up to 5.16
apt-get update
apt-get upgrade
apt-get install python-dev python-pip
pip install spidev
python setup.py install
pip install --upgrade pip
sudo pip install setuptools
sudo pip install pip
sudo apt install python-dev
cd ..
git clone https://github.com/duxingkei33/orangepi_PC_gpio_pyH3
cd orangepi_PC_gpio_pyH3
python setup.py install
cd ..
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
python setup.py install
cd ..
git clone https://github.com/gnummig/MFRC522-python

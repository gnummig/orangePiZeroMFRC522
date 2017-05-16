#! /bin/bash
#Start with fresh  5.25 jessie server image.
sudo pt-get --yes update
sudo apt-get --yes upgrade 
sudo apt-get --yes install python-dev python-pip
sudo pip install spidev
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

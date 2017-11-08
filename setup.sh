#! /bin/bash
#Start with fresh Armbian_5.25_Orangepizero_Debian_jessie_default_3.4.113.img
#printf "for wifi usage please enter the BSSID and the password of your wifi\n be aware that to this point the password is saved as plaintext on the operating system \n SSID:"
#read wifissid
#printf "password:"
#read wifipasswd
apt-key update
apt-get --yes update
apt-get --yes upgrade 
apt-get --yes install python-dev python-pip locate
updatedb   # jsut for debugging convenience and keeping the overview.
# install vundle for vim --highly optional, but for convenience--
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
#python setup.py install
pip install --upgrade pip --user
pip install setuptools --user
#pip install pip --user
pip install spidev --user
#apt install python-dev --user
# change owndership of the python library folder to be able to run librarys as user door
#sudo chown -R door /usr/local/lib/
cd ..
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
#git clone https://github.com/gnummig/MFRC522-python
# edit rc.local to run script automatically at startup
#sudo sed -i "/exit 0/c\exec \/usr\/bin\/python \/root\/orangePiZeroMFRC522\/door.py 1>\/dev\/null 2>&1 & \nexit 0" /etc/rc.local 
# alternatively start script via init.d
#mv orangePiZeroMFRC522/initdoor.sh /etc/init.d/initdoor.sh
#ln -s /etc/init.d/initdoor.sh /etc/rc5.d/S06initdoor.sh
#cd /etc/init.d/
#update-rc.d initdoor.sh defaults
# configure wifi( not sure whether it works:
#cp /etc/network/interfaces /etc/network/interfacesoriginal
#rm /etc/network/interfaces
#printf "iface lo inet loopback\n\nauto eth0\nallow-hotplug eth0\niface eth0 inet dhcp\n\nallow-hotplug wlan0\niface wlan0 inet manual\nwpa-roam /etc/wpa_supplicant/wpa_supplicant.conf\niface default inet dhcp" > /etc/network/interfaces
#printf "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\n\nnetwork={\nssid=\""$wifissid\""\npsk=\""$wifipasswd\""\n}" > /etc/wpa_supplicant/wpa_supplicant.conf
#make the orPi slow so that it doesnt consume to much energy:
echo 0 >/sys/devices/system/cpu/cpu3/online
echo 0 >/sys/devices/system/cpu/cpu2/online
echo 0 >/sys/devices/system/cpu/cpu1/online
echo 408000 >/sys/devices/platform/sunxi-ddrfreq/devfreq/sunxi-ddrfreq/userspace/set_freq

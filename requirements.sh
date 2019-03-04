#!/bin/bash

clear
sleep 1

echo -e "\e[1;33m███──█───██─████──████──███
█────██─███─█──█──█──█───█
███──█─█─██─████──████───█
──█──█───██─█──█──█─█────█
███──█───██─█──█──█─█────█\e[0m"

sleep 1
echo ""

echo -e "\e[1;37m█───██─███──████──████──████──████
██─███──█───█──█──█──█──█──█──█──█
█─█─██──█───████──████──█──█──████
█───██──█───█─█───█─█───█──█──█─█
█───██─███──█─█───█─█───████──█─█\e[0m"
sleep 1
echo ""

echo -n -e "\e[1mEnter num core: \e[0m"
read core

#Установка пакетов для python3
sudo apt-get install python3-lxml
pip3 install request feedparser Pillow beautifulsoup4 SpeechRecognition gTTS

#Удаление барохла с Raspberry Pi
sudo apt-get purge wolfram-engine
sudo apt-get purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove

#Установка OpenCV
sudo apt-get install -y build-essential pkg-config
sudo apt-get install -y cmake cmake-curses-gui libgtk2.0-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libx264-dev libxvidcore-dev
sudo apt-get install -y libjpeg-dev libpng12-dev libtiff5-dev libjasper-dev
sudo apt-get install -y gfortran libatlas-base-dev
sudo apt-get install -y libdc1394-22-dev libavresample-dev libgphoto2-dev ffmpeg libgtk-3-dev
sudo apt-get install -y libvtk6-dev

sudo pip3 install numpy

cd  /home/pi
mkdir opencv
cd  opencv

wget https://github.com/opencv/opencv/archive/3.4.0.zip -O opencv_source.zip
wget https://github.com/opencv/opencv_contrib/archive/3.4.0.zip -O opencv_contrib.zip
unzip opencv_source.zip
unzip opencv_contrib.zip

rm opencv_source.zip
rm opencv_contrib.zip

cd /home/pi/opencv/opencv-3.4.0
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=OFF \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D OPENCV_EXTRA_MODULES_PATH=/home/pi/opencv/opencv_contrib-3.4.0/modules \
      -D BUILD_EXAMPLES=ON \
      -D BUILD_DOCS=ON \
      -D ENABLE_NEON=ON ..

make -j$core

sudo make install
sudo ldconfig

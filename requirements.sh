#!/usr/bin/env bash

OPENCV_VERSION="$1"                                                                                 # Версию скрипта передаем параметром, например 3.4.0

OPENCV_SOURCE_ZIP="https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip"
OPENCV_CONTRIB_SOURCE_ZIP="https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.zip"  # Задаем путь к архиву с дополнительными модулями
OPENCV_PACKAGE_NAME="opencv-${OPENCV_VERSION}"                                                      # Папка для распаковки архива с библиотекой
OPENCV_CONTRIB_PACKAGE_NAME="opencv_contrib-${OPENCV_VERSION}"                                      # Папка для распаковки архива с дополнительными модулями

PREFIX="${PREFIX:-/usr/local}"
MAKEFLAGS="${MAKEFLAGS:--j 4}"


install_build_dependencies() {

    # Список устанавливаемых пакетов:
    # - cmake                   Утилита для автоматической сборки программы из исходного кода
    # - cmake-curses-gui        Пакет GUI (графический интерфейс) для cmake

    # - libgtk2.0-dev           GTK+ инструментарий для создания графических пользовательских интерфейсов

    # - libjpeg-dev             Библиотеки для работы с разными форматами изображений
    # - libpng12-dev
    # - libtiff5-dev
    # - libjasper-dev           JasPer - набор программ для кодирования и обработки изображений

    # - libavcodec-dev	        Библиотека кодеков от Libav (аудио/видео)
    # - libavformat-dev         Библиотека кодеков от Libav (аудио/видео)
    # - libswscale-dev          Библиотека для выполнения высокооптимизированных масштабирований изображений и цветовых пространств и операций преобразований
    # - libv4l-dev              Набор библиотек, для работы с устройствами video4linux2
    # - libx264-dev             Библиотека кодирования для создания видеопотоков H.264 (MPEG-4 AVC)
    # - libxvidcore-dev         Видеокодек MPEG-4 (Xvid)
 
    # - gfortran	        Матричные преобразования
    # - libatlas-base-dev 	Матричные преобразования


    local build_packages="cmake cmake-curses-gui"
                                # build-essential        Предустановлены в системе
                                # pkg-config"

    local gtk_packages="libgtk2.0-dev"

    local image_packages="libjpeg-dev libpng12-dev \
                               libtiff5-dev libjasper-dev"

    local video_packages="libavcodec-dev libavformat-dev \
                               libswscale-dev libv4l-dev \
                               libxvidcore-dev libx264-dev"

    local matrix_packages="gfortran libatlas-base-dev"

    sudo apt-get install -y $build_packages $gtk_packages $image_io_packages \
                               $video_io_packages $matrix_packages
}

download_packages() {
    cd  /home/pi
    mkdir opencv
    cd  opencv
    wget "$OPENCV_SOURCE_ZIP" -O "${OPENCV_PACKAGE_NAME}.zip"
    wget "$OPENCV_CONTRIB_SOURCE_ZIP" -O "${OPENCV_CONTRIB_PACKAGE_NAME}.zip"
}

unzip_packages() {
    unzip "${OPENCV_PACKAGE_NAME}.zip"
    unzip "${OPENCV_CONTRIB_PACKAGE_NAME}.zip"

    rm "${OPENCV_PACKAGE_NAME}.zip"
    rm "${OPENCV_CONTRIB_PACKAGE_NAME}.zip"
}

install_numpy() {
    sudo pip3 install numpy
}

configure() {
    cd  /home/pi/opencv/"$OPENCV_PACKAGE_NAME"
    mkdir build
    cd build

    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX="$PREFIX" \
          -D INSTALL_C_EXMAPLES=OFF \
          -D INSTALL_PYTHON_EXAMPLES=ON \
          -D OPENCV_EXTRA_MODULES_PATH=/home/pi/opencv/"$OPENCV_CONTRIB_PACKAGE_NAME"/modules \
          -D BUILD_EXAMPLES=ON \
          -D BUILD_DOCS=ON \
          -D ENABLE_NEON=ON \
          ..
    make ${MAKEFLAGS}
}

install_opencv() {
    sudo make install
    sudo ldconfig
}

log() {
    local msg="$1"; shift
    local _color_bold_yellow='\033[1;33m'
    local _color_reset='\033[0m'
    echo -e "${_color_bold_yellow}*  ${msg}  *${_color_reset}"
}

main() {
    if [ $OPENCV_VERSION = "" ]
    then
	log "Need OpenCV_version, for example '3.4.0'"
    	exit
    fi

    log "Installing build dependencies..."
    install_build_dependencies

    log "Installing NumPy..."
    install_numpy

    log "Downloading OpenCV packages..."
    download_packages

    log "Unpacking OpenCV packages..."
    unzip_packages

    log "Building OpenCV..."
    configure

    log "Installing OpenCV..."
    install_opencv

}

main

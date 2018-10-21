#!/bin/sh
# For compiling when MPFR and BOOST libraries are not automatically found, example cmake command:
# cmake ../${CGAL_VERSION}/ -DWITH_CGAL_Qt5=OFF -DWITH_CGAL_ImageIO=OFF -DCGAL_HEADER_ONLY=ON -DCMAKE_INSTALL_PREFIX=.. -DMPFR_INCLUDE_DIR=/N/soft/rhel7/mpfr/gnu/3.1.5/include -DMPFR_LIBRARIES=/N/soft/rhel7/mpfr/gnu/3.1.5/lib/libmpfr.so -DBOOST_ROOT=/N/soft/rhel7/boost/gnu/1.64.0

CGAL_VERSION=CGAL-4.11

echo "I'm going to download and compile ${CGAL_VERSION} for you."
echo "This will take about 100MB of disk space."
echo "Press ENTER to continue, Ctrl+C to cancel."
read -p "" key

mkdir cgal/
cd cgal/
wget -nc -O ${CGAL_VERSION}.tar.xz https://github.com/CGAL/cgal/releases/download/releases%2F${CGAL_VERSION}/${CGAL_VERSION}.tar.xz
tar -xf ${CGAL_VERSION}.tar.xz
rm ${CGAL_VERSION}.tar.xz
cd ..

mkdir cgal/build
cd cgal/build
cmake ../${CGAL_VERSION}/ -DWITH_CGAL_Qt5=OFF -DWITH_CGAL_ImageIO=OFF -DCGAL_HEADER_ONLY=ON -DCMAKE_INSTALL_PREFIX=..
make
make install
cd ..
rm -r build
rm -r $CGAL_VERSION
cd ..

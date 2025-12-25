#!/bin/bash
set -e

VERSION="0.1.2"
PACKAGE_NAME="treecatt"
BUILD_DIR="deb_dist/${PACKAGE_NAME}_${VERSION}_all"
INSTALL_PREFIX="/usr/local"

rm -rf deb_dist
mkdir -p "${BUILD_DIR}/DEBIAN"
mkdir -p "${BUILD_DIR}${INSTALL_PREFIX}/lib/python3/dist-packages"
mkdir -p "${BUILD_DIR}${INSTALL_PREFIX}/bin"

cp -r src/treecatt "${BUILD_DIR}${INSTALL_PREFIX}/lib/python3/dist-packages/"

cat > "${BUILD_DIR}/DEBIAN/control" <<EOF
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: all
Maintainer: TreeCatt <contact@treecatt.dev>
Depends: python3 (>= 3.8)
Description: Advanced CLI tool combining tree and cat
 TreeCatt is an advanced command-line tool that combines directory
 tree visualization with file content display, search, filtering,
 and checksum calculation.
EOF

dpkg-deb --build "${BUILD_DIR}" "deb_dist/${PACKAGE_NAME}_${VERSION}_all.deb"

echo "✅ .deb package created: deb_dist/${PACKAGE_NAME}_${VERSION}_all.deb"

###############################################################################
#                                                                             #
# YencaP software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM                #
# Copyright (C) 2005  Vincent CRIDLIG                                         #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU           #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
#                                                                             #
# Author Info:                                                                #
#   Name : Vincent CRIDLIG                                                    #
#   Email: Vincent.Cridlig@loria.fr                                           #
#                                                                             #
###############################################################################


ENSUITE=ensuite
YM=yencap-manager
VERSION=3
YMV=${YM}-${VERSION}

ENSUITE_INSTALL_DIR=$(DESTDIR)/usr/local/${ENSUITE}
YM_INSTALL_DIR=${ENSUITE_INSTALL_DIR}/${YM}
ENSUITE_CONF_DIR=$(DESTDIR)/etc/${ENSUITE}
YM_CONF_DIR=${ENSUITE_CONF_DIR}/${YM}

TMP_PATH=/tmp
YENCAP_TMP_PATH=${TMP_PATH}/${YMV}


build:
	mkdir -p build
	# Copy python files and other needed files to build dir
	cp *.py build
	cp -r Components build
	cp -r www build

install: build

	# Install configuration files
	mkdir -p ${YM_CONF_DIR}
	cp conf/*.xml ${YM_CONF_DIR}
	cp conf/id_rsa ${YM_CONF_DIR}
	cp conf/id_rsa.pub ${YM_CONF_DIR}
	cp conf/server.pem ${YM_CONF_DIR}

	# Install YencaP sources
	mkdir -p ${YM_INSTALL_DIR}
	cp -r build/* ${YM_INSTALL_DIR}
	rm -rf build

	# Install daemon service
	mkdir -p $(DESTDIR)/etc/init.d
	cp bin/${YM} $(DESTDIR)/etc/init.d
	mkdir -p $(DESTDIR)/usr/bin
	ln -s /usr/local/ensuite/yencap-manager/yencaPManager.py $(DESTDIR)/usr/bin/yencaPManager


uninstall:
	rm -Rf ${YM_INSTALL_DIR}
	rm -Rf /usr/bin/yencaPManager
	rm -Rf /etc/init.d/yencap-manager



#####################
#   Distributions   #
#####################

targz:	mrproper
	mkdir -p /tmp/${YMV}
	cp -r * /tmp/${YMV}
	find /tmp/${YMV} -name .so6 -exec /bin/rm -R {} \;
	tar -C /tmp -zcvf /tmp/${YMV}.tar.gz ${YMV}

rpm: mrproper
	mkdir -p /tmp/${YMV}
	cp -r * /tmp/${YMV}
	tar -C /tmp -zcvf /usr/src/redhat/SOURCES/${YMV}.tar.gz ${YMV}
	cd /tmp;rpmbuild -ba /tmp/${YMV}/Package/FEDORA/${YM}.spec
	rm -rf /tmp/${YMV}

deb: mrproper
	mkdir -p /tmp/${YM}${YM_CONF_DIR}
	mkdir -p /tmp/${YM}/etc/init.d
	mkdir -p /tmp/${YM}${YM_INSTALL_DIR}

	cp -r ./Package/DEBIAN /tmp/yencap

	cp conf/*.xml /tmp/${YM}${YM_CONF_DIR}
	cp conf/id_rsa /tmp/${YM}${YM_CONF_DIR}
	cp conf/id_rsa.pub /tmp/${YM}${YM_CONF_DIR}

	cp *.py /tmp/${YM}${YM_INSTALL_DIR}
	cp -r Filters /tmp/${YM}${YM_INSTALL_DIR}
	cp -r Modules /tmp/${YM}${YM_INSTALL_DIR}
	cp -r Operations /tmp/${YM}${YM_INSTALL_DIR}
	cp -r rbac /tmp/${YM}${YM_INSTALL_DIR}
	cp -r Servers /tmp/${YM}${YM_INSTALL_DIR}

	cp bin/netconfd /tmp/${YM}/etc/init.d

	cd /tmp;dpkg -b /tmp/${YM} ${YMV}.deb
	rm -rf /tmp/${YM}


#####################
#  Clean tmp files  #
#####################

mrproper: clean cleanSource cleanBuild


clean:
	find . -name \*.pyc -exec rm {} \;
	find . -name \*~ -exec rm {} \;

cleanSource:
	rm -rf ${YENCAP_TMP_PATH}

cleanBuild:
	rm -rf build


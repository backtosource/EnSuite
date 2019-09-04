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
YENCAP=yencap
VERSION=3
YV=${YENCAP}-${VERSION}

ENSUITE_INSTALL_HOME=$(DESTDIR)/usr/local/${ENSUITE}
YENCAP_INSTALL_HOME=${ENSUITE_INSTALL_HOME}/${YENCAP}
ENSUITE_CONF_HOME=$(DESTDIR)/etc/${ENSUITE}
YENCAP_CONF_HOME=${ENSUITE_CONF_HOME}/${YENCAP}
YENCAP_CONF_KEYS=${YENCAP_CONF_HOME}/conf

TMP_PATH=/tmp
YENCAP_TMP_PATH=${TMP_PATH}/${YV}


build:
	mkdir -p build
	# Copy python files and other needed files to build dir
	cp *.py build
	cp -r Modules build
	cp -r Operations build
	cp -r Servers build
	cp -r rbac build
	cp -r Filters build
	cp -r yapps2lc build


install: build

	# Install configuration files
	mkdir -p ${YENCAP_CONF_KEYS}
	cp conf/*.xml ${YENCAP_CONF_HOME}
	cp conf/id_rsa ${YENCAP_CONF_KEYS}
	cp conf/id_rsa.pub ${YENCAP_CONF_KEYS}

	# Install YencaP sources
	mkdir -p ${YENCAP_INSTALL_HOME}
	cp -r build/* ${YENCAP_INSTALL_HOME}
	rm -rf build

	# Install daemon service
	mkdir -p $(DESTDIR)/etc/init.d
	cp bin/${YENCAP} $(DESTDIR)/etc/init.d/
	mkdir -p $(DESTDIR)/usr/bin
	 ln -s  ${YENCAP_INSTALL_HOME}/netconfd.py $(DESTDIR)/usr/bin/netconfd
	#ln -s /usr/local/ensuite/yencap/netconfd.py $(DESTDIR)/usr/bin/netconfd

uninstall:
	rm -Rf ${YENCAP_INSTALL_HOME}
	rm -Rf /usr/bin/netconfd
	rm -Rf /etc/init.d/yencap


#####################
#   Distributions   #
#####################

targz: mrproper
	mkdir -p ${YENCAP_TMP_PATH}
	cp -r * ${YENCAP_TMP_PATH}
	find ${YENCAP_TMP_PATH} -name .so6 -exec /bin/rm -R {} \;
	tar -C ${TMP_PATH} -zcvf ${YENCAP_TMP_PATH}.tar.gz ${YV}

tarbz2: mrproper
	mkdir /tmp/${YV}
	cp -r * /tmp/${YV}
	find /tmp/${YV} -name .so6 -exec /bin/rm -R {} \;
	tar -C /tmp -cvf /tmp/${YV}.tar ${YV}
	bzip2 /tmp/${YV}.tar 

rpm: mrproper
	mkdir /tmp/${YV}
	cp -r * /tmp/${YV}
	find /tmp/${YV} -name .so6 -exec /bin/rm -R {} \;
	tar -C /tmp -zcvf /usr/src/redhat/SOURCES/${YV}.tar.gz ${YV}
	cd /tmp;rpmbuild -ba /tmp/${YV}/Package/FEDORA/yencap.spec
	rm -rf /tmp/${YV}

deb: mrproper
	mkdir -p /tmp/yencap${YENCAP_CONF_HOME}
	mkdir -p /tmp/yencap/etc/init.d
	mkdir -p /tmp/yencap${YENCAP_INSTALL_HOME}

	cp -r ./Package/DEBIAN /tmp/yencap

	cp conf/*.xml /tmp/yencap${YENCAP_CONF_HOME}
	cp conf/id_rsa /tmp/yencap${YENCAP_CONF_KEYS}
	cp conf/id_rsa.pub /tmp/yencap${YENCAP_CONF_KEYS}

	cp *.py /tmp/yencap${YENCAP_INSTALL_HOME}
	cp -r Filters /tmp/yencap${YENCAP_INSTALL_HOME}
	cp -r Modules /tmp/yencap${YENCAP_INSTALL_HOME}
	cp -r Operations /tmp/yencap${YENCAP_INSTALL_HOME}
	cp -r rbac /tmp/yencap${YENCAP_INSTALL_HOME}
	cp -r Servers /tmp/yencap${YENCAP_INSTALL_HOME}
	cp -r yapps2lc /tmp/yencap${YENCAP_INSTALL_HOME}

	cp bin/netconfd /tmp/yencap/etc/init.d

	cd /tmp;dpkg -b /tmp/yencap ${YV}.deb
	rm -rf /tmp/yencap



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


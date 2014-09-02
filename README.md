openresty-rpm-spec
==================

This spec file will build an RPM for OpenResty. I've only tried it on CentOS 6, but it will likely work on other RedHat-like Linuxes.

To build the RPM, you'll first need to set up your build environment. Typically, this means creating some directories and installing some packages:

	mkdir ~/rpmbuild/{SOURCES,SPECS}
	sudo yum install make openssl-devel pcre-devel readline-devel gcc-c++

Then get the relevant files into your tree (replacing `version` with the appropriate version string):

	cd ~/rpmbuild/SOURCES
	wget http://openresty.org/download/ngx_openresty-{version}.tar.gz
	wget https://github.com/brnt/openresty-rpm-spec/raw/master/nginx.init
	cd ~/rpmbuild/SPECS
	wget https://github.com/brnt/openresty-rpm-spec/raw/master/ngx_openresty.spec

Then just build the RPM:

	rpmbuild -ba ~/rpmbuild/SPECS/ngx_openresty.spec

The RPM will be in `~/rpmbuild/RPMS/{platform}/` and the SRPM will be in `~/rpmbuild/SRPMS/`.

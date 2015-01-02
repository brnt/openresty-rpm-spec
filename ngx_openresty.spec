Name:		ngx_openresty
Version:	1.7.4.1
Release:	1%{?dist}
Summary:	a fast web app server by extending nginx

Group:		Productivity/Networking/Web/Servers
License:	BSD
URL:		openresty.org
Source0:	http://openresty.org/download/%{name}-%{version}.tar.gz
Source1:	https://github.com/brnt/openresty-rpm-spec/raw/master/nginx.init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	sed openssl-devel pcre-devel readline-devel
Requires:	openssl pcre readline
Requires(pre):	shadow-utils

%define _unpackaged_files_terminate_build 0
%define user nginx
%define homedir /opt/openresty

%description
OpenResty (aka. ngx_openresty) is a full-fledged web application server by bundling the standard Nginx core, lots of 3rd-party Nginx modules, as well as most of their external dependencies.


%prep
%setup -q


%build
./configure --prefix=/opt/openresty --with-ipv6 --with-pcre-jit --with-luajit
make %{?_smp_mflags}


%pre
getent group %{user} || groupadd -f -r %{user}
getent passwd %{user} || useradd -M -d %{homedir} -g %{user} -s /bin/nologin %{user}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/etc/init.d
sed -e 's/%NGINX_CONF_DIR%/%{lua: esc,qty=string.gsub(rpm.expand("%{homedir}"), "/", "\\/"); print(esc)}\/nginx\/conf/g' \
	-e 's/%NGINX_BIN_DIR%/%{lua: esc,qty=string.gsub(rpm.expand("%{homedir}"), "/", "\\/"); print(esc)}\/nginx\/sbin/g' \
	%{SOURCE1} > %{buildroot}/etc/init.d/nginx


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
#%{homedir}/*

%attr(755,root,root) /etc/init.d/nginx
%{homedir}/luajit/*
%{homedir}/lualib/*
%{homedir}/nginx
%{homedir}/nginx/html/*
%{homedir}/nginx/logs
%{homedir}/nginx/sbin
%{homedir}/nginx/sbin/nginx

%{homedir}/nginx/conf
%{homedir}/nginx/conf/fastcgi.conf.default
%{homedir}/nginx/conf/fastcgi_params.default
%{homedir}/nginx/conf/mime.types.default
%{homedir}/nginx/conf/nginx.conf.default
%{homedir}/nginx/conf/scgi_params.default
%{homedir}/nginx/conf/uwsgi_params.default

%config %{homedir}/nginx/conf/fastcgi.conf
%config %{homedir}/nginx/conf/fastcgi_params
%config %{homedir}/nginx/conf/koi-utf
%config %{homedir}/nginx/conf/koi-win
%config %{homedir}/nginx/conf/mime.types
%config %{homedir}/nginx/conf/nginx.conf
%config %{homedir}/nginx/conf/scgi_params
%config %{homedir}/nginx/conf/uwsgi_params
%config %{homedir}/nginx/conf/win-utf


%postun


%changelog


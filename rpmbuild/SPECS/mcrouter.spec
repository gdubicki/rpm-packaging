%define debug_package %{nil}

%define _prefix /local

#%define git_commit 26f3209d47791aed2aecb510efd8dbbed806fceb
#%define shortcommit %(c=%{commit}; echo ${c:0:7})
%define version_major 0
%define version_minor 19
%define version_revision 0

Name:		mcrouter
Version:	%{version_major}.%{version_minor}.%{version_revision}
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/facebook/mcrouter
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        https://github.com/facebook/%{name}/archive/release-%{version_minor}-%{version_revision}/tar.gz/%{name}-%{version}.tar.gz
#Patch0:        mcrouter-%{commit}-rebase-to-slash-tmp.patch
Summary:	Memcached protocol router for scaling memcached deployments
Group:		System Environment/Daemons

Requires:	gflags glog folly

BuildRequires:  libstdc++-devel autoconf automake libtool pkgconfig m4
BuildRequires:	libcap-devel openssl-devel libevent-devel python-devel
BuildRequires:	boost-devel gflags-devel glog-devel folly-devel double-conversion-devel ragel
BuildRequires:	jemalloc-devel snappy-devel xz-devel lz4-devel 
BuildRequires:	fbthrift-python fbthrift-devel

%if 0%{?rhel} <= 6
BuildRequires:	devtoolset-2-toolchain
%else
BuildRequires:	glibc-devel gcc gcc-c++
%endif


%description
Mcrouter is a memcached protocol router for scaling memcached (http://memcached.org/) deployments.
It's a core component of cache infrastructure at Facebook and Instagram where mcrouter handles almost 5 billion requests per second at peak.

%prep
%if 0%{?rhel} <= 6
source /opt/rh/devtoolset-2/enable
%endif
%setup -q -n %{name}-release-%{version_minor}-%{version_revision}
#%setup -q
#%patch0 -p1

%build
%if 0%{?rhel} <= 6
source /opt/rh/devtoolset-2/enable
%endif
cd %{name} 
autoreconf -if
%configure THRIFT2_COMP_DIR=/usr/lib64/python2.7/site-packages/thrift_compiler/
#%{__make} %{?_smp_mflags}
make

%install
make -C %{name} install DESTDIR=$RPM_BUILD_ROOT
install -d -m 0755 %{buildroot}%{_localstatedir}/%{name}
install -d -m 0755 %{buildroot}%{_localstatedir}/spool/%{name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%{_bindir}/mcrouter
%{_bindir}/mcpiper
%dir %{_localstatedir}/%{name}
%dir %{_localstatedir}/spool/%{name}
%dir %{_sysconfdir}/%{name}

%changelog
* Tue Feb 23 2016 Samveen <samveen@yahoo.com> 0.19.0
- Bump to 0.19.0

* Fri Jan 08 2016 Samveen <samveen@yahoo.com> - 0.16.0
- Bump to 0.16.0

* Fri Dec 04 2015 Samveen <samveen@yahoo.com> - 0.14.0
- Bump to 0.14.0

* Wed Jul 08 2015 Samveen <samveen@yahoo.com> - 0.2.0
- Change to version 0.2.0 to follow facebook release scheme

* Wed Mar 04 2015 Samveen <samveen@yahoo.com> - 20150304
- Fix spec file to better match other spec files

* Sun Feb 1 2015 Kenichi Otsuka <shivaken@gmail.com> - 1.0.0
- initial package

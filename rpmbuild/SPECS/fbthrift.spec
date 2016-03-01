%define debug_package %{nil}

%global commit 1cec9f96f8b897bb89be1b4d9637db3d97541579
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global version_hack 2

Summary:        FBThrift: Facebook's branch of apache thrift
Name:           fbthrift
%if 0%{?commit:1} 
Version:        0.31.%{version_hack}.%{shortcommit}
%else
Version:        0.31.0
%endif
Release:        1%{?dist}
License:        APLv2.0
Group:          Development/Languages
URL:            https://github.com/facebook/fbthrift
%if 0%{?commit:1} 
Source0:        https://github.com/facebook/%{name}/archive/%{commit}/tar.gz/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/facebook/%{name}/archive/v%{version}/tar.gz/%{name}-%{version}.tar.gz
%endif
#Patch1:         fbthrift-0.31.0-compilefixes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libstdc++-devel autoconf automake libtool pkgconfig m4
BuildRequires:  bison flex python-devel
BuildRequires:  glog-devel gflags-devel snappy-devel double-conversion-devel
BuildRequires:  folly-devel python-devel openssl-devel
# BuildRequires:  wangle
BuildRequires:  krb5-devel cyrus-sasl-devel numactl-devel
BuildRequires:  jemalloc-devel lz4-devel xz-devel

#BuildRequires: pkgconfig  autoconf automake libtool
#BuildRequires: boost-devel libevent-devel
#BuildRequires:  scons 
#BuildRequires: autoconf-archive
#BuildRequires:  binutils
#BuildRequires: 
Requires: %{name}-libs = %{version}

%description
The main focus of this package is the new C++ server, under thrift/lib/cpp2.
This repo also contains a branch of the rest of apache thrift's repo with
any changes Facebook has made, however the build system only supports cpp2.

%package devel
Summary: Header files and static libraries for fbthrift
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Development files for fbthrift

%package libs
Summary: fbthrift libraries
Group: Development/Libraries

%description libs
fbthrift libraries

%package python
Summary: fbthrift python support
Group: Development/Languages
Requires: %{name} = %{version}

%description python
fbthrift python support

%prep
%if 0%{?commit:1} 
%setup -c -n %{name}-%{version}
mv %{name}-%{commit}/* %{name}-%{commit}/.* . || :
rmdir %{name}-%{commit}
%else
%setup -q
%endif
#%patch1 -p1 -b .compilefixes
cd thrift/compiler
ln -s thrifty.h thrifty.hh

%build
#. /etc/profile.d/modules.sh
#module load rh autoconf boost python bison
cd thrift
autoreconf -if
%configure --without-cpp
# --with-boost=$BOOSTHOME --with-boost-libdir=$BOOSTHOME/%{_lib}
%{__make} %{?_smp_mflags}


%install
#. /etc/profile.d/modules.sh
#module load rh autoconf boost python bison
cd thrift
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}" PY_INSTALL_HOME=/tmp PY_LOCAL_ROOT=/tmp PY_INSTALL_ARGS='--skip-build --root=%{buildroot}'
rm -f %{buildroot}%{_libdir}/lib*.la
%if "%{_lib}" != "lib"
mkdir -p %{buildroot}%{_libdir}/python2.7
mv %{buildroot}/usr/lib/python2.7/* %{buildroot}%{_libdir}/python2.7
%endif

%clean
%{__rm} -rf %{buildroot}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc CONTRIBUTING.md LICENSE README.md
%{_bindir}/thrift1

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/thrift
#%{_libdir}/pkgconfig/thrift*pc
%{_libdir}/lib*.a

%files libs
%defattr(-, root, root, 0755)
%doc CONTRIBUTING.md LICENSE README.md
%{_libdir}/lib*.so
#%{_libdir}/lib*.so.*

%files python
%defattr(-, root, root, 0755)
%{python_sitearch}/thrift*

%changelog
* Tue Feb 23 2016 Samveen <samveen@yahoo.com> 0.31.2
- Bump to 0.31.2 for Mcrouter-v0.19.0

* Tue Jan 19 2016 Samveen <samveen@yahoo.com> 0.31.0
- Initial RPM release.

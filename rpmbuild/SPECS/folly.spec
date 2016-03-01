
%global commit bb5ed8070d533c016e1e93cd274e76ce28a780bb
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# Increment if commit hash decreases and release version remains the same eg. from 5d820ea6512b730ec44696bb1a98d689f0b1c302 to 3f93d7830a8cf7a3edfe13f87812b2d41825f70b
# reset to 1 if release version is incremented
%global version_hack 7

# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Library of C++11 components designed with practicality and efficiency in mind
Name:		folly
%if 0%{?commit:1} 
Version:	0.57.%{version_hack}.%{shortcommit}
%else
Version:	0.57.0
%endif
%global         libver %(echo %{version}|cut -f2 -d.)
Release:	1%{?dist}
License:	Apache v2.0
Group:		Libraries
# Source0:        https://github.com/facebook/folly/archive/v0.48.0/tar.gz/folly-0.48.0.tar.gz
%if 0%{?commit:1} 
Source0:        https://github.com/facebook/%{name}/archive/%{commit}/tar.gz/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/facebook/%{name}/archive/v%{version}/tar.gz/%{name}-%{version}.tar.gz
%endif
URL:		https://github.com/facebook/%{name}
BuildRequires:	boost-devel >= 1.20.0
BuildRequires:	double-conversion-devel
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
BuildRequires:	openssl-devel libevent-devel
BuildRequires:	jemalloc-devel snappy-devel xz-devel lz4-devel
#BuildRequires:	gtest-devel >= 1.6.0
BuildRequires:	libstdc++-devel autoconf automake libtool pkgconfig
%if 0%{?rhel} <= 6
BuildRequires:    devtoolset-2-toolchain
%else
BuildRequires:    python
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Folly (acronymed loosely after Facebook Open Source Library) is a
library of C++11 components designed with practicality and efficiency
in mind. It complements (as opposed to competing against) offerings
such as Boost and of course std. In fact, we embark on defining our
own component only when something we need is either not available, or
does not meet the needed performance profile.

Performance concerns permeate much of Folly, sometimes leading to
designs that are more idiosyncratic than they would otherwise be (see
e.g. PackedSyncPtr.h, SmallLocks.h). Good performance at large scale
is a unifying theme in all of Folly.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.20.0
Requires:	double-conversion-devel gflags-devel glog-devel
Requires:	libevent-devel

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%if 0%{?rhel} <= 6
source /opt/rh/devtoolset-2/enable
%endif
%if 0%{?commit:1} 
%setup -c -n %{name}-%{version}
mv %{name}-%{commit}/* %{name}-%{commit}/.* . || :
rmdir %{name}-%{commit}
%else
%setup -q
%endif

%build
%if 0%{?rhel} <= 6
source /opt/rh/devtoolset-2/enable
%endif
cd folly

autoreconf -if
CPPFLAGS="%{rpmcppflags}"
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C folly install \
	DESTDIR=$RPM_BUILD_ROOT

# these aren't supposed to be installed!
rm $RPM_BUILD_ROOT%{_libdir}/libgtest* || true

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_libdir}/libfolly.so.*.*.*
%attr(755,root,root) %{_libdir}/libfolly.so.%{libver}
%attr(755,root,root) %{_libdir}/libfollybenchmark.so.*.*.*
%attr(755,root,root) %{_libdir}/libfollybenchmark.so.%{libver}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libfolly.so
%{_libdir}/libfollybenchmark.so
%{_libdir}/libfolly.la
%{_libdir}/libfollybenchmark.la
%{_includedir}/folly

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfolly.a
%{_libdir}/libfollybenchmark.a
%endif

%changelog
* Tue Feb 23 2016 Samveen <samveen@yahoo.com> - 0.57.0
- Bump to 0.57.7 for Mcrouter-v0.19.0

* Fri Dec 04 2015 Samveen <samveen@yahoo.com> - 0.57.0
- Bump to 0.57.0

* Tue Jul 07 2015 Samveen <samveen@yahoo.com> - 0.48.0
- Improve spec file
- Update to 0.48.0

* Wed Mar 04 2015 Samveen <samveen@yahoo.com>
- Fix spec file to better match other spec files
- Update for 0.22.0

* Sun Oct 06 2013  Elan Ruusamäe <glensc@github.com>
- Initial checkin

Name:           ragel   
Summary:        Finite state machine compiler
Version:        6.9
Release:        1%{?dist}
Group:          Development/Tools
License:        GPLv2+
URL:            http://www.colm.net/open-source/%{name}
Source0:        http://www.colm.net/files/ragel/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc, gcc-c++, libstdc++-devel
# for documentation building
#BuildRequires:  transfig, tetex-latex, gcc-objc
Requires:       gawk

%description
Ragel compiles finite state machines from regular languages into executable C,
C++, Objective-C, or D code. Ragel state machines can not only recognize byte
sequences as regular expression machines do, but can also execute code at
arbitrary points in the recognition of a regular language. Code embedding is
done using inline operators that do not disrupt the regular language syntax.

%prep
%setup -q


%build
# set the names of the other programming commandline programs
%configure

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -fR %{buildroot}%{_datadir}/doc


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING ragel.vim CREDITS ChangeLog
#%doc doc/ragel-guide.pdf
%{_bindir}/%{name}
%{_mandir}/*/*

%changelog
* Thu Aug 20 2015 Samveen <samveen@yahoo.com>
- Change release tag to contain dist tag

* Mon Mar 02 2015 Samveen <samveen@yahoo.com>
- Ragel 6.9
- Remove pdf docs and dependencies

* Wed Jan 12 2011 Holger Manthey <holger.manthey@bertelsmann.de>
- initial packet

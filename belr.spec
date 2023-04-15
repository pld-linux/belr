#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Belledonne Communications' language recognition library
Summary(pl.UTF-8):	Biblioteka rozpoznawania języków Belledonne Communications
Name:		belr
Version:	5.2.51
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/belr/-/tags
Source0:	https://gitlab.linphone.org/BC/public/belr/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	053d6cd98345c7a6c80ca4c67f71883e
Patch0:		%{name}-static.patch
URL:		https://linphone.org/
BuildRequires:	bctoolbox-devel >= 0.0.5
BuildRequires:	cmake >= 3.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	udev-devel
Requires:	bctoolbox >= 0.0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Belr is Belledonne Communications' language recognition library. It
aims at parsing any input formatted according to a language defined by
an ABNF grammar, such as the protocols standardized at IETF.

It is based on finite state machine theory and heavily relies on
recursivity from an implementation standpoint.

%description -l pl.UTF-8
Belr to biblioteka do rozpoznawania języków Belledonne Communications.
Jej celem jest analiza dowolnego wejścia sformatowanego zgodnie z
językiem zdefiniowanym przez gramatykę ABNF, np. protokołów
standaryzowanych przez IETF.

Biblioteka jest oparta na teorii automatów skończonych, implementacja
znacząco wykorzystuje rekusywność.

%package devel
Summary:	Header files for belr library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki belr
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bctoolbox-devel >= 0.0.5
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for belr library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki belr.

%package static
Summary:	Static belr library
Summary(pl.UTF-8):	Statyczna biblioteka belr
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static belr library.

%description static -l pl.UTF-8
Statyczna biblioteka belr.

%prep
%setup -q
%patch0 -p1

%build
install -d builddir
cd builddir
# cmake build relies on relative CMAKE_INSTALL_DATADIR
%cmake .. \
	-DCMAKE_INSTALL_DATADIR=share \
	%{!?with_static_libs:-DENABLE_STATIC=OFF} \
	-DENABLE_TESTS=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# dir for grammars (see CMakeLists.txt)
install -d $RPM_BUILD_ROOT%{_datadir}/belr/grammars

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_libdir}/cmake/belr/belrTargets.cmake

# missing from cmake
test ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/belr.pc
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -e 's,@CMAKE_INSTALL_PREFIX@,%{_prefix},' \
	-e 's,@PROJECT_NAME@,belr,' \
	-e 's,@PROJECT_VERSION@,%{version},' \
	-e 's,@CMAKE_INSTALL_FULL_LIBDIR@,%{_libdir},' \
	-e 's,@LIBS_PRIVATE@,-lbctoolbox,' \
	-e 's,@CMAKE_INSTALL_FULL_INCLUDEDIR@,%{_includedir},' \
	belr.pc.in >$RPM_BUILD_ROOT%{_pkgconfigdir}/belr.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/belr-compiler
%attr(755,root,root) %{_bindir}/belr-parse
%attr(755,root,root) %{_libdir}/libbelr.so.1
%dir %{_datadir}/belr
%dir %{_datadir}/belr/grammars

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbelr.so
%{_includedir}/belr
%{_pkgconfigdir}/belr.pc
%{_libdir}/cmake/belr

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbelr.a
%endif

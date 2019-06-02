#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Belledonne Communications' language recognition library
Summary(pl.UTF-8):	Biblioteka rozpoznawania języków Belledonne Communications
Name:		belr
Version:	0.1.3
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://linphone.org/releases/sources/belr/%{name}-%{version}.tar.gz
# Source0-md5:	91dc921d48db2b8337bab56996fe8800
Patch0:		%{name}-pc.patch
URL:		https://linphone.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	bctoolbox-devel >= 0.0.3
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
Requires:	bctoolbox >= 0.0.3
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
%setup -q -n %{name}-%{version}-0
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbelr.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/belr-parse
%attr(755,root,root) %{_libdir}/libbelr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbelr.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbelr.so
%{_includedir}/belr
%{_pkgconfigdir}/belr.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbelr.a
%endif

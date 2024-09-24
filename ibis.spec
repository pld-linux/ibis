#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Ibis IRCv3 parsing library
Summary(pl.UTF-8):	Biblioteka Ibis do analizy protokołu IRCv3
Name:		ibis
Version:	0.8.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/pidgin/%{name}-%{version}.tar.xz
# Source0-md5:	bad64d9fa6a2da289481eb6a2613a774
URL:		https://keep.imfreedom.org/ibis/ibis/
BuildRequires:	birb-devel
# C17
BuildRequires:	gcc >= 6:7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2023.1}
BuildRequires:	glib2-devel >= 1:2.76.0
BuildRequires:	hasl-devel
BuildRequires:	meson >= 1.0.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.70
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GObject based IRCv3 library.

%description -l pl.UTF-8
Oparta na bibliotece GObject biblioteka do protokołu IRCv3.

%package devel
Summary:	Header files for ibis library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ibis
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	birb-devel
Requires:	glib2-devel >= 1:2.76.0
Requires:	hasl-devel

%description devel
Header files for ibis library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ibis.

%package static
Summary:	Static ibis library
Summary(pl.UTF-8):	Statyczna biblioteka ibis
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ibis library.

%description static -l pl.UTF-8
Statyczna biblioteka ibis.

%package apidocs
Summary:	API documentation for ibis library
Summary(pl.UTF-8):	Dokumentacja API biblioteki ibis
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for ibis library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ibis.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Ddocs=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/ibis $RPM_BUILD_ROOT%{_gidocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) %{_libdir}/libibis.so
%{_libdir}/girepository-1.0/Ibis-1.0.typelib

%files devel
%defattr(644,root,root,755)
%{_includedir}/ibis-1.0
%{_datadir}/gir-1.0/Ibis-1.0.gir
%{_pkgconfigdir}/ibis.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libibis.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/ibis
%endif

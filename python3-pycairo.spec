Summary:	Python 3.x Cairo bindings
Summary(pl.UTF-8):	Dowiązania Pythona 3.x dla Cairo
Name:		python3-pycairo
Version:	1.8.10
Release:	1
License:	LGPL v3
Group:		Libraries
Source0:	http://cairographics.org/releases/pycairo-%{version}.tar.bz2
# Source0-md5:	ddc544943d791e3c22ca8f019e10e1e3
URL:		http://cairographics.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9.6
BuildRequires:	cairo-devel >= 1.8.10
BuildRequires:	libtool >= 2:1.4
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 3.1
BuildRequires:	python3-devel >= 3.1
# for tests only
#BuildRequires:	python-numpy
# not release yet
#BuildRequires:	python-xpyb >= 1.3
BuildRequires:	rpm-pythonprov
Requires:	cairo >= 1.8.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 3.x Cairo bindings.

%description -l pl.UTF-8
Dowiązania Pythona 3.x dla Cairo.

%package devel
Summary:	Development files for pycairo
Summary(pl.UTF-8):	Pliki programistyczne pycairo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel >= 1.8.10

%description devel
Development files for pycairo.

%description devel -l pl.UTF-8
Pliki programistyczne pycairo.

%package examples
Summary:	Example programs using Python Cairo bindings
Summary(pl.UTF-8):	Przykładowe programy w Pythonie używające Cairo
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description examples
Example programs using Python Cairo bindings.

%description examples -l pl.UTF-8
Przykładowe programy w Pythonie używające Cairo.

%prep
%setup -q -n pycairo-%{version}

%build
CC="%{__cc}" \
CXX="%{__cxx}" \
CPP="%{__cpp}" \
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
PYTHONDIR="%{py3_sitedir}" \
python3 ./waf %{?_smp_mflags} configure \
	--prefix=%{_prefix}

#LIB="%{_lib}" \
python3 ./waf build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

python3 ./waf install \
	--destdir=$RPM_BUILD_ROOT

%if "%{_lib}" != "lib"
	install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
	mv $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
%endif

cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

#rm $RPM_BUILD_ROOT%{py3_sitedir}/cairo/*.{la,py}
%py3_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%dir %{py3_sitedir}/cairo
%attr(755,root,root) %{py3_sitedir}/cairo/_cairo.so
%{py3_sitedir}/cairo/__init__.py[co]

%files devel
%defattr(644,root,root,755)
%{_includedir}/pycairo
%{_pkgconfigdir}/py3cairo.pc

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

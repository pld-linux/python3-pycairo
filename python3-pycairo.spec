#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	pycairo
Summary:	Python 3 Cairo bindings
Summary(pl.UTF-8):	Dowiązania Pythona 3 dla Cairo
Name:		python3-%{module}
Version:	1.28.0
Release:	1
License:	LGPL v2.1 or MPL v1.1
Group:		Libraries/Python
#Source0Download: https://github.com/pygobject/pycairo/releases
Source0:	https://github.com/pygobject/pycairo/releases/download/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	f1bb0ee59ddd78a452f27ffda3ed68ae
URL:		https://www.cairographics.org/
BuildRequires:	cairo-devel >= 1.15.10
BuildRequires:	meson >= 0.64.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-devel >= 1:3.9
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-numpy
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.042
%if %{with doc}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-sphinx_rtd_theme
%endif
Requires:	python3-libs >= 1:3.9
Requires:	cairo >= 1.15.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 3 Cairo bindings.

%description -l pl.UTF-8
Dowiązania Pythona 3 dla Cairo.

%package devel
Summary:	Development files for Python 3 pycairo
Summary(pl.UTF-8):	Pliki programistyczne pycairo dla Pythona 3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel >= 1.15.10
Requires:	python3-devel >= 1:3.9

%description devel
Development files for Python 3 pycairo.

%description devel -l pl.UTF-8
Pliki programistyczne pycairo dla Pythona 3.

%package apidocs
Summary:	API documentation for Python Cairo bindings
Summary(pl.UTF-8):	Dokumentacja API dla wiązań Pythona do Cairo
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python Cairo bindings.

%description apidocs -l pl.UTF-8
Dokumentacja API dla wiązań Pythona do Cairo.

%package examples
Summary:	Example programs using Python Cairo bindings
Summary(pl.UTF-8):	Przykładowe programy w Pythonie używające Cairo
Group:		Libraries/Python
BuildArch:	noarch

%description examples
Example programs using Python Cairo bindings.

%description examples -l pl.UTF-8
Przykładowe programy w Pythonie używające Cairo.

%prep
%setup -q -n pycairo-%{version}

%build
%meson
%meson_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest build/tests
%endif

%if %{with doc}
%{__make} -C docs
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%meson_install

cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.rst
%dir %{py3_sitedir}/cairo
%attr(755,root,root) %{py3_sitedir}/cairo/_cairo.cpython-*.so
%{py3_sitedir}/cairo/__init__.py
%{py3_sitedir}/cairo/__init__.pyi
%{py3_sitedir}/cairo/__pycache__
%{py3_sitedir}/cairo/include
%{py3_sitedir}/cairo/py.typed
%{py3_sitedir}/pycairo-%{version}.dist-info

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/pycairo
%{_includedir}/pycairo/py3cairo.h
%{_pkgconfigdir}/py3cairo.pc

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/{_images,_static,reference,*.html,*.js}
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

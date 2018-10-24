#
# spec file for package diamond
#

Name:           diamond
Version:        master
Release:        1.0
Summary:        Daemon that collects and publishes system metrics
License:        MIT
Group:          System/Monitoring
Url:            https://github.com/python-diamond/Diamond
Source:         diamond-%{version}.tar.bz2
Source1:        diamond.service
Patch1:         diamond-master.patch1
BuildRequires:  python-devel python-configobj python-setuptools
Requires:       python-configobj python-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif
BuildArch:      noarch

%description
Diamond is a python daemon that collects system metrics and publishes them to
Graphite (and others). It is capable of collecting cpu, memory, network, i/o,
load and disk metrics. Additionally, it features an API for implementing
custom collectors for gathering metrics from almost any source.

%prep
%setup -q -n diamond-%{version}
#Check if we are running an older python and patch 
%{!?python_ver: %global python_ver %(python -c "import sys; print ('true' if sys.version_info >= (2,7) else 'false')")}
%if %{?python_ver} == "false"
%patch -P 1
%endif

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm -f %{buildroot}/etc/diamond/diamond.conf.example.windows
cp %{buildroot}/etc/diamond/diamond.conf.example %{buildroot}/etc/diamond/diamond.conf
mkdir -p ${RPM_BUILD_ROOT}/etc/init.d
install -m 0744 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/init.d/diamond
install -d -m 0755 %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}/etc/diamond/collectors
install -d -m 0755 %{buildroot}/etc/diamond/handlers
mkdir -p ${RPM_BUILD_ROOT}/var/log/diamond

%files
%defattr(-,root,root,-)
%doc CHANGELOG README.md LICENSE
%config /etc/diamond/diamond.conf
%config /etc/diamond/diamond.conf.example
%config /etc/init.d/diamond
%dir /etc/diamond
%dir /etc/diamond/collectors
%dir /etc/diamond/handlers
/usr/bin/diamond
/usr/bin/diamond-setup
%{python_sitelib}/*
%dir /usr/share/diamond
/usr/share/diamond/*
%dir /var/log/diamond

%changelog
* Sun Mar 20 2016 jfunk@funktronics.ca
- Initial release


%define version 1.2.1
#define snapshot 304
%define rel	1

# REV=$(svn info https://cdemu.svn.sourceforge.net/svnroot/cdemu/trunk/vhba-module| sed -ne 's/^Last Changed Rev: //p')
# svn export -r $REV https://cdemu.svn.sourceforge.net/svnroot/cdemu/trunk/vhba-module vhba-module-$REV
# tar -cjf vhba-module-$REV.tar.bz2 vhba-module-$REV

Summary:	Virtual SCSI HBA kernel module
%define module	vhba
%define oname	vhba-module
Name:		dkms-vhba
Version:	1.2.1
%if %snapshot
Release:	%mkrel 1.svn%snapshot.%rel
%else
Release:	%mkrel %rel
%endif
Group:		System/Kernel and hardware
License:	GPLv2+
URL:		http://cdemu.sourceforge.net/
%if %snapshot
Source:		%oname-%snapshot.tar.bz2
%else
Source:		http://downloads.sourceforge.net/cdemu/%oname-%version.tar.bz2
%endif
BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch
Requires:	dkms
Requires(post):	dkms
Requires(preun): dkms

%description
Virtual SCSI HBA kernel module. The vhba module is used by cdemu.

%prep
%if %snapshot
%setup -q -n %oname-%snapshot
%else
%setup -q -n %oname-%version
%endif

%install
rm -rf %buildroot

install -d -m755 %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}
cp -r * %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}

cat > %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME="%module"
PACKAGE_VERSION="%version-%release"
DEST_MODULE_LOCATION[0]="/kernel/%module"
BUILT_MODULE_NAME[0]="%module"
MAKE[0]="make KDIR=\${kernel_source_dir}"
AUTOINSTALL="yes"
EOF

%clean
rm -rf %{buildroot}

%post
dkms add     -m %{module} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms build   -m %{module} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms install -m %{module} -v %{version}-%{release} --rpm_safe_upgrade
true

%preun
dkms remove  -m %{module} -v %{version}-%{release} --all --rpm_safe_upgrade
true

%files
%defattr(-,root,root)
%{_usrsrc}/%{module}-%{version}-%{release}

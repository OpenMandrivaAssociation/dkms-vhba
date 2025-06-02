%define module vhba
%define oname vhba-module
# upstream release tarball is a snapshot-style one
%define snapshot 20130607

Summary:	Virtual SCSI HBA kernel module
Name:		dkms-vhba
# Sync version with cdemu because there's no version for module
Version:	20250329
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2+
Url:		https://cdemu.sourceforge.net/
Source0:	https://downloads.sourceforge.net/cdemu/%{oname}-%{version}.tar.xz
Source10:	%{name}.rpmlintrc

Requires:	dkms
Requires(post,preun):	dkms
BuildArch:	noarch

%description
Virtual SCSI HBA kernel module. The vhba module is used by cdemu.

%files
%{_usrsrc}/%{module}-%{version}-%{release}

%post
dkms add	-m %{module} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms build	-m %{module} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms install	-m %{module} -v %{version}-%{release} --rpm_safe_upgrade
true

%preun
dkms remove  -m %{module} -v %{version}-%{release} --all --rpm_safe_upgrade
true

#----------------------------------------------------------------------------

%prep
%autosetup -n %{oname}-%{version} -p1
rm -rf debian

%build

%install
install -d -m755 %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}
cp -r * %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}

cat > %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME="%{module}"
PACKAGE_VERSION="%{version}-%{release}"
DEST_MODULE_LOCATION[0]="/kernel/%{module}"
BUILT_MODULE_NAME[0]="%{module}"
MAKE[0]="make KDIR=\${kernel_source_dir}"
AUTOINSTALL="yes"
EOF
sed -i 's/-Werror//' %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}/Makefile



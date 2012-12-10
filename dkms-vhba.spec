
%define version 1.2.1
# upstream release tarball is a snapshot-style one
%define snapshot 20110915
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
Release:	%mkrel 4.%snapshot.%rel
%else
Release:	%mkrel %rel
%endif
Group:		System/Kernel and hardware
License:	GPLv2+
URL:		http://cdemu.sourceforge.net/
%if %snapshot
Source0:	http://downloads.sourceforge.net/cdemu/%oname-%snapshot.tar.bz2
%else
Source0:	http://downloads.sourceforge.net/cdemu/%oname-%version.tar.bz2
%endif
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

%build

%install
install -d -m755 %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}
cp -r kat  Makefile  vhba.c %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}

cat > %{buildroot}%{_usrsrc}/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME="%module"
PACKAGE_VERSION="%version-%release"
DEST_MODULE_LOCATION[0]="/kernel/%module"
BUILT_MODULE_NAME[0]="%module"
MAKE[0]="make KDIR=\${kernel_source_dir}"
AUTOINSTALL="yes"
EOF

%post
dkms add	-m %{module} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms build	-m %{module} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms install	-m %{module} -v %{version}-%{release} --rpm_safe_upgrade
true

%preun
dkms remove  -m %{module} -v %{version}-%{release} --all --rpm_safe_upgrade
true

%files
%defattr(-,root,root)
%doc AUTHORS  ChangeLog  COPYING README
%{_usrsrc}/%{module}-%{version}-%{release}


%changelog
* Fri Feb 24 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.2.1-4.20110915.1mdv2012.0
+ Revision: 780095
- new snapshot 20110915

* Sat Sep 04 2010 Anssi Hannula <anssi@mandriva.org> 1.2.1-4.20100822.1mdv2011.0
+ Revision: 575727
- new version 20100822
- drop patches for kernel compatibility, fixed upstream

* Mon Aug 16 2010 Pascal Terjan <pterjan@mandriva.org> 1.2.1-4mdv2011.0
+ Revision: 570620
- Add missing include (#60674)

* Sun Mar 21 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.2.1-3mdv2010.1
+ Revision: 525984
- P0 to let new kernels

* Sat Feb 28 2009 Anssi Hannula <anssi@mandriva.org> 1.2.1-2mdv2009.1
+ Revision: 345909
- rebuild due to missing packages

* Mon Jan 26 2009 Guillaume Bedot <littletux@mandriva.org> 1.2.1-1mdv2009.1
+ Revision: 333900
- Release 1.2.1

* Wed Apr 23 2008 Anssi Hannula <anssi@mandriva.org> 1.0.0-1.svn304.1mdv2009.0
+ Revision: 196900
- initial Mandriva release


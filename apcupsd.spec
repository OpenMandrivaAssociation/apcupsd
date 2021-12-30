%define _halpolicydir %{_datadir}/hal/fdi/policy/20thirdparty
%define	_cgibin /var/www/cgi-bin
%define	_sbindir /sbin

%global optflags %{optflags} -I%{_includedir}/libusb-1.0
%global LDFLAGS %{__global_ldflags} -lusb-1.0

Summary:	Power management software for APC UPS hardware
Name:		apcupsd
Version:	3.14.14
Release:	2
License:	GPLv2
Group:		System/Servers
URL:		https://sourceforge.net/projects/apcupsd/
Source0:	https://download.sourceforge.net/sourceforge/apcupsd/%{name}-%{version}.tar.gz
# (fedora)
Source1:	apcupsd.service
Source2:	apcupsd_shutdown
Source3:	apcupsd-httpd.conf
Source4:	apcupsd.logrotate

Patch0:		apcupsd-3.14.10-lockdir.patch
Patch1:		apcupsd-3.14.14_fix-build.patch
# (fedora)
Patch2:		apcupsd-3.14.4-shutdown.patch

BuildRequires:	glibc-devel
BuildRequires:	net-snmp-devel
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gdlib)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	nail
BuildRequires:	tcp_wrappers-devel
BuildRequires:	systemd
# docs
BuildRequires:	python3dist(docutils)

Requires(post): rpm-helper
Requires(preun):rpm-helper

Requires:	nail
Requires:	tcp_wrappers
Requires:	util-linux
# cgi
Requires:	httpd

%description
UPS power management under Linux for APC Products. It allows your
computer/server to run during power problems for a specified length of time or
the life of the batteries in your BackUPS, BackUPS Pro, SmartUPS v/s, or
SmartUPS, and then properly executes a controlled shutdown during an extended
power failure.

%files
%license COPYING
%doc ChangeLog DISCLAIMER Developers ReleaseNotes examples doc/manual
%{_initrddir}/apcupsd
%dir %{_sysconfdir}/apcupsd
/lib/systemd/system/apcupsd.service
/lib/systemd/system-shutdown/apcupsd_shutdown
%config(noreplace) %{_sysconfdir}/apcupsd/*
%config(noreplace) %{_sysconfdir}/logrotate.d/apcupsd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/apcupsd.conf
%{_halpolicydir}/80-apcupsd-ups-policy.fdi
%{_sbindir}/apcaccess
%{_sbindir}/apctest
%{_sbindir}/apcupsd
%{_sbindir}/smtp
%{_cgibin}/multimon.cgi
%{_cgibin}/upsfstats.cgi
%{_cgibin}/upsimage.cgi
%{_cgibin}/upsstats.cgi
%{_mandir}/man8/*
%{_mandir}/man5/apcupsd.conf.5*

#----------------------------------------------------------------------------

%package gui
Summary:      GUI interface for apcupsd
Requires:     apcupsd = %{version}-%{release}

%description gui
UPS power management under Linux for APCC Products. It allows your
computer/server to run during power problems for a specified length of time or
the life of the batteries in your BackUPS, BackUPS Pro, SmartUPS v/s, or
SmartUPS, and then properly executes a controlled shutdown during an extended
power failure.

This package provides a GUI interface to the APC UPS monitoring daemon.

%files gui	
%{_bindir}/gapcmon
%{_datadir}/applications/*gapcmon.desktop
%{_datadir}/pixmaps/apcupsd.png
%{_datadir}/pixmaps/charging.png
%{_datadir}/pixmaps/gapc_prefs.png
%{_datadir}/pixmaps/onbatt.png
%{_datadir}/pixmaps/online.png
%{_datadir}/pixmaps/unplugged.png

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# fix attribs
find examples -type f | xargs chmod 644

%build
%configure \
	--sysconfdir=%{_sysconfdir}/apcupsd \
	--enable-apcsmart \
	--enable-cgi \
	--enable-dumb \
	--enable-gapcmon \
	--enable-master-slave \
	--enable-modbus \
	--enable-no-modbus-usb \
	--enable-net \
	--enable-pcnet \
	--enable-pthreads \
	--enable-snmp \
	--enable-test \
	--enable-usb \
	--with-cgi-bin=%{_cgibin} \
	--with-halpolicydir=%{_halpolicydir} \
	--with-libwrap \
	--with-lock-dir=/var/lock \
	--with-nisip=127.0.0.1 \
	--with-serial-dev= \
	--with-upscable=usb \
	--with-upstype=usb \
	%{nil}
%make_build V=

%install
install -d %{buildroot}%{_cgibin}

%make_install
install -m0755 platforms/apccontrol %{buildroot}%{_sysconfdir}/apcupsd/
install -m0644 platforms/etc/apcupsd.conf %{buildroot}%{_sysconfdir}/apcupsd/
install -m0755 platforms/mandrake/apcupsd %{buildroot}%{_initrddir}/

for src in changeme commfailure commok onbattery offbattery; do
	install -m0744 platforms/etc/$src %{buildroot}%{_sysconfdir}/apcupsd/$src
done

# systemd
install -p -D -m0644 %SOURCE1 %buildroot/lib/systemd/system/apcupsd.service
install -p -D -m0755 %SOURCE2 %buildroot/lib/systemd/system-shutdown/apcupsd_shutdown

# cgi
install -p -D -m0644 %SOURCE3 %buildroot/%{_sysconfdir}/httpd/conf.d/apcupsd.conf

# logrotate
install -p -D -m0644 %SOURCE4 %buildroot/%{_sysconfdir}/logrotate.d/apcupsd

# cleanup
pushd doc/manual
	rm -f *.rst publishdoc Makefile
popd

%post
%systemd_post apcupsd.service
	
%preun
%systemd_preun apcupsd.service

%postun
%systemd_postun_with_restart apcupsd.service

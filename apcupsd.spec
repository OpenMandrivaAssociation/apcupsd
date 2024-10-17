# A change in RPM 4.15 causes the make_build macro to misbuild this package.
# See https://github.com/rpm-software-management/rpm/issues/798
%global _make_verbose %nil

Name:       apcupsd
Version:    3.14.14
Release:    5
Summary:    APC UPS Power Control Daemon

# Automatically converted from old format: GPLv2 - review is highly recommended.
License:    GPL-2.0-only
URL:        https://www.apcupsd.com
Source0:    https://downloads.sourceforge.net/apcupsd/apcupsd-%version.tar.gz
Source1:    apcupsd.service
Source2:    apcupsd_shutdown
Source3:    apcupsd-httpd.conf
Source4:    apcupsd.logrotate
Source5:    apcupsd64x64.png

# fix crash in gui, rhbz#578276
Patch0:       apcupsd-3.14.9-fixgui.patch
# Halt without powering off, rhbz#1442577
Patch1:       apcupsd-3.14.4-shutdown.patch
# Fix format-security error so we can enable the checks
Patch2:       patch-format-security

BuildRequires: net-snmp-devel
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: pkgconfig(gdlib)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gthread-2.0)
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(libusb-1.0)
BuildRequires: pkgconfig(ncurses)
BuildRequires: nail
BuildRequires: tcp_wrappers-devel
BuildRequires: systemd
# docs
BuildRequires: python3dist(docutils)

%description
Apcupsd can be used for controlling most APC UPSes. During a
power failure, apcupsd will inform the users about the power
failure and that a shutdown may occur.  If power is not restored,
a system shutdown will follow when the battery is exausted, a
timeout (seconds) expires, or the battery runtime expires based
on internal APC calculations determined by power consumption
rates.  If the power is restored before one of the above shutdown
conditions is met, apcupsd will inform users about this fact.
Some features depend on what UPS model you have (simple or smart).


%package cgi
Summary:      Web interface for apcupsd
Requires:     %{name} = %{EVRD}

%description cgi
A CGI interface to the APC UPS monitoring daemon.


%package gui
Summary:      GUI interface for apcupsd
Requires:     %{name} = %{EVRD}

%description gui
A GUI interface to the APC UPS monitoring daemon.

%prep
%autosetup -p1

# Override the provided platform makefile
printf 'install:\n\techo skipped\n' > platforms/redhat/Makefile

%build
%configure \
        --sysconfdir="%{_sysconfdir}/apcupsd" \
        --with-cgi-bin="/srv/www/apcupsd" \
        --sbindir=%{_bindir} \
        --enable-cgi \
        --enable-pthreads \
        --enable-net \
        --enable-apcsmart \
        --enable-dumb \
        --enable-net-snmp \
        --enable-snmp \
        --enable-usb \
        --enable-modbus-usb \
        --enable-gapcmon \
        --enable-pcnet \
        --with-serial-dev= \
        --with-upstype=usb \
        --with-upscable=usb \
        --with-lock-dir=%{_localstatedir}/lock \
        APCUPSD_MAIL=%{_bindir}/mail
%make_build

%install
mkdir -p %buildroot/srv/www/apcupsd
%make_install
install -m744 platforms/apccontrol \
              %buildroot%{_sysconfdir}/apcupsd/apccontrol

install -p -D -m0644 %SOURCE1 %buildroot%{_prefix}/lib/systemd/system/apcupsd.service
install -p -D -m0755 %SOURCE2 %buildroot%{_prefix}/lib/systemd/system-shutdown/apcupsd_shutdown
install -p -D -m0644 %SOURCE3 %buildroot%{_sysconfdir}/httpd/conf.d/apcupsd.conf
install -p -D -m0644 %SOURCE4 %buildroot%{_sysconfdir}/logrotate.d/apcupsd
install -p -D -m0644 %SOURCE5 %buildroot%{_datadir}/pixmaps/apcupsd64x64.png

desktop-file-install \
        --vendor="openmandriva" \
        --dir=%buildroot%{_datadir}/applications \
        --set-icon=apcupsd64x64 \
        --delete-original \
        %buildroot%{_datadir}/applications/gapcmon.desktop

# Cleanup for later %%doc processing
chmod -x examples/*.c
rm examples/*.in

# Drop old sysv bits
rm -rf %{buildroot}%{_sysconfdir}/rc.d

%files
%license COPYING
%doc ChangeLog examples ReleaseNotes
%dir %{_sysconfdir}/apcupsd
%{_prefix}/lib/systemd/system/apcupsd.service
%{_prefix}/lib/systemd/system-shutdown/apcupsd_shutdown
%config(noreplace) %{_sysconfdir}/apcupsd/apcupsd.conf
%attr(0755,root,root) %{_sysconfdir}/apcupsd/apccontrol
%config(noreplace) %{_sysconfdir}/apcupsd/changeme
%config(noreplace) %{_sysconfdir}/apcupsd/commfailure
%config(noreplace) %{_sysconfdir}/apcupsd/commok
%config(noreplace) %{_sysconfdir}/apcupsd/offbattery
%config(noreplace) %{_sysconfdir}/apcupsd/onbattery
%config(noreplace) %{_sysconfdir}/logrotate.d/apcupsd
%{_datadir}/hal/fdi/policy/20thirdparty/80-apcupsd-ups-policy.fdi
%{_bindir}/apc*
%{_bindir}/smtp
%{_mandir}/*/*

%files cgi
%config(noreplace) %{_sysconfdir}/apcupsd/apcupsd.css
%config(noreplace) %{_sysconfdir}/httpd/conf.d/apcupsd.conf
%config(noreplace) %{_sysconfdir}/apcupsd/hosts.conf
%config(noreplace) %{_sysconfdir}/apcupsd/multimon.conf
/srv/www/apcupsd/

%files gui
%{_bindir}/gapcmon
%{_datadir}/applications/*gapcmon.desktop
%{_datadir}/pixmaps/apcupsd.png
%{_datadir}/pixmaps/apcupsd64x64.png
%{_datadir}/pixmaps/charging.png
%{_datadir}/pixmaps/gapc_prefs.png
%{_datadir}/pixmaps/onbatt.png
%{_datadir}/pixmaps/online.png
%{_datadir}/pixmaps/unplugged.png

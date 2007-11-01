%define	name	apcupsd
%define	version	3.14.2
%define	release	%mkrel 1
%define	_cgibin /var/www/cgi-bin
%define	_sysconfdir /etc/apcupsd
%define	_sbindir /sbin

Summary:	Power management software for APC UPS hardware
Name:		%{name}
Version:	%{version}
Release:	%{release}

Source0:	http://mesh.dl.sourceforge.net/sourceforge/apcupsd/%{name}-%{version}.tar.bz2
Patch0:		%{name}-3.12.2-usbhiddev.patch
Patch1:		%{name}-3.10.16-staleusb.patch
License:	GPL
URL:		http://sourceforge.net/projects/apcupsd/
Group:		System/Servers
Requires:	initscripts >= 6.27-5mdk
Requires(post): rpm-helper
Requires(preun):rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ncurses-devel gd-devel

%description
UPS power management under Linux for APCC Products.
It allows your computer/server to run during power problems
for a specified length of time or the life of the batteries
in your BackUPS, BackUPS Pro, SmartUPS v/s, or SmartUPS, and
then properly executes a controlled shutdown during an
extended power failure.

%prep
%setup -q
%patch0 -p1 -b .usbhid
%patch1 -p1 -b .usbstale

%build
%serverbuild
%configure2_5x	--enable-usb \
		--enable-net \
		--enable-master-slave \
		--enable-powerflute \
		--enable-pthreads \
		--enable-cgi \
		--with-cgi-bin=%{_cgibin} \
		--enable-nls \
		--with-serial-dev= \
		--with-upstype=usb \
		--with-upscable=usb \
		--with-nisip=127.0.0.1

# %%make doesn't work
make


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d \
	 $RPM_BUILD_ROOT%{_cgibin}

#perl -pi -e 's|/etc|\$\$RPM_BUILD_ROOT/etc|g' platforms/mandrake/Makefile.in
perl -pi -e 's|\@/sbin/chkconfig|\#\@/sbin/chkconfig|' platforms/mandrake/Makefile.in

%makeinstall cgibin=$RPM_BUILD_ROOT%{_cgibin}
install -m 644 ./platforms/etc/apcupsd.conf $RPM_BUILD_ROOT/etc/apcupsd/
install -m 755 ./platforms/apccontrol $RPM_BUILD_ROOT/etc/apcupsd/
install -m 755 ./platforms/mandrake/apcupsd $RPM_BUILD_ROOT/etc/rc.d/init.d

for src in changeme commfailure commok \
        onbattery offbattery; do \
	install -m 744 ./platforms/etc/$src $RPM_BUILD_ROOT/etc/apcupsd/$src
done

%find_lang %{name}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
%_post_service apcupsd

%preun
%_preun_service apcupsd

%files -f %{name}.lang
%defattr(-,root,root)
%dir /etc/apcupsd
%config(noreplace) /etc/apcupsd/*
%config(noreplace) /etc/rc.d/init.d/apcupsd
%{_sbindir}/*
%{_mandir}/man8/*
%{_cgibin}/*
%doc ChangeLog doc/ examples/



%define _halpolicydir %{_datadir}/hal/fdi/policy/20thirdparty
%define	_cgibin /var/www/cgi-bin
%define	_sbindir /sbin

Summary:	Power management software for APC UPS hardware
Name:		apcupsd
Version:	3.14.8
Release:	%mkrel 3
License:	GPLv2
Group:		System/Servers
URL:		http://sourceforge.net/projects/apcupsd/
Source0:	http://mesh.dl.sourceforge.net/sourceforge/apcupsd/%{name}-%{version}.tar.gz
Patch0:		apcupsd-3.12.2-usbhiddev.patch
Patch1:		apcupsd-3.10.16-staleusb.patch
Patch2:		apcupsd-3.14.4-mdv_conf.diff
Patch3:		apcupsd-3.14.8-link.patch
Requires(post): rpm-helper
Requires(preun):rpm-helper
Requires:	tcp_wrappers
Requires:	nail
BuildRequires:	gd-devel
BuildRequires:	ncurses-devel
BuildRequires:	tcp_wrappers-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
UPS power management under Linux for APCC Products. It allows your
computer/server to run during power problems for a specified length of time or
the life of the batteries in your BackUPS, BackUPS Pro, SmartUPS v/s, or
SmartUPS, and then properly executes a controlled shutdown during an extended
power failure.

%prep

%setup -q
%patch0 -p0 -b .usbhid
%patch1 -p1 -b .usbstale
%patch2 -p0 -b .mdv_conf
%patch3 -p0 -b .link

# fix attribs
find examples -type f | xargs chmod 644

%build
%serverbuild

%configure2_5x \
    --sysconfdir=%{_sysconfdir}/apcupsd \
    --enable-usb \
    --enable-net \
    --enable-master-slave \
    --enable-pthreads \
    --enable-cgi \
    --with-cgi-bin=%{_cgibin} \
    --with-serial-dev= \
    --with-upstype=usb \
    --with-halpolicydir=%{_halpolicydir} \
    --with-upscable=usb \
    --with-nisip=127.0.0.1 \
    --with-libwrap

%make VERBOSE=1

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_cgibin}

#perl -pi -e 's|/etc|\$\%{buildroot}/etc|g' platforms/mandrake/Makefile.in
perl -pi -e 's|\@/sbin/chkconfig|\#\@/sbin/chkconfig|' platforms/mandrake/Makefile.in

%makeinstall_std
#cgibin=%{buildroot}%{_cgibin}

install -m0644 platforms/etc/apcupsd.conf %{buildroot}%{_sysconfdir}/apcupsd/
install -m0755 platforms/apccontrol %{buildroot}%{_sysconfdir}/apcupsd/
install -m0755 platforms/mandrake/apcupsd %{buildroot}%{_initrddir}/

for src in changeme commfailure commok onbattery offbattery; do
    install -m0744 platforms/etc/$src %{buildroot}%{_sysconfdir}/apcupsd/$src
done

%find_lang %{name}

# cleanup
pushd doc/manual
    rm -f *.rst publishdoc Makefile
popd

%post
%_post_service apcupsd

%preun
%_preun_service apcupsd

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog DISCLAIMER Developers ReleaseNotes examples doc/manual
%{_initrddir}/apcupsd
%dir %{_sysconfdir}/apcupsd
%config(noreplace) %{_sysconfdir}/apcupsd/*
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

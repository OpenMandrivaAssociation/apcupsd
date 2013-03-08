%define _halpolicydir %{_datadir}/hal/fdi/policy/20thirdparty
%define	_cgibin /var/www/cgi-bin
%define	_sbindir /sbin

Summary:	Power management software for APC UPS hardware
Name:		apcupsd
Version:	3.14.8
Release:	5
License:	GPLv2
Group:		System/Servers
Url:		http://sourceforge.net/projects/apcupsd/
Source0:	http://mesh.dl.sourceforge.net/sourceforge/apcupsd/%{name}-%{version}.tar.gz
Patch0:		apcupsd-3.12.2-usbhiddev.patch
Patch1:		apcupsd-3.10.16-staleusb.patch
Patch2:		apcupsd-3.14.4-mdv_conf.diff
Patch3:		apcupsd-3.14.8-link.patch

BuildRequires:	man
BuildRequires:	gd-devel
BuildRequires:	wrap-devel
BuildRequires:	pkgconfig(ncurses)
Requires(post,postun):	rpm-helper
Requires:	nail
Requires:	tcp_wrappers

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
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_cgibin}

sed -i -e 's|\@/sbin/chkconfig|\#\@/sbin/chkconfig|' \
	platforms/mandrake/Makefile.in

%makeinstall_std
#cgibin=%{buildroot}%{_cgibin}

install -m0644 platforms/etc/apcupsd.conf %{buildroot}%{_sysconfdir}/apcupsd/
install -m0755 platforms/apccontrol %{buildroot}%{_sysconfdir}/apcupsd/
install -m0755 platforms/mandrake/apcupsd %{buildroot}%{_initrddir}/

for src in changeme commfailure commok onbattery offbattery; do
    install -m0744 platforms/etc/$src %{buildroot}%{_sysconfdir}/apcupsd/$src
done

# cleanup
pushd doc/manual
    rm -f *.rst publishdoc Makefile
popd

%post
%_post_service apcupsd

%preun
%_preun_service apcupsd

%files
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


%changelog
* Tue May 03 2011 Funda Wang <fwang@mandriva.org> 3.14.8-3mdv2011.0
+ Revision: 663746
- fix linkage

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 3.14.8-2mdv2011.0
+ Revision: 603181
- rebuild

* Tue Jan 19 2010 Frederik Himpe <fhimpe@mandriva.org> 3.14.8-1mdv2010.1
+ Revision: 493775
- update to new version 3.14.8

* Tue Aug 04 2009 Frederik Himpe <fhimpe@mandriva.org> 3.14.7-1mdv2010.0
+ Revision: 409415
- update to new version 3.14.7

* Mon May 18 2009 Frederik Himpe <fhimpe@mandriva.org> 3.14.6-1mdv2010.0
+ Revision: 377285
- Update to new version 3.14.6
- Adapt SPEC file for new manual

* Wed Mar 11 2009 Oden Eriksson <oeriksson@mandriva.com> 3.14.5-1mdv2009.1
+ Revision: 353768
- 3.14.5

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 3.14.4-1mdv2009.1
+ Revision: 316478
- 3.14.4
- rediff patches, add patches, fix deps

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 3.14.2-3mdv2009.0
+ Revision: 220350
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Nov 17 2007 Funda Wang <fwang@mandriva.org> 3.14.2-2mdv2008.1
+ Revision: 109197
- rebuild for new lzma

* Thu Nov 01 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 3.14.2-1mdv2008.1
+ Revision: 104359
- Release 3.14.2.
- Release 3.14.1.


* Fri Feb 09 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 3.13.12-1mdv2007.0
+ Revision: 118664
- Import apcupsd

* Thu Feb 08 2007 Giuseppe Ghibò <ghibo@mandriva.com> 3.13.12-1mdkv2007.1
- Release 3.13.12.

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.12.3-2mdv2007.0
- Rebuild

* Wed Jul 26 2006 Emmanuel Andry <eandry@mandriva.org> 3.12.3-1mdv2007.0
- Release 3.12.3

* Tue Apr 04 2006 Giuseppe Ghibò <ghibo@mandriva.com> 3.12.2-1mdk
- Release 3.12.2.

* Fri Dec 23 2005 Giuseppe Ghibò <ghibo@mandriva.com> 3.10-18-5mdk
- added missed /etc/apcupsd/apccontrol.

* Sun Oct 16 2005 Giuseppe Ghibò <ghibo@mandriva.org> 3.10.18-4mdk
- added missed default config file (apcupsd.conf).

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 3.10.18-3mdk
- fix rpmlint errors (PreReq)

* Thu Aug 11 2005 Nicolas Lécureuil <neoclust@mandriva.org> 3.10.18-2mdk
- fix rpmlint errors (PreReq)

* Sun Jul 24 2005 Giuseppe Ghibò <ghibo@mandriva.com> 3.10.18-1mdk
- Release 3.10.18.
- Rebuilt Patch0.

* Thu Dec 30 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.10.16-2mdk
- Added Patch0 to fix USB default device under UDEV.
- Added Patch1 to support cleaning for usb stale lock files when
  default device is used.

* Tue Nov 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.10.16-1mdk
- 3.10.16.

* Mon Aug 09 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.10.15-1mdk
- Release 3.10.14.
- Dropped Patch0, merged upstream.

* Tue Aug 03 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.10.14-2mdk
- Added Patch0 to avoid segfault during EEPROM configuring.

* Tue Aug 03 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.10.14-1mdk
- Dropped Patch0, Patch1, merged upstream.
- Release 3.10.14.

* Fri Jul 30 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.10.13-3mdk
- fix problem with lock files (Giuseppe Ghibo)

* Thu Jul 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.10.13-2mdk
- fix build (P0 from Pascal Terjan)
- fix unowned dir
- cosmetics
- drop docs there's no need for
- add prereq on rpm-helper

* Sat May 22 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.10.13-1mdk
- 3.10.13.


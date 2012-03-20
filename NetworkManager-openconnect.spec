%define nm_version          1:0.9.2
%define dbus_version        1.1
%define gtk3_version        3.0.0
%define openconnect_version 3.00

%define snapshot %{nil}
%define realversion 0.9.3.997

Summary:   NetworkManager VPN integration for openconnect
Name:      NetworkManager-openconnect
Version:   0.9.3.997
Release:   1%{snapshot}%{?dist}
License:   GPLv2+, LGPLv2.1
Group:     System Environment/Base
URL:       http://www.gnome.org/projects/NetworkManager/
Source:    ftp://ftp.gnome.org/pub/GNOME/sources/NetworkManager-openconnect/0.9/%{name}-%{realversion}%{snapshot}.tar.bz2

BuildRequires: gtk3-devel             >= %{gtk3_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: dbus-glib-devel        >= 0.74
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: GConf2-devel
%if 0%{?fedora} > 16
BuildRequires: libgnome-keyring-devel
%else
BuildRequires: gnome-keyring-devel
%endif
BuildRequires: intltool gettext
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(openconnect) >= 3.11
BuildRequires: openconnect-devel

Requires: NetworkManager   >= %{nm_version}
Requires: openconnect      >= %{openconnect_version}

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(pre): %{_sbindir}/useradd
Requires(pre): %{_sbindir}/groupadd


%description
This package contains software for integrating the openconnect VPN software
with NetworkManager and the GNOME desktop

%prep
%setup -q -n NetworkManager-openconnect-%{realversion}

%build
autoreconf
%configure --enable-more-warnings=yes
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

%find_lang %{name}

%pre
%{_sbindir}/groupadd -r nm-openconnect &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d / -M \
                     -c 'NetworkManager user for OpenConnect' \
                     -g nm-openconnect nm-openconnect &>/dev/null || :

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-, root, root)

%doc AUTHORS ChangeLog COPYING
%{_libdir}/NetworkManager/lib*.so*
%{_sysconfdir}/dbus-1/system.d/nm-openconnect-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-openconnect-service.name
%{_libexecdir}/nm-openconnect-service
%{_libexecdir}/nm-openconnect-service-openconnect-helper
%{_libexecdir}/nm-openconnect-auth-dialog
%dir %{_datadir}/gnome-vpn-properties/openconnect
%{_datadir}/gnome-vpn-properties/openconnect/nm-openconnect-dialog.ui

%changelog
* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.997-1
- Update to 0.9.3.997 (0.9.4-rc1)

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.995-1
- Update to 0.9.3.995 (0.9.4-beta1)

* Sun Feb 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.2.0-3
- Update for unannounced gnome-keyring devel changes

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.0-1
- bump to 0.9.2.0
- pull david's patches properly from upstream

* Tue Nov 08 2011 David Woodhouse <David.Woodhouse@intel.com> - 0.9.0-5
- Deal with stupid premature glib API breakage.

* Tue Nov 08 2011 David Woodhouse <David.Woodhouse@intel.com> - 0.9.0-4
- Fix build failure due to including <glib/gtypes.h> directly.

* Tue Nov 08 2011 David Woodhouse <David.Woodhouse@intel.com> - 0.9.0-3
- Look for openconnect in /usr/sbin too

* Fri Aug 26 2011 Dan Williams <dcbw@redhat.com> - 0.9.0-1
- Update to 0.9.0
- ui: translation fixes

* Thu Aug 25 2011 David Woodhouse <David.Woodhouse@intel.com> - 0.8.999-3
- Rebuild again to really use shared library this time (#733431)

* Thu Jun 30 2011 David Woodhouse <David.Woodhouse@intel.com> - 0.8.999-2
- Link against shared libopenconnect.so instead of static library

* Tue May 03 2011 Dan Williams <dcbw@redhat.com> - 0.8.999-1
- Update to 0.8.999 (0.9-rc2)
- Updated translations
- Port to GTK+ 3.0

* Tue Apr 19 2011 David Woodhouse <dwmw2@infradead.org> - 0.8.1-9
- Fix handling of manually accepted certs and double-free of form answers

* Mon Apr 18 2011 David Woodhouse <dwmw2@infradead.org> - 0.8.1-8
- Update to *working* git snapshot

* Sat Mar 26 2011 Christopher Aillon <caillon@redhat.com> - 0.8.1-7
- Update to git snapshot

* Sat Mar 26 2011 Christopher Aillon <caillon@redhat.com> - 0.8.1-6
- Rebuild against NetworkManager 0.9

* Wed Mar 09 2011 David Woodhouse <dwmw2@infradead.org> 1:0.8.1-5
- BuildRequire openconnect-devel-static, although we don't. (rh #689043)

* Wed Mar 09 2011 David Woodhouse <dwmw2@infradead.org> 1:0.8.1-4
- BuildRequire libxml2-devel

* Wed Mar 09 2011 David Woodhouse <dwmw2@infradead.org> 1:0.8.1-3
- Rebuild with auth-dialog, no longer in openconnect package

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.1-1
- Update to 0.8.1 release
- Updated translations

* Sun Apr 11 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.0-1
- Add support for proxy and "key from fsid" settings
- Add flag to enable Cisco Secure Desktop checker program
- Updated translations

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.997-1
- Correctly handle PEM certificates without an ending newline (rh #507315)

* Mon Oct  5 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-4.git20090921
- Rebuild for updated NetworkManager

* Mon Sep 21 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-2
- Rebuild for updated NetworkManager

* Sun Aug 30 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-1
- Rebuild for updated NetworkManager
- Drop upstreamed patches

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0.99-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0.99-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  1 2009 David Woodhouse <David.Woodhouse@intel.com> 1:0.7.0.99-5
- Accept 'pem_passphrase_fsid' key in gconf

* Wed May 27 2009 David Woodhouse <David.Woodhouse@intel.com> 1:0.7.0.99-4
- Handle 'gwcert' as a VPN secret, because openconnect might not be able
  to read the user's cacert file when it runs as an unprivileged user.

* Sat May  9 2009 David Woodhouse <David.Woodhouse@intel.com> 1:0.7.0.99-3
- Accept 'form:*' keys in gconf
- Allow setting of MTU option in gconf

* Wed Apr  1 2009 David Woodhouse <David.Woodhouse@intel.com> 1:0.7.0.99-2
- Update translations from SVN
- Accept 'lasthost' and 'autoconnect' keys in gconf

* Thu Mar  5 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0.99-1
- Update to 0.7.1rc3

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Dan Williams <dcbw@redhat.com> 0.7.0.97-1
- Update to 0.7.1rc1

* Mon Jan  5 2009 David Woodhouse <David.woodhouse@intel.com> 0.7.0-4.svn14
- Rebuild for updated NetworkManager
- Update translations from GNOME SVN

* Sun Dec 21 2008 David Woodhouse <David.Woodhouse@intel.com> 0.7.0-3.svn9
- Update from GNOME SVN (translations, review feedback merged)

* Wed Dec 17 2008 David Woodhouse <David.Woodhouse@intel.com> 0.7.0-2.svn3
- Review feedback

* Tue Dec 16 2008 David Woodhouse <David.Woodhouse@intel.com> 0.7.0-1.svn3
- Change version numbering to match NetworkManager

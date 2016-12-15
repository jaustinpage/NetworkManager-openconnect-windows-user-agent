%global nm_version          1.2.0
%global gtk3_version        3.4.0
%global openconnect_version 7.00

Summary:   NetworkManager VPN plugin for openconnect
Name:      NetworkManager-openconnect
Version:   1.2.4
Release:   2%{?dist}
License:   GPLv2+ and LGPLv2
URL:       http://www.gnome.org/projects/NetworkManager/
Group:     System Environment/Base
Source:    https://download.gnome.org/sources/NetworkManager-openconnect/1.2/%{name}-%{version}.tar.xz
Patch1: 0001-Bug-770880-Revamp-certificate-warning-accept-dialog.patch
Patch2: 0002-Bug-770880-Disallow-manual-cert-acceptance.patch

BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(NetworkManager) >= %{nm_version}
BuildRequires: pkgconfig(libnm) >= %{nm_version}
BuildRequires: pkgconfig(libnm-util) >= %{nm_version}
BuildRequires: pkgconfig(libnm-glib) >= %{nm_version}
BuildRequires: pkgconfig(libnm-glib-vpn) >= %{nm_version}
BuildRequires: pkgconfig(libsecret-1)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: intltool gettext libtool
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(openconnect) >= %{openconnect_version}
BuildRequires: pkgconfig(gcr-3) >= 3.4

BuildRequires: automake autoconf libtool

Requires: NetworkManager   >= %{nm_version}
Requires: openconnect      >= %{openconnect_version}
Requires: dbus

Requires(pre): %{_sbindir}/useradd
Requires(pre): %{_sbindir}/groupadd


%description
This package contains software for integrating the openconnect VPN software
with NetworkManager and the GNOME desktop

%package gnome
Summary: NetworkManager VPN plugin for OpenConnect - GNOME files
Group:   System Environment/Base

Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: NetworkManager-openconnect < 1.2.3-0

%description gnome
This package contains software for integrating VPN capabilities with
the OpenConnect client with NetworkManager (GNOME files).

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
autoreconf -f -i
%configure \
        --enable-more-warnings=yes \
        --disable-static \
        --with-dist-version=%{version}-%{release}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%pre
%{_sbindir}/groupadd -r nm-openconnect &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d / -M \
                     -c 'NetworkManager user for OpenConnect' \
                     -g nm-openconnect nm-openconnect &>/dev/null || :

%post
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%{_libdir}/NetworkManager/libnm-vpn-plugin-openconnect.so
%{_sysconfdir}/dbus-1/system.d/nm-openconnect-service.conf
%{_prefix}/lib/NetworkManager/VPN/nm-openconnect-service.name
%{_libexecdir}/nm-openconnect-service
%{_libexecdir}/nm-openconnect-service-openconnect-helper
%doc AUTHORS ChangeLog NEWS
%license COPYING

%files gnome
%{_libexecdir}/nm-openconnect-auth-dialog
%{_libdir}/NetworkManager/libnm-*-properties.so
%{_libdir}/NetworkManager/libnm-vpn-plugin-openconnect-editor.so
%dir %{_datadir}/gnome-vpn-properties/openconnect
%{_datadir}/gnome-vpn-properties/openconnect/nm-openconnect-dialog.ui
%{_sysconfdir}/NetworkManager/VPN/nm-openconnect-service.name
%{_datadir}/appdata/network-manager-openconnect.metainfo.xml


%changelog
* Thu Dec 15 2016 David Woodhouse <dwmw2@infradead.org> - 1.2.4-2
- Improve certificate acceptance dialog and allow it to be disabled (bgo#770800)

* Mon Dec 05 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.4-1
- Update to 1.2.4
- Fix IPv6-only operation
- Automatically submit forms with remembered values

* Fri Sep 23 2016 David Woodhouse <dwmw2@infradead.org> - 1.2.3-0.20160923gitac5cdf
- Update to a newer 1.2.3 prerelease
- Allow protocol selection through UI
- Add Yubikey OATH support

* Wed Jul 06 2016 David Woodhouse <dwmw2@infradead.org> - 1.2.3-0.20160606git5009f9
- Update to 1.2.3 prerelease
- Split GNOME support into separate package (#1088672)
- Add Juniper support (#1340495)

* Wed May 11 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.2-1
- Update to 1.2.2 release

* Wed Apr 20 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-1
- Update to 1.2.0 release

* Tue Apr  5 2016 Lubomir Rintel <lkundrak@v3.sk> - 1:1.2.0-0.3.rc1
- Update to NetworkManager-openconnect 1.2-rc1

* Tue Mar 29 2016 Lubomir Rintel <lkundrak@v3.sk> - 1:1.2.0-0.3.beta3
- Update to NetworkManager-openconnect 1.2-beta3

* Tue Mar  1 2016 Lubomir Rintel <lkundrak@v3.sk> - 1:1.2.0-0.3.beta2
- Update to NetworkManager-openconnect 1.2-beta2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.3.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Lubomir Rintel <lkundrak@v3.sk> - 1:1.2.0-0.2.beta1
- Update to NetworkManager-openconnect 1.2-beta1

* Fri Oct 23 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-0.1.20151023gitbf9b033
- Update to 1.2 git snapshot with multiple vpn connections support

* Mon Aug 31 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-0.1.20150831git8e20043
- Update to 1.2 git snapshot with libnm-based properties plugin

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.2-1
- Update to 1.0.2 release

* Mon Dec 22 2014 Dan Williams <dcbw@redhat.com> - 1.0.0-1
- Update to 1.0

* Tue Dec 02 2014 David Woodhouse <David.Woodhouse@intel.com> - 0.9.8.6-2
- Actually remember to add the patch

* Tue Dec 02 2014 David Woodhouse <David.Woodhouse@intel.com> - 0.9.8.6-1
- Update to 0.9.8.6 + later patches for libopenconnect5 support

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Adam Williamson <awilliam@redhat.com> - 0.9.8.4-2
- rebuilt for new openconnect

* Wed Mar 05 2014 David Woodouse <David.Woodhouse@intel.com> - 0.9.8.4-1
- Update to 0.9.8.4 + later patches for libopenconnect3 support

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 David Woodouse <David.Woodhouse@intel.com> - 0.9.8.0-1
- Update to 0.9.8.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7.0-2.git20120918
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 18 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-1.git20120918
- Update to new snapshot to get IPv6 support (#829010)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.0-8.git20120612
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.9.4-7
- Add missing patch to git

* Sat Jun 16 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.9.4-6
- Add gnome-keyring support for saving passwords (bgo #638861)

* Wed Jun 13 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.9.4-5
- Update to work with new libopenconnect

* Wed Jun 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.9.4.0-4
- Remove unnecessary ldconfig calls from scriptlets (#737330).

* Fri May 25 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.9.4-3
- Fix cancel-after-failure-causes-next-attempt-to-immediately-abort bug.

* Thu May 17 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.9.4-2
- BR an appropriate version of openconnect, to ensure cancellation support.

* Thu May 17 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.9.4-1
- Update to 0.9.4.0 and some later patches:
- Properly cancel connect requests instead of waiting (perhaps forever).
- Wait for QUIT before exiting (bgo #674991).
- Create persistent tundev on demand for each connection.
- Check for success when dropping privileges.

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

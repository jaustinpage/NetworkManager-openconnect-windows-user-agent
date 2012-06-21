%define nm_version          1:0.7.0
%define dbus_version        1.1
%define gtk2_version        2.10.0
%define openconnect_version 0.99

%define snapshot %{nil}
%define realversion 0.8.6.0

Summary:   NetworkManager VPN integration for openconnect
Name:      NetworkManager-openconnect
Version:   0.8.6.0
Release:   1%{snapshot}%{?dist}
License:   GPLv2+
Group:     System Environment/Base
URL:       http://www.gnome.org/projects/NetworkManager/
Source:    %{name}-%{realversion}%{snapshot}.tar.bz2
# Patches from upstream git NM_0_8 branch:
Patch1: build-against-libopenconnect2.patch
# Other patches to make it build in RHEL5:
Patch2: 0001-Build-against-NetworkManager-0.8.1-again.patch
Patch3: 0002-Revert-to-glade.patch
Patch4: 0003-Revert-trivial-fix-for-NM-0.8.1.999-0.8.2-rc1.patch
Patch5: 0004-Revert-Use-GChecksum-for-sha1-not-OpenSSL.patch
# If only 'autoreconf' or even 'gnome-autogen.sh' worked...
Patch6: update-autohate.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel             >= %{gtk2_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: dbus-glib-devel        >= 0.73
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: pkgconfig(openconnect) >= 3.99
BuildRequires: GConf2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: libglade2-devel
BuildRequires: intltool gettext
BuildRequires: autoconf automake libtool openssl-devel
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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%configure --enable-more-warnings=yes
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_datadir}/gnome-vpn-properties/openconnect/nm-openconnect-dialog.glade

%changelog
* Wed Jun 20 2012 David Woodhouse <David.Woodhouse@intel.com> - 0.8.6.0-1
- Update to 0.8.6.0 and backport for EPEL5

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

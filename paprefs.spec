%define name paprefs
%define version 0.9.9
%define git 0
%if %{git}
%define release %mkrel 0.%{git}.%rel
%else
%define release 9
%endif

Summary: PulseAudio Preferences
Name: %{name}
Version: %{version}
Release: %{release}
%if %{git}
Source0: %{name}-%{git}.tar.lzma
%else
Source0: %{name}-%{version}.tar.gz
%endif
Source1: %{name}-16.png
Source2: %{name}-32.png
Patch100: 0100-packagekit-Tidy-up-packagekit-UI-integration-code.patch
Patch101: 0101-Enable-the-PackageKit-install-buttons-only-when-Pack.patch
Patch102: 0102-Dynamically-build-the-paths-to-the-modules.patch
License: GPL
Group: Sound
Url: http://0pointer.de/lennart/projects/paprefs/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtkmm2.4-devel
BuildRequires: libglademm2.4-devel
BuildRequires: gconfmm2.6-devel
BuildRequires: intltool
BuildRequires: gettext-devel
BuildRequires: libpulseaudio-devel >= 0.9.7
BuildRequires: lynx
BuildRequires: desktop-file-utils
Requires: pulseaudio-module-gconf
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
PulseAudio Preferences is a simple GTK based configuration dialog for
the PulseAudio sound server.

Please note that this program can only configure local servers, and
requires that a special module module-gconf is loaded in the sound
server.

%prep
%if %{git}
%setup -q -n %{name}
%else
%setup -q
%endif
%apply_patches

%build
%if %{git}
libtoolize --force
NOCONFIGURE=1 ./bootstrap.sh
%endif
autoreconf
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

sed -i "s/^Icon=.*/Icon=%{name}/" %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="System" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop

echo "NotShowIn=KDE" >> %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons
install -D -m 0644 %SOURCE1 %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 0644 %SOURCE2 %{buildroot}%{_iconsdir}/%{name}.png

%find_lang %{name}

%if %mdkversion < 200900
%post
%update_desktop_database
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_desktop_database
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README LICENSE
%{_bindir}/%name
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/%{name}.glade
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.9-8mdv2011.0
+ Revision: 666987
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.9-7mdv2011.0
+ Revision: 607072
- rebuild

* Sat Dec 05 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.9-6mdv2010.1
+ Revision: 473959
- Add upstream patches to disable package kit and not require recompile on PA version bump

* Sat Oct 03 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.9-5mdv2010.0
+ Revision: 452840
- Disable packagekit install buttons. This doesn't work well on Mandriva and will just add to confusion

* Wed Sep 30 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.9-4mdv2010.0
+ Revision: 451188
- Rebuild for PA 0.9.19

* Sat Sep 26 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.9-3mdv2010.0
+ Revision: 449507
- Recompile for PulseAudio 0.9.18

* Tue Sep 15 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.9-2mdv2010.0
+ Revision: 443120
- Remove packagekit deps. Proper removal of the functionality will follow sometime soon.

* Thu Sep 10 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.9-1mdv2010.0
+ Revision: 436457
- New version: 0.9.9
- Demote gnome-packagekit to a suggestion only
- Add dep on gnome-packagekit so we can talk to gpk-update-icon's dbus service

* Tue Aug 25 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.9-0.20090825.1mdv2010.0
+ Revision: 420900
- New snapshot supporting rygel and packagekit (which is not currently in mdv but will package soon)

* Fri Jul 24 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.8-2mdv2010.0
+ Revision: 399122
- Rebuild for new pulse (and fix it to work with new pulse for good measure)

* Tue Apr 14 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.8-1mdv2009.1
+ Revision: 367225
- New version: 0.9.8

* Sun Feb 22 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.7-5mdv2009.1
+ Revision: 343913
- Fix the module directory detection
- Update patch to properly attribute trademarked terms

* Sun Feb 08 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.7-4mdv2009.1
+ Revision: 338438
- Rebuild for newer pulse

* Mon Jan 26 2009 Colin Guthrie <cguthrie@mandriva.org> 0.9.7-3mdv2009.1
+ Revision: 333849
- Fix the enabling/disabling of the RAOP option if the module is not detected
- Fix paprefs for pulseaudio module location

* Sat Oct 11 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9.7-2mdv2009.1
+ Revision: 292024
- Fix a typo and an initial-state bug in my airtunes patch

* Fri Sep 12 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9.7-1mdv2009.0
+ Revision: 284280
- New version: 0.9.7

* Mon Jul 28 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9.6-8mdv2009.0
+ Revision: 252051
- Add support for Airtunes autodiscovery

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Jan 31 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9.6-7mdv2008.1
+ Revision: 160892
- Fix %%postun (#37210)

* Wed Jan 16 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9.6-6mdv2008.1
+ Revision: 153651
- Fix an error between my chair and keyboard.
- Remove the X-MandrivaLinux-Multimedia-Sound as Fred has previously done.
- Reinstate the correct macros accidentally overwritten.

* Tue Jan 15 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9.6-5mdv2008.1
+ Revision: 152546
- Rebuild due to submission failure
- Add icons for x-desktop use (MDV#36579)
- Add to X-MandrivaLinux-Multimedia-Sound category for greater exposure

* Thu Jan 10 2008 Frederic Crozat <fcrozat@mandriva.com> 0.9.6-3mdv2008.1
+ Revision: 147540
- Move menu entry to Tools/System
- Ensure correct macros are called in post/postun

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 03 2007 Colin Guthrie <cguthrie@mandriva.org> 0.9.6-2mdv2008.1
+ Revision: 114518
- Require pulseaudio-module-gconf

* Tue Oct 30 2007 Colin Guthrie <cguthrie@mandriva.org> 0.9.6-1mdv2008.1
+ Revision: 103904
- New version

* Tue Oct 30 2007 Colin Guthrie <cguthrie@mandriva.org> 0.9.6-0.30.1mdv2008.1
+ Revision: 103684
- Add BuildRequires for intltool
- Add BuildRequires for gettext-devel
- Make the gettextize thing a patch to go upstream (ugly and evil but effective)
- Update to svn snapshot.


* Mon Feb 05 2007 Colin Guthrie <cguthrie@mandriva.org> 0.9.5-2mdv2007.0
+ Revision: 116467
- Fix BuildRequires for x86_64 compatibility
- Import paprefs

* Mon Aug 28 2006 Götz Waschk <waschk@mandriva.org> 0.9.5-1mdv2007.0
- initial package


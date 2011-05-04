%define name paprefs
%define version 0.9.9
%define rel 8
%define git 0
%if %{git}
%define release %mkrel 0.%{git}.%rel
%else
%define release %mkrel %rel
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



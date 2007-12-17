%define name paprefs
%define version 0.9.6
%define rel 2
%define svn 0
%if %{svn}
%define release %mkrel 0.%{svn}.%rel
%else
%define release %mkrel %rel
%endif

Summary: PulseAudio Preferences
Name: %{name}
Version: %{version}
Release: %{release}
%if %{svn}
Source0: %{name}-%{svn}.tar.gz
%else
Source0: %{name}-%{version}.tar.gz
%endif
License: GPL
Group: Sound
Url: http://0pointer.de/lennart/projects/paprefs/
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
%if %{svn}
%setup -q -n %{name}
%else
%setup -q
%endif

%build
%if %{svn}
libtoolize --force
NOCONFIGURE=1 ./bootstrap.sh
%endif
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --remove-category="Application" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %{name}
%post
%{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null

%postun
if [ -x %{_bindir}/update-desktop-database ]; then %{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null ; fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README LICENSE
%_bindir/%name
%_datadir/applications/%name.desktop
%_datadir/%name/%name.glade



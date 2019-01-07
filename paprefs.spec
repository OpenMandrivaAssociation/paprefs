Summary:	PulseAudio Preferences
Name:		paprefs
Version:	0.9.10
Release:	20
License:	GPLv2
Group:		Sound
Url:		http://0pointer.de/lennart/projects/paprefs/
Source0:	http://freedesktop.org/software/pulseaudio/paprefs/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	lynx
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(gconfmm-2.6)
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	pkgconfig(libglademm-2.4)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(libpulse)
Requires:	pulseaudio-module-gsettings
Requires(post,postun):	desktop-file-utils

%description
PulseAudio Preferences is a simple GTK based configuration dialog for
the PulseAudio sound server.

Please note that this program can only configure local servers, and
requires that a special module module-gconf is loaded in the sound
server.

%prep
%autosetup -p1

%build
export CXXFLAGS="%{optflags} -std=c++11"

%configure
%make_build

%install
%make_install

sed -i "s/^Icon=.*/Icon=%{name}/" %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor="" \
	--add-category="GTK" \
	--add-category="System" \
	--add-category="X-MandrivaLinux-CrossDesktop" \
	--remove-category="Application" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

echo "NotShowIn=KDE;" >> %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%files -f %{name}.lang
%doc README LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/%{name}.glade

Summary:	A X11 program for watching TV
Name:		xawtv
Version:	3.95
Release:	%mkrel 8
Source0:	%{name}-%{version}.tar.bz2
Source2:	%{name}
Patch0:		xawtv-3.84-fixes.patch
Patch1:		xawtv-3.74-ia64.patch
Patch10:	xawtv-3.94-gcc4.patch
Patch20:	xawtv-3.94-quicktime.patch
Patch21:	xawtv-3.95-xorg71.patch
Group:		Video
License:	GPL
#OLD_STILL_VALID_URLs: http://www.strusel007.de/linux/xawtv/
#http://bytesex.org/xawtv/
URL:		http://linux.bytesex.org/xawtv/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	MesaGLU-devel
BuildRequires:	aalib-devel
BuildRequires:	gpm-devel
BuildRequires:	lesstif-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libzvbi-devel >= 0.2.1
BuildRequires:	ncurses-devel
BuildRequires:	recode
BuildRequires:	slang-devel
BuildRequires:	xpm-devel
BuildRequires:	libxaw-devel
BuildRequires:	libx11-devel
BuildRequires:	libfs-devel
BuildRequires:	libxinerama-devel
BuildRequires:	libxv-devel
BuildRequires:	libxxf86dga-devel
BuildRequires:	libxrandr-devel
BuildRequires:	libdv-devel
BuildRequires:	liblirc-devel
BuildRequires:	x11-server-common

Requires:	common-licenses
Requires:	xawtv-common = %version

%package	common
Summary:	Common files for fbtv/motv/ttv/xawtv
Group:		Video
Requires:	tv-fonts

%package	control
Summary:	Control video4linux devices
Group:		Video

%package -n	fbtv
Summary:	A console program for watching TV
Group:		Video
Requires:	xawtv-common = %version

%package	misc
Summary:	Xawtv miscellous stuff
Group:		Video
Requires:	xawtv-common = %version

%package -n	radio
Summary:	Console radio application
Group:		Sound
Provides:	xawtv-radio
Obsoletes:	xawtv-radio

%package -n	streamer
Summary:	Record audio and/or video streams
Group:		Video
Requires:	xawtv-common = %version

%package -n	motv
Summary:	A Motif program for watching TV
Group:		Video
Requires:	xawtv-common = %version

%package -n	ttv
Summary:	Display TV/video on a tty
Group:		Video
Requires:	xawtv-common = %version

%package	web
Summary:	Videotext pages webserver & images capture/upload to a webserver
Group:		Networking/WWW
Requires:	xawtv-common = %version

%description
Xawtv is a Video4Linux Stream Capture Viewer, that is a X11 program for
watching TV.

It uses the Athena widgets.
MoTV has a nicer GUI which use lesstif (motif) widgets.

%description	common
These are common files for fbtv, motv, ttv and xawtv.
They are:
 * scantv: small text program that look for tv channels
 * streamer - capture tool (images / movies)

%description	control
Xawtv-remote and v4lctl can be used to control a video4linux driven TV card.

Xawtv-remote passes the command to a already running xawtv or motv instance
using X11 properties.

V4lctl is a command line tool that sets the parameters directly.

%description -n	fbtv
Fbtv is a program for watching TV with your linux box.
It runs on top of a graphic framebuffer device (/dev/fb0).

This is useful for watching TV without X11.

fbtv shares the config file ($HOME/.xawtv) with the xawtv
application.

Check the xawtv(1) manpage for details about the config file format.


%description	misc
This package has a few tools you might find useful. They
have not to do very much to do with xawtv. They were written
for debugging:
 * dump-mixers - dump mixer settings to stdout
 * propwatch   - monitors properties of X11 windows.  If you
                 want to know how to keep track of xawtv's
                 _XAWTV_STATION property, look at this.
 * mtt         - teletext browser for X11 and console
 * ntsc-cc     - reads vbi data from /dev/vbi and decodes the enclosed cc data.
 * pia         - play media files
 * record      - console sound recorder.  Has a simple input
                 level meter which might be useful to trouble
                 shoot sound problems.
 * showriff    - display the structure of RIFF files (avi, wav).


%description -n	motv
This is a motv-based Video4Linux capture viewer.

It is basically xawtv with a more user-friendly GUI.
It has the same features, uses the same config file, has the same command
line switches, you can control it using xawtv-remote.
Most keyboards shortcuts are identical too.

%description -n	radio
This is a ncurses-based radio application

%description -n	streamer
streamer reads audio and/or video data from /dev/video0 and /dev/dsp
and writes the data to the disk.
Various output formats are supported.
Start streamer with '-h' for a list of options and supported output formats.

%description -n	ttv
Ttv displays TV/video on a terminal, rendering the images using aalib.

%description	web
Webcam captures images from a video4linux device like bttv,
annotates them and and uploads them to a webserver using ftp
in a endless loop.

Alevtd is http daemon which serves videotext pages as HTML.
Tune in some station with a utility like v4lctl or some TV application.
Then start it and point your browser to http://localhost:5654/

Pages may be requested either in HTML format (http://localhost:5654/<page>/
or http://localhost:5654/<page>/<subpage>.html) or in ASCII text format
(http://localhost:5654/<page>/<subpage>.txt).
Subpage "00" can be used for pages without subpages.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch10 -p0
%patch20 -p0
%patch21 -p0
%build
%configure	--enable-xfree-ext \
		--enable-xvideo \
		--enable-aa \
		--enable-alsa \
		--disable-quicktime \
		--x-includes=%{_includedir}/freetype2

# Quicktime support not enabled, so libpng is not needed
find . -name 'Makefile' | xargs perl -pi -e 's/-lpng//g'
%make

%install
rm -fr $RPM_BUILD_ROOT
perl -pi -e 's!-o root -g root!!g' src/Makefile
mkdir -p $RPM_BUILD_ROOT/usr/lib/X11/app-defaults
 %makeinstall_std ROOT="$RPM_BUILD_ROOT" FONTDIR=$RPM_BUILD_ROOT/%_datadir/fonts/misc SUID_ROOT=""

install -m 644 x11/Xawtv.ad $RPM_BUILD_ROOT/usr/lib/X11/app-defaults
(cd $RPM_BUILD_ROOT/usr/lib/X11/app-defaults; ln Xawtv.ad Xawtv; ln Xawtv.ad Xawtv-color)

install -m 755 %SOURCE2 $RPM_BUILD_ROOT/%_bindir/XawTV

# Menu entries

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=XawTV
Comment=A program for watching TV
Exec=%{_bindir}/XawTV
Icon=video_section
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Video;TV;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-motv.desktop <<EOF
[Desktop Entry]
Name=MoTV
Comment=A program for watching TV (nicer interface)
Exec=%{_bindir}/motv
Icon=video_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Motif;AudioVideo;Video;TV;
EOF

# dynamic desktop support
%define webcam_launcher /etc/dynamic/launchers/webcam
%define tvtuner_launcher /etc/dynamic/launchers/tvtuner

mkdir -p $RPM_BUILD_ROOT{%tvtuner_launcher,%webcam_launcher}
cat > $RPM_BUILD_ROOT%webcam_launcher/%name.desktop << EOF
[Desktop Entry]
Name=XawTV \$devicename
Comment=The X11 Video4Linux Stream Capture Viewer
TryExec=/usr/bin/xawtv
Exec=/usr/bin/xawtv -c \$device
Terminal=false
Icon=video_section
Type=Application
EOF
cat > $RPM_BUILD_ROOT%tvtuner_launcher/%name.desktop << EOF
[Desktop Entry]
Name=XawTV \$devicename
Comment=The X11 Video4Linux Stream Capture Viewer
TryExec=/usr/bin/XawTV
Exec=/usr/bin/XawTV -c \$device
Terminal=false
Icon=video_section
Type=Application
EOF


%post
update-alternatives --install %webcam_launcher/gnome.desktop webcam.gnome.dynamic %webcam_launcher/%name.desktop 20
update-alternatives --install %webcam_launcher/kde.desktop webcam.kde.dynamic %webcam_launcher/%name.desktop 20
update-alternatives --install %tvtuner_launcher/kde.desktop tvtuner.kde.dynamic %tvtuner_launcher/%name.desktop 20
update-alternatives --install %tvtuner_launcher/gnome.desktop tvtuner.gnome.dynamic %tvtuner_launcher/%name.desktop 20
%if %mdkversion < 200900
%update_menus
%endif

%postun
if [ $1 = 0 ]; then
  update-alternatives --remove webcam.kde.dynamic %webcam_launcher/%name.desktop
  update-alternatives --remove webcam.gnome.dynamic %webcam_launcher/%name.desktop
  update-alternatives --remove tvtuner.kde.dynamic %tvtuner_launcher/%name.desktop
  update-alternatives --remove tvtuner.gnome.dynamic %tvtuner_launcher/%name.desktop
fi
%if %mdkversion < 200900
%clean_menus
%endif

%if %mdkversion < 200900
%post -n motv
%update_menus
%endif

%if %mdkversion < 200900
%postun -n motv
%clean_menus 
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %tvtuner_launcher/%name.desktop
%config(noreplace) %webcam_launcher/%name.desktop
%config(noreplace) %_sysconfdir/X11/app-defaults/Xawtv
%_bindir/xawtv
%_bindir/XawTV
%_mandir/man1/xawtv.1*
%_mandir/fr/man1/xawtv.1*
%{_datadir}/applications/mandriva-%{name}.desktop
/usr/lib/X11/app-defaults/Xawtv*
%_datadir/%name

%files common
%attr(4711,root,root) %_bindir/v4l-conf
%defattr(-,root,root)
%_bindir/rootv
%_bindir/scantv
%_bindir/subtitles 
%_bindir/v4l-info
%lang(es) %_mandir/es/man1/rootv.*
%lang(es) %_mandir/es/man1/scantv.*
%lang(es) %_mandir/es/man1/subtitles.*
%lang(es) %_mandir/es/man1/xawtv.*
%lang(es) %_mandir/es/man5/xawtvrc.*
%lang(es) %_mandir/es/man8/v4l-conf.*
%_mandir/man1/rootv.1*
%_mandir/man1/scantv.1*
%_mandir/man1/subtitles*
%_mandir/man5/xawtvrc*
%_mandir/man8/v4l*
%_mandir/man1/v4l-info.*
%dir %_libdir/%name
%_libdir/%name/*
%doc Changes README*
%doc README*
%doc contrib/frequencies*

%files control
%defattr(-,root,root)
%_bindir/v4lctl
%_bindir/xawtv-remote
%_mandir/man1/v4lctl.1*
%lang(es) %_mandir/es/man1/v4lctl.*
%_mandir/man1/xawtv-remote.1*
%lang(es) %_mandir/es/man1/xawtv-remote.*

%files -n fbtv
%defattr(-,root,root)
%_bindir/fbtv
%_mandir/man1/fbtv*
%lang(es) %_mandir/es/man?/fbtv.*

%files misc
%defattr(-,root,root)
%config(noreplace) /etc/X11/app-defaults/mtt
%_bindir/dump-mixers
%_bindir/mtt
%_bindir/ntsc-cc
%_bindir/pia
%_bindir/propwatch
%_bindir/record
%_bindir/showqt
%_bindir/showriff
%_mandir/man1/dump-mixers*
%_mandir/man1/mtt*
%_mandir/man1/ntsc*
%_mandir/man1/pia*
%_mandir/man1/record*
%_mandir/man1/propwatch*
%_mandir/man1/showriff.1*

%files -n motv
%defattr(-,root,root)
%_bindir/motv
%_mandir/man1/motv*
%{_datadir}/applications/mandriva-motv.desktop
%config(noreplace) %_sysconfdir/X11/app-defaults/MoTV
%config(noreplace) %_sysconfdir/X11/de_DE.UTF-8/app-defaults/MoTV
%config(noreplace) %_sysconfdir/X11/de/app-defaults/MoTV
%config(noreplace) %_sysconfdir/X11/fr/app-defaults/MoTV
%config(noreplace) %_sysconfdir/X11/it/app-defaults/MoTV

%files -n radio
%defattr(-,root,root)
%_bindir/radio
%_mandir/man1/radio*

%files -n streamer
%defattr(-,root,root)
%_bindir/streamer
%_mandir/man1/streamer*
%lang(es) %_mandir/es/man1/streamer.*

%files -n ttv
%defattr(-,root,root)
%_bindir/ttv
%_mandir/man1/ttv*
%lang(es) %_mandir/es/man1/ttv.*

%files web
%defattr(-,root,root)
%_bindir/alevtd
%_bindir/webcam
%_mandir/man1/alevtd.1*
%_mandir/man1/webcam.1*

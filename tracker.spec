Summary:	Desktop-neutral search tool and indexer
Name:		tracker
Version:	0.12.7
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/System
URL:		http://projects.gnome.org/tracker/
Source0:	http://download.gnome.org/sources/tracker/0.12/%{name}-%{version}.tar.xz

BuildRequires:	poppler-glib-devel evolution-devel libxml2-devel libgsf-devel
BuildRequires:	libuuid-devel dbus-glib-devel
BuildRequires:	nautilus-devel
BuildRequires:	libjpeg-devel libexif-devel exempi-devel raptor-devel
BuildRequires:	libiptcdata-devel libtiff-devel libpng-devel giflib-devel
BuildRequires:	sqlite-devel vala-devel libgee06-devel
BuildRequires:  gstreamer-plugins-base-devel gstreamer-devel id3lib-devel
BuildRequires:	totem-pl-parser-devel libvorbis-devel flac-devel enca-devel
BuildRequires:	upower-devel gnome-keyring-devel NetworkManager-glib-devel
BuildRequires:	libunistring-devel gupnp-dlna-devel taglib-devel rest-devel
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	desktop-file-utils intltool gettext
BuildRequires:	gtk-doc graphviz dia
BuildRequires:	gobject-introspection


%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database, search tool and indexer.

It consists of a common object database that allows entities to have an
almost infinte number of properties, metadata (both embedded/harvested as
well as user definable), a comprehensive database of keywords/tags and
links to other entities.

It provides additional features for file based objects including context
linking and audit trails for a file object.

It has the ability to index, store, harvest metadata. retrieve and search
all types of files and other first class objects

%package devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	dbus-glib-devel gtk2-devel

%description devel
This package contains the static libraries and header files needed for
developing with tracker

%package ui-tools
Summary:	Tracker search tool(s)
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}
Obsoletes:	paperbox <= 0.4.4
Obsoletes:	tracker-search-tool <= 0.12.0

%description ui-tools
Graphical frontend to tracker search (tracker-needle) and configuration
(tracker-preferences) facilities. This also contains A test tool to navigate
around objects in the database based on their relationships (tracker-explorer)

%package evolution-plugin
Summary:	Tracker's evolution plugin
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description evolution-plugin
Tracker's evolution plugin

%package nautilus-plugin
Summary:	Tracker's nautilus plugin
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description nautilus-plugin
Tracker's nautilus plugin, provides 'tagging' functionality. Ability to perform
search in nuautilus using tracker is built-in directly in the nautilus package.

%package docs
Summary:	Documentations for tracker
Group:		Documentation
BuildArch:      noarch

%description docs
This package contains the documentation for tracker

%prep
%setup -q

%global evo_plugins_dir %(pkg-config evolution-plugin-3.0 --variable=plugindir)

## nuke unwanted rpaths, see also
## https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure

%build
%configure --disable-static		\
	--disable-tracker-search-bar	\
	--disable-miner-thunderbird	\
	--disable-miner-firefox		\
	--enable-gtk-doc		\
	--disable-functional-tests
# Disable the functional tests for now, they use python bytecodes.

make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/tracker-0.12"	\
	> %{buildroot}%{_sysconfdir}/ld.so.conf.d/tracker-%{_arch}.conf

desktop-file-install --delete-original			\
	--vendor="fedora"				\
	--dir=%{buildroot}%{_datadir}/applications	\
	%{buildroot}%{_datadir}/applications/%{name}-needle.desktop

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -rf %{buildroot}%{_datadir}/tracker-tests

%find_lang %{name}

%post -p /sbin/ldconfig

%post ui-tools
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas || :
fi

%postun ui-tools
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas || :

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/tracker*
%{_libexecdir}/tracker*
%{_datadir}/tracker/
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*
%{_libdir}/*.so.*
%{_libdir}/tracker-0.12/
%{_libdir}/girepository-1.0/Tracker-0.12.typelib
%{_libdir}/girepository-1.0/TrackerExtract-0.12.typelib
%{_libdir}/girepository-1.0/TrackerMiner-0.12.typelib
%{_mandir}/*/tracker*.gz
%{_sysconfdir}/ld.so.conf.d/tracker-%{_arch}.conf
%{_sysconfdir}/xdg/autostart/tracker*.desktop
%{_datadir}/glib-2.0/schemas/*
%exclude %{_bindir}/tracker-explorer
%exclude %{_bindir}/tracker-needle
%exclude %{_bindir}/tracker-preferences
%exclude %{_mandir}/man1/tracker-preferences.1.gz
%exclude %{_mandir}/man1/tracker-needle.1.gz

%files devel
%defattr(-, root, root, -)
%{_includedir}/tracker-0.12/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/vala/vapi/tracker*.*
%{_datadir}/gir-1.0/Tracker-0.12.gir
%{_datadir}/gir-1.0/TrackerExtract-0.12.gir
%{_datadir}/gir-1.0/TrackerMiner-0.12.gir

%files ui-tools
%defattr(-, root, root, -)
%{_bindir}/tracker-explorer
%{_bindir}/tracker-needle
%{_bindir}/tracker-preferences
%{_datadir}/icons/*/*/apps/tracker.*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/tracker-preferences.1.gz
%{_mandir}/man1/tracker-needle.1.gz

%files evolution-plugin
%defattr(-, root, root, -)
%{evo_plugins_dir}/liborg-freedesktop-Tracker-evolution-plugin.so
%{evo_plugins_dir}/org-freedesktop-Tracker-evolution-plugin.eplug

%files nautilus-plugin
%defattr(-, root, root, -)
%{_libdir}/nautilus/extensions-3.0/libnautilus-tracker-tags.so

%files docs
%defattr(-, root, root, -)
%doc docs/reference/COPYING
%{_datadir}/gtk-doc/html/libtracker-miner/
%{_datadir}/gtk-doc/html/libtracker-extract/
%{_datadir}/gtk-doc/html/libtracker-sparql/
%{_datadir}/gtk-doc/html/ontology/

%changelog
* Mon Oct 31 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.7-1
- Update to 0.12.7
- http://ftp.gnome.org/pub/GNOME/sources/tracker/0.12/tracker-0.12.6.news
- http://ftp.gnome.org/pub/GNOME/sources/tracker/0.12/tracker-0.12.7.news

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.12.5-2
- rebuild(poppler)

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.12.5-1
- Update to 0.12.5

* Tue Oct 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.4-2
- Rebuild for new poppler 0.18

* Sun Oct 09 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.4-1
- Update to 0.12.4 stable release
- http://download.gnome.org/sources/tracker/0.12/tracker-0.12.4.changes

* Fri Sep 30 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.12.3-2
- Rebuilt for new 0.18 poppler

* Tue Sep 27 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.3-1
- Update to 0.12.3 stable release

* Fri Sep 23 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.2-1
- Update to 0.12.2 stable release
- Replace the search-tool sub-package with more appropriately named ui-tools
- Disable the search-bar until upstream redo it for GNOME 3

* Fri Sep 23 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.12.0-3
- Rebuild (poppler-0.17.3)
- Readd --enable-miner-evolution as forgotten in 0.12.0-1
- Conditionally BR libgee06-devel instead of libgee-devel for Fedora > 16

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 0.12.0-2
- Rebuild (poppler-0.17.3)

* Fri Sep 09 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.0-1
- Update to 0.12.0 stable release
- Re-enable the evolution plugin

* Thu Sep  1 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2
- Drop the evolution miner temporarily

* Tue Aug 30 2011 Milan Crha <mcrha@redhat.com> - 0.10.24-2
- Rebuild against newer evolution-data-server

* Thu Aug 25 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.24-1
- Update to 0.10.24
- Re-enable the evolution plugin

* Thu Aug 04 2011 Adam Williamson <awilliam@redhat.com> - 0.10.21-2
- obsolete the evo plugin as well so upgrades work

* Wed Aug 03 2011 Adam Williamson <awilliam@redhat.com> - 0.10.21-1
- complete disabling the evolution plugin

* Tue Jul 26 2011 Deji Akingunola <dakingun@gmail.com>
- Update to 0.10.21
- Temporarily disable the evolution plugin

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 0.10.15-2
- Rebuild (poppler-0.17.0)

* Tue May 31 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.15-1
- Update to 0.10.15

* Fri May 13 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.13-1
- Update to 0.10.13

* Tue Apr 26 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.10-1
- Update to 0.10.10

* Thu Apr 14 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.9-1
- Update to 0.10.9

* Tue Apr 12 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.8-2
- Rebuild against new gupnp-dlna, build introspection support

* Sat Apr 09 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.8-1
- Update to 0.10.8

* Sat Mar 26 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.5-1
- Update to 0.10.5

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.10.3-2
- Rebuild (poppler-0.16.3)

* Fri Mar 11 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.3-1
- Update to 0.10.3

* Thu Mar 10 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.2-1
- Update to 0.10.2

* Fri Feb 17 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.0-1
- Update to 0.10.0
- Re-enable tracker-search-bar

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.9.37-3
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.37-1
- Update to 0.9.37
- Disable tracker-search-bar - building it is currently failing with gtk3

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.36-2
- Rebuild against newer gtk

* Tue Feb 01 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.36-1
- Update to 0.9.36
- Temporarily disable the docs subpackage

* Tue Jan 25 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.35-1
- Update to 0.9.35
- Re-enable gupnp-dlna support 

* Tue Jan 11 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.33-3
- Temporarily disable gupnp-dlna.
- Update nautilus extensions directory for nautilus-3.x.

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.33-2
- Rebuild against newer gtk

* Tue Jan 04 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.33-1
- Update to 0.9.33
- Substitute gdk-pixbuf for qt4 as music album extractor
- Split off nautilus-plugin into a sub-package

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.9.30-3
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.30-2
- rebuild (poppler)

* Fri Dec 04 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.28-1
- Update to 0.9.30

* Sun Nov 07 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.27-1
- Update to 0.9.27

* Tue Oct 12 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.24-2
- Rebuild for evolution-data-server-2.91.0.

* Fri Oct 08 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.24-1
- First update to 0.9.x series
- Re-word the package summary (conformant to upstream wording).

* Thu Sep 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.17-3
- Rebuild for poppler-0.15.

* Tue Sep 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.17-2
- Rebuild for evolution (camel) update.
- Apply patch to build with gtk >= 2.90.7

* Thu Sep 02 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.17-1
- Update to 0.8.17 release

* Fri Aug 20 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.16-1
- Update to 0.8.16 release

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.15-2
- rebuild (poppler)

* Fri Jul 16 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.15-1
- Update to 0.8.15 release
- Package the docs licensing file
- Patch for EDS API changes (Migrate from CamelException to GError)
- Backport a memory leak fix

* Mon Jun 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.13-1
- Update to 0.8.13 release

* Tue Jun 22 2010 Matthias Clasen <mclasen@redhat.com> - 0.8.11-2
- Rebuild against new poppler

* Tue Jun 15 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.11-1
- Update to 0.8.11 release
- Adapt to EDS Camel API changes (Convert CamelObject events to GObject signals), patch not tested yet.

* Thu May 27 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.9-1
- Update to 0.8.9 release

* Thu May 06 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.5-1
- Update to 0.8.5 release
- Provide an upgrade path for paperbox (make ~-search-tool obsolete it) on F-13.
- Patch to build with eds-2.31.1 (Camel headers locked down)

* Thu Apr 29 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.4-1
- Update to 0.8.4 release

* Mon Apr 19 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.2-1
- Update to 0.8.2 release

* Thu Apr 01 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.0-1
- Update to 0.8.0 release

* Thu Mar 25 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.28-1
- Update to 0.7.28 release

* Thu Mar 11 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.25-1
- Update to 0.7.25 release

* Tue Mar 02 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.23-1
- Update to 0.7.23 release

* Sat Aug 29 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.95-4
- Explicitly require apps needed in the text filters of common documents (Fedora bug #517930)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.95-2
- Ship the manpages in the appropriate sub-packages (Fedora bug #479278)

* Fri May 22 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.95-1
- Update to 0.6.95 release

* Fri May 01 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.94-1
- Update to 0.6.94 release

* Thu Apr 09 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.93-1
- Update to 0.6.93 release

* Fri Mar 28 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.92-1
- Update to 0.6.92 release

* Fri Mar 13 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.91-1
- Update to 0.6.91 release

* Mon Feb 09 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.90-1
- New release, with tons of changes

* Tue Dec 23 2008 - Caolán McNamara <caolanm@redhat.com> - 0.6.6-10
- make build

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-9
- Add libtool BR

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-8
- Update patch to actually apply, way to do releases often

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-7
- Add patch to port to GMime 2.4

* Wed Dec 10 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-6
- Rebuild for gmime dependency

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.6-5
- Rebuild for Python 2.6

* Fri Nov 28 2008 Caolán McNamara <caolanm@redhat.com> - 0.6.6-4
- rebuild for dependancies

* Thu Jun 05 2008 Caolán McNamara <caolanm@redhat.com> - 0.6.6-3
- rebuild for dependancies

* Fri Mar 14 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.6-2
- BR poppler-glib-devel instead of poppler-devel for pdf extract module (Thanks to Karsten Hopp mass rebuild work for bringing this to light)

* Sun Mar 02 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.6-1
- New release 0.6.6

* Thu Feb 28 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.5-1
- New release 0.6.5

* Fri Feb 22 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-7
- Ship the tracker-applet program in the tracker-search-tool subpackage
  (Bug #434551)

* Sun Feb 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-6
- Rebuild for gcc43

* Thu Jan 24 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-5
- Backport assorted fixes from upstream svn (Fix Fedora bug 426060)

* Mon Jan 21 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-4
- Now require the externally packaged o3read to provide o3totxt

* Fri Dec 14 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.4-3
- Undo the patch, seems to be issues (bug #426060)

* Fri Dec 14 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.4-2
- Backport crasher fixes from upstream svn trunk

* Mon Dec 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.4-1
- Version 0.6.4

* Tue Dec 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.3-3
- Rebuild for exempi-1.99.5

* Sun Nov 25 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.6.3-2
- Add missing gtk+ icon cache scriptlets.

* Tue Sep 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.3-1
- Version 0.6.3

* Tue Sep 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.2-2
- Make trackerd start on x86_64 (Bug #286361, fix by Will Woods)

* Wed Sep 05 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.2-1
- Version 0.6.2

* Sat Aug 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.1-2
- Rebuild

* Wed Aug 08 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.0-3
- License tag update

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 0.6.0-2.1
- rebuild for toolchain bug

* Mon Jul 23 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.0-1
- Update to 0.6.0
- Manually specify path to deskbar-applet handler directory, koji can't find it

* Mon Jan 29 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-2
- Split out tracker-search-tool sub-packages, for the GUI facility
- Add proper requires for the -devel subpackage
- Deal with the rpmlint complaints on rpath

* Sat Jan 27 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-1
- Update to 0.5.4

* Tue Dec 26 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.3-1
- Update to 0.5.3

* Mon Nov 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.2-2
- Apply patch on Makefile.am instead of Makefile.in
- Add libtool to BR

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.2-1
- Update to 0.5.2

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.1-1
- Update to new version

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-7
- Have the devel subpackage require pkgconfig
- Make the description field not have more than 76 characters on a line
- Fix up the RPM group

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-6
- Explicitly require dbus-devel and dbus-glib (needed for FC < 6) 

* Sun Nov 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-5
- Remove unneeded BRs (gnome-utils-devel and openssl-devel) 

* Sun Nov 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-4
- Add autostart desktop file.
- Edit the package description as suggested in review

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-3
- More cleaups to the spec file.

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-2
- Add needed BRs

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-1
- Initial packaging for Fedora Extras

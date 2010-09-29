Summary:	An object database, tag/metadata database, search tool and indexer
Name:		tracker
Version:	0.8.17
Release:	2%{?dist}
License:	GPLv2+
Group:		Applications/System
URL:		http://projects.gnome.org/tracker/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/tracker/0.8/%{name}-%{version}.tar.bz2
Patch0:		tracker-0.8-doc-build.patch
Patch1:		tracker-eds-build-fix.patch
Patch2:		tracker-gtk-2.90.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	poppler-glib-devel libxml2-devel libgsf-devel 
BuildRequires:	libuuid-devel libnotify-devel dbus-devel
BuildRequires:	gnome-desktop-devel nautilus-devel gnome-panel-devel
BuildRequires:	libjpeg-devel libexif-devel exempi-devel raptor-devel
BuildRequires:	libiptcdata-devel libtiff-devel libpng-devel 
BuildRequires:	sqlite-devel vala-devel libgee-devel pygtk2-devel
BuildRequires:  gstreamer-plugins-base-devel gstreamer-devel id3lib-devel
BuildRequires:	totem-pl-parser-devel libvorbis-devel flac-devel enca-devel
BuildRequires:	upower-devel gnome-keyring-devel evolution-devel
BuildRequires:	desktop-file-utils intltool gettext graphviz

Requires:	odt2txt

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

%package search-tool
Summary:	Tracker search tool(s)
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}
Obsoletes:	paperbox <= 0.4.4

%description search-tool
Graphical frontend to tracker search and tagging facilities. This has
dependencies on GNOME libraries

%package evolution-plugin
Summary:	Tracker's evolution plugin
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description evolution-plugin
Tracker's evolution plugin

%package docs
Summary:	Documentations for tracker
Group:		Documentation
BuildArch:      noarch

%description docs
This package contains the documentation for tracker

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0

%global evo_plugins_dir %(pkg-config evolution-plugin --variable=plugindir)

%build
%configure --disable-static --enable-tracker-search-bar		\
	--enable-gtk-doc --disable-functional-tests

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make V=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/tracker-0.8"	\
	> %{buildroot}%{_sysconfdir}/ld.so.conf.d/tracker-%{_arch}.conf

desktop-file-install --delete-original			\
	--vendor="fedora"				\
	--dir=%{buildroot}%{_datadir}/applications	\
	%{buildroot}%{_datadir}/applications/%{name}-search-tool.desktop

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -rf %{buildroot}%{_datadir}/tracker-tests

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%post search-tool
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun -p /sbin/ldconfig

%postun search-tool
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/tracker*
%{_libexecdir}/tracker*
%{_datadir}/tracker/
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*
%{_libdir}/*.so.*
%{_libdir}/tracker-0.8/
%{_mandir}/*/tracker*.gz
%{_sysconfdir}/ld.so.conf.d/tracker-%{_arch}.conf
%{_sysconfdir}/xdg/autostart/tracker*.desktop
%exclude %{_bindir}/tracker-preferences
%exclude %{_bindir}/tracker-search-tool
%exclude %{_libexecdir}/tracker-search-bar
%exclude %{_mandir}/man1/tracker-search-bar.1.gz
%exclude %{_mandir}/man1/tracker-preferences.1.gz
%exclude %{_mandir}/man1/tracker-search-tool.1.gz

%files devel
%defattr(-, root, root, -)
%{_includedir}/tracker-0.8/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/vala/vapi/tracker*.*

%files search-tool
%defattr(-, root, root, -)
%{_bindir}/tracker-preferences
%{_bindir}/tracker-search-tool
%{_libexecdir}/tracker-search-bar
%{_libdir}/nautilus/extensions-2.0/libnautilus-tracker-tags.so
%{_libdir}/bonobo/servers/GNOME_Search_Bar_Applet.server
%{_datadir}/icons/*/*/apps/tracker.*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/tracker-search-bar.1.gz
%{_mandir}/man1/tracker-preferences.1.gz
%{_mandir}/man1/tracker-search-tool.1.gz

%files evolution-plugin
%defattr(-, root, root, -)
%{evo_plugins_dir}/liborg-freedesktop-Tracker-evolution-plugin.so
%{evo_plugins_dir}/org-freedesktop-Tracker-evolution-plugin.eplug

%files docs
%defattr(-, root, root, -)
%doc docs/reference/COPYING
%{_datadir}/gtk-doc/html/libtracker-common/
%{_datadir}/gtk-doc/html/libtracker-miner/
%{_datadir}/gtk-doc/html/libtracker-client/
%{_datadir}/gtk-doc/html/libtracker-extract/
%{_datadir}/gtk-doc/html/ontology/

%changelog
* Tue Sep 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.17-2
- Rebuild for evolution (camel) update.

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

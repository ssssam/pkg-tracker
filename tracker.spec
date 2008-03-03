Summary:	An object database, tag/metadata database, search tool and indexer
Name:		tracker
Version:	0.6.6
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/System
URL:		http://www.gnome.org/~jamiemcc/tracker/
Source0:	http://www.gnome.org/~jamiemcc/tracker/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	gmime-devel, poppler-devel, gettext
BuildRequires:	gnome-desktop-devel, gamin-devel, libnotify-devel
BuildRequires:	libexif-devel, libgsf-devel, gstreamer-devel, exempi-devel
BuildRequires:	desktop-file-utils, intltool, deskbar-applet
BuildRequires:	sqlite-devel, qdbm-devel, pygtk2-devel
Requires:	o3read

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

%description search-tool
Graphical frontend to tracker search facilities. This has dependencies on
GNOME libraries

%prep
%setup -q

%define deskbar_applet_ver %(pkg-config --modversion deskbar-applet)
%if "%deskbar_applet_ver" >= "2.19.4"
 %define deskbar_applet_dir %(pkg-config --variable modulesdir deskbar-applet)
 %define deskbar_type module
%else
 %define deskbar_applet_dir %(pkg-config --variable handlersdir deskbar-applet)
 %define deskbar_type handler
%endif

%build
%configure --disable-static --enable-deskbar-applet=%{deskbar_type}	\
		--enable-external-qdbm
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

desktop-file-install --delete-original			\
	--vendor="fedora"				\
	--dir=%{buildroot}%{_datadir}/applications	\
	%{buildroot}%{_datadir}/applications/%{name}-search-tool.desktop

rm -rf %{buildroot}%{_libdir}/*.la

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
%exclude %{_bindir}/tracker-applet
%exclude %{_bindir}/tracker-preferences
%exclude %{_bindir}/tracker-search-tool
%exclude %{_bindir}/tracker-thumbnailer
%exclude %{_bindir}/o3totxt
%{_datadir}/tracker/
%{_datadir}/dbus-1/services/tracker.service
%{_libdir}/*.so.*
%{_libdir}/tracker/
%{_mandir}/*/tracker*.gz
%{_sysconfdir}/xdg/autostart/trackerd.desktop

%files devel
%defattr(-, root, root, -)
%{_includedir}/tracker*
%{_includedir}/libtracker-gtk/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files search-tool
%defattr(-, root, root, -)
%{_bindir}/tracker-applet
%{_bindir}/tracker-preferences
%{_bindir}/tracker-search-tool
%{_bindir}/tracker-thumbnailer
%{deskbar_applet_dir}/tracker*.py*
%{_datadir}/icons/*/*/apps/tracker.*
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/autostart/tracker-applet.desktop

%changelog
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

Summary: An object database, tag/metadata database, search tool and indexer
Name: tracker
Version: 0.5.3
Release: 1%{?dist}
License: GPL
Group: Applications/System
URL: http://www.gnome.org/~jamiemcc/tracker/
Source0: http://www.gnome.org/~jamiemcc/tracker/tracker-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gmime-devel, poppler-devel, gettext
BuildRequires: gnome-desktop-devel, gamin-devel
BuildRequires: libexif-devel, libgsf-devel, gstreamer-devel
BuildRequires: desktop-file-utils, intltool
%if "%fedora" >= "6"
BuildRequires: sqlite-devel
%else
BuildRequires: dbus-devel, dbus-glib
%endif

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
Summary: Headers for developing programs that will use %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the static libraries and header files needed for
developing with tracker

%prep
%setup -q

%build
%if "%fedora" >= "6"
%configure --disable-static --enable-external-sqlite
%else
%configure --disable-static
%endif
# make %{?_smp_mflags} fails
make

										
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Add an autostart for trackerd (for KDE)
mkdir -p %{buildroot}%{_datadir}/autostart
cp -pr trackerd.desktop %{buildroot}%{_datadir}/autostart/

desktop-file-install --delete-original                   \
        --vendor="fedora"                           \
        --dir=%{buildroot}%{_datadir}/applications   \
        %{buildroot}%{_datadir}/applications/%{name}-search-tool.desktop

rm -rf %{buildroot}%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/htmless
%{_bindir}/o3totxt
%{_bindir}/tracker*
%{_datadir}/tracker/
%{_datadir}/pixmaps/tracker/
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/tracker.service
%{_datadir}/autostart/*.desktop
%{_libdir}/*.so.*
%{_libdir}/tracker/
%{_mandir}/man1/tracker*.1.gz
%{_sysconfdir}/xdg/autostart/trackerd.desktop

%files devel
%defattr(-, root, root, -)
%{_includedir}/tracker*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
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

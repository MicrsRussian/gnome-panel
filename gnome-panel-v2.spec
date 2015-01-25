%define ver_major 3.14
%define api_ver 3.0

# Whether to build clock applet with evolution-data-server.

# This switch controls whether to build some applets as running inside
# gnome-panel process (as for 2.16, these are clock, fish, notification
# area, and window list). Note that if this is on, then a crash of an applet is
# a crash of a panel.


Name: gnome-panel
Version: %ver_major.0


Summary: The core programs for the GNOME GUI desktop environment
License: GPLv2+ and LGPLv2+ and GFDL+
Group: Graphical desktop/GNOME
Url: ftp://ftp.gnome.org


Source0: http://download.gnome.org/sources/gnome-panel/3.14/%{name}-%{version}.tar.xz

# From configure.in

%global gnome_desktop_version 2.91.6
%global glib2_version 2.31.14
%global gtk3_version 3.14.0
%global libwnck_version 2.91.6
%global gnome_menus_version 3.1.4
%global evolution_data_server_version 3.5.3
%global cairo_version 1.0.0
%global dbus_version 1.1.2
%global dbus_glib_version 0.80
%global gnome_doc_utils_version 0.3.2
%global libgweather_version 3.5.1
Conflicts: gnome-power-manager < 2.15.3

PreReq: librarian
Requires: lib%name = %version-%release

# for Wanda
Requires: fortune-mod
# for clock
Requires: tzdata

BuildPreReq: rpm-build-gnome >= 0.4

# From configure.in
Requires: gnome-desktop3 >= %{gnome_desktop_version}
Requires: libwnck3 >= %{libwnck_version}
Requires: gnome-menus >= %{gnome_menus_version}
%if %{use_evolution_data_server}
Requires: evolution-data-server >= %{evolution_data_server_version}
%endif
Requires: gnome-session-xsession
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires(post): hicolor-icon-theme
Requires(post): GConf2
Requires(pre): GConf2
Requires(preun): GConf2
BuildRequires: libxml2-python
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: GConf2-devel
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: itstool
BuildRequires: libxslt
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: pkgconfig(gnome-desktop-3.0) >= %{gnome_desktop_version}
BuildRequires: pkgconfig(libwnck-3.0) >= %{libwnck_version}
BuildRequires: dconf-devel
BuildRequires: gnome-menus-devel >= %{gnome_menus_version}
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: yelp-tools
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: gtk-doc
BuildRequires: pango-devel
BuildRequires: libXau-devel
BuildRequires: libXrandr-devel
%if %{use_evolution_data_server}
BuildRequires: evolution-data-server-devel >= %{evolution_data_server_version}
BuildRequires: dbus-devel >= %{dbus_version}
%endif
BuildRequires: polkit-devel >= 0.92
BuildRequires: libgweather-devel >= %{libgweather_version}
BuildRequires: librsvg2-devel
BuildRequires: NetworkManager-devel
BuildRequires: intltool
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: libcanberra-devel
BuildRequires: desktop-file-utils
BuildRequires: gobject-introspection-devel
BuildRequires: gnome-common
Obsoletes: gdm-user-switch-applet < 1:2.91.6
Conflicts: gnome-power-manager < 2.15.3

%description
GNOME (GNU Network Object Model Environment) is a user-friendly
set of applications and desktop tools to be used in conjunction with a
window manager for the X Window System.  GNOME is similar in purpose and
scope to CDE and KDE, but GNOME is based completely on free
software.

The GNOME panel packages provides the gnome panel, menu's and some
basic applets for the panel.

%package -n lib%name
Summary: GNOME panel shared libraries
License: LGPLv2+
Group: System/Libraries

%description -n lib%name
Panel shared libraries for creating GNOME panels.

%package -n lib%name-devel
Summary: GNOME panel libraries, includes, and more
License: LGPLv2+
Group: Development/GNOME and GTK+
Requires: lib%name = %version-%release

%description -n lib%name-devel
Panel libraries and header files for creating GNOME panels.

%package -n lib%name-devel-static
Summary: GNOME panel static libraries
Group: Development/GNOME and GTK+
Requires: lib%name-devel = %version-%release

%description -n lib%name-devel-static
Panel static libraries for creating GNOME panels.

%package -n lib%name-devel-doc
Summary: GNOME Panel development documentation
Group: Development/GNOME and GTK+
Conflicts: lib%name-devel < %version
BuildArch: noarch

%description -n lib%name-devel-doc
Development documentation for Gnome Panel Applet library.

%package -n lib%name-gir
Summary: GObject introspection data for the GNOME panel library
License: LGPLv2+
Group: System/Libraries

%description -n lib%name-gir
GObject introspection data for the GNOME Panel shared library.

%package -n lib%name-gir-devel
Summary: GObject introspection devel data for the GNOME panel library
License: LGPLv2+
Group: System/Libraries
BuildArch: noarch
Requires: lib%name-gir = %version-%release

%description -n lib%name-gir-devel
GObject introspection devel data for the GNOME Panel shared library.


%define _gtk_docdir %_datadir/gtk-doc/html
%define _libexecdir %gnome_appletsdir

%prep
%setup

%build
gnome-doc-common --copy
%autoreconf
%configure \
   %{subst_enable static} \
   %{subst_enable eds} \
   %{?_with_in_process_applets:--with-in-process-applets=all} \
   --disable-schemas-compile \
   %{?_enable_gtk_doc:--enable-gtk-doc}

# SMP-incompatible build
%make

%install
%make DESTDIR=%buildroot install

%find_lang --with-gnome --output=%name.lang %name %name-%api_ver clock fish fish-applet-2 window-list workspace-switcher

%files -f %name.lang
%_bindir/*
%dir %gnome_appletsdir
%gnome_appletsdir/*
%dir %_datadir/gnome-panel
%_datadir/gnome-panel/*
%_desktopdir/%name.desktop
%_iconsdir/hicolor/*x*/apps/%{name}*.png
%_iconsdir/hicolor/scalable/apps/%{name}*.svg
%_man1dir/*
%_datadir/dbus-1/services/org.gnome.panel.applet.ClockAppletFactory.service
%_datadir/dbus-1/services/org.gnome.panel.applet.FishAppletFactory.service
%_datadir/dbus-1/services/org.gnome.panel.applet.NotificationAreaAppletFactory.service
%_datadir/dbus-1/services/org.gnome.panel.applet.WnckletFactory.service
%config %_datadir/glib-2.0/schemas/*.xml
%doc AUTHORS NEWS README

%files -n lib%name
%_libdir/*.so.*

%files -n lib%name-devel
%_includedir/*
%_libdir/*.so
%_pkgconfigdir/*

%files -n lib%name-devel-doc
%_gtk_docdir/*

%if_enabled static
%files -n lib%name-devel-static
%_libdir/*.a

%if_enabled introspection
%files -n lib%name-gir
%_typelibdir/*

%files -n lib%name-gir-devel
%_girdir/*

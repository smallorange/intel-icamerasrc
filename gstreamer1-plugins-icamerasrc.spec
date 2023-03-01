%global commit 3b7cdb93071360aacebb4e808ee71bb47cf90b30
%global commitdate 20220926
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           gstreamer1-plugins-icamerasrc
Summary:        GStreamer 1.0 Intel IPU6 camera plug-in
Version:        0.0
Release:        6.%{commitdate}git%{shortcommit}%{?dist}
License:        LGPLv2

Source0:        https://github.com/intel/icamerasrc/archive/%{commit}/icamerasrc-%{shortcommit}.tar.gz

BuildRequires:  ipu6-camera-bins-devel
BuildRequires:  ipu6-camera-hal-devel
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  libdrm-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

ExclusiveArch:  x86_64

%description
This package provides the GStreamer 1.0 plug-in for MIPI camera.

%package devel
Summary:        GStreamer plug-in development files for Intel IPU6 camera
Requires:       gstreamer1-devel
Requires:       ipu6-camera-bins-devel
Requires:       ipu6-camera-hal-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This provides the necessary header files for IPU6 GStreamer plugin development.

%prep
%autosetup -p1 -n icamerasrc-%{commit}
autoreconf --verbose --force --install --make

%build
export CHROME_SLIM_CAMHAL=ON
export STRIP_VIRTUAL_CHANNEL_CAMHAL=ON
%configure
%make_build

%install
%make_install

%files
%license LICENSE
%{_libdir}/gstreamer-1.0/*
%{_libdir}/libgsticamerainterface-1.0.so.1
%{_libdir}/libgsticamerainterface-1.0.so.1.0.0

%files devel
%{_libdir}/libgsticamerainterface-1.0.so
%{_includedir}/gstreamer-1.0/gst/*
%{_libdir}/pkgconfig/*

%changelog
* Wed Mar 1 2023 Kate Hsuan <hpa@redhat.com> - 0.0-6.20220926git3b7cdb9
- Fixed requires
- Fixed directory ownership

* Fri Feb 17 2023 Kate Hsuan <hpa@redhat.com> - 0.0-5.20220926git3b7cdb9
- A few minor revisions includes
- Removed unnecessary %dir
- Removed .so file from devel package

* Wed Feb 15 2023 Kate Hsuan <hpa@redhat.com> - 0.0-4.20220926git3b7cdb9
- Updated the build and installation scripts

* Tue Dec 20 2022 Kate Hsuan <hpa@redhat.com> - 0.0-3.20220926git3b7cdb9
- Modify library path for build

* Tue Dec 20 2022 Kate Hsuan <hpa@redhat.com> - 0.0-2.20220926git3b7cdb9
- File placement fixes
- Format for style fixes

* Tue Nov 29 2022 Kate Hsuan <hpa@redhat.com> - 0.0-1.20220926git3b7cdb9
- First commit

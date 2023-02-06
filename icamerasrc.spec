#ignore rpath check for a invalid path
%global __brp_check_rpaths %{nil}
%global commit 3b7cdb93071360aacebb4e808ee71bb47cf90b30
%global commitdate 20220926
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           icamerasrc
Summary:        GStreamer plugin for Intel IPU6
Version:        0.0
Release:        3.%{commitdate}git%{shortcommit}%{?dist}
License:        LGPLv2

Source0:        https://github.com/intel/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  chrpath
BuildRequires:  patchelf
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

Requires:       ipu6-camera-bins
Requires:       ipu6-camera-hal
Requires:       gstreamer1-plugins-base
Requires:       libdrm >= 2.4.114

%description
This package provides the GStreamer plugin for MIPI camera.

%package devel
Summary:        GStreamer plugin development header files for Intel IPU6
Requires:       ipu6-camera-bins-devel
Requires:       ipu6-camera-hal-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This provides the necessary header files for IPU6 GStreamer plugin development.

%prep

%setup -q -n %{name}-%{commit}

%build
export CHROME_SLIM_CAMHAL=ON
export STRIP_VIRTUAL_CHANNEL_CAMHAL=ON
export PKG_CONFIG_PATH="/usr/lib64/pkgconfig"
./autogen.sh
make -j`nproc`

%install

mkdir -p %{buildroot}%{_libdir}/gstreamer-1.0
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}/icamerasrc/interfaces
mkdir -p %{buildroot}%{_includedir}/gstreamer-1.0/gst
cp -rp src/.libs/*.so* %{buildroot}%{_libdir}/gstreamer-1.0
cp src/*.la %{buildroot}%{_libdir}/gstreamer-1.0
cp -rp src/interfaces/.libs/*.so* %{buildroot}%{_libdir}
cp src/interfaces/*.la %{buildroot}%{_libdir}
cp -rp src/interfaces/*.h %{buildroot}%{_includedir}/icamerasrc/interfaces
cp -rp src/interfaces/*.h %{buildroot}%{_includedir}/gstreamer-1.0/gst
cp -rp src/gst/gstcamerasrcmeta.h %{buildroot}%{_includedir}/gstreamer-1.0/gst
cp -rp libgsticamerasrc.pc %{buildroot}%{_libdir}/pkgconfig/libgsticamerasrc.pc
sed -i \
    -e "s/^libdir=\/usr\/lib$/libdir=\/usr\/lib64/" \
    -e "s/^prefix=\/.\+$/prefix=\/usr/" \
    %{buildroot}%{_libdir}/pkgconfig/libgsticamerasrc.pc

chrpath --delete %{buildroot}%{_libdir}/gstreamer-1.0/libgsticamerasrc.so
patchelf --set-rpath %{_rundir} %{buildroot}%{_libdir}/gstreamer-1.0/libgsticamerasrc.so
patchelf --set-rpath %{_rundir} %{buildroot}%{_libdir}/libgsticamerainterface-1.0.so.1.0.0

%files
%license LICENSE
%dir %{_libdir}/gstreamer-1.0
%{_libdir}/gstreamer-1.0/*
%{_libdir}/libgsticamerainterface-1.0.so
%{_libdir}/libgsticamerainterface-1.0.so.1
%{_libdir}/libgsticamerainterface-1.0.so.1.0.0

%files devel
%dir %{_includedir}/icamerasrc
%dir %{_includedir}/icamerasrc/interfaces
%dir %{_includedir}/gstreamer-1.0
%dir %{_includedir}/gstreamer-1.0/gst
%{_includedir}/icamerasrc/interfaces/*
%{_includedir}/gstreamer-1.0/gst/*
%{_libdir}/pkgconfig/*

%changelog
* Tue Dec 20 2022 Kate Hsuan <hpa@redhat.com> - 0.0-3.20220926git3b7cdb9
- Modify library path for build

* Tue Dec 20 2022 Kate Hsuan <hpa@redhat.com> - 0.0-2.20220926git3b7cdb9
- File placement fixes
- Format for style fixes

* Tue Nov 29 2022 Kate Hsuan <hpa@redhat.com> - 0.0-1.20220926git3b7cdb9
- First commit

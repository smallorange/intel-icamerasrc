%global commit 3b7cdb93071360aacebb4e808ee71bb47cf90b30
%global commitdate 20220926
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           icamerasrc
Summary:        Gstreamer plugin for Intel IPU6
Version:        0.0
Release:        1.%{commitdate}git%{shortcommit}%{?dist}
License:        GNU

Source0: https://github.com/intel/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  chrpath
BuildRequires:  ipu6-camera-bins
BuildRequires:  ipu6-camera-bins-devel
BuildRequires:  ipu6-camera-hal
BuildRequires:  ipu6-camera-hal-devel
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  libdrm-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

Requires:       ipu6-camera-bins
Requires:       ipu6-camera-hal
Requires:       gstreamer1-plugins-base
Requires:       libdrm

ExclusiveArch:  x86_64

%description
This package provide the gstreamer plugin for MIPI cameras.

%package devel
Summary:        Gstreamer plugin development header files for Intel IPU6

%description devel
This provides the necessary header files for IPU6 Gstreamer plugin development.

Requires:       ipu6-camera-bins-devel
Requires:       ipu6-camera-hal-devel

%prep

%setup -q -n %{name}-%{commit}

%build
export CHROME_SLIM_CAMHAL=ON
export STRIP_VIRTUAL_CHANNEL_CAMHAL=ON
export PKG_CONFIG_PATH="/usr/lib64/ipu6ep/pkgconfig"
./autogen.sh
make -j`nproc`

%install

mkdir -p %{buildroot}%{_libdir}/gstreamer-1.0
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}/icamerasrc/interfaces
mkdir -p %{buildroot}%{_includedir}/gstreamer-1.0/gst
cp -rp src/.libs/*.so* %{buildroot}%{_libdir}/gstreamer-1.0
cp -rp src/*.la %{buildroot}%{_libdir}/gstreamer-1.0
cp -rp src/interfaces/.libs/*.so* %{buildroot}%{_libdir}
cp -rp src/interfaces/*.la %{buildroot}%{_libdir}
cp -rp src/interfaces/*.h %{buildroot}%{_includedir}/icamerasrc/interfaces
cp -rp src/interfaces/*.h %{buildroot}%{_includedir}/gstreamer-1.0/gst
cp -rp src/gst/gstcamerasrcmeta.h %{buildroot}%{_includedir}/gstreamer-1.0/gst
sed 's/^prefix=\/.\+$/prefix=\/usr/' libgsticamerasrc.pc > %{buildroot}%{_libdir}/pkgconfig/libgsticamerasrc.pc

chrpath -d %{buildroot}%{_libdir}/gstreamer-1.0/libgsticamerasrc.so

%files
%license LICENSE
%{_libdir}/gstreamer-1.0/*
%{_libdir}/*

%files devel
%{_includedir}/icamerasrc/interfaces/*
%{_includedir}/gstreamer-1.0/gst/*

%changelog
* Tue Nov 29 2022 Kate Hsuan <hpa@redhat.com> - 0.0-1.20220926git3b7cdb9
- First commit
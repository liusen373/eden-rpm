# 当启用 PGO 时，改用 clang 编译器
%bcond_with pgo

# 默认目标架构为 x86-64-v3，指定此标志时使用 -march=native -mtune=native
%bcond_with native

Name:           eden
Version:        0.0.4
Release:        1%{?dist}
Summary:        High-performance Nintendo Switch emulator forked from yuzu

License:        GPL-3.0-or-later
URL:            https://eden-emu.dev/
Source0:        https://github.com/eden-emulator/Releases/releases/download/v0.0.4/Eden-Source-v0.0.4.tar.zst   
Source1:        https://github.com/Eden-CI/PGO/releases/latest/download/eden.profdata

BuildRequires:  clang lld llvm-devel
BuildRequires:  gcc gcc-c++ mold libusb1-devel
BuildRequires:  cmake ninja-build glslang ffmpeg-free-devel spirv-tools-devel
BuildRequires:  openssl-devel fmt-devel json-devel lz4-devel opus-devel boost-devel sdl2-compat-devel systemd-devel
BuildRequires:  qt6-qtbase-devel qt6-qtbase-private-devel qt6-qtmultimedia-devel qt6-qttools-devel qt6-linguist qt6-qtwebengine-devel
BuildRequires:  libtool stb_image-devel stb_image_write-devel stb_image_resize-devel renderdoc-devel gamemode-devel
BuildRequires:  spirv-headers-devel

%description
Eden is an experimental open-source emulator for the Nintendo Switch, built with performance and stability in mind. It is written in C++ with cross-platform support for Windows, Linux, FreeBSD, Solaris, OpenBSD, and Android.

%prep
%autosetup -c


%build

cmake -S . -B build -GNinja \
    -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
    -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
    -DUSE_DISCORD_PRESENCE=ON \
    -DYUZU_USE_CPM=OFF \
    -DCPM_USE_LOCAL_PACKAGES=ON \
    -DYUZU_USE_BUNDLED_FFMPEG=OFF \
    -DYUZU_USE_BUNDLED_SDL2=OFF \
    -DYUZU_USE_EXTERNAL_SDL2=OFF \
    -DYUZU_USE_BUNDLED_QT=OFF \
    -DENABLE_QT_TRANSLATION=ON \
    -DYUZU_USE_QT_MULTIMEDIA=ON \
    -DYUZU_USE_QT_WEB_ENGINE=ON \
    -Dhttplib_FORCE_BUNDLED=ON \
    -DYUZU_TESTS=OFF \
    -DDYNARMIC_TESTS=OFF \
    -DBUILD_TESTING=OFF \
    -DYUZU_USE_FASTER_LD=ON \
    -DYUZU_ENABLE_LTO=ON \
    -DDYNARMIC_ENABLE_LTO=ON \
%if %{with native}
    -DYUZU_BUILD_PRESET="native" \
%endif
%if %{without native}
    -DYUZU_BUILD_PRESET="v3" \
%endif
%if %{with pgo}
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_C_FLAGS="-fprofile-use=%{SOURCE1} -Wno-backend-plugin -Wno-profile-instr-unprofiled -Wno-profile-instr-out-of-date" \
    -DCMAKE_CXX_FLAGS="-fprofile-use=%{SOURCE1} -Wno-backend-plugin -Wno-profile-instr-unprofiled -Wno-profile-instr-out-of-date" \
%endif
    -Wno-dev

cmake --build build

%install
cmake --install build


%files
%license LICENSE.txt
%license LICENSES/*
%{_bindir}/eden
%{_bindir}/eden-cli
%{_bindir}/eden-room
%{_datarootdir}/applications/dev.eden_emu.eden.desktop
%{_datarootdir}/icons/hicolor/scalable/apps/dev.eden_emu.eden.svg
%{_datarootdir}/mime/packages/dev.eden_emu.eden.xml
%{_datarootdir}/metainfo/dev.eden_emu.eden.metainfo.xml


%changelog
* Wed 
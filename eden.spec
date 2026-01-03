# 当启用 PGO 时，改用 clang 编译器
%bcond_with pgo

# Build preset to use. One of: custom, generic, v3, zen2, zen4, native
%if ! %{defined build_preset}
%global build_preset v3
%endif

Name:           eden
Version:        0.0.4
Release:        1%{?dist}
Summary:        High-performance Nintendo Switch emulator forked from yuzu

License:        GPL-3.0-or-later
URL:            https://eden-emu.dev/
Source0:        https://github.com/eden-emulator/Releases/releases/download/v0.0.4/Eden-Source-v0.0.4.tar.zst   
Source1:        https://github.com/Eden-CI/PGO/releases/latest/download/eden.profdata

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mold

BuildRequires:  ninja-build
BuildRequires:  clang
BuildRequires:  lld

BuildRequires:  cmake
BuildRequires:  cmake(LLVM)
BuildRequires:  cmake(Qt6)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(zlib)
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(nlohmann_json)
BuildRequires:  cmake(SPIRV-Headers)
BuildRequires:  cmake(SPIRV-Tools)
BuildRequires:  cmake(SDL2)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6WebEngineCore)
BuildRequires:  cmake(Qt6WebEngineWidgets)

BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(gamemode)
BuildRequires:  pkgconfig(libudev)

BuildRequires:  glslang
BuildRequires:  automake
BuildRequires:  ffmpeg-free-devel 
BuildRequires:  boost-devel 
BuildRequires:  stb_image-devel
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_resize-devel
BuildRequires:  renderdoc-devel 
BuildRequires:  VulkanMemoryAllocator-devel

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
    -DYUZU_BUILD_PRESET=%{build_preset} \
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
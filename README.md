
Eden Emulator RPM Build

> Native Eden client for RPM-based distributions

📦 Install Prebuilt Package

Users can install the prebuilt RPM from [releases](https://github.com/liusen373/eden-rpm/releases) (default optimization: `x86-64-v3`):

```bash
sudo dnf install ./eden-0.0.4-1.fc42.x86_64.rpm
```

> The prebuilt package targets Fedora 42+ systems. For other RPM-based distributions, you have to build eden from source.

🔧 Build from Source

1. Install build dependencies
```bash
sudo dnf group install -y rpm-development-tools c-development development-tools
sudo dnf builddep eden-0.0.4-1.fc42.src.rpm
rpmdev-setuptree
```

1. Basic build
```bash
rpmbuild -rb eden-0.0.4-1.fc42.src.rpm
```

1. Advanced optimizations

| Optimization           | Command                                                      |
| ---------------------- | ------------------------------------------------------------ |
| Compile with Clang     | `rpmbuild --define "toolchain clang" -rb ...`                |
| CPU architecture       | `rpmbuild --define "build_preset zen4" -rb ...`              |
| PGO optimization       | `rpmbuild --with pgo -rb ...` (switches to Clang)            |
| Combined optimizations | `rpmbuild --define "build_preset native" --with pgo -rb ...` |

CPU Presets

| Preset    | Use Case                                               |
| --------- | ------------------------------------------------------ |
| `generic` | Baseline compatibility (widest support)                |
| `v3`      | x86-64-v3 instruction set (default)                    |
| `zen2`    | Optimized for AMD Zen2 architecture                    |
| `zen4`    | Optimized for AMD Zen4 architecture                    |
| `native`  | Maximum optimization for current CPU (less compatible) |

ℹ️ Important Notes
1. Packages built with `native` preset may not run on other CPUs
2. Output RPMs are located at `~/rpmbuild/RPMS/x86_64/`

# CUMM-GPU

This repo is just a fork from `cumm` — [CUDA Matrix Multiply library](https://github.com/FindDefinition/cumm).

## ⬇️ Install

Before you install, you must uninstall all existing versions to avoid conflicts:

```bash
pip uninstall -y cumm cumm-cu128 cumm-cu126 cumm-cu121 
```

For easy installation using prebuilt wheels (example for CUDA 13.0):

```bash
pip install cumm-cu130 --extra-index-url https://ratharog.github.io/cumm-spconv/
```

See [ratharog.github.io/cumm-spconv](https://ratharog.github.io/cumm-spconv/) for prebuilt wheel info and supported CUDA versions.

## 🛠️ Build and install from source

Building from source requires:
- A C++ compiler
- CUDA Toolkit installed (for CUDA support)

### On Linux with CUDA 13.0:

```bash
export CUMM_CUDA_VERSION="13.0"
export CUMM_CUDA_ARCH_LIST="all"
export CUMM_DISABLE_JIT="1"
pip install git+https://github.com/rathaROG/cumm-gpu.git
```

### On Windows with CUDA 13.0 + MSVC 2019 (cmd terminal):

```cmd
git clone https://github.com/rathaROG/cumm-gpu.git
cumm-gpu\tools\msvc_setup.bat
RMDIR /s /q cumm-gpu
SET CUMM_CUDA_VERSION=13.0
SET CUMM_CUDA_ARCH_LIST=all
SET CUMM_DISABLE_JIT=1
pip install git+https://github.com/rathaROG/cumm-gpu.git
```

### On any platform with CPU only:

```bash
pip install git+https://github.com/rathaROG/cumm-gpu.git
```

**Note**: 

- For detailed build logs, add `--verbose` to the `pip install` command.
- On Windows, you can also use the scripts below to build and install from source; feel free to modify:
  - For CUDA 12.8: [install_cumm_cu128.bat](https://github.com/rathaROG/cumm-gpu/blob/main/tools/install_cumm_cu128.bat)
  - For CUDA 13.0: [install_cumm_cu130.bat](https://github.com/rathaROG/cumm-gpu/blob/main/tools/install_cumm_cu130.bat)

## 📝 License

[![LICENSE](https://img.shields.io/badge/LICENSE-Apache_2.0-blue)](LICENSE)

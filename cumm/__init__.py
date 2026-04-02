# Modified by rathaROG in 2026.

# Copyright 2024 Yan Yan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

import pccm
from pccm.utils import project_is_editable, project_is_installed
import os 
import sys
from .__version__ import __version__
from .constants import CUMM_CPU_ONLY_BUILD, CUMM_DISABLE_JIT, PACKAGE_NAME
from cumm.constants import PACKAGE_ROOT
from ccimport import compat
from pathlib import Path 
import importlib.util 
import subprocess


if project_is_installed(PACKAGE_NAME) and project_is_editable(PACKAGE_NAME) and not CUMM_DISABLE_JIT:
    from cumm.csrc.arrayref import ArrayPtr
    from cumm.tensorview_bind import TensorViewBind, AppleMetalImpl
    pccm.builder.build_pybind(
        [ArrayPtr(), TensorViewBind(), AppleMetalImpl()],
        PACKAGE_ROOT / "core_cc",
        namespace_root=PACKAGE_ROOT,
        load_library=False,
        std="c++17" if compat.InMacOS else "c++14",
        verbose=False
    )


def _determine_windows_cuda_dll_dir():
    cuda_dll_paths = []
    res_msgs = []

    # step 1: check pip installed nvidia package (e.g. nvidia-cuda-runtime-cu12)
    try:
        import nvidia 
        from nvidia import cuda_runtime
        from nvidia import cuda_nvrtc
        res = [Path(cuda_runtime.__file__).resolve().parent / "bin", Path(cuda_nvrtc.__file__).resolve().parent / "bin"]
        return res, res_msgs
    except:
        res_msgs.append("\nStep 1: Couldn't find pip NVIDIA CUDA package." \
                        "\n\tWARNING: pip NVIDIA CUDA package doesn't support runtime kernels.")

    # step 2: try to load cuda dll from torch path
    spec = importlib.util.find_spec("torch")
    if spec is not None and spec.origin is not None:
        torch_path = Path(spec.origin).parent
        libdir = torch_path / "lib"
        nvrtc_paths = list(libdir.glob("nvrtc*.dll"))
        cudart_paths = list(libdir.glob("cudart*.dll"))
        if cudart_paths and nvrtc_paths:
            cuda_dll_paths = [str(torch_path / "lib")]
            return cuda_dll_paths, res_msgs
    res_msgs.append("\nStep 2: Couldn't find PyTorch CUDA libraries.")

    # step 3: check conda installed nvidia package (e.g. conda install cuda -c nvidia) 
    # use nvcc path to find cuda dll path
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        try:
            nvcc_path = subprocess.check_output(["powershell", "-command", "(Get-Command nvcc).Source"]).decode("utf-8").strip()
            conda_prefix_norm = os.path.abspath(conda_prefix).lower()
            nvcc_path_norm = os.path.abspath(nvcc_path).lower()
            if nvcc_path_norm.startswith(conda_prefix_norm + os.sep):
            # if Path(conda_prefix) in Path(nvcc_path).parents:
                nvcc_root = Path(nvcc_path).parent.parent
                lib = nvcc_root / "lib"
                include = nvcc_root / "include"
                if lib.exists() and include.exists():
                    cuda_dll_paths = [nvcc_root / "bin"]
                    if (Path(nvcc_root) / "bin" / "x64").exists():
                        cuda_dll_paths.append(Path(nvcc_root) / "bin" / "x64")
                    return cuda_dll_paths, res_msgs
        except:
            pass
    res_msgs.append("\nStep 3: Couldn't find conda NVIDIA CUDA package.")

    # step 4: try to load cuda dll from system installed cuda path
    cuda_path = os.getenv("CUDA_PATH", None)
    if cuda_path and (Path(cuda_path)).exists():
        cuda_dll_paths = [Path(cuda_path) / "bin"]
        if (Path(cuda_path) / "bin" / "x64").exists():
            cuda_dll_paths.append(Path(cuda_path) / "bin" / "x64")
        res_msgs.append(f"\nStep 4: Found CUDA Toolkit in system env CUDA_PATH.")
        return cuda_dll_paths, res_msgs

    res_msgs.append("\nStep 4: Couldn't find system installed CUDA Toolkit.")

    return cuda_dll_paths, res_msgs


if compat.InWindows:
    try:
        from cumm import core_cc
    except:
        cuda_dll_paths, msgs = _determine_windows_cuda_dll_dir()
        
        if not cuda_dll_paths:
            print("\n".join(msgs), file=sys.stderr)
            raise RuntimeError("Couldn't find cuda libraries, install cuda first.")
        for p in cuda_dll_paths:
            os.add_dll_directory(str(p))
        try:
            from cumm import core_cc
        except:
            if cuda_dll_paths:
                print("\nCUMM found CUDA *.dll here:", cuda_dll_paths, file=sys.stderr)
                print("\n*** BUT couldn't load due to version mismatched? ***", file=sys.stderr)
            else:
                print("\nCUMM couldn't find any CUDA *.dll in the system.", file=sys.stderr)
            print("\n".join(msgs), file=sys.stderr)
            print("\n*** Please install CUMM/CUDA with correct version. ***\n", file=sys.stderr)
            raise 

@ECHO OFF
CHCP 65001 >NUL 2>&1
SETLOCAL
CD /d %~dp0
SET "PYTHONWARNINGS=ignore"
RMDIR /s /q cumm-gpu >NUL 2>&1
ECHO.
ECHO [----------------------------------------------------------------------------------]
ECHO [                  Install CUMM (CUDA 13.0) by rathaROG - v0.0.2                   ]
ECHO [----------------------------------------------------------------------------------]
ECHO.
ECHO 🚨 You must manually install Microsoft Visual Studio 2019+ with C++ !
ECHO 🌐 URL: https://visualstudio.microsoft.com/downloads/
ECHO.
ECHO 🚨 You must manually install CUDA 13.0 Toolkit (and cuDNN if needed) !
ECHO 🌐 URL: https://developer.nvidia.com/cuda-13-0-2-download-archive
ECHO.
PAUSE
ECHO.
ECHO [INFO] Installing the latest PyTorch for CUDA 13.0 ...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130 >NUL 2>&1
ECHO [DONE] PyTorch installed. ✅
ECHO.
ECHO [INFO] Installing build requirements ...
pip install -U pybind11 pccm ccimport ninja build wheel >NUL 2>&1
ECHO [DONE] All build requirements installed. ✅
ECHO.
ECHO [INFO] Uninstalling existing cumm ...
pip uninstall -y cumm cumm-cu130 cumm-cu128 cumm-cu126 cumm-cu121 >NUL 2>&1
ECHO [DONE] All cumm uninstalled. ✅
ECHO.
ECHO [INFO] Cloning cumm-gpu repo ...
git clone https://github.com/rathaROG/cumm-gpu.git >NUL 2>&1
CD cumm-gpu
SET CUMM_CUDA_VERSION=13.0
SET CUMM_CUDA_ARCH_LIST=all
SET CUMM_DISABLE_JIT=1
SET CUMM_NVRTC_STD=c++17
ECHO [INFO] Activating MSVC environment for cumm ...
call tools\msvc_setup.bat
ECHO [INFO] Building cumm-gpu from source ...
python -m build --wheel --skip-dependency-check --no-isolation >NUL 2>&1
IF EXIST dist\*.whl (
    FOR %%F IN (dist\*.whl) DO pip install "%%F" >NUL 2>&1
    CD ..
    ECHO [DONE] spconv-gpu built and installed. ✅
) ELSE (
    ECHO.
    ECHO [FAIL] cumm-gpu build did not success! ❌
    GOTO BUILDFAIL
)
ECHO.
ECHO [INFO] Testing import
python -c "import cumm;print(cumm.__version__);print(cumm.__file__)"
ECHO [DONE] Test step finished. ✅
ECHO.
ECHO [INFO] Cleaning up ...
RMDIR /s /q cumm-gpu >NUL 2>&1
ECHO.
ECHO [----------------------------------------------------------------------------------]
ECHO [                                     COMPLETE                                     ]
ECHO [----------------------------------------------------------------------------------]
PAUSE
ENDLOCAL
GOTO END

:BUILDFAIL
ECHO.
ECHO [----------------------------------------------------------------------------------]
ECHO [                                       FAIL                                       ]
ECHO [----------------------------------------------------------------------------------]
ECHO.
CD ..
RMDIR /s /q cumm-gpu >NUL 2>&1
PAUSE
ENDLOCAL
exit /b 1

:END

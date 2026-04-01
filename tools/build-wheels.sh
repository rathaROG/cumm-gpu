#!/bin/bash

# Modified by rathaROG in 2026.

set -euxo pipefail

PLAT=$(cat /etc/manylinux-platform-tag)

function repair_wheel {
  wheel="$1"
  outpath="$2"
  if ! auditwheel show "$wheel"; then
    echo "Skipping non-platform wheel $wheel"
  else
    auditwheel repair "$wheel" --plat "$PLAT" -w "$outpath"
  fi
}

export CUMM_DISABLE_JIT="1"
export CUMM_CUDA_ARCH_LIST="all"

VERSIONS=$(echo "$BUILD_PYTHON_VERSIONS" | tr -d "[]'," )
for pv in $VERSIONS; do
  py_tag="cp${pv/./}"
  PYBIN="/opt/python/${py_tag}-${py_tag}/bin"
  "${PYBIN}/pip" install --upgrade pip
  "${PYBIN}/pip" install --upgrade setuptools build wheel
  "${PYBIN}/python" -m build --skip-dependency-check --sdist --wheel --outdir /io/wheelhouse_tmp /io/
done

# Bundle external shared libraries into the wheels
for whl in /io/wheelhouse_tmp/*.whl; do
  repair_wheel "$whl" /io/dist
done

echo "Copying source distributions *.tar.gz to /io/dist ..."
find /io/wheelhouse_tmp -maxdepth 1 -type f -name "*.tar.gz" -exec cp {} /io/dist/ \;

rm -rf /io/wheelhouse_tmp

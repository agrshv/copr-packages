#!/usr/bin/env bash
# Build a source RPM from a package directory.
#
# Usage: scripts/build-srpm.sh <package-dir>
set -euo pipefail

pkgdir=${1:?usage: build-srpm.sh <package-dir>}
pkgdir=$(realpath "$pkgdir")

shopt -s nullglob
specs=("$pkgdir"/*.spec)
shopt -u nullglob
[[ ${#specs[@]} -eq 1 ]] || { echo "expected exactly one .spec in $pkgdir" >&2; exit 1; }
spec=${specs[0]}

rpmbuild -bs "$spec" --define "_srcrpmdir $(rpm --eval '%{_srcrpmdir}')"

srpm=$(rpmspec -q --srpm --qf '%{name}-%{version}-%{release}.src.rpm\n' "$spec")
echo "$(rpm --eval '%{_srcrpmdir}')/$srpm"

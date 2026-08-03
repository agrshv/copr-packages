#!/usr/bin/env bash
# Fetch upstream sources and build a vendored-dependency tarball.
#
# COPR/mock builders run without network access, so Go modules cannot be
# downloaded at build time. We vendor them here and ship the result as Source1.
#
# Usage: scripts/prepare-sources.sh <package-dir>
set -euo pipefail

pkgdir=${1:?usage: prepare-sources.sh <package-dir>}
pkgdir=$(realpath "$pkgdir")

shopt -s nullglob
specs=("$pkgdir"/*.spec)
shopt -u nullglob
[[ ${#specs[@]} -eq 1 ]] || { echo "expected exactly one .spec in $pkgdir" >&2; exit 1; }
spec=${specs[0]}

sourcedir=$(rpm --eval '%{_sourcedir}')
mkdir -p "$sourcedir"

read -r name version < <(rpmspec -q --srpm --qf '%{name} %{version}\n' "$spec")
echo "==> $name $version"

# spectool only fetches sources that are URLs; local Source entries are skipped.
echo "==> fetching upstream tarball"
spectool -g -S -C "$sourcedir" "$spec"

tarball=$(rpmspec -P "$spec" | awk '/^Source0:/ {print $2}')
tarball="$sourcedir/$(basename "$tarball")"
[[ -f $tarball ]] || { echo "Source0 not found: $tarball" >&2; exit 1; }

vendor_tarball=$(rpmspec -P "$spec" | awk '/^Source1:/ {print $2}')
if [[ -z $vendor_tarball ]]; then
  echo "==> no Source1: upstream ships vendor/ in the archive, nothing to do"
  ls -lh "$tarball"
  exit 0
fi
vendor_tarball="$sourcedir/$(basename "$vendor_tarball")"

workdir=$(mktemp -d)
# Go's module cache is deliberately read-only, so make the tree writable before
# removing it. The cache itself is left in its default shared location so that
# repeated runs do not re-download the whole dependency graph.
trap 'chmod -R u+w "$workdir" 2>/dev/null || true; rm -rf "$workdir"' EXIT

echo "==> extracting"
mkdir -p "$workdir/src"
tar -xf "$tarball" -C "$workdir/src" --strip-components=1

echo "==> vendoring Go modules (needs network)"
(
  cd "$workdir/src"
  export GOFLAGS=-mod=mod
  go mod vendor
)

[[ -d $workdir/src/vendor ]] || { echo "go mod vendor produced no vendor/ dir" >&2; exit 1; }

echo "==> packing $(basename "$vendor_tarball")"
tar -czf "$vendor_tarball" -C "$workdir/src" vendor

ls -lh "$tarball" "$vendor_tarball"

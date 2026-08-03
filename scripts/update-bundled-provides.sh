#!/usr/bin/env bash
# Rewrite the bundled-dependency block of a spec in place.
#
# The block is delimited by these two marker lines, which must already exist:
#   # BEGIN bundled provides
#   # END bundled provides
#
# Usage: scripts/update-bundled-provides.sh <package-dir> <extracted-source-dir>
set -euo pipefail

pkgdir=${1:?usage: update-bundled-provides.sh <package-dir> <source-dir>}
srcdir=${2:?usage: update-bundled-provides.sh <package-dir> <source-dir>}
here=$(dirname "$(realpath "$0")")

shopt -s nullglob
specs=("$(realpath "$pkgdir")"/*.spec)
shopt -u nullglob
[[ ${#specs[@]} -eq 1 ]] || { echo "expected exactly one .spec in $pkgdir" >&2; exit 1; }
spec=${specs[0]}

grep -q '^# BEGIN bundled provides$' "$spec" || { echo "missing BEGIN marker in $spec" >&2; exit 1; }
grep -q '^# END bundled provides$' "$spec"   || { echo "missing END marker in $spec" >&2; exit 1; }

block=$(mktemp); trap 'rm -f "$block"' EXIT
{
  echo "# Vendored dependencies, per Fedora's bundling policy."
  echo "# Regenerate with: scripts/update-bundled-provides.sh <package-dir> <source-dir>"
  "$here/gen-bundled-provides.sh" "$srcdir"
} > "$block"

awk -v blockfile="$block" '
  /^# BEGIN bundled provides$/ {
    print
    while ((getline line < blockfile) > 0) print line
    skip = 1
    next
  }
  /^# END bundled provides$/ { skip = 0 }
  !skip
' "$spec" > "$spec.new"

mv "$spec.new" "$spec"
echo "==> $(grep -c 'bundled(golang' "$spec") bundled provides written to $spec"

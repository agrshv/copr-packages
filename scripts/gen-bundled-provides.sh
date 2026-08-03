#!/usr/bin/env bash
# Emit "Provides: bundled(golang(...))" lines from a vendor/modules.txt.
#
# Fedora's bundling policy requires a package that ships vendored dependencies
# to declare each one, so that a CVE in a dependency can be traced back to the
# packages carrying it.
#
# Usage: scripts/gen-bundled-provides.sh <path-to-vendor/modules.txt>
#        scripts/gen-bundled-provides.sh <extracted-source-dir>
set -euo pipefail

target=${1:?usage: gen-bundled-provides.sh <modules.txt|source-dir>}
[[ -d $target ]] && target="$target/vendor/modules.txt"
[[ -f $target ]] || { echo "no modules.txt at $target" >&2; exit 1; }

# Module lines look like "# github.com/foo/bar v1.2.3" or
# "# github.com/foo/bar v1.2.3 => github.com/fork/bar v1.2.4"; markers such as
# "## explicit" and bare package paths are skipped.
awk '
  /^# / {
    path = $2; ver = $3
    # For replaced modules, credit the module actually vendored.
    if ($4 == "=>") { path = $5; ver = ($6 == "" ? ver : $6) }
    if (ver == "" || ver !~ /^v/) next
    sub(/^v/, "", ver)
    # RPM versions cannot contain "-"; pseudo-versions and prereleases use it.
    gsub(/-/, "_", ver)
    if (seen[path]++) next
    printf "Provides:          bundled(golang(%s)) = %s\n", path, ver
  }
' "$target" | sort -u

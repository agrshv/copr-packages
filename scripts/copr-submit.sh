#!/usr/bin/env bash
# Submit a package's SRPM to its COPR project.
#
# Usage: scripts/copr-submit.sh <package-dir> [copr-project]
#
# The project defaults to the package directory name under the account
# configured in ~/.config/copr. Override with a second argument or $COPR_OWNER.
set -euo pipefail

pkgdir=${1:?usage: copr-submit.sh <package-dir> [copr-project]}
pkgdir=$(realpath "$pkgdir")

here=$(dirname "$(realpath "$0")")
srpm=$("$here/build-srpm.sh" "$pkgdir" | tail -1)

project=${2:-${COPR_OWNER:?set COPR_OWNER to your FAS username or pass a project}/$(basename "$pkgdir")}

echo "==> submitting $(basename "$srpm") to $project"
copr-cli build "$project" "$srpm"

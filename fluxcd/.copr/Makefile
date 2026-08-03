# COPR source-build recipe for the fluxcd package.
#
# COPR invokes this as:
#   make -f .copr/Makefile srpm outdir=<dir> spec=<path>
#
# Why this exists instead of the simpler "rpkg" method used for ghorg: flux does
# not commit vendor/, so the vendored dependency tarball referenced as Source1
# has to be produced rather than downloaded. This source phase is the only part
# of a COPR build with network access — the RPM build that follows runs offline,
# which is exactly why the dependencies must be baked into a tarball here.

srpm:
	dnf -y install golang rpm-build rpmdevtools
	rpmdev-setuptree
	# Downloads Source0 and Source2, then vendors the Go modules into Source1.
	../scripts/prepare-sources.sh .
	rpmbuild -bs fluxcd.spec --define "_srcrpmdir $(outdir)"

.PHONY: srpm

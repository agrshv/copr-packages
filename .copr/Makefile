# COPR source-build recipe for packages using the "make_srpm" method.
#
# COPR always reads this file from the repository root, but runs make with the
# working directory set to the package's subdirectory, and passes:
#   outdir=<where to write the .src.rpm>  spec=<absolute path to the .spec>
# So this recipe stays package-agnostic and works for any subdirectory.
#
# Why any of this is needed instead of the simpler "rpkg" method used for ghorg:
# a package whose Source1 is a vendored-dependency tarball cannot use rpkg,
# because that tarball has to be produced rather than downloaded. This source
# phase is the only stage of a COPR build with network access — the RPM build
# that follows runs offline, which is precisely why the dependencies must be
# baked into a tarball here.

srpm:
	dnf -y install golang rpm-build rpmdevtools
	rpmdev-setuptree
	# Downloads the remote sources and vendors the Go modules into Source1.
	../scripts/prepare-sources.sh .
	rpmbuild -bs "$(spec)" --define "_srcrpmdir $(outdir)"

.PHONY: srpm

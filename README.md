# copr-packages

RPM packaging for tools that are not in the Fedora repositories, built and
published through [COPR](https://copr.fedorainfracloud.org/).

| Package | Binary | Upstream | Version | COPR project | Source method |
| --- | --- | --- | --- | --- | --- |
| `ghorg` | `ghorg` | [gabrie30/ghorg](https://github.com/gabrie30/ghorg) | 1.11.14 | `ghorg` | `rpkg` |
| `fluxcd` | `flux` | [fluxcd/flux2](https://github.com/fluxcd/flux2) | 2.9.3 | `fluxcd` | `make_srpm` |

The `fluxcd` package installs a binary called `flux`, because that is what every
upstream tutorial, script and manifest invokes.

Each tool gets its own COPR project so it can be enabled independently, but the
packaging sources share one repository because the helper scripts are identical.

First-time COPR account, token and project setup: see
[docs/copr-setup.md](docs/copr-setup.md).

## Layout

```
ghorg/ghorg.spec      # spec files, one directory per package
fluxcd/flux.spec
scripts/              # shared helpers, all take a package directory as argument
docs/copr-setup.md
```

## Building

Sources live in `~/rpmbuild/SOURCES` (create the tree once with
`rpmdev-setuptree`).

```bash
# Fetch the upstream tarball, and build a vendored-deps tarball if the spec
# declares a Source1 for one.
./scripts/prepare-sources.sh ghorg

# Build binary RPMs locally to check the spec.
rpmbuild -bb ghorg/ghorg.spec

# Build just the SRPM, which is what COPR consumes.
./scripts/build-srpm.sh ghorg

# Build the SRPM and submit it to COPR in one step.
COPR_OWNER=<fas-username> ./scripts/copr-submit.sh ghorg
```

A local build in `mock` reproduces the COPR builder much more faithfully than
`rpmbuild` does — in particular it has no network and a clean `$HOME` — and is
worth doing before spending COPR build time:

```bash
mock -r fedora-44-x86_64 ~/rpmbuild/SRPMS/ghorg-1.11.14-1.fc44.src.rpm
```

## Why dependencies are vendored

COPR builders run without network access, so Go modules cannot be downloaded
during the build. There are two cases:

- **ghorg** commits `vendor/` upstream and ships it in the release archive, so
  the tarball is already self-contained. Nothing extra is needed, and COPR can
  build it with the default `rpkg` method, which just downloads `Source0`.
- **fluxcd** does not, so its `Source1` is a vendored-deps tarball that has to be
  *produced* rather than downloaded. That is why it uses the `make_srpm` method
  and carries a [`.copr/Makefile`](fluxcd/.copr/Makefile): COPR's source phase is
  the only part of the build with network access, so the vendoring happens there.
  `scripts/prepare-sources.sh` is what runs, both locally and on COPR.

Both specs set `GOPROXY=off` and `GOFLAGS=-mod=vendor`, and assert that
`vendor/modules.txt` exists in `%prep`, so a build that would otherwise reach
for the network fails loudly instead of silently.

Fedora's bundling policy requires every vendored dependency to be declared with
a `Provides: bundled(golang(...))` line, so that a CVE in a dependency can be
traced to the packages carrying it. Regenerate that block after a version bump:

```bash
./scripts/update-bundled-provides.sh ghorg /path/to/extracted-source
```

The block is delimited by `# BEGIN bundled provides` / `# END bundled provides`
markers in the spec and is rewritten in place.

## Updating to a new upstream release

1. Bump `Version:` and reset `Release:` to `1%{?dist}` in the spec.
2. Add a `%changelog` entry.
3. `./scripts/prepare-sources.sh <pkg>` to fetch the new tarball.
4. Regenerate the bundled provides from the new source tree (see above).
5. `rpmbuild -bb <pkg>/<pkg>.spec`, then submit.

## Notes

- `%gobuild` defaults `GO111MODULE` to `off`, which makes Go ignore `go.mod` and
  the vendor tree entirely. Both specs set `%global gomodulesmode GO111MODULE=on`
  to prevent that.
- Upstream release ldflags often include `-s -w`, which strips the symbol table
  and DWARF data. The specs deliberately omit those so the `-debuginfo`
  subpackage is usable.
- `fluxcd` embeds the Flux controller manifests with `go:embed`. Upstream
  generates them with `manifests/scripts/bundle.sh`, which runs `kustomize build`
  over kustomizations whose resources are remote GitHub release URLs — so it
  cannot run in an offline builder. The spec instead uses the `manifests.tar.gz`
  release asset, which is the published output of that same script.
- The `flux` binary name is also used by the unrelated Flux Framework HPC
  resource manager. Nothing in Fedora currently ships `/usr/bin/flux`, but
  enabling a third-party COPR that packages `flux-core` alongside this one would
  produce a file conflict.

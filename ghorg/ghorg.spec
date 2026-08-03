%global goipath     github.com/gabrie30/ghorg
%global forgeurl    https://github.com/gabrie30/ghorg
%global tag         v%{version}

# Upstream commits vendor/ and ships it in the release archive, so the build is
# fully offline. Enable module mode explicitly: %%gobuild defaults GO111MODULE
# to "off", which would ignore go.mod and the vendor directory entirely.
%global gomodulesmode GO111MODULE=on

Name:               ghorg
Version:            1.11.14
Release:            1%{?dist}
Summary:            Clone and keep in sync every repository in a Git organization

License:            Apache-2.0
URL:                %{forgeurl}
Source0:            %{forgeurl}/archive/refs/tags/%{tag}/%{name}-%{version}.tar.gz

BuildRequires:      golang >= 1.26
BuildRequires:      git-core

# ghorg shells out to git for every clone and pull.
Requires:           git-core >= 2.19.0

# BEGIN bundled provides
# Vendored dependencies, per Fedora's bundling policy.
# Regenerate with: scripts/update-bundled-provides.sh <package-dir> <source-dir>
Provides:          bundled(golang(code.gitea.io/sdk/gitea)) = 0.25.1
Provides:          bundled(golang(github.com/42wim/httpsig)) = 1.2.4
Provides:          bundled(golang(github.com/alecthomas/chroma)) = 0.10.0
Provides:          bundled(golang(github.com/bradleyfalzon/ghinstallation/v2)) = 2.19.0
Provides:          bundled(golang(github.com/briandowns/spinner)) = 1.23.2
Provides:          bundled(golang(github.com/clipperhouse/uax29/v2)) = 2.7.0
Provides:          bundled(golang(github.com/davecgh/go-spew)) = 1.1.2_0.20180830191138_d8f796af33cc
Provides:          bundled(golang(github.com/davidmz/go-pageant)) = 1.0.2
Provides:          bundled(golang(github.com/disintegration/imaging)) = 1.6.3_0.20201218193011_d40f48ce0f09
Provides:          bundled(golang(github.com/dlclark/regexp2)) = 1.12.0
Provides:          bundled(golang(github.com/eliukblau/pixterm/pkg/ansimage)) = 0.0.0_20191210081756_9fb6cf8c2f75
Provides:          bundled(golang(github.com/fatih/color)) = 1.19.0
Provides:          bundled(golang(github.com/fsnotify/fsnotify)) = 1.9.0
Provides:          bundled(golang(github.com/go-fed/httpsig)) = 1.1.0
Provides:          bundled(golang(github.com/golang-jwt/jwt/v4)) = 4.5.2
Provides:          bundled(golang(github.com/gomarkdown/markdown)) = 0.0.0_20260417124207_7d523f7318df
Provides:          bundled(golang(github.com/google/go-github/v72)) = 72.0.0
Provides:          bundled(golang(github.com/google/go-github/v88)) = 88.0.0
Provides:          bundled(golang(github.com/google/go-querystring)) = 1.2.0
Provides:          bundled(golang(github.com/go-viper/mapstructure/v2)) = 2.4.0
Provides:          bundled(golang(github.com/hashicorp/go-cleanhttp)) = 0.5.2
Provides:          bundled(golang(github.com/hashicorp/go-retryablehttp)) = 0.7.8
Provides:          bundled(golang(github.com/hashicorp/go-version)) = 1.9.0
Provides:          bundled(golang(github.com/inconshreveable/mousetrap)) = 1.1.0
Provides:          bundled(golang(github.com/Klaus-Tockloth/go-term-markdown)) = 0.0.0_20250129073703_91600624167c
Provides:          bundled(golang(github.com/korovkin/limiter)) = 0.0.0_20220422174850_01f593e64cf7
Provides:          bundled(golang(github.com/ktrysmt/go-bitbucket)) = 0.10.0
Provides:          bundled(golang(github.com/kyokomi/emoji/v2)) = 2.2.13
Provides:          bundled(golang(github.com/lucasb-eyer/go-colorful)) = 1.4.0
Provides:          bundled(golang(github.com/mattn/go-colorable)) = 0.1.14
Provides:          bundled(golang(github.com/mattn/go-isatty)) = 0.0.22
Provides:          bundled(golang(github.com/mattn/go-runewidth)) = 0.0.23
Provides:          bundled(golang(github.com/MichaelMure/go-term-text)) = 0.3.1
Provides:          bundled(golang(github.com/mitchellh/go-homedir)) = 1.1.0
Provides:          bundled(golang(github.com/mitchellh/mapstructure)) = 1.5.0
Provides:          bundled(golang(github.com/pelletier/go-toml/v2)) = 2.2.4
Provides:          bundled(golang(github.com/sagikazarmark/locafero)) = 0.11.0
Provides:          bundled(golang(github.com/sourcegraph/conc)) = 0.3.1_0.20240121214520_5f936abd7ae8
Provides:          bundled(golang(github.com/spf13/afero)) = 1.15.0
Provides:          bundled(golang(github.com/spf13/cast)) = 1.10.0
Provides:          bundled(golang(github.com/spf13/cobra)) = 1.10.2
Provides:          bundled(golang(github.com/spf13/pflag)) = 1.0.10
Provides:          bundled(golang(github.com/spf13/viper)) = 1.21.0
Provides:          bundled(golang(github.com/subosito/gotenv)) = 1.6.0
Provides:          bundled(golang(gitlab.com/gitlab-org/api/client-go)) = 1.46.0
Provides:          bundled(golang(golang.org/x/crypto)) = 0.52.0
Provides:          bundled(golang(golang.org/x/image)) = 0.41.0
Provides:          bundled(golang(golang.org/x/net)) = 0.55.0
Provides:          bundled(golang(golang.org/x/oauth2)) = 0.36.0
Provides:          bundled(golang(golang.org/x/sys)) = 0.45.0
Provides:          bundled(golang(golang.org/x/term)) = 0.43.0
Provides:          bundled(golang(golang.org/x/text)) = 0.37.0
Provides:          bundled(golang(golang.org/x/time)) = 0.14.0
Provides:          bundled(golang(gopkg.in/yaml.v2)) = 2.4.0
Provides:          bundled(golang(go.yaml.in/yaml/v3)) = 3.0.4
# END bundled provides

%description
ghorg clones or pulls every repository in a GitHub, GitLab, Bitbucket, Gitea or
Codeberg organization or user account into a single directory, and can be re-run
to keep that directory in sync. It is aimed at code search, backups, and
reviewing changes across many repositories at once.

Configuration lives in ~/.config/ghorg/conf.yaml; see the sample configuration
in %{_datadir}/%{name} for the available settings.

%prep
%autosetup -n %{name}-%{version}

# Fail loudly rather than silently attempting a network fetch mid-build.
test -f vendor/modules.txt

%build
export GOPROXY=off
export GOFLAGS="-mod=vendor"
%gobuild -o _bin/%{name} .

# cobra registers a "completion" subcommand, so the shell completions can be
# generated from the binary we just built rather than hand-maintained.
for shell in bash zsh fish; do
  ./_bin/%{name} completion $shell > %{name}.$shell
done

%install
install -Dpm 0755 _bin/%{name} %{buildroot}%{_bindir}/%{name}

install -Dpm 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -Dpm 0644 %{name}.zsh  %{buildroot}%{zsh_completions_dir}/_%{name}
install -Dpm 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

install -Dpm 0644 sample-conf.yaml    %{buildroot}%{_datadir}/%{name}/sample-conf.yaml
install -Dpm 0644 sample-reclone.yaml %{buildroot}%{_datadir}/%{name}/sample-reclone.yaml

%check
export GOPROXY=off
export GOFLAGS="-mod=vendor"

# TestDefaultSettings calls Execute(), which loads ~/.config/ghorg/conf.yaml and
# exports its keys to the environment, then asserts the values are upstream's
# defaults. Point HOME at an empty directory so a config file on the build host
# cannot fail the test.
export HOME="$(mktemp -d)"
export XDG_CONFIG_HOME="$HOME/.config"

# The scripts/ directory holds integration tests that need live SCM
# credentials; the Go unit tests are self-contained.
%gotest ./...

%files
%license LICENSE
%doc README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/sample-conf.yaml
%{_datadir}/%{name}/sample-reclone.yaml

%changelog
* Mon Aug 03 2026 Anton Groshev <anton@agrshv.dev> - 1.11.14-1
- Initial package

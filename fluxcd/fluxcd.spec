%global goipath      github.com/fluxcd/flux2/v2
%global forgeurl     https://github.com/fluxcd/flux2
%global tag          v%{version}
# The GitHub archive unpacks to flux2-%%{version}.
%global archivedir   flux2-%{version}
# The package is named fluxcd, but the binary it installs is "flux" — that is
# what every upstream tutorial, script and manifest invokes.
%global cliname      flux

# %%gobuild defaults GO111MODULE to "off", which would ignore go.mod and the
# vendored dependency tree entirely.
%global gomodulesmode GO111MODULE=on

Name:                fluxcd
Version:             2.9.3
Release:             1%{?dist}
Summary:             Command line tool for Flux, the GitOps toolkit for Kubernetes

License:             Apache-2.0
URL:                 %{forgeurl}
Source0:             %{forgeurl}/archive/refs/tags/%{tag}/%{name}-%{version}.tar.gz
# Upstream does not commit vendor/, and COPR builders have no network access.
# Generate with: scripts/prepare-sources.sh fluxcd
Source1:             %{name}-%{version}-vendor.tar.gz
# cmd/flux embeds the controller manifests via go:embed, so they must exist
# before the build. Upstream generates them with manifests/scripts/bundle.sh,
# but that runs "kustomize build" over kustomizations whose resources are remote
# GitHub release URLs — unavailable in an offline builder. This release asset is
# the published output of that same script.
Source2:             %{forgeurl}/releases/download/%{tag}/manifests.tar.gz#/%{name}-%{version}-manifests.tar.gz

BuildRequires:       golang >= 1.26
# The golang package does not depend on go-rpm-macros, so without this
# %%gobuild is passed through unexpanded and the build fails in a clean
# buildroot even though it works on a developer machine.
BuildRequires:       go-rpm-macros

# Nothing is required at runtime: flux speaks to the Kubernetes API directly
# rather than shelling out to kubectl.

# BEGIN bundled provides
# Vendored dependencies, per Fedora's bundling policy.
# Regenerate with: scripts/update-bundled-provides.sh <package-dir> <source-dir>
Provides:          bundled(golang(cloud.google.com/go/auth)) = 0.20.0
Provides:          bundled(golang(cloud.google.com/go/auth/oauth2adapt)) = 0.2.8
Provides:          bundled(golang(cloud.google.com/go/compute/metadata)) = 0.9.0
Provides:          bundled(golang(code.gitea.io/sdk/gitea)) = 0.25.1
Provides:          bundled(golang(dario.cat/mergo)) = 1.0.1
Provides:          bundled(golang(github.com/42wim/httpsig)) = 1.2.4
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2)) = 1.41.7
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/config)) = 1.32.17
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/credentials)) = 1.19.16
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/feature/ec2/imds)) = 1.18.23
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/internal/configsources)) = 1.4.23
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/internal/endpoints/v2)) = 2.7.23
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/internal/v4a)) = 1.4.24
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/ecr)) = 1.57.2
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/ecrpublic)) = 1.38.15
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/eks)) = 1.83.0
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding)) = 1.13.9
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/presigned-url)) = 1.13.23
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/signin)) = 1.0.11
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/sso)) = 1.30.17
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/ssooidc)) = 1.35.21
Provides:          bundled(golang(github.com/aws/aws-sdk-go-v2/service/sts)) = 1.42.1
Provides:          bundled(golang(github.com/aws/smithy-go)) = 1.25.1
Provides:          bundled(golang(github.com/aws/smithy-go/aws-http-auth)) = 1.1.3
Provides:          bundled(golang(github.com/AzureAD/microsoft-authentication-library-for-go)) = 1.6.0
Provides:          bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azcore)) = 1.21.1
Provides:          bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azidentity)) = 1.13.1
Provides:          bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/containers/azcontainerregistry)) = 0.2.3
Provides:          bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/internal)) = 1.12.0
Provides:          bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/containerservice/armcontainerservice)) = 1.0.0
Provides:          bundled(golang(github.com/Azure/go-ansiterm)) = 0.0.0_20250102033503_faa5f7b0171c
Provides:          bundled(golang(github.com/Azure/go-ntlmssp)) = 0.0.0_20221128193559_754e69321358
Provides:          bundled(golang(github.com/beorn7/perks)) = 1.0.1
Provides:          bundled(golang(github.com/blang/semver/v4)) = 4.0.0
Provides:          bundled(golang(github.com/briandowns/spinner)) = 1.23.2
Provides:          bundled(golang(github.com/bshuster-repo/logrus-logstash-hook)) = 1.1.0
Provides:          bundled(golang(github.com/BurntSushi/toml)) = 1.6.0
Provides:          bundled(golang(github.com/cenkalti/backoff/v5)) = 5.0.3
Provides:          bundled(golang(github.com/cespare/xxhash/v2)) = 2.3.0
Provides:          bundled(golang(github.com/chai2010/gettext-go)) = 1.0.2
Provides:          bundled(golang(github.com/chzyer/readline)) = 1.5.1
Provides:          bundled(golang(github.com/cloudflare/circl)) = 1.6.3
Provides:          bundled(golang(github.com/coreos/go-systemd/v22)) = 22.7.0
Provides:          bundled(golang(github.com/cpuguy83/go-md2man/v2)) = 2.0.7
Provides:          bundled(golang(github.com/cyphar/filepath-securejoin)) = 0.6.1
Provides:          bundled(golang(github.com/davecgh/go-spew)) = 1.1.2_0.20180830191138_d8f796af33cc
Provides:          bundled(golang(github.com/davidmz/go-pageant)) = 1.0.2
Provides:          bundled(golang(github.com/dgryski/go-rendezvous)) = 0.0.0_20200823014737_9f7001d12a5f
Provides:          bundled(golang(github.com/distribution/distribution/v3)) = 3.1.1
Provides:          bundled(golang(github.com/distribution/reference)) = 0.6.0
Provides:          bundled(golang(github.com/docker/cli)) = 29.4.3+incompatible
Provides:          bundled(golang(github.com/docker/docker-credential-helpers)) = 0.9.5
Provides:          bundled(golang(github.com/docker/go-events)) = 0.0.0_20250808211157_605354379745
Provides:          bundled(golang(github.com/docker/go-metrics)) = 0.0.1
Provides:          bundled(golang(github.com/emicklei/go-restful/v3)) = 3.13.0
Provides:          bundled(golang(github.com/emirpasic/gods)) = 1.18.1
Provides:          bundled(golang(github.com/evanphx/json-patch)) = 5.9.11+incompatible
Provides:          bundled(golang(github.com/evanphx/json-patch/v5)) = 5.9.11
Provides:          bundled(golang(github.com/exponent-io/jsonpath)) = 0.0.0_20210407135951_1de76d718b3f
Provides:          bundled(golang(github.com/fatih/color)) = 1.19.0
Provides:          bundled(golang(github.com/felixge/httpsnoop)) = 1.0.4
Provides:          bundled(golang(github.com/fluxcd/cli-utils)) = 1.2.2
Provides:          bundled(golang(github.com/fluxcd/go-git-providers)) = 0.27.0
Provides:          bundled(golang(github.com/fluxcd/helm-controller/api)) = 1.6.3
Provides:          bundled(golang(github.com/fluxcd/image-automation-controller/api)) = 1.2.3
Provides:          bundled(golang(github.com/fluxcd/image-reflector-controller/api)) = 1.2.3
Provides:          bundled(golang(github.com/fluxcd/kustomize-controller/api)) = 1.9.4
Provides:          bundled(golang(github.com/fluxcd/notification-controller/api)) = 1.9.2
Provides:          bundled(golang(github.com/fluxcd/pkg/apis/acl)) = 0.10.0
Provides:          bundled(golang(github.com/fluxcd/pkg/apis/event)) = 0.27.1
Provides:          bundled(golang(github.com/fluxcd/pkg/apis/kustomize)) = 1.19.1
Provides:          bundled(golang(github.com/fluxcd/pkg/apis/meta)) = 1.30.1
Provides:          bundled(golang(github.com/fluxcd/pkg/auth)) = 0.54.1
Provides:          bundled(golang(github.com/fluxcd/pkg/cache)) = 0.14.0
Provides:          bundled(golang(github.com/fluxcd/pkg/chartutil)) = 1.27.1
Provides:          bundled(golang(github.com/fluxcd/pkg/envsubst)) = 1.7.0
Provides:          bundled(golang(github.com/fluxcd/pkg/git)) = 0.52.0
Provides:          bundled(golang(github.com/fluxcd/pkg/kustomize)) = 1.35.4
Provides:          bundled(golang(github.com/fluxcd/pkg/oci)) = 0.68.1
Provides:          bundled(golang(github.com/fluxcd/pkg/runtime)) = 0.110.1
Provides:          bundled(golang(github.com/fluxcd/pkg/sourceignore)) = 0.18.0
Provides:          bundled(golang(github.com/fluxcd/pkg/ssa)) = 0.76.1
Provides:          bundled(golang(github.com/fluxcd/pkg/ssh)) = 0.25.0
Provides:          bundled(golang(github.com/fluxcd/pkg/tar)) = 1.2.0
Provides:          bundled(golang(github.com/fluxcd/pkg/version)) = 0.16.0
Provides:          bundled(golang(github.com/fluxcd/source-controller/api)) = 1.9.3
Provides:          bundled(golang(github.com/fluxcd/source-watcher/api/v2)) = 2.2.2
Provides:          bundled(golang(github.com/fsnotify/fsnotify)) = 1.9.0
Provides:          bundled(golang(github.com/fxamacker/cbor/v2)) = 2.9.2
Provides:          bundled(golang(github.com/go-asn1-ber/asn1-ber)) = 1.5.7
Provides:          bundled(golang(github.com/go-errors/errors)) = 1.5.1
Provides:          bundled(golang(github.com/go-fed/httpsig)) = 1.1.0
Provides:          bundled(golang(github.com/go-git/gcfg)) = 1.5.1_0.20230307220236_3a3c6141e376
Provides:          bundled(golang(github.com/go-git/go-billy/v5)) = 5.9.0
Provides:          bundled(golang(github.com/go-git/go-git/v5)) = 5.19.1
Provides:          bundled(golang(github.com/golang/groupcache)) = 0.0.0_20241129210726_2c02b8208cf8
Provides:          bundled(golang(github.com/golang-jwt/jwt/v5)) = 5.3.1
Provides:          bundled(golang(github.com/go-ldap/ldap/v3)) = 3.4.10
Provides:          bundled(golang(github.com/go-logr/logr)) = 1.4.3
Provides:          bundled(golang(github.com/go-logr/stdr)) = 1.2.2
Provides:          bundled(golang(github.com/gonvenience/bunt)) = 1.4.2
Provides:          bundled(golang(github.com/gonvenience/idem)) = 0.0.2
Provides:          bundled(golang(github.com/gonvenience/neat)) = 1.3.16
Provides:          bundled(golang(github.com/gonvenience/term)) = 1.0.4
Provides:          bundled(golang(github.com/gonvenience/text)) = 1.0.9
Provides:          bundled(golang(github.com/gonvenience/ytbx)) = 1.4.7
Provides:          bundled(golang(github.com/googleapis/enterprise-certificate-proxy)) = 0.3.15
Provides:          bundled(golang(github.com/googleapis/gax-go/v2)) = 2.22.0
Provides:          bundled(golang(github.com/google/btree)) = 1.1.3
Provides:          bundled(golang(github.com/google/gnostic-models)) = 0.7.0
Provides:          bundled(golang(github.com/google/go-cmp)) = 0.7.0
Provides:          bundled(golang(github.com/google/go-containerregistry)) = 0.21.6
Provides:          bundled(golang(github.com/google/go-github/v82)) = 82.0.0
Provides:          bundled(golang(github.com/google/go-querystring)) = 1.2.0
Provides:          bundled(golang(github.com/google/s2a-go)) = 0.1.9
Provides:          bundled(golang(github.com/google/uuid)) = 1.6.0
Provides:          bundled(golang(github.com/go-openapi/jsonpointer)) = 0.21.1
Provides:          bundled(golang(github.com/go-openapi/jsonreference)) = 0.21.0
Provides:          bundled(golang(github.com/go-openapi/swag)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/cmdutils)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/conv)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/fileutils)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/jsonname)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/jsonutils)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/loading)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/mangling)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/netutils)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/stringutils)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/typeutils)) = 0.25.4
Provides:          bundled(golang(github.com/go-openapi/swag/yamlutils)) = 0.25.4
Provides:          bundled(golang(github.com/gorilla/handlers)) = 1.5.2
Provides:          bundled(golang(github.com/gorilla/mux)) = 1.8.1
Provides:          bundled(golang(github.com/gregjones/httpcache)) = 0.0.0_20190611155906_901d90724c79
Provides:          bundled(golang(github.com/grpc-ecosystem/grpc-gateway/v2)) = 2.28.0
Provides:          bundled(golang(github.com/hashicorp/errwrap)) = 1.1.0
Provides:          bundled(golang(github.com/hashicorp/go-cleanhttp)) = 0.5.2
Provides:          bundled(golang(github.com/hashicorp/golang-lru/arc/v2)) = 2.0.5
Provides:          bundled(golang(github.com/hashicorp/golang-lru/v2)) = 2.0.5
Provides:          bundled(golang(github.com/hashicorp/go-multierror)) = 1.1.1
Provides:          bundled(golang(github.com/hashicorp/go-retryablehttp)) = 0.7.8
Provides:          bundled(golang(github.com/hashicorp/go-version)) = 1.9.0
Provides:          bundled(golang(github.com/hiddeco/sshsig)) = 0.2.0
Provides:          bundled(golang(github.com/homeport/dyff)) = 1.10.2
Provides:          bundled(golang(github.com/inconshreveable/mousetrap)) = 1.1.0
Provides:          bundled(golang(github.com/jbenet/go-context)) = 0.0.0_20150711004518_d14ea06fba99
Provides:          bundled(golang(github.com/json-iterator/go)) = 1.1.12
Provides:          bundled(golang(github.com/kevinburke/ssh_config)) = 1.4.0
Provides:          bundled(golang(github.com/klauspost/compress)) = 1.18.6
Provides:          bundled(golang(github.com/klauspost/cpuid/v2)) = 2.3.0
Provides:          bundled(golang(github.com/kylelemons/godebug)) = 1.1.0
Provides:          bundled(golang(github.com/liggitt/tabwriter)) = 0.0.0_20181228230101_89fcab3d43de
Provides:          bundled(golang(github.com/lucasb-eyer/go-colorful)) = 1.2.0
Provides:          bundled(golang(github.com/MakeNowJust/heredoc)) = 1.0.0
Provides:          bundled(golang(github.com/manifoldco/promptui)) = 0.9.0
Provides:          bundled(golang(github.com/Masterminds/semver/v3)) = 3.5.0
Provides:          bundled(golang(github.com/mattn/go-ciede2000)) = 0.0.0_20170301095244_782e8c62fec3
Provides:          bundled(golang(github.com/mattn/go-colorable)) = 0.1.14
Provides:          bundled(golang(github.com/mattn/go-isatty)) = 0.0.20
Provides:          bundled(golang(github.com/mattn/go-runewidth)) = 0.0.16
Provides:          bundled(golang(github.com/mattn/go-shellwords)) = 1.0.13
Provides:          bundled(golang(github.com/Microsoft/go-winio)) = 0.6.2
Provides:          bundled(golang(github.com/mitchellh/go-ps)) = 1.0.0
Provides:          bundled(golang(github.com/mitchellh/go-wordwrap)) = 1.0.1
Provides:          bundled(golang(github.com/mitchellh/hashstructure)) = 1.1.0
Provides:          bundled(golang(github.com/moby/term)) = 0.5.2
Provides:          bundled(golang(github.com/modern-go/concurrent)) = 0.0.0_20180306012644_bacd9c7ef1dd
Provides:          bundled(golang(github.com/modern-go/reflect2)) = 1.0.3_0.20250322232337_35a7c28c31ee
Provides:          bundled(golang(github.com/monochromegane/go-gitignore)) = 0.0.0_20200626010858_205db1a8cc00
Provides:          bundled(golang(github.com/munnerz/goautoneg)) = 0.0.0_20191010083416_a7dc8b61c822
Provides:          bundled(golang(github.com/notaryproject/notation-core-go)) = 1.3.0
Provides:          bundled(golang(github.com/notaryproject/notation-go)) = 1.3.2
Provides:          bundled(golang(github.com/olekukonko/tablewriter)) = 0.0.5
Provides:          bundled(golang(github.com/onsi/gomega)) = 1.42.1
Provides:          bundled(golang(github.com/opencontainers/go-digest)) = 1.0.0
Provides:          bundled(golang(github.com/opencontainers/image-spec)) = 1.1.1
Provides:          bundled(golang(github.com/peterbourgon/diskv)) = 2.0.1+incompatible
Provides:          bundled(golang(github.com/phayes/freeport)) = 0.0.0_20220201140144_74d24b5ae9f5
Provides:          bundled(golang(github.com/pjbgf/sha1cd)) = 0.6.0
Provides:          bundled(golang(github.com/pkg/browser)) = 0.0.0_20240102092130_5ac0b6a4141c
Provides:          bundled(golang(github.com/pkg/errors)) = 0.9.1
Provides:          bundled(golang(github.com/pmezard/go-difflib)) = 1.0.1_0.20181226105442_5d4384ee4fb2
Provides:          bundled(golang(github.com/prometheus/client_golang)) = 1.23.2
Provides:          bundled(golang(github.com/prometheus/client_model)) = 0.6.2
Provides:          bundled(golang(github.com/prometheus/common)) = 0.67.5
Provides:          bundled(golang(github.com/prometheus/otlptranslator)) = 1.0.0
Provides:          bundled(golang(github.com/prometheus/procfs)) = 0.20.1
Provides:          bundled(golang(github.com/ProtonMail/go-crypto)) = 1.4.1
Provides:          bundled(golang(github.com/redis/go-redis/extra/rediscmd/v9)) = 9.0.5
Provides:          bundled(golang(github.com/redis/go-redis/extra/redisotel/v9)) = 9.0.5
Provides:          bundled(golang(github.com/redis/go-redis/v9)) = 9.7.3
Provides:          bundled(golang(github.com/rivo/uniseg)) = 0.2.0
Provides:          bundled(golang(github.com/russross/blackfriday/v2)) = 2.1.0
Provides:          bundled(golang(github.com/sergi/go-diff)) = 1.4.0
Provides:          bundled(golang(github.com/sirupsen/logrus)) = 1.9.4
Provides:          bundled(golang(github.com/skeema/knownhosts)) = 1.3.1
Provides:          bundled(golang(github.com/spf13/cobra)) = 1.10.2
Provides:          bundled(golang(github.com/spf13/pflag)) = 1.0.10
Provides:          bundled(golang(github.com/texttheater/golang-levenshtein)) = 1.0.1
Provides:          bundled(golang(github.com/tidwall/gjson)) = 1.18.0
Provides:          bundled(golang(github.com/tidwall/match)) = 1.1.1
Provides:          bundled(golang(github.com/tidwall/pretty)) = 1.2.1
Provides:          bundled(golang(github.com/tidwall/sjson)) = 1.2.5
Provides:          bundled(golang(github.com/virtuald/go-ordered-json)) = 0.0.0_20170621173500_b18e6e673d74
Provides:          bundled(golang(github.com/wI2L/jsondiff)) = 0.6.1
Provides:          bundled(golang(github.com/x448/float16)) = 0.8.4
Provides:          bundled(golang(github.com/xanzy/ssh-agent)) = 0.3.3
Provides:          bundled(golang(github.com/xlab/treeprint)) = 1.2.0
Provides:          bundled(golang(gitlab.com/gitlab-org/api/client-go)) = 1.46.0
Provides:          bundled(golang(golang.org/x/crypto)) = 0.53.0
Provides:          bundled(golang(golang.org/x/net)) = 0.56.0
Provides:          bundled(golang(golang.org/x/oauth2)) = 0.36.0
Provides:          bundled(golang(golang.org/x/sync)) = 0.21.0
Provides:          bundled(golang(golang.org/x/sys)) = 0.46.0
Provides:          bundled(golang(golang.org/x/term)) = 0.44.0
Provides:          bundled(golang(golang.org/x/text)) = 0.38.0
Provides:          bundled(golang(golang.org/x/time)) = 0.15.0
Provides:          bundled(golang(gomodules.xyz/jsonpatch/v2)) = 2.5.0
Provides:          bundled(golang(google.golang.org/api)) = 0.278.0
Provides:          bundled(golang(google.golang.org/genproto/googleapis/api)) = 0.0.0_20260401024825_9d38bb4040a9
Provides:          bundled(golang(google.golang.org/genproto/googleapis/rpc)) = 0.0.0_20260427160629_7cedc36a6bc4
Provides:          bundled(golang(google.golang.org/grpc)) = 1.80.0
Provides:          bundled(golang(google.golang.org/protobuf)) = 1.36.12_0.20260120151049_f2248ac996af
Provides:          bundled(golang(go.opentelemetry.io/auto/sdk)) = 1.2.1
Provides:          bundled(golang(go.opentelemetry.io/contrib/bridges/prometheus)) = 0.67.0
Provides:          bundled(golang(go.opentelemetry.io/contrib/exporters/autoexport)) = 0.67.0
Provides:          bundled(golang(go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp)) = 0.67.0
Provides:          bundled(golang(go.opentelemetry.io/otel)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploggrpc)) = 0.19.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploghttp)) = 0.19.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlptrace)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/prometheus)) = 0.65.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/stdout/stdoutlog)) = 0.19.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/stdout/stdoutmetric)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/exporters/stdout/stdouttrace)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/log)) = 0.19.0
Provides:          bundled(golang(go.opentelemetry.io/otel/metric)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/sdk)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/sdk/log)) = 0.19.0
Provides:          bundled(golang(go.opentelemetry.io/otel/sdk/metric)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/otel/trace)) = 1.43.0
Provides:          bundled(golang(go.opentelemetry.io/proto/otlp)) = 1.10.0
Provides:          bundled(golang(gopkg.in/evanphx/json-patch.v4)) = 4.13.0
Provides:          bundled(golang(gopkg.in/inf.v0)) = 0.9.1
Provides:          bundled(golang(gopkg.in/warnings.v0)) = 0.1.2
Provides:          bundled(golang(gopkg.in/yaml.v2)) = 2.4.0
Provides:          bundled(golang(gopkg.in/yaml.v3)) = 3.0.1
Provides:          bundled(golang(go.yaml.in/yaml/v2)) = 2.4.4
Provides:          bundled(golang(go.yaml.in/yaml/v3)) = 3.0.4
Provides:          bundled(golang(helm.sh/helm/v4)) = 4.2.2
Provides:          bundled(golang(k8s.io/api)) = 0.36.2
Provides:          bundled(golang(k8s.io/apiextensions-apiserver)) = 0.36.2
Provides:          bundled(golang(k8s.io/apimachinery)) = 0.36.2
Provides:          bundled(golang(k8s.io/client-go)) = 0.36.2
Provides:          bundled(golang(k8s.io/cli-runtime)) = 0.36.2
Provides:          bundled(golang(k8s.io/component-base)) = 0.36.2
Provides:          bundled(golang(k8s.io/klog/v2)) = 2.140.0
Provides:          bundled(golang(k8s.io/kubectl)) = 0.36.2
Provides:          bundled(golang(k8s.io/kube-openapi)) = 0.0.0_20260603220949_865597e52e25
Provides:          bundled(golang(k8s.io/utils)) = 0.0.0_20260507154919_ff6756f316d2
Provides:          bundled(golang(sigs.k8s.io/controller-runtime)) = 0.24.1
Provides:          bundled(golang(sigs.k8s.io/json)) = 0.0.0_20250730193827_2d320260d730
Provides:          bundled(golang(sigs.k8s.io/kustomize/api)) = 0.21.1
Provides:          bundled(golang(sigs.k8s.io/kustomize/kyaml)) = 0.21.1
Provides:          bundled(golang(sigs.k8s.io/randfill)) = 1.0.0
Provides:          bundled(golang(sigs.k8s.io/structured-merge-diff/v6)) = 6.4.0
Provides:          bundled(golang(sigs.k8s.io/yaml)) = 1.6.0
# END bundled provides

%description
Flux is a set of continuous and progressive delivery controllers for Kubernetes
that keep a cluster in sync with sources of configuration such as Git
repositories, OCI artifacts and Helm repositories.

This package provides the flux command line tool, used to bootstrap Flux into a
cluster and to create, inspect and reconcile its custom resources. The
controllers themselves run in-cluster and are installed by "flux bootstrap" or
"flux install"; they are not part of this package.

%prep
%autosetup -n %{archivedir} -a 1

# Fail loudly rather than silently attempting a network fetch mid-build.
test -f vendor/modules.txt

# The manifests tarball has no leading directory, so unpack it where the
# go:embed directive in cmd/flux/manifests.embed.go expects to find it.
mkdir -p cmd/%{cliname}/manifests
tar -xf %{SOURCE2} -C cmd/%{cliname}/manifests
# go:embed fails the build on an empty directory, so check the glob it uses.
ls cmd/%{cliname}/manifests/*.yaml >/dev/null

%build
export GOPROXY=off
export GOFLAGS="-mod=vendor"
# Upstream stamps the version into main.VERSION, which "flux --version" and the
# bootstrap manifests both read. Upstream also passes "-s -w"; we deliberately
# do not, so that the debuginfo subpackage is usable.
export GO_LDFLAGS="-X main.VERSION=%{version}"
%gobuild -o _bin/%{cliname} ./cmd/%{cliname}

for shell in bash zsh fish; do
  ./_bin/%{cliname} completion $shell > %{cliname}.$shell
done

%install
install -Dpm 0755 _bin/%{cliname} %{buildroot}%{_bindir}/%{cliname}

install -Dpm 0644 %{cliname}.bash %{buildroot}%{bash_completions_dir}/%{cliname}
install -Dpm 0644 %{cliname}.zsh  %{buildroot}%{zsh_completions_dir}/_%{cliname}
install -Dpm 0644 %{cliname}.fish %{buildroot}%{fish_completions_dir}/%{cliname}.fish

%check
# Upstream's unit tests are tagged "unit" and need envtest control-plane
# binaries via KUBEBUILDER_ASSETS, which cannot be downloaded in a COPR builder;
# the e2e suite needs a live cluster. Verify instead that the binary runs and
# that the version stamp actually took effect.
test "$(./_bin/%{cliname} --version)" = "%{cliname} version %{version}"

%files
%license LICENSE
%doc README.md CONTRIBUTING.md CODE_OF_CONDUCT.md MAINTAINERS
%{_bindir}/%{cliname}
%{bash_completions_dir}/%{cliname}
%{zsh_completions_dir}/_%{cliname}
%{fish_completions_dir}/%{cliname}.fish

%changelog
* Mon Aug 03 2026 Anton Groshev <anton@agrshv.dev> - 2.9.3-1
- Initial package

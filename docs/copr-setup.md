# One-time COPR setup

Everything here is done once, before the first build.

## 1. Create a Fedora Account (FAS)

COPR authenticates against the Fedora Account System. There is no way to script
this — it needs a browser and an email confirmation.

1. Go to <https://accounts.fedoraproject.org/> and choose **Create an account**.
2. Fill in username, full name, and email. Your username becomes your COPR
   namespace, so `agrshv` gives you `copr.fedorainfracloud.org/coprs/agrshv/ghorg`.
3. Confirm the address from the email Fedora sends, then set your password.

No CLA or package-maintainer sponsorship is required for COPR — a plain account
is enough. (Sponsorship only matters for official Fedora repos.)

## 2. Accept the COPR terms

Log in once at <https://copr.fedorainfracloud.org/> with the new account. The
first login creates your COPR user record and shows the terms of use. Builds
submitted before this step fail with an authorisation error.

## 3. Generate an API token

1. Visit <https://copr.fedorainfracloud.org/api/> while logged in.
2. The page shows a ready-made config block. Copy it verbatim into
   `~/.config/copr`:

   ```ini
   [copr-cli]
   login = <generated>
   username = agrshv
   token = <generated>
   copr_url = https://copr.fedorainfracloud.org
   ```

3. Tighten the permissions — the token is a credential:

   ```bash
   chmod 600 ~/.config/copr
   ```

Tokens expire (currently after 180 days). When `copr-cli` starts returning
authentication errors, regenerate from the same page and replace the file.

Verify it works:

```bash
copr-cli whoami
```

## 4. Create the two projects

Each tool gets its own COPR project so users can enable them independently.

```bash
copr-cli create ghorg \
  --chroot fedora-44-x86_64 \
  --chroot fedora-rawhide-x86_64 \
  --description "ghorg — clone and keep in sync every repo in a GitHub/GitLab org"

copr-cli create fluxcd \
  --chroot fedora-44-x86_64 \
  --chroot fedora-rawhide-x86_64 \
  --description "flux — the Flux CD command line tool for GitOps on Kubernetes"
```

Useful project settings to consider:

- `--enable-net on` is **not** needed and should stay off. Our specs vendor all
  Go dependencies, and keeping the network off matches Fedora policy and catches
  accidental download-at-build-time bugs.
- `--delete-after-days` is for throwaway projects; leave unset for these.

## 5. Local mock builds (optional but recommended)

Testing in mock reproduces the COPR builder exactly and catches missing
`BuildRequires` before you burn COPR build time. It needs group membership:

```bash
sudo usermod -a -G mock "$USER"
```

Log out and back in (or run `newgrp mock`) for the group to take effect.

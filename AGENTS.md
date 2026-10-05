# Repository guidance

Pixel Audio Visualizer is part of the homelab's pixel light-show system. How it is deployed and how it fits with
the controllers, FPP and the other cluster apps: the homelab wiki at
`~/Code/smarthome/homenetwork` (`wiki/apps/pixels.md`); read its `AGENTS.md` before changing
anything that affects the cluster.

## Commits and releases

Releases are automatic and are driven by commit messages, so every commit that reaches
`master` — including the squash-merge title of a pull request — must be a
[Conventional Commit](https://www.conventionalcommits.org/): `<type>: <summary>`, lower-case
type, imperative summary.

| Type | Use for | Release effect |
|---|---|---|
| `feat` | A new capability | minor version |
| `fix` | A bug fix in shipped behavior | patch version |
| `feat!` / `fix!`, or a `BREAKING CHANGE:` footer | An incompatible change to configuration, chart values, or output | major version |
| `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `deps` | Everything else | none |

Examples: `feat: add external config to chart`, `fix: pin to a node when the node value is set`,
`docs: describe the release flow`.

- A message without a type (for example `Cleanup`) is ignored by release-please: the change
  ships only when a later `feat` or `fix` triggers a release.
- How a release happens: release-please keeps a `chore(master): release X.Y.Z` PR open with the
  next version and `CHANGELOG.md`. Merging it is the release approval: it tags `vX.Y.Z`, the tag
  build publishes the image and the Helm chart to `ghcr.io/ttarhan`, Renovate in
  `ttarhan-sh/k8s-infra` auto-merges the chart bump, and ArgoCD rolls it out — usually within
  minutes.
- Never create tags by hand, and never edit versions outside the release PR.

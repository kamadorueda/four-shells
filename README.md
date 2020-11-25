# [Four shells](https://4shells.com)

Website, server, infrastructure and orchestration for:

- **CachIPFS**: Implementation of a Nix Binary Cache over IPFS,

  Formerly: https://github.com/kamadorueda/nix-ipfs

- **NixDB**: A database with Nix packages from all versions, all commits and all channels,

  Formerly: https://github.com/kamadorueda/nixpkgs-db

## Philosophy

- Dependencies as code:
  - Everything in Nix: Declarative, reproducible, stable across machines.
  - Everything is pinned to a specific version/hash/revision:
    No third party surprises.
- Infrastructure as code:
  - Everything in terraform: Declarative, code is the inventory,
    all configurations and deployments made through the code.
- Processes as code:
  - Everything is scripted (Bash, etc): Anyone can perform a deployment with
    1 command, same for linters, testing, updates, software builds, etc.
  - The code is the manual: No need to ask colleagues, everything is automated,
    the code teaches the steps.
- Robust scripting:
  - Strict Bash: Any missing var or non-handled failing command stops the entire execution.
  - Strict compiler: Strict static typing, strict code linters, strict low
    code complexity. The code is simple, easy to read, self-documenting.
- Functional programming:
  - No side-effects: State is encapsulated in small functions, code is structured
    in isolated components.

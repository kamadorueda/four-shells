# About us

Four Shells is an small group of people who put a name to a cause:

- Building things for the community!

Currently we build and maintain:

- [NixDB](/nixdb):
  Database with Nix packages from all versions, all commits and all channels.
- [CachIPFS](/cachipfs):
  Encrypted Nix binary cache over IPFS.

All of the projects are open source licensed
and their source code can be found at [GitHub](https://github.com/kamadorueda/four-shells).

Please see [contributing](/docs#contributing) if you want to join us!

# About NixDB

One of the advantages of **Nix** is the ability to install / use packages in
**isolated environments** from the host system:

```bash
# Version installed in my host system
$ python3 --version

  Python 3.8.5

# Launch a Nix Shell with a different version of the package
$ nix-shell -p python39

  # Version installed in the Nix shell
  nix-shell $ python3 --version

              Python 3.9.0
```

Sometime ago while migrating an old **Kubernetes** cluster
we found in the need of having two different versions of **Kubernetes Helm**
to deal with different kind of deployments.

**Nix** allows us to install / use different versions of a package side-by-side
in the host system.

So let's search the versions that Nix offers to us out-of-the-box:

```bash
# Query the <nixpkgs> set in the host system
$ nix-env -q --available --description | grep helm

  helm-3.3.4  A package manager for kubernetes
```

Problem is that **nix-channels** usually offer a single version of a package,
so... What to do?

Sadly,
there is no native way of searching the Nix history for all versions of a package.

This is the problem we want to solve at [NixDB](https://4shells.com/nixdb).

We index every piece of the Nixpkgs history in order to provide versions lookups:

```text
Attribute        Description                       Versions  License
kubernetes-helm  A package manager for kubernetes  30        Apache License 2.0

  https://4shells.com/nixdb/pkg/kubernetes-helm/3.4.0
  https://4shells.com/nixdb/pkg/kubernetes-helm/3.3.4
  https://4shells.com/nixdb/pkg/kubernetes-helm/3.3.1
  ...
```

And cool badges that you can add to your project:

[![](https://img.shields.io/endpoint?color=green&label=kubernetes&labelColor=grey&logo=NixOS&logoColor=white&style=flat&url=https%3A%2F%2Fraw.githubusercontent.com%2Fkamadorueda%2Ffour-shells%2Fdata-nixdb%2Fbadges%2Fkubernetes.json)](https://4shells.com/nixdb/pkg/kubernetes)

```bash
# Launch a Nix Shell with version 3.4.0 found in Nixpkgs Database
$ nix-shell -p kubernetes-helm -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/0126c86672b7d14843225df16ddfefd7091eabe7.tar.gz

  # Version installed in the Nix shell
  nix-shell $ helm version

              version.BuildInfo{Version:"v3.4.0", GitCommit:"", GitTreeState:"", GoVersion:"go1.15.3"}
```

These commands are also available for all versions that ever existed for this package:

```bash
# Launch a Nix Shell with version 2.6.1 found in Nixpkgs Database
$ nix-shell -p kubernetes-helm -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/01a664e7793158b434fefac9217ec48313b2dd45.tar.gz

  # Version installed in the Nix shell
  nix-shell $ helm version

              Client: &version.Version{SemVer:"v2.6.1", GitCommit:"bbc1f71dc03afc5f00c6ac84b9308f8ecb4f39ac", GitTreeState:"clean"}
```

# About CachIPFS

[Nix](https://nixos.org) allows you to build software.

Software that is built with Nix is [reproducible](https://reproducible-builds.org),
which means that different builds of the **same software** will produce the **same outputs**.

Normally the same project is build many times by different people:

- Developers
- Continuous integration system
- Quality assurance team
- Operations team
- End users

This easily adds up in time and resources and everyone is building
exactly the **same software** and getting the **same outputs**.

There is an efficient alternative, though:
- You build your software **once** and put the outputs on [IPFS](https://ipfs.io)
- Other people just download the outputs from [IPFS](https://ipfs.io), skipping the build

This helps people save the time, money and machine resources required to build the software themselves

[CachIPFS](https://4shells.com/cachipfs) help you coordinate the process
into a seamless experience.

# Contributing

There are many ways to contribute and many of them are not necessarily technical:

- Help us spread the word!
  Telling other people of the work being done here helps us reach the people
  who may benefit the most from the project.
- Star or fork the [repository](https://github.com/kamadorueda/four-shells),
  this help us with funding, popularity and finding new contributors from time to time.
- Fire up an issue! we welcome ideas, feature requests, problems, use cases, feedback,
  anything you may think of!
- [Become a sponsor of the project](/docs#sponsors).

Of course if you know some techy things you are also welcome!

Please read the [developing](/docs#developing) section for details about
firing up a local environment:

- Have an idea that may benefit the community?
  Contribute it! no need to ask for permission!
- Improve the user interface.
- Triage [issues](https://github.com/kamadorueda/four-shells/issues).

## Contributors

We thank the following members for their contributions:

- [NixDB] Versions used to be sorted alphabetically and sometimes that
  rendered a weird ordering.
  Now they are sorted by semver which is very realistic!

  Contributed by [Benjamin Borowski](https://github.com/typeoneerror)

- [NixDB] The website used to block when a user entered or deleted a character in the
  search bar.
  It's now fluid and fast!

  Contributed by [Lucas Eduardo](https://github.com/lucasew)

- [NixDB] There used to be a typo in the nix-shell command.
  It's now fixed :)

  Contributed by [Patryk Niedźwiedziński](https://github.com/pniedzwiedzinski)

- [NixDB] The search engine used to be naive (a `String.contains`).
  Now we use a mix of Levenshtein distance with grep behavior!

  Contributed by [Kevin Amado](https://github.com/kamadorueda)

- [NixDB] The database size used to be small.
  We have finally processed the 280k+ commits and 100k+ packages

  Contributed by [Kevin Amado](https://github.com/kamadorueda)

## Sponsors

This and other
[Free and Open Source](https://en.wikipedia.org/wiki/FOSS)
projects are possible by the financial contributions of some amazing members.

Thank you so much for your support!

|||
|:--------------------------------------:|:-----------------------------|
| [![Fluid Attacks][0_img]][0_url]       | [Fluid Attacks][0_url]       |
| [![Nathan Fish][1_img]][1_url]         | [Nathan Fish][1_url]         |
| [![Alejandra Gómez][2_img]][2_url]     | [Alejandra Gómez][2_url]     |
| [![Precision Nutrition][3_img]][3_url] | [Precision Nutrition][3_url] |

You also can be part of this list by
[Sponsoring @kamadorueda on Patreon](https://www.patreon.com/kamadorueda).

Every penny goes to build and host the project, promise!

[0_img]: https://github.com/kamadorueda/four-shells/raw/main/front/static/sponsors/fluid_attacks.png
[0_url]: https://fluidattacks.com

[1_img]: https://github.com/kamadorueda/four-shells/raw/main/front/static/sponsors/anonymous.png
[1_url]: https://github.com/lordcirth

[2_img]: https://github.com/kamadorueda/four-shells/raw/main/front/static/sponsors/anonymous.png
[2_url]: https://www.linkedin.com/in/alejandra-g%C3%B3mez-r-618a10138

[3_img]: https://github.com/kamadorueda/four-shells/raw/main/front/static/sponsors/precision_nutrition.png
[3_url]: https://precisionnutrition.com

# Developing

This project is kind of a monolith in the sense that everything lives
on the same repository.
This has some reasons but mostly is because we think it makes things simpler.

The project structure is more or less the following:

- `/back`: Backend server, written in Python, mostly in charge of rendering NixDB templates
  and handling CachIPFS related operations
- `/cmd`: common commands to wrap developing operations
- `/front`: Front-end server, written in Javascript and React, mostly in charge
  of rendering the web user interface

There are other _not very important_ folders that you can ignore for now:

- `/build`: build system functions and Nix expressions
- `/infra`: Terraform files to describe the infrastructure

## Local environment

Requirements:

1.  Linux (preferably) or Windows WSL (slow here because of virtualization)
1.  Having Nix installed in your system: https://nixos.org/download.html
1.  Please clone and locate your shell at the root of the repository,
    you'll need 2 shells (we need 4, that's why **Four Shells**!)
1.  You'll need a local back-end and a local front-end server:
    1.  Back-end:

        Run `./cmd/back-local/run.sh`

        ```bash
        four-shells$ ./cmd/back-local/run.sh

        [INFO] Launching local back-end server!
        [WARNING] Please be aware that login functionality wont work

        INFO:     Started server process [3898829]
        INFO:     Waiting for application startup.
        INFO:     Application startup complete.
        INFO:     Uvicorn running on http://localhost:8400 (Press CTRL+C to quit)
        ```

        You can quit by pressing CTRL + C

    1.  Front-end:

        Run `./cmd/front-local/run.sh`

        The output is similar to this, once you modify and save a file
        the front-end server will automatically reload with the changes.

        ```bash
        four-shells$ ./cmd/front-local/run.sh

        [INFO] Launching local front-end server!

        webpack 5.10.0 compiled successfully in 1045 ms
        ```
1.  Visit [http://localhost:8400](http://localhost:8400) and you are ready to hack!

## Technical Philosophy

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

# Help

Fire up an [issue](https://github.com/kamadorueda/four-shells/issues),
we are very open to any kind of feedback, bugs, feature requests, anything,

Really

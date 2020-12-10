# Welcome to the docs!

Four Shells is a community-driven [Free and Open Source](https://en.wikipedia.org/wiki/FOSS) project that brings to the world two things:
- [NixDB](/nixdb): Database with Nix packages from all versions, all commits and all channels.
- [CachIPFS](/cachipfs): Encrypted Nix binary cache over IPFS.

Everything you see here, like the infrastructure, website, domain,
and documentation has been written by individuals like you and me.
There is room for everyone and you can be part of it!
We genuinely appreciate people who are trying to make this project a better
place for the community.

Please see [contributing](/docs#contributing) for more information.

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
|:------------------------------------:|:-------------------------|
| [![Fluid Attacks][0_img]][0_url]     | [Fluid Attacks][0_url]   |
| [![Nathan Fish][1_img]][1_url]       | [Nathan Fish][1_url]     |
| [![Alejandra Gómez][2_img]][2_url]   | [Alejandra Gómez][2_url] |

You also can be part of this list by
[Sponsoring me on Patreon](https://www.patreon.com/kamadorueda).

It goes far beyond the money.
It's about the people who have found their lives a little bit better thanks to the project!

[0_img]: https://github.com/kamadorueda/four-shells/raw/main/static/sponsors/fluid_attacks.png
[0_url]: https://fluidattacks.com
[1_img]: https://github.com/kamadorueda/four-shells/raw/main/static/sponsors/anonymous.png
[1_url]: https://github.com/lordcirth
[2_img]: https://github.com/kamadorueda/four-shells/raw/main/static/sponsors/anonymous.png
[2_url]: https://www.linkedin.com/in/alejandra-g%C3%B3mez-r-618a10138

# Developing

This project is kind of a monolith in the sense that everything lives
on the same repository.
This has some reasons but mostly is because we think it makes things simpler.

The project structure is more or less the following:

- `/cmd`: common commands to wrap developing operations
- `/server`
  - `/back`: Backend server, written in Python, mostly in charge of rendering NixDB templates
    and handling CachIPFS related operations
  - `/front`: Front-end server, written in Javascript and React, mostly in charge
    of rendering the web user interface
  - `/public`: Static files, basically

There are other _not very important_ folders that you can ignore for now:

- `/bin`: a few executables
- `/build`: build system functions and Nix expressions
- `/client`: a CLI (work in progress)
- `/infra`: Terraform files to describe the infrastructure

## Local environment

Requirements:

1.  Linux (preferably) or Windows WSL (slow here because of virtualization)
1.  Having Nix installed in your system: https://nixos.org/download.html
1.  Please clone and locate your shell at the root of the repository,
    you'll need 2 shells (we need 4, that's why **Four Shells**!)
1.  You'll need a local back-end and a local front-end server:
    1.  Back-end:

        Run `./cmd/server-local/back/run.sh`

        ```
        four-shells$ ./cmd/server-local/back/run.sh

        [INFO] Launching local back-end server!
        [WARNING] Please be aware that login functionality wont work

        Configuration:

        AWS_ACCESS_KEY_ID_SERVER = test
        AWS_CLOUDFRONT_DOMAIN = test
        AWS_REGION = us-east-1
        AWS_SECRET_ACCESS_KEY_SERVER = test
        GOOGLE_OAUTH_CLIENT_ID_SERVER = test
        GOOGLE_OAUTH_SECRET_SERVER = test
        SERVER_PATH_PUBLIC = /nix/store/w2fw9lxc7qz2j87zi1xf6f2bzf7haz6v-public
        SERVER_SESSION_SECRET = test

        INFO:     Started server process [3475269]
        INFO:     Waiting for application startup.
        INFO:     Application startup complete.
        INFO:     Uvicorn running on http://0.0.0.0:8400 (Press CTRL+C to quit)
        ```

        You can quit by pressing CTRL + C

    1.  Front-end:

        Run `./cmd/server-local/front/run.sh`

        The output is similar to this, once you modify and save a file
        the front-end server will automatically reload with the changes.

        ```
        [INFO] Launching local front-end server!

        # ...

        webpack 5.10.0 compiled successfully in 1045 ms
        ℹ ｢wdm｣: Compiled successfully.
        ```
1.  Visit [http://localhost:8400](http://localhost:8400) and you are ready to hack!

## Help

Email me! `kamadorueda [at] gmail [dot] com`, I'll be happy to help.

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

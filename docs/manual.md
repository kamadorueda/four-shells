# Nix-IPFS Guide

## Table of contents

- [Nix-IPFS Guide](#nix-ipfs-guide)
  * [Table of contents](#table-of-contents)
  * [Introduction](#introduction)
  * [Installing](#installing)
    + [Latest release](#latest-release)
    + [From source](#from-source)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Introduction

Nix-IPFS is a [binary cache](https://nixos.wiki/wiki/Binary_Cache) implementation over [IPFS](https://ipfs.io/).

A binary cache can store Nixpkgs, Nix builds, and in a more general sense /nix/store paths.

Results in the binary cache can be used by other machines to avoid building the result from source. This helps you save the time, resources, and bandwidth required to build them in the first place.

Nix-IPFS serve those results over a peer-to-peer distributed file system,
enabling many powerful features.

- [Decentralization](https://en.wikipedia.org/wiki/Decentralization) of stored content.
- [Peer-to-peer](https://en.wikipedia.org/wiki/Peer-to-peer) content distribution.
- Cryptographic [content-addressing](https://en.wikipedia.org/wiki/Content-addressable_storage).

## Installing

### Latest release

You can install the latest release with:

```bash
nix-env -i -f https://github.com/kamadorueda/nix-ipfs/archive/latest.tar.gz
```

### From source

Clone the repository and then install from source:

`/my/repositories/nix-ipfs $ ./build/install.sh`

You can also use live commands without installing:

`/my/repositories/nix-ipfs $ ./bin/<command>`

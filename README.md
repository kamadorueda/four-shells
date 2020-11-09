# Mirroring binary caches over IPFS

## Whitepaper and implementation

### Concepts

Let's start talking about what happens when you evaluate (nix-build, nix-shell, etc) some expression:

1.  Nix turns the expression into a .drv file, let's use GCC as example:

    The derivation is `/nix/store/5qpl4n6fl7dr406xpf5c35ym6lpzm6b3-gcc-9.3.0.drv`.

    It contains in the first array the outputs as /nix/store paths, in this case
    this single GCC derivation produces 4 outputs:

    ```bash
    Derive([
        ("info","/nix/store/9dy5p8h4k31b6kavr204vd307yfc3g52-gcc-9.3.0-info","",""),
        ("lib","/nix/store/zhwcys6hmmz3k9vf348dk2y79k0x62na-gcc-9.3.0-lib","",""),
        ("man","/nix/store/l5s2cqqxqfa0p7c8xyyc9vwv2i1kqg0p-gcc-9.3.0-man","",""),
        ("out","/nix/store/xb953d5ss803xhmk60xgrwl9afjbzx3l-gcc-9.3.0","","")
    ], # continues ...
    ```

    Let's focus in the *lib* one: `/nix/store/zhwcys6hmmz3k9vf348dk2y79k0x62na-gcc-9.3.0-lib`

    The first characters are the hash of the inputs of the derivation
    (`zhwcys6hmmz3k9vf348dk2y79k0x62na`).

    As long as the inputs remain the same,
    the outputs will always be the same (reproducibility).

1.  For each binary cache Nix will lookup the NAR manifest:

    The template is: `<binary-cache-host>/<inputs-hash>.narinfo`.

    For instance: http://cache.nixos.org/zhwcys6hmmz3k9vf348dk2y79k0x62na.narinfo

    There are two possible outcomes:
    - The file exists in the binary cache and therefore it can be used as cache.
    - The file does not exist and Nix will look at another binary cache (if configured)
        or build the derivation locally if there is no binary cache that contains the manifest.

    In this case it's available:

    ```
    StorePath: /nix/store/zhwcys6hmmz3k9vf348dk2y79k0x62na-gcc-9.3.0-lib
    URL: nar/17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz.nar.xz
    Compression: xz
    FileHash: sha256:17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz
    FileSize: 1365304
    NarHash: sha256:0j00ws2af025qd80hs0ljnxxwjmlhbl5xdlx5fasxdhp3qcv22w1
    NarSize: 5551528
    References: ddw72ph4qzikgldz3ciy6whlfz6bjwrw-glibc-2.32 zhwcys6hmmz3k9vf348dk2y79k0x62na-gcc-9.3.0-lib
    Sig: cache.nixos.org-1:fXRl9j1NIdVoX//jr/s0d9ZiTo43kpgjVtLAs+fzGGMEkXAfIAOlViF1FeC/DaLKaDO7ssW/V055XB1RWFdUDQ==
    ```

    This manifest contains two important fields:
    - URL: Which you can expand to `<binary-cache-host>/<URL>` and contains
        the actual contents of the artifact.
    - References: The dependencies (closure) of this output that need
        to be fetched too.

### Some facts

1.  Binary caches can also be local (a path in the file system):

    ```
    /path/to/narstore
    ├── 5dk0ij0wn5s3ycxm8v92b9gpvhz2c786.narinfo
    ├── ddw72ph4qzikgldz3ciy6whlfz6bjwrw.narinfo
    ├── y2jgdxrwqcmdvg6f65g2awgg29vp7k6d.narinfo
    ├── zhwcys6hmmz3k9vf348dk2y79k0x62na.narinfo
    ├── nar
    │   ├── 02jdzfnhz17h6qy9bk83hxk7i3qq5j1aalj0fdab8k03yssv5126.nar.xz
    │   ├── 16140qibjmh2hk8d4y4yf8j90lx6nxfxlbki3dyvd8hvgg8v7qa9.nar.xz
    │   ├── 17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz.nar.xz
    │   └── 1n6miwc4qq5fkpr9sqcs9g8sqr8alyk3rwnmvya5cl6174mmxsx0.nar.xz
    └── nix-cache-info
    ```

    Actually https://cache.nixos.org is just an AWS S3 bucket with such structure.

    They can be configured easily by adding this to the config:

    ```
    substituters = file:///path/to/narstore https://cache.nixos.org
    trusted-public-keys = <...>
    ```

    Now nix will lookup `/path/to/narstore` as if it were a binary cache.

1.  Nar files are content addressed!!!!

    In: `02jdzfnhz17h6qy9bk83hxk7i3qq5j1aalj0fdab8k03yssv5126.nar.xz`

    `02jdzfnhz17h6qy9bk83hxk7i3qq5j1aalj0fdab8k03yssv5126` is the sha256 of the
    file encoded in base32.

    We can turn this base32 string into an IPFS CID, without the need of
    downloading anything, just by knowing the string, which is provided by the
    `FileHash` field of the manifest.

1.  The entire binary cache is Peta Bytes of data, it can't be mirrored on
    a single machine, so we need a way of mirroring just what we need.

    If every user mirrors what he/she need, together it forms a distributed file
    system of _popular_ derivations, which is as good as mirroring the
    entire binary cache, subtracting what nobody cares about.

1.  You can mount a virtual file system with FUSE and programmatically answer
    OS queries.

    For instance we can mount an **empty** directory at `/path/to/fuse`.

    When a user (or nix) asks for: `cat /path/to/fuse/some-file`,
    FUSE allows us to define what to do which such request:

    ```py
    def read(self, path, length, offset, fh):
        # The power is that we can return whatever we like!! keep reading

        # For now let's return something cool
        return 'Hello World!'
    ```

    ```bash
    $ cat /path/to/fuse/some-file
    Hello World!

    $ cat /path/to/fuse/another-file
    Hello World!
    ```

    Note how we didn't even touched the file system (it's still size 0)
    and we were able to return contents to the user.

    This is where the magic happens:

    - We can create a local binary cache with FUSE (size 0)
    - Nix will query our local binary cache for two contents:
      - `<binary-cache-host>/<inputs-hash>.narinfo`
      - `<binary-cache-host>/<URL>`
    - We will program our `read` function to answer such request as explained bellow.

    You can read more about this technology here: https://www.stavros.io/posts/python-fuse-filesystem/

### Implementing the read function

When nix ask our local binary cache (a FUSE file system that we control via the `read` function), our `read` function will:

1.  Check over IPFS if CID(FileHash) is available:

    - If it's, stream it from IPFS to the user.
    - If it's not but it's available on a binary cache, stream it from the binary
      cache to the user AND add it to the user IPFS node.

      Now the user helps to distribute the artifact over the IPFS swarm and
      other users are able to discover the content.
    - If it's not and it's not available on a binary cache,
      just build it
      (pending to implement adding to the cache as this require some signing and trust mechanisms for security purposes).

### User experience

What a user who wants to use the binary cache over IPFS needs to do is:

- Launch a local IPFS daemon (easy, 1 command)
- Launch a local FUSE server (easy, 1 command) <- pending to develop!
- Configure Nix to use the local FUSE server (easy, 1 line of config)

And that's it!

Source code for this implementation is hosted at: https://github.com/kamadorueda/nix-ipfs

## Contributing

I'm currently interested in developing such project and releasing it for
free to the community, but I need your help!

The amount of time I can dedicate to it is proportional to the level of funding.

Please consider [supporting me](https://www.patreon.com/kamadorueda). It has some cool benefits!

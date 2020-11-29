# Whitepaper and implementation

## Concepts

Let's start talking about what happens when you evaluate (nix-build, nix-shell, etc) some expression:

1.  Nix turns the expression (.nix) into a .drv file, let's use GCC as example:

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

    The first characters are the hash of the inputs of the derivation:

    `zhwcys6hmmz3k9vf348dk2y79k0x62na`

    As long as the inputs remain the same,
    the outputs will always be the same (reproducibility).

1.  For each binary cache Nix will lookup the .narinfo file:

    The manifest lives at a URL that follow: `<binary-cache-host>/<inputs-hash>.narinfo`.

    For instance: http://cache.nixos.org/zhwcys6hmmz3k9vf348dk2y79k0x62na.narinfo

    There are two possible outcomes:
    - The .narinfo exists in the binary cache
    - The .narinfo does not exist in the binary cache

    Nix will keep looking for this .narinfo file in all configured _substituters_
    (binary caches) until a cache-hit occurs.

    If Nix can't find a binary cache that contains the .narinfo, it will build
    the derivation locally.

    In this case the .narinfo is available and contains information like this:

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

    This .narinfo contains two important fields:
    - **URL** contains the actual contents of the artifact,
      the ones Nix will use to reconstruct the corresponding /nix/store tree.

      This is the most important file and the larger one (in size).

      We definitely want to serve and receive these files through IPFS.

      For instance: http://cache.nixos.org/nar/17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz.nar.xz

    - **References** are the dependencies (closure) of this output. They need
        to be fetched too, recursively.

1.  Note that there are two files: .narinfo and .nar.xz:
    - **.narinfo** contains metadata: URL (to the .nar.xz) and References (dependencies)
    - **.nar.xz** contains a compressed version of the /nix/store path that
      nix will use as cache

    We want to serve through IPFS the .nar.xz files because they are the big ones
    (and also because they are content-addressed, keep reading)

    .narinfo files are small, and can be fetched from the binary cache, no problem.
    (and also because they are not content-addressed, keep reading)

## Some facts

1.  The entire binary cache is Petabytes of data, no single regular user can have it all.

1.  We can create a **local** HTTP server that acts as binary cache.

    This server must answer requests to:
    - `http://localhost:8888/`**:narinfo:**
    - `http://localhost:8888/nar/`**:nar_xz:**
    - `http://localhost:8888/nix-cache-info` (more metadata, no need to explain)

    This is where the magic happens as we can act as a proxy between the
    local _substituter_ (http://localhost:8888) and the remote _substituter_ (for instance http://cache.nixos.org) and performs extra actions like:
    - fetching data from IPFS instead of http://cache.nixos.org.
    - adding data to IPFS instead of to the remote binary cache.

    We will program our http://localhost:8888 server to answer such request as explained bellow.

## Implementing the local server

Let's assume one more time that Nix is about to build:

`/nix/store/5qpl4n6fl7dr406xpf5c35ym6lpzm6b3-gcc-9.3.0.drv`.

Which has 4 outputs, and one of them is:

`/nix/store/zhwcys6hmmz3k9vf348dk2y79k0x62na-gcc-9.3.0-lib`

### READ data

1.  The local server receives a request for:

    http://localhost:8888/zhwcys6hmmz3k9vf348dk2y79k0x62na.narinfo

    The local server fetches the configured remote binary cache in order to inspect the metadata:

    http://cache.nixos.org/zhwcys6hmmz3k9vf348dk2y79k0x62na.narinfo

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

    We turn this FileHash into an IPFS CID by calling a remote translation service:

    GET http://some.key.value.service/api/translate/sha256:17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz

    Which should returned something like:

    QmPW7pVJGdV4wkANRgZDmTnMiQvUrwy4EnQpVn4qHAdrTj

1.  Check over IPFS if the CID is available (.nar.xz), use some seconds as timeout:

    - If it's available on IPFS, stream the .nar.xz from IPFS to the user.
    - If it's not:
      - Stream from http://cache.nixos.org/nar/17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz.nar.xz
        to the user
      - Add the .nar.xz to IPFS:

        ```bash
        $ ipfs add -q 17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz.nar.xz
        QmPW7pVJGdV4wkANRgZDmTnMiQvUrwy4EnQpVn4qHAdrTj
        ```

      - Announce the IPFS CID into the remote key value service so it can be used
        to translate future requests:

        POST http://some.key.value.service/api/announce/sha256:17g1n8hxhq7h5h4jh0vy15pp6l1yyy1rg9mdq3pi60znnj53dzzz/to/QmPW7pVJGdV4wkANRgZDmTnMiQvUrwy4EnQpVn4qHAdrTj

### Translation service security considerations

1.  POST `http://some.key.value.service/api/announce/`**:nix_nar_xz_hash:**`/to/`**:ipfs_cid:**
1.  GET `http://some.key.value.service/api/translate/`**:nix_nar_xz_hash:**

    An attacker may announce a wrong `nix_nar_xz_hash` -> `ipfs_cid` relation.

    If the translation points to a wrong `ipfs_cid` the `nix_nar_xz_hash` can be used to verify the integrity of the received file and reject the received object.

    Also the file size obtained from the .narinfo can be used to early reject the
    object without even downloading anything.

1.  DELETE `http://some.key.value.service/api/translation/`**:nix_nar_xz_hash:**

    An attacker could delete a legit `nix_nar_xz_hash`.

    As long as there are more active good users than bad users the network grows safe.

1.  When the server fetches the upstream substituter, the substituter may
    return a sufficiently big file as to consume the entire server memory.

## User experience

What a user who wants to use the binary cache over IPFS need to do is:

1.  Launch the http://localhost:8888 server: `$ some-command-not-yet-created`

    This server launches the IPFS daemon and node internally.

1.  Add to nix.conf the local binary cache:

    ```
    substituters = http://localhost:8888 https://cache.nixos.org/
    trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
    ```

    We just need to trust a single public key, the same as the remote binary cache
    that we'll be following to, in this cache cache.nixos.org, but may be one from
    cachix, or S3.

And that's it!

Source code for this implementation is hosted at: https://github.com/kamadorueda/nix-ipfs

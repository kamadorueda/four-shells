# Install the software
# ./build/install.sh

# nix_ipfs_instance="http://127.0.0.1:${NIX_IPFS_NODE_PORT}"
store_path='/nix/store/zhwcys6hmmz3k9vf348dk2y79k0x62na-gcc-9.3.0-lib'

nix-store --delete "${store_path}"
nix-store \
    --option substituters "http://127.0.0.1:8400/abc/123" \
    --option narinfo-cache-negative-ttl 0 \
    --option narinfo-cache-positive-ttl 0 \
    --realise "${store_path}"

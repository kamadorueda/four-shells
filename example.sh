# Install the software
./build/install.sh

nix_ipfs_instance="http://127.0.0.1:${NIX_IPFS_NODE_PORT}"
store_path='/nix/store/zhwcys6hmmz3k9vf348dk2y79k0x62na-gcc-9.3.0-lib'

nix-store --delete "${store_path}"
nix-store --option substituters "${nix_ipfs_instance}" --realise "${store_path}"

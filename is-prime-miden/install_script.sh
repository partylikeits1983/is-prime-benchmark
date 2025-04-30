rustup default nightly

git clone git@github.com:0xMiden/compiler.git
cd compiler
git checkout next

# install compiler stuff
cargo install --path tools/cargo-miden
cargo install --path midenc --locked

cd ..

# install vm CLI
git clone git@github.com:0xMiden/miden-vm.git
cd miden-vm/miden
cargo install --path . --features concurrent,executable
cd .. 
cd ..
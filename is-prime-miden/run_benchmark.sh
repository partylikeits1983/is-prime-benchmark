cargo miden build --release
midenc run target/miden/release/is_prime.masp --inputs inputs.toml
miden prove target/miden/release/is_prime.masp -i is_prime.inputs

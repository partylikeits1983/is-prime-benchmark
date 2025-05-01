if [[ "$(uname)" == "Darwin" ]]; then
  source ~/.zshrc
elif [[ -f /etc/os-release ]] && grep -qi ubuntu /etc/os-release; then
  source ~/.bashrc
else
  echo "⚠️  Could not detect macOS or Ubuntu; not sourcing anything."
fi

cargo miden build --release
midenc run target/miden/release/is_prime.masp --inputs inputs.toml
miden prove target/miden/release/is_prime.masp -i is_prime.inputs -p proof.proof
stat -f %z proof.proof

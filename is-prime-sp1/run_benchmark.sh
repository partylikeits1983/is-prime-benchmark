curl -L https://sp1up.succinct.xyz | bash

if [[ "$(uname)" == "Darwin" ]]; then
  source ~/.zshrc
  source ~/.zshenv
elif [[ -f /etc/os-release ]] && grep -qi ubuntu /etc/os-release; then
  source ~/.bashrc
  if [[ -f ~/.bash_profile ]]; then
    source ~/.bash_profile
  else
    source ~/.profile
  fi

else
  echo "⚠️  Could not detect macOS or Ubuntu; not sourcing anything."
fi

sp1up

cd program
cargo prove build
cd ..

cd script
RUST_LOG=info cargo run --release -- --execute
stat -f %z proof.bin
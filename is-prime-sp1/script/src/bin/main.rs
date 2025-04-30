use sp1_sdk::{include_elf, utils, ProverClient, SP1ProofWithPublicValues, SP1Stdin};
use std::time::Instant; // Import Instant for timing

const ELF: &[u8] = include_elf!("is-prime-program");

fn main() {
    // Setup a tracer for logging.
    utils::setup_logger();

    let mut stdin = SP1Stdin::new();

    // Create an input stream and write '29' to it
    let n = 7069067389u64;
    stdin.write(&n);

    // Generate and verify the proof
    let client = ProverClient::from_env();
    let (pk, vk) = client.setup(ELF);

    // Start timing before running prove()
    let start_time = Instant::now();

    let mut proof = client.prove(&pk, &stdin).run().unwrap();

    // Calculate elapsed time after prove()
    let elapsed_time = start_time.elapsed();

    // Print the elapsed time in milliseconds
    println!(
        "Time taken to run prove(): {} milliseconds",
        elapsed_time.as_millis()
    );

    let is_prime = proof.public_values.read::<bool>();
    println!("Is {} prime? {}", n, is_prime);

    client.verify(&proof, &vk).expect("verification failed");

    // Test a round trip of proof serialization and deserialization.
    proof
        .save("proof.bin")
        .expect("saving proof failed");
    let deserialized_proof =
        SP1ProofWithPublicValues::load("proof.bin").expect("loading proof failed");

    // Verify the deserialized proof.
    client
        .verify(&deserialized_proof, &vk)
        .expect("verification failed");

    println!("successfully generated and verified proof for the program!")
}
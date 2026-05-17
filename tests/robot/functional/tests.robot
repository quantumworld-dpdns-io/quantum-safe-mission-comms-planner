*** Settings ***
Documentation     Functional tests for Quantum Safe Mission Communications Planner
Library           OperatingSystem
Library           Collections
Library           String
Library           ../resources/QuantumTestLibrary.py
Library           ../resources/CryptoTestLibrary.py
Test Teardown     Log Test State

*** Variables ***
${QASM_DIR}       ../../src/quantum/circuits
${TEST_SHOTS}     1024
${ERROR_THRESHOLD} 0.25

*** Test Cases ***
Test BB84 Circuit Loads Correctly
    [Documentation]    Verify that BB84 OpenQASM circuit loads without errors
    ${circuit}=    Load Quantum Circuit    ${QASM_DIR}/bb84.qasm
    Should Not Be Empty    ${circuit}
    ${name}=    Get Circuit Name    ${circuit}
    Should Contain    ${name}    bb84

Test E91 Circuit Loads Correctly
    [Documentation]    Verify that E91 OpenQASM circuit loads without errors
    ${circuit}=    Load Quantum Circuit    ${QASM_DIR}/e91.qasm
    Should Not Be Empty    ${circuit}
    ${name}=    Get Circuit Name    ${circuit}
    Should Contain    ${name}    e91

Test BB84 With Eavesdropping Circuit Loads
    [Documentation]    Verify that BB84 with eavesdropping circuit loads
    ${circuit}=    Load Quantum Circuit    ${QASM_DIR}/bb84_with_eavesdropping.qasm
    Should Not Be Empty    ${circuit}
    ${name}=    Get Circuit Name    ${circuit}
    Should Contain    ${name}    bb84_with_eavesdropping

Test BB84 Protocol Simulation
    [Documentation]    Test BB84 protocol simulation with known parameters
    ${result}=    Simulate BB84 Protocol    0    1    1    ${TEST_SHOTS}
    # Alice bit=0, Alice basis=X(1), Bob basis=X(1) -> should get correlated results
    ${sifted_key}=    Get From Dictionary    ${result}    sifted_key_alice
    ${bob_sifted}=    Get From Dictionary    ${result}    sifted_key_bob
    Should Be Equal As Strings    ${sifted_key}    ${bob_sifted}
    ${error_rate}=    Get From Dictionary    ${result}    error_rate
    Should Be True    ${error_rate} < 0.1  # Low error rate expected when no eavesdropping

Test BB84 Protocol With Mismatched Bases
    [Documentation]    Test BB84 when Alice and Bob use different bases
    ${result}=    Simulate BB84 Protocol    0    1    0    ${TEST_SHOTS}
    # Alice bit=0, Alice basis=X(1), Bob basis=Z(0) -> should get ~50% correlation
    ${sifted_key}=    Get From Dictionary    ${result}    sifted_key_alice
    ${bob_sifted}=    Get From Dictionary    ${result}    sifted_key_bob
    # When bases don't match, sifted key should be empty or very small
    ${key_length}=    Get From Dictionary    ${result}    key_length
    Should Be True    ${key_length} < 5  # Expect very few matches with random bases

Test PQC Key Generation
    [Documentation]    Test that PQC keypair generation works
    ${public_key}, ${secret_key}=    Generate PQC Keypair
    Should Not Be Empty    ${public_key}
    Should Not Be Empty    ${secret_key}
    ${length}=    Get Length    ${public_key}
    Should Be True    ${length} > 0

Test PQC Encapsulation Decapsulation
    [Documentation]    Test PQC key encapsulation and decapsulation
    ${public_key}, ${secret_key}=    Generate PQC Keypair
    ${ciphertext}, ${shared_secret}=    PQC Encapsulate    ${public_key}
    ${decrypted_secret}=    PQC Decapsulate    ${ciphertext}    ${secret_key}
    Should Be Equal As Bytes    ${shared_secret}    ${decrypted_secret}

Test PQC Sign Verify
    [Documentation]    Test PQC signature generation and verification
    ${data}=    Create List    81    72    65    76    73    32    67    79    77    77    85    78    73    67    65    83    72    65    67    85    82  # "Quantum Secure" in ASCII
    ${message}=    Convert To Bytes    ${data}
    ${signature}, ${pub_key}, ${sec_key}=    Sign Message    ${message}
    ${valid}=    Verify Signature    ${message}    ${signature}    ${pub_key}
    Should Be True    ${valid}

Test DuckDB Analytics
    [Documentation]    Verify DuckDB analytical queries
    ${analytics}=    Get Mission Analytics
    Should Not Be Empty    ${analytics}
    Dictionary Should Contain Key    ${analytics}    total_simulations
    Dictionary Should Contain Key    ${analytics}    success_rate

Test Chroma Policy Storage
    [Documentation]    Verify Chroma vector store for policies
    ${policy_id}=    Generate Random String    8
    Add Security Policy    ${policy_id}    This is a quantum security policy    {"type": "encryption"}
    ${policies}=    List Security Policies
    Should Contain    ${policies}    ${policy_id}
    ${search_results}=    Search Security Policies    quantum security
    ${documents}=    Get From Dictionary    ${search_results}    documents
    Should Not Be Empty    ${documents}
    Delete Security Policy    ${policy_id}

*** Keywords ***
Load Quantum Circuit
    [Arguments]    ${filepath}
    ${circuit}=    Import Library    QuantumCircuitSimulator    ../../src/quantum/utils/simulator.py
    ${qc}=    Call Method    ${circuit}    load_qasm_file    ${filepath}
    [Return]    ${qc}

Get Circuit Name
    [Arguments]    ${circuit}
    ${name}=    Get Attribute    ${circuit}    name
    [Return]    ${name}

Simulate BB84 Protocol
    [Arguments]    ${alice_bit}    ${alice_basis}    ${bob_basis}    ${shots}
    ${simulator}=    Import Library    QuantumCircuitSimulator    ../../src/quantum/utils/simulator.py
    ${alice_bits}=    Create List    ${alice_bit}
    ${alice_bases}=    Create List    ${alice_basis}
    ${bob_bases}=    Create List    ${bob_basis}
    ${result}=    Call Method    ${simulator}    analyze_bb84_protocol    ${alice_bits}    ${alice_bases}    ${bob_bases}    ${shots}
    [Return]    ${result}

Generate PQC Keypair
    [Arguments]
    ${crypto}=    Import Library    PQCManager    ../../src/crypto/pqc.py
    ${public_key}, ${secret_key}=    Call Method    ${crypto}    generate_keypair
    [Return]    ${public_key}    ${secret_key}

PQC Encapsulate
    [Arguments]    ${public_key}
    ${crypto}=    Import Library    PQCManager    ../../src/crypto/pqc.py
    ${ciphertext}, ${shared_secret}=    Call Method    ${crypto}    encapsulate    ${public_key}
    [Return]    ${ciphertext}    ${shared_secret}

PQC Decapsulate
    [Arguments]    ${ciphertext}    ${secret_key}
    ${crypto}=    Import Library    PQCManager    ../../src/crypto/pqc.py
    ${shared_secret}=    Call Method    ${crypto}    decapsulate    ${ciphertext}    ${secret_key}
    [Return]    ${shared_secret}

Sign Message
    [Arguments]    ${message}
    ${crypto}=    Import Library    PQCManager    ../../src/crypto/pqc.py
    ${signature}, ${public_key}, ${secret_key}=    Call Method    ${crypto}    sign_message    ${message}
    [Return]    ${signature}    ${public_key}    ${secret_key}

Verify Signature
    [Arguments]    ${message}    ${signature}    ${public_key}
    ${crypto}=    Import Library    PQCManager    ../../src/crypto/pqc.py
    ${valid}=    Call Method    ${crypto}    verify_signature    ${message}    ${signature}    ${public_key}
    [Return]    ${valid}
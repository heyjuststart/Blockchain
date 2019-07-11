import hashlib
import requests
import json
import time

import sys


# TODO: Implement functionality to search for a proof
def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f"{last_proof}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof


if __name__ == "__main__":
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    start_time = time.time()
    last_time = start_time
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(f"{node}/last_proof").json()["result"]
        # TODO: When found, POST it to the server {"proof": new_proof}
        next_proof = proof_of_work(int(last_proof))

        did_we_get_one = (
            requests.post(
                f"{node}/mine",
                data=json.dumps({"proof": next_proof}),
                headers={"content-type": "application/json"},
            ).status_code
            == 200
        )

        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if did_we_get_one:
            coins_mined += 1
            print(f"Found one! {next_proof}, #coins: {coins_mined}, time: {(time.time() - last_time) / 60} min")
            last_time = time.time()
        else:
            print("Nope!")

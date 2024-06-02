import os
import re

# Define the curl command to post the CSV file
curl_command = """
curl -X 'POST' \
  'http://localhost:8000/claims/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@claim_1234.csv;type=text/csv'
"""

# Execute the curl command
os.system(curl_command)

# Check docker processes and capture the output
docker_ps_output = os.popen("docker ps").read()

# Find the container name similar to "claim_process-claim_process-1" and "payments-1"
claim_process_container_name = None
payment_container_name = None
for line in docker_ps_output.split("\n"):
    if re.search(r"payments-1", line):
        payment_container_name = line.split()[-1]


if payment_container_name:
    # Retrieve and filter logs for the payment container name
    os.system(f"docker logs {payment_container_name} > payment.log")

    # Reading the content of the log file to search for the specific message
    with open('payment.log', 'r') as file:
        logs = file.readlines()

    # Check if 'payments-1' is in the log and print the entire log if found
    for log in logs:
        if "payments-1" in log:
            print("Entire log for 'payments-1':\n")
            for line in logs:
                print(line)
            break
else:
    print("No container found with the name similar to 'payments-1'")

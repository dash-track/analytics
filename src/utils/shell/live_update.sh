#!/bin/bash
# Prototype file for live updates in the terminal
counter=0
while [ $counter -lt 10 ]; do
    # Print the counter value with no newline, then move the cursor back to the start of the line
    echo -ne "Counter: $counter\r"
    # Increment the counter
    ((counter++))
    # Wait for a second
    sleep 1
done
# Print a newline after the loop is done to move to the next line
echo ""

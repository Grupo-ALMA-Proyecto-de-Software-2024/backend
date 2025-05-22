#!/bin/bash
# entrypoint.sh

# Execute the command
echo "Running entrypoint.sh"

make migrate
make collectstatic
make run-prod

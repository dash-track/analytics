#!/usr/bin/env bash
#^ Dynamically set the path to the bash interpreter
while [[ $# -gt 0 ]]; do
    case $1 in
    *)
        echo "Unknown argument: $1"
        exit 1
        ;;
    esac
done
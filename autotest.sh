#!/bin/bash

echo "Running code formatting..."
black .

echo "Running Tests..."
make test

echo "Checks passed!"

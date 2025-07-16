#!/bin/bash

# Copy scripts to app directory for Docker builds
echo "📁 Copying scripts to app directory for Docker build..."

# Create scripts directory in app if it doesn't exist
mkdir -p app/scripts

# Copy all scripts to app/scripts
cp -r scripts/* app/scripts/

echo "✅ Scripts copied to app/scripts/" 
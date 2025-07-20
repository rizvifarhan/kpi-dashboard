#!/bin/bash

# Quick deployment fix for module import error
echo "Fixing deployment error..."

# Add all changes
git add .

# Commit the fix
git commit -m "Fix deployment: rename database module to kpi_database"

# Force push to update GitHub
git push origin main --force

echo "Deployment fix pushed to GitHub!"
echo "Your app will be live in 2-3 minutes."
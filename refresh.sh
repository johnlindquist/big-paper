#!/bin/bash
# Force TRMNL X refresh for big-paper project
DEVICE_KEY="_vsw73kEVbDRGFZTR4qHTQ"
MAC="3C:0F:02:CD:39:BC"

echo "Forcing TRMNL refresh..."
curl -s -X POST "https://api.trmnl.com/api/devices/refresh" \
  -H "Authorization: Bearer $DEVICE_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"mac\":\"$MAC\"}" | jq .

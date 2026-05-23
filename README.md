# big-paper

Hermes-powered TRMNL X news jokes plugin.

## Overview
- Generates witty jokes about current news headlines
- Updates every 15 minutes during work hours (9am–6pm)
- Full HTML screens optimized for TRMNL X (large text, dense layout)
- Pushed via TRMNL webhook + Device API refresh

## Files
- `refresh.sh` — manually force a TRMNL screen update
- `cron.md` — details on the Hermes cron job

## Commands
```bash
~/bin/trmnl-refresh     # Force immediate refresh
```

## Cron Job
Managed via Hermes (`job_id: 231a0c32fbe3`)

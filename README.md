# Python Discord Bot

## Overview
A Discord bot for tracking speedrun times across different maps. Users can submit times, view leaderboards, and administrators can manage the data.

## Purpose
This bot allows Discord server members to:
- Submit speedrun times for different maps
- View top 10 times for any map
- List all maps with recorded times
- Administrators can delete maps or remove specific times

## Project Architecture
- **main.py**: Discord bot setup and command handlers
- **mapTime.py**: Class for managing map time data (stored in JSON files)
- **times_*.json**: Data files storing times for each map (gitignored)
- **discord.log**: Bot activity log (gitignored)

## Commands
- `!submit <map_name> <time>`: Submit a time for a map
- `!times <map_name>`: View top 10 times for a map
- `!maplist`: List all maps with recorded times
- `!deletemap <map_name>`: (Admin only) Delete all times for a map
- `!removetime <map_name> <index>`: (Admin only) Remove a specific time entry

## Setup Requirements
- Python 3.11
- Discord bot token (stored in DISCORD_TOKEN secret)
- Required Python packages: discord.py, python-dotenv

## Recent Changes
- 2025-11-02: Initial import and Replit environment setup
  - Installed Python 3.11 and dependencies
  - Configured .gitignore to allow requirements.txt in version control
  - Set up workflow to run the Discord bot
#!/bin/bash
# Backup Local Deployment Script for Upemba Edge Server

PI_USER="admin"
PI_IP="192.168.1.72"
DEST_DIR="~/upemba-backend"

echo "Deploying Upemba Backend to Raspberry Pi ($PI_IP)..."

# Ensure destination directory exists before syncing
ssh $PI_USER@$PI_IP "mkdir -p $DEST_DIR"

# Rsync securely transfers exclusively the changed files over SSH cleanly, skipping the heavy dev dependencies
rsync -avz --exclude-from='.gitignore' --exclude='.git/' --exclude='.venv/' ./ $PI_USER@$PI_IP:$DEST_DIR

echo "Rebuilding Production Docker Architecture on the Edge Server..."
ssh $PI_USER@$PI_IP "cd $DEST_DIR && docker compose -f docker-compose.production.yml up -d --build"

echo "Cleaning up old Docker images..."
ssh $PI_USER@$PI_IP "docker system prune -f"

echo "Backup Deployment Complete!"

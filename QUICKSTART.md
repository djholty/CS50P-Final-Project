# Quick Start Guide

## Get Started in 3 Steps

### Option 1: Docker (Easiest)

```bash
# Start the application
docker-compose up -d

# View it in your browser
open http://localhost:8000

# Stop the application
docker-compose down
```

### Option 2: Local Python

```bash
# Run the startup script
./run.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

## First Time Setup

1. **Add Your Children**
   - Click "Add Child" in the navigation
   - Enter each child's name

2. **Add Workbooks**
   - Click "Add Workbook"
   - Enter workbook names (e.g., "Grade 3 Math")

3. **Start Tracking**
   - From home page, click "Add Transaction" for a child
   - Enter positive amounts for earnings
   - Enter negative amounts for purchases

## Common Tasks

### Record a Completed Workbook
1. Go to child's dashboard
2. Click "Complete Workbook"
3. Select workbook and date
4. Submit

### Add Money (Reward)
1. Click "Add Transaction"
2. Enter date and description
3. Enter positive amount (e.g., 25.00)
4. Submit

### Record a Purchase
1. Click "Add Transaction"
2. Enter date and description
3. Enter negative amount (e.g., -10.50)
4. Submit

## Accessing from Other Devices

### On Same Network

1. Find your computer's IP address:
   ```bash
   # macOS/Linux
   hostname -I
   
   # macOS alternative
   ifconfig | grep "inet "
   ```

2. On other device, open browser to:
   ```
   http://[YOUR_IP]:8000
   ```
   Example: `http://192.168.1.100:8000`

## Troubleshooting

**Port already in use?**
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 [PID]

# Or change port in docker-compose.yml or run command
```

**Database locked?**
```bash
# Check if CLI version is running
ps aux | grep project.py

# Close any running instances
```

## Testing

Run tests before making changes:
```bash
pytest
```

## Getting Help

- Check README.md for detailed documentation
- Check PLANNING.md for architecture details
- Check TASK.md for development notes

## Tips

1. **Backup regularly**: Copy `ledgerdb.sqlite` before major changes
2. **Use Docker**: Easier deployment and updates
3. **Mobile access**: Works great on phones/tablets
4. **Bookmark it**: Add to home screen on mobile devices

## Next Steps

Once familiar with basics:
- Review README.md for advanced features
- Set up automated backups
- Configure auto-start on server
- Customize styling in `app/static/css/custom.css`

Enjoy tracking your children's finances! 🎉



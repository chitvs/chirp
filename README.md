# Chirp, a Python bot for effortless Twitter content automation

A Python-based Twitter/X automation bot that posts photos from your repository at scheduled intervals using GitHub Actions. Built with Tweepy for reliable photo uploads, file management, and comprehensive error handling.

## Features

* Automated photo posting to Twitter/X at scheduled intervals
* GitHub Actions integration for seamless deployment
* Smart file management with automatic organization
* Comprehensive logging and activity tracking
* Manual execution capability for on-demand posting
* Robust error handling with retry logic
* Simple environment variable configuration

## Project Structure

```
chirp/
├── .github/
│   └── workflows/
│       └── bot-workflow.yml     # GitHub Actions automation
├── photos/                      # Put your photos here              
├── posted_photos/               # Successfully posted photos              
├── photos_rejected/             # Rejected photos              
├── bot.py                       # Main bot script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template                  
├── LICENSE                      
├── post_log.txt                 # Activity log 
└── README.md                    
```

## Quick Start

### Get X API Access

1. Apply for X Developer Account

   * Go to [X Developer Portal](https://developer.x.com)
   * Click "Sign up" or "Apply for a developer account"
   * Complete the application (explain you're building a personal photo bot)
   * Wait for approval

2. Create a X App

   * Once approved, go to [Developer Portal Dashboard](https://developer.x.com/portal/dashboard)
   * Click "Create App" or "New App"
   * Fill in app details
   * Click "Create"

3. Generate API Keys

   * In your app dashboard, go to "Keys and Tokens" tab
   * API Key & Secret: Click "Regenerate" and copy both
   * Access Token & Secret: Click "Generate" and copy both

4. Set App Permissions

   * Go to "App Settings" and then "App Permissions"
   * Select "Read and Write" (required for posting)
   * Save changes

### Repository Setup

Clone this repository

```bash
git clone https://github.com/chitvs/chirp.git
cd chirp
```

### Configure GitHub Secrets

> [!CAUTION]
> Your X API keys must be added as GitHub repository secrets.

1. Go to your repository on GitHub
2. Click the Settings tab
3. In the left sidebar, click "Secrets and variables" and then "Actions"
4. Click "New repository secret" and add each of these:

| Secret Name           | Value                      |
| --------------------- | -------------------------- |
| `API_KEY`             | Your X API Key             |
| `API_SECRET`          | Your X API Secret          |
| `ACCESS_TOKEN`        | Your X Access Token        |
| `ACCESS_TOKEN_SECRET` | Your X Access Token Secret |

These correspond to the variables in your `.env` file:

```
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
ACCESS_TOKEN=your_access_token_here
ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

> [!WARNING]
> Never commit these keys to your repository or share them publicly.

### Add Your Photos

Upload photos to the `photos/` directory. The bot posts photos in alphabetical order, so consider using numbered prefixes for consistent ordering:

```
photos/
├── 01_sunset.jpg
├── 02_coffee.png
├── 03_cat.jpg
```

Photo Requirements:

* Maximum size: 5MB per photo
* Place files directly in the `photos` folder, not in subfolders

### Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. If prompted, click "I understand my workflows, go ahead and enable them"
4. The bot will now run automatically every 32 hours (you can change this value as explained then)

## Configuration

### Changing Post Schedule

Edit the cron expression in `.github/workflows/bot-workflow.yml`:

```yaml
schedule:
  - cron: '0 */32 * * *'  # Every 32 hours (default)
```

> [!TIP]
> Use [Crontab Guru](https://crontab.guru/) to validate custom expressions.

### Customizing Bot Behavior

* Retry attempts: adjust `max_attempts=3` in `post_random_photo()`
* Tweet text: modify the `text=""` parameter in `client.create_tweet()`
* Photo selection logic: currently selects the first photo alphabetically, update logic in `post_random_photo()` if needed

## How It Works

1. Scans the `photos/` directory for the first alphabetically sorted photo
2. Attempts to upload the photo to Twitter/X
3. On success:
   * Moves photo to `posted_photos/`
   * Logs the post in `post_log.txt`
4. On failure:
   * Moves the photo to `photos_rejected/`
   * Logs the error
   * Tries the next photo (up to 3 attempts per run)

## Automation Schedule

| Trigger Type | When It Runs    | Description                              |
| ------------ | --------------- | ---------------------------------------- |
| Scheduled    | Every 32 hours  | Automatic execution via GitHub Actions   |
| Push         | On code commits | Runs when you push to the main branch    |
| Manual       | On demand       | Trigger manually from GitHub Actions tab |

## File Management

```
photos/                   # Your source photos
├── photo1.jpg
└── photo2.png

posted_photos/            # Successfully posted
├── photo3.jpg
└── photo4.png

photos_rejected/          # Failed to post
├── corrupted.jpg
└── too_large.png
```

## Monitoring and Logs

### Viewing Execution Logs

1. Go to your GitHub repository
2. Click the "Actions" tab
3. Click on a workflow run to view logs

### Local Activity Log

`post_log.txt` will include entries like:

```
2025-07-01 10:30:15: Posted photo 'sunset.jpg'
2025-07-01 10:30:20: Rejected photo 'corrupted.jpg' - File format not supported
2025-07-02 18:45:32: Posted photo 'coffee.png'
2025-07-03 02:15:45: No photos found in directory
```

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make and test your changes
4. Commit: `git commit -m 'Add feature'`
5. Push: `git push origin feature/my-feature`
6. Open a Pull Request

## Acknowledgments

Chirp uses:

* Tweepy: Python library for Twitter API integration
* GitHub Actions: For seamless automation
* X Developer Platform: Providing API access

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
import os
import yt_dlp
import instaloader
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Initialize Instaloader for Instagram
ig_loader = instaloader.Instaloader()

# Function to download from YouTube using yt-dlp
def download_youtube(url: str):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# Function to download from Instagram using Instaloader
def download_instagram(url: str):
    ig_post = instaloader.Post.from_shortcode(ig_loader.context, url.split("/")[-2])
    ig_loader.download_post(ig_post, target="downloads/")
    return f'downloads/{ig_post.owner_username}_{ig_post.date_utc}.mp4'

# Placeholder function for LinkedIn (requires custom implementation)
def download_linkedin(url: str):
    # For LinkedIn video scraping (simplified for demonstration)
    response = requests.get(url)
    video_path = 'downloads/linkedin_video.mp4'
    with open(video_path, 'wb') as f:
        f.write(response.content)
    return video_path

# Handler function to detect platform and process the video link
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    try:
        if 'youtube.com' in url or 'youtu.be' in url:
            update.message.reply_text('Downloading video from YouTube...')
            video_file = download_youtube(url)
        elif 'instagram.com' in url:
            update.message.reply_text('Downloading video from Instagram...')
            video_file = download_instagram(url)
        elif 'linkedin.com' in url:
            update.message.reply_text('Downloading video from LinkedIn...')
            video_file = download_linkedin(url)
        else:
            update.message.reply_text('Unsupported URL!')
            return

        # Send the downloaded video to Telegram
        with open(video_file, 'rb') as video:
            update.message.reply_video(video)
        update.message.reply_text('Video uploaded successfully!')

    except Exception as e:
        update.message.reply_text(f"Failed to download the video: {str(e)}")

# Main function to start the bot
def main():
    # Set up Telegram bot token
    TOKEN = os.getenv("7828501958:AAFGuzqo1eKWYNBsQmita2MqD8or6xc3_jU")
    updater = Updater(TOKEN)

    # Add a message handler to process any text message (URL links)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot with polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

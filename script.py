import os
import csv
import time
import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('instagram_comments.log'),
        logging.StreamHandler()
    ]
)

class InstagramCommentDownloader:
    def __init__(self):
        self.client = Client()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.max_retries = 3
        self.delay = 2
        self.comments_count = 0

    def login(self):
        """Handle Instagram login with retry logic"""
        try:
            username = os.getenv('INSTAGRAM_USERNAME')
            password = os.getenv('INSTAGRAM_PASSWORD')
            
            if not username or not password:
                raise ValueError("Missing credentials in .env file")

            self.client.login(username, password)
            logging.info(f"Successfully logged in as {username}")
            return True
        except Exception as e:
            logging.error(f"Login failed: {e}")
            return False

    def get_all_comments(self, media_id):
        """Download all comments with pagination and retry logic"""
        comments = []
        retry_count = 0
        
        while retry_count < self.max_retries:
            try:
                # Get comments with pagination
                for comment in self.client.media_comments(media_id, amount=0):
                    comment_data = {
                        'comment_id': comment.pk,
                        'user_id': comment.user.pk,
                        'username': comment.user.username,
                        'text': comment.text,
                        'created_at': comment.created_at_utc.strftime('%Y-%m-%d %H:%M:%S'),
                        'likes': comment.like_count
                    }
                    comments.append(comment_data)
                    self.comments_count += 1
                    
                    if self.comments_count % 100 == 0:
                        logging.info(f"Downloaded {self.comments_count} comments...")
                    time.sleep(0.5)  # Rate limiting
                    
                return comments
                
            except LoginRequired:
                retry_count += 1
                if retry_count >= self.max_retries:
                    logging.error("Max retries reached - failed to get comments")
                    break
                logging.warning(f"Session expired, retrying {retry_count}/{self.max_retries}...")
                self.login()
                time.sleep(self.delay)
                
            except Exception as e:
                logging.error(f"Error getting comments: {e}")
                break
                
        return comments

    def save_outputs(self, comments, media_id):
        """Save comments in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_path = self.output_dir / f"comments_{media_id}_{timestamp}"
        
        # Save CSV
        csv_path = base_path.with_suffix('.csv')
        fieldnames = ['comment_id', 'user_id', 'username', 'text', 'created_at', 'likes']
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(comments)
            
        # Convert to DataFrame and sort
        df = pd.DataFrame(comments)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df = df.sort_values(['created_at', 'likes'], ascending=[False, False])
        
        # Save Excel with formatting
        excel_path = base_path.with_suffix('.xlsx')
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Comments')
            workbook = writer.book
            worksheet = writer.sheets['Comments']
            
            # Add header formatting
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D3D3D3',
                'border': 1
            })
            
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Set column widths
            worksheet.set_column('A:A', 20)  # comment_id
            worksheet.set_column('B:B', 15)  # user_id
            worksheet.set_column('C:C', 20)  # username
            worksheet.set_column('D:D', 40)  # text
            worksheet.set_column('E:E', 20)  # created_at
            worksheet.set_column('F:F', 10)  # likes
            
        # Save JSON
        json_path = base_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
            
        return csv_path, excel_path, json_path

    def download_comments(self, post_url):
        """Main method to download and save comments"""
        try:
            if not self.login():
                return False

            media_id = self.client.media_pk_from_url(post_url)
            logging.info(f"Downloading comments for media ID: {media_id}")

            comments = self.get_all_comments(media_id)
            if not comments:
                logging.warning("No comments found")
                return False

            csv_path, excel_path, json_path = self.save_outputs(comments, media_id)
            logging.info(f"""
            Successfully saved {len(comments)} comments to:
            CSV: {csv_path}
            Excel: {excel_path}
            JSON: {json_path}
            """)
            return True

        except Exception as e:
            logging.error(f"Error downloading comments: {e}")
            return False

def main():
    load_dotenv()
    post_url = os.getenv('INSTA_POST_URL')
    
    if not post_url:
        logging.error("INSTA_POST_URL not set in .env file")
        return
        
    downloader = InstagramCommentDownloader()
    if downloader.download_comments(post_url):
        print("\nSuccessfully downloaded all comments!")
    else:
        print("\nFailed to download comments")

if __name__ == "__main__":
    main()
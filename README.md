# Instagram Comment Downloader

Download and analyze Instagram post comments with multi-format export capabilities.

## Features

- Download all comments from Instagram posts
- Export to CSV, Excel, and JSON formats
- Sort by date and likes
- Rate limiting and retry logic
- Progress tracking
- Detailed error logging

## Installation

1. Clone repository and create virtual environment:

```powershell
git clone https://github.com/yourusername/instagram-comment-downloader.git
cd instagram-comment-downloader
python -m venv venv
.\venv\Scripts\activate
```


2. Install dependencies:

   pip install -r requirements.txt
3. Configure [.env](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) file:

   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   INSTA_POST_URL=https://www.instagram.com/p/POST_ID/

## Usage

Run the script:

python script.py


## Output Files

The script generates three files in the [output](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) directory:


### CSV Format:

comment_id,user_id,username,text,created_at,likes
12345,67890,user123,"Great post!",2024-02-06 12:34:56,5


### Excel Format

* Sorted by date (newest first)
* Formatted headers
* Optimized column widths
* Filter capabilities



### JSON Format

**{**

**  **"comment_id"**: **"12345"**,**

**  **"user_id"**: **"67890"**,**

**  **"username"**: **"user123"**,**

**  **"text"**: **"Great post!"**,**

**  **"created_at"**: **"2024-02-06 12:34:56"**,**

**  **"likes"**: **5

**}**




## Error Handling

The script handles:

* Login failures
* Rate limiting
* Network issues
* Session expiration
* Challenge required

## Requirements

* Python 3.8+
* Required packages listed in [requirements.txt](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
* Instagram account credentials
* Post URL

## Project Structure

instagram-comment-downloader/
├── script.py           # Main script
├── .env               # Configuration
├── requirements.txt   # Dependencies
├── README.md         # Documentation
└── output/           # Generated files
    ├── comments_[POST_ID]_[TIMESTAMP].csv
    ├── comments_[POST_ID]_[TIMESTAMP].xlsx
    └── comments_[POST_ID]_[TIMESTAMP].json


## License

MIT License

## Disclaimer

This tool is for educational purposes only. Please comply with Instagram's terms of service. ```

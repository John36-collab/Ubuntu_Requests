---

Ubuntu Image Fetcher - Enhanced Edition

A Python-based utility designed to mindfully collect images from the web, while prioritizing safety, efficiency, and community awareness. This tool embodies the spirit of Ubuntu by responsibly handling web resources and avoiding redundant downloads.


---

📁 Project Structure

The script is a standalone executable Python file that can be run directly in a Unix-like terminal. It is structured into clearly defined functional sections, each serving a dedicated purpose within the image fetching workflow.


---

🔧 Modules & Libraries

The script uses standard Python libraries such as:

requests – For sending HTTP/HTTPS requests.

os and pathlib – For file system operations.

hashlib – For generating hashes to detect duplicates.

urllib.parse – To parse and interpret URLs.

mimetypes – To infer file types from content types.


These are all part of the Python Standard Library or widely accepted third-party packages.


---

🔍 Functional Overview

1. Hash Calculation

A function computes the MD5 hash of image files. This is used to detect duplicate images by comparing the hash of new content with already downloaded files.


---

2. Duplicate Detection

Before saving any image, the script checks the target directory for existing images with the same hash. If found, it skips downloading the image again and provides user feedback about the duplication.


---

3. Safety Checks

Each image undergoes a series of safety checks before being downloaded:

Content Type Check: Ensures the resource is a valid image.

File Size Check: Blocks files larger than 10MB.

Extension Check: Issues a warning if the URL doesn't contain a common image extension.


These checks are built to prevent downloading unsafe or incorrect files.


---

4. Filename Handling

The script tries to determine an appropriate filename using several strategies:

Extracts the filename from the URL path.

Falls back on HTTP headers like Content-Disposition.

Uses the content type to generate a safe extension if necessary.


It also sanitizes the filename by removing problematic characters and ensures uniqueness by appending counters if the filename already exists.


---

5. Download Process

The actual download logic uses a streaming request to efficiently manage memory, especially with larger files. It handles:

Redirects

Network failures

Duplicate avoidance

Filename collisions


A success or failure message is printed for each image.


---

6. User Interaction

At runtime:

The user is greeted with a welcome message.

They're prompted to enter one or more image URLs, separated by commas.

Each URL is processed in sequence, with live feedback.

A summary report is displayed at the end.



---

✅ Output

All successfully fetched images are saved in a local folder called Fetched_Images.

Duplicate files are skipped, and a log message indicates their status.



---

✨ Ubuntu Ethos

True to its name, this tool is designed not just for utility but with a sense of responsibility and consideration:

It avoids waste by skipping duplicates.

It respects bandwidth and server limits.

It informs the user without overwhelming them.



---

🔄 Execution Flow

1. Startup – Greeting and setup.


2. User Input – Collects image URLs.


3. Processing – Each image is validated, fetched, and saved.


4. Feedback – Console logs communicate progress.


5. Summary – A final report highlights successful downloads.




---

💡 Usage Notes

Requires an internet connection.

Best used in environments where direct image downloads are needed quickly and reliably.

Can be expanded to support batch processing from files or APIs.



---

📌 Final Thoughts

The Ubuntu Image Fetcher is a demonstration of how simple tools can be mindful, safe, and user-centered. Its modular structure makes it ideal for extension, automati


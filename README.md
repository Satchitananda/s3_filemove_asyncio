# s3 filemove asyncio
Example of using aiobotocore (Async fork of boto3 - Amazon S3 API) for asynchronous file moving from one bucket to another with monitor service on django.

# Installation

Setup requirements:
```
pip install -r requirements.txt
```

Fill up settings of your Amazon S3 in django settings.py
```
AWS_KEY = 'Your key'
AWS_SECRET = 'Your secret'
FROM = 'bucket name from which files should be moved'
TO = 'bucket to move files to'
```

Set up your PostgreSQL database and change settings.py accordingly

Run django development server
```
python manage.py runserver
```
Locate your browser to 'http://localhost:8000'

Run these commands to fill up sample files and move them across the buckets
```
python manage.py create_files N > files.txt
python manage.py move_files -f files.txt
```
Watch the progress

Requires Python 3.4+ or Python 3.3 with asyncio.

Asynchronous website monitoring script. If some of websites are not responding
script will notify you via email.

Put your list of domains into domains.txt

Add script to crontab

Example:
```
*/30 * * * * /usr/bin/python /home/username/sitepinger/sitepinger.py
```
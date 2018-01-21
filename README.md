# Grade Tracker
**Grade Tracker** is a simple python script made to track any new grades on college's website.
The script uses a platform-independent api to push notifications to user.
It is made for students of Faculty of Engineering, Alexandria University for Ibn Elhaitham system.

# Installing dependencies and usage
[Python 3][1] is required to run this script.

In `config.ini` you need to change `UserName` and `Password` values.

* To install dependencies
```bash
    $ pip install -r requirements.txt
```
* To run the script once
```bash
    $ python GradeTracker.py
```
* To run the script periodically (Runs every 5 minutes)
```bash
    $ python Scheduler.py
```

Note: To hide the console while using the `Scheduler.py` script, change the extension to `.pyw`.

[1]: https://www.python.org/downloads/

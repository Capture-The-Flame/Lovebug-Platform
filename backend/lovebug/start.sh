#!/bin/bash
python manage.py migrate --noinput
gunicorn lovebug.wsgi --log-file -
```

Then update your `Procfile`:
```
web: bash start.sh
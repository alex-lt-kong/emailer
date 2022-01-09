# emailer

An email sending facility for personal use.

# Usage

1.
```
import importlib

emailer = importlib.machinery.SourceFileLoader(
                    fullname='emailer',
                    path='path to this repo'
                ).load_module()
```

2. Add the path of this repo to $PYTHONPATH, e.g.
```
export PYTHONPATH="$HOME/bin:$PYTHONPATH"
```
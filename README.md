# emailer

An email sending facility for personal use.

# Usage

1. Dynamically import this repo
```
import importlib

emailer = importlib.machinery.SourceFileLoader(
                    fullname='emailer',
                    path='path to this repo'
                ).load_module()

emailer.send()
```

2. Add the path of this repo to $PYTHONPATH, e.g.
```
export PYTHONPATH="$HOME/bin:$PYTHONPATH"
```
and them import and use as an ordinary Python package
```
import emailer.emailer as em

em.send()
```
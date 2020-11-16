# common-ledger-tech-test

I used Python 3.7.4 but I'm sure Python 3.6 and higher will work fine. If you've got an older version installed, it's probably best to use Pyenv to get Python 3.7 while maintaining your older version.

To install and run this project:

```
# Set up the venv
python -m venv venv/

# Activate the virtual environment
source venv/bin/activate

# Install the packages
pip install -r requirements.txt

# Run the server
sh startup.sh
```

If there are no errors then the website will be on `localhost:5000`. The virtual environment step _can_ be skipped but you'll end up polluting your global packages and collisions could happen with other projects.

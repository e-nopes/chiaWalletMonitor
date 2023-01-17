# chiaWalletMonitor
When your wallet gets XCH, you get a Discord webhook message



## Usage

First create a virtual env and install de dependencies:
```cli
python3 -m venv --system-site-packages venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Start the application with:
`python ./chiaWallet.py`

#ubuntu gotcha
if pip install cannot find dbus, try `apt install python-dbus`

Run on windows with `pythonw` instead of `python` to run it in the background on windows.  Linux users have their own ways.

## Notifications supported

Currently notification support is:  Discord

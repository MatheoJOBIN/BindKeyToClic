# BindKeyToClic

This project is made for binding arrow keys to moving click in dofus.
It's currently tested on windows 10 OS only.
There might be 5 to 10 seconds latency on the first key press.

## Binded keys

- Arrow keys : click on the corresponding direction on the screens of all your selected accounts
- `ctrl+q` OR `escape` quit the application
- `,` open a window allowing you to fast travel to a location with autopilot

## How to launch

- Double click on the exe in dist folder
- Enjoy your moves

## Troubleshooting

If the executable does not launch, check the following advices:

- rebuild the project [Click here to see how to do](#build-the-project)

## Build the project

Open a command terminal, go to the keytoclick folder (ex : cd C:/user/userName/downloads)
Execute the following command `pyinstaller .\keyToClic.py --clean -F -y`
The executable is renewed, retry executing it

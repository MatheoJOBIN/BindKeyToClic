# BindKeyToClic

This project is made for binding arrow keys to moving click in dofus.
It's currently tested on windows 10 OS only

## How to launch

- Double click on the exe in dist folder.
- Enter your characters names case sensitive, seprated by a comma (ex : Scoupp,Scoupsoin) for each window you want to control
- Enjoy your arrow keys

## Troubleshooting

If the executable does not launch, check the following advices:

- rebuild the project [Click here to see how to do](#build-the-project)

## Build the project

Open a command terminal, go to the keytoclick folder (ex : cd C:/user/userName/downloads)
Execute the following command `pyinstaller .\keyToClic.py --clean -F -y`
The executable is renewed, retry executing it

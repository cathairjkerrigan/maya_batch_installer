# Maya Batch Installer

Template setup for adding a batch installer for your repository. 

Includes a drag and drop installer which installs the repository on the users PC and creates the .bat files required for starting Maya with the repository. 

Also includes setup for a custom menu and shelf to access code within the repository and a reload function to reload any modules inside of the repos folder without closing or reopening Maya. Note this won't affect the shelf or menu by default.


# Install
Download the ZIP folder and replace the repos folder with your own code repository.

To adjust the menu name and items and reload function, open src.core.startup.py and adjust to fit your needs. 

To adjust the shelf name and items, open src.core.shelf.toolkit_shelf.py and adjust to fit your needs.

# Known Limitations
Code has only been tested using Windows and may not work without adjustment with other operating systems such as Linux or macOS.
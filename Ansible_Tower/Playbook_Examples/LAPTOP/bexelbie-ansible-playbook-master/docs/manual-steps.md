# Things I haven't figured out so I do by hand

  * Set displays to mirror in GNOME

  * Configure Firefox
    * Reload Bookmarks (or restore the places.sqlite file/database)
    * General: Startup: Restore Previous Session and Warn When Quitting
    * General: Downloads: Always ask where to save
    * General: Applications: Set mailto: handler to always ask
    * Home: New Windows and Tabs: Blank Page
    * Home: Turn off all Firefox Content
    * Search: Set Search to Duck Duck Go
    * Privacy and Security: Always send do not track
    * Privacy and Security: Uncheck Ask to save logins and passwords for websites
    * Privacy and Security: Clear data at this point so new settings override previous browsing
    * Privacy and Security: Firefox Data Collection and Use: Disable studies and personalized extensions
    * Extensions: Add Stop Facebook tracking with Facebook Container by Mozilla
    * Extensions: Add Tree Style Tab
    * Extensions: Add DuckDuckGo Privacy Essentials
    * Menu:View:Show bookmark toolbar

  * Run Dropbox and manage the login process to start syncing

  * Install Franz: https://meetfranz.com/download
    1. Download
    2. mkdir ~/bin && mv <file> ~/bin
    3. chmod a+x ~/bin/<file>
    4. Copy over the ~/.config/Franz dir from the backup
    5. execute <file>

  * Configure Chrome
    * Make Default Browser
    * Reload Bookmarks
    * Settings: Passwords: uncheck offer to save passwords and auto sign-in
    * Settings: Payment Methods: uncheck save and fill payment methods
    * Settings: Addresses: uncheck save and fill addresses
    * Settings: Turn on Show Bookmark bar
    * Settings: On Startup: Continue where you left off
    * Settings: Advanced: Privacy and Security: turn off Allow Chrome sign-in
    * Settings: Advanced: Privacy and Security: turn on Do Not Track
    * Settings: Advanced: Privacy and Security: turn off payment method checking
    * Settings: Advanced: Clear All Browsing data for a clean reset
    * Settings: Advanced: Downloads: turn on Ask Where to Save
    * Add Extensions: https://chrome.google.com/webstore
      - HTTPS Everywhere
      - Privacy Badger
      - DuckDuckGo Privacy Essentials
      - uBlock Origin
      - Adblock Plus
      - TamperMonkey
        - https://greasyfork.org/en/scripts/9165-auto-close-youtube-ads
        - Enable for Incognito Mode
      - Feedly
      - Instapaper

  * Calibre - Configure proper library path

  * Install gocryptfs from Release Source (vendored): https://github.com/rfjakob/gocryptfs
    1. Verify download and untar
    2. mkdir -p ~/bin/man1
    3. mv gocryptfs ~/bin
    3. mv gocryptfs.1 ~/bin/man1

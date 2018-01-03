# Symc with deezer

Sync your local music library to your deezer account

## Requriements
You need git, python and python-pip installed on your machine.
And of course you need a deezer account.

## Install
```
git clone https://github.com/raffis/deezer-local-sync.git
pip install mutagen
pip install requests
```

## Register deezer app
You need to create an [OAUTH2](https://developers.deezer.com/myapps) app first on deezer dev.
 Create the app with followind data (it doesn't really matter though since you only need to obtain the access token once);
App name: move_from_local
Domain: http://localhost
Redirect URL: http://localhost
Link to your term of use: http://localhost
Description: Move local music library to deezer

## Obtain deezer access token
1. Open your browser and go to ` https://connect.deezer.com/oauth/auth.php?app_id=CLIENT_ID&redirect_uri=http://localhost&perms=basic_access,email,manage_library` (Replace CLIENT_ID with the client id you have received after registering your app)
2. Accept the terms and copy the response code
3. Go to `https://connect.deezer.com/oauth/access_token.php?app_id=CLIENT_ID&secret=CLIENT_SECRET&code=CODE`(And again replace CLIENT_ID and CLIENT_SECRET with the strings you have received during registering your app, replace CODE with the return value from the request of step 1.)
4. Copy access token (The token is only valid for 1h)

## Start sync
`python deezersync.py --access_token=adfergCbreeeddefgveggecbrrblksahrdhjlnwOC3d4rxxgvddzzzbtfr -p /home/user/music/flac`

This will start the sync, depending how much stuff you have it can take a while. The sync requires an access_token param and the path to your local music library. The library must contain files which contain propper ID3 tagged files. All major formats like FLAC, OGG, MP3, WAV,... are supported as long as they contain ID3 tags for `albumartist` and `album`.

[Steam Deck Plugin Loader](https://github.com/SteamDeckHomebrew/PluginLoader) to modify the nested resolution as seen by your games.

* Copy gamescope-mode-change to `/path/to/homebrew/plugins/gamescope-mode-change`


Gamescope-mode-change works by modifying the launch options of your game, wich will make Steam run a script right before starting the game.
```
--fullscreen
```
becomes
```
/path/to/homebrew/plugins/gamescope-mode-change/gamescope-mode-change.py --id=1 --nestedWidth=${width} --nestedHeight=${height} xX-gamescope-Xx && %command% --fullscreen
```

and
```
ENVIRONMENT_VAR=VALUE %command% --fullscreen
```
becomes
```
/path/to/homebrew/plugins/gamescope-mode-change/gamescope-mode-change.py --id=1 --nestedWidth=${width} --nestedHeight=${height} xX-gamescope-Xx && ENVIRONMENT_VAR=VALUE %command% --fullscreen
```


If you wish to change launch options for your game while the script is active, be sure to do so after `xX-gamescope-Xx && `. <- please do not forget the extra space after `&&`


Good luck :)
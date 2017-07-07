# Changelog
All notable changes to this project will be documented in this file.

Versions labeled as 'pre' will not run. Versions before 1.0.0 will not be officially released. It is recommended to always use the latest version to prevent any unexpected behavior, and to get the newest additions.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Need to add future plans

## [0.10.0] - 2017-07-06 ()
### Added
- Server moderators can be added using the mod command, mods can use server setting commands
- Members with the 'admin' permission are automatically added as a mod
- Modules can be enabled or disabled by server moderators
- The prefix command has been added, but prefix changing will come soon
### Changed
- Some modules (only fun and misc for now) check if the module is enabled in the server object

## [0.9.3] - 2017-07-06 (2f90d5)
### Fixed
- Google command: doesn't try to add picture if it doesn't exist

## [0.9.2] - 2017-07-05 (3c4745)
### Changed
- Added all past changes into this changelog

## [0.9.1] - 2017-07-05 (ef6f05)
### Added
- Google command: tell when there are no results
- Fixed syntax in example command in README

## [0.9.0] - 2017-07-04 (aa2cb0)
### Added
- Misc commands: Google search
- Searches a given query and returns the first result, also links to all of the results

## [0.8.1] - 2017-07-04 (22431d)
### Added
- Misc commands: ping (shows the bot's response time)
- Logs how long it takes for the bot to startup

## [0.8.0] - 2017-07-04  (e92cf2)
### Added
- Fun commands: xkcd (allows you to get a random xkcd, by number, or the latest)

## [0.7.0] - 2017-07-04
### Added
- Voice commands: play, queue, stop, etc (49b4e3)
- This needs to be rewritten, I just added them for now
- Prefix can be changed from the config file (894e2c)

## [0.6.1] - 2017-07-04 (0a82b8)
### Added
- Misc commands: clean (deletes the bot's messages and any commands)

## [0.6.0] - 2017-07-04 (722060)
### Added
- Fun commands: 8ball, say, and urban

## [0.5.0] - 2017-07-04 (ba2bad)
### Added
- Admin commands: gitpull, restart, and exit

## [0.4.0] - 2017-07-03 (ddccfd)
### Added
- Info command for information about the bot

## [0.3.2] - 2017-07-03 (7d5a4f)
### Added
- Installation instructions and how to use cogs in the README

## [0.3.1] - 2017-07-03 (f463b4)
### Added
- Error handling for commands

## [0.3.0] - 2017-07-03 (10a278)
### Added
- Module reload and unload commands

## [0.2.0] - 2017-07-03
### Changed
- Logs can now be sent to an optional discord channel, specified in config (f534fa)
- Using 'PrettyOutput' for logging (link in README) (585893)
- Checks if the given log channel is valid (3ec1f1)

## [0.1.0] - 2017-07-03 (55d554)
### Added
- Loads all cogs from the cogs folder after the bot logs in

## [Pre 0.0.0] - 2017-07-03 (78c162)
### Added
- Imports configuration from config.json
- If configuration file not found, creates it
- Logs into discord with token in config file

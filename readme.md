# Announcer - Discord bot

Simple discord bot, which announces voice recordings in text channel along with sound effects.

## Prerequisites

In order to run Recorder Discord Bot, you must have Docker installed.

## How to initialize and run

- Copy locally conf.example.json -> conf.json and configure it
- Build and run docker image


### Out-of-docker development

If for some reason you must try something or develop outside docker:

- Run `./run.sh`

### Mac OS - SSL Certificate error

In order to resolve, basically navigate to your `Applications/Python *.*` folder and simply run `Install Certificates.command` file.

# TwitScrapper

## Commands
- `docker-compose exec api python command.py timeline [HANDLE]`: extract tweets from a specific Twitter user.
- `docker-compose exec api python command.py tag`: Tag all the database.
- `docker-compose exec api python command.py stats`: Generate stats.

## Installing Redash

Redash is the software used to consume and display the data extracted from Twitter. To install Redash is necessary to create the appropiate schema in the internal Redash postgres database. To do so, just execute the next command:

`docker-compose run --rm server create_db`

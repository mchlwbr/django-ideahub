# IdeaHub

IdeaHub is a Django app for collecting ideas and voting on them.

## Motivation

My friends and I were planning a trip to london and keeping track of all the
suggestions in our group chat seemed horrifying to me.

So I wrote this app where you can submit `Ideas` to a `Collection` and
vote on them to get a ranking.

## Preview

![Ideas](./doc/images/ideas.png)

## Container

To spin up the container simply run

```terminal
docker compose up --build
```

then visit http://127.0.0.1:8000/ideahub/.

## Tests

To execute the tests run 

```terminal
pytest
```

### Debugging tests

To debug during tests, comment out `addopts` for `tool.pytest.ini_options` in `pyproject.toml`
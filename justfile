# Cross-platform shell configuration
# Use PowerShell on Windows (higher precedence than shell setting)
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
# Use sh on Unix-like systems
set shell := ["sh", "-c"]
# Params
botname := "mdabojbot"

[doc("All command information")]
default:
  @just --list --unsorted --list-heading $'Bot  commands…\n'


[doc("Run bot throw poetry")]
run-bot:
  poetry run run-bot


[doc("Run unit tests")]
[group("tests")]
unit-tests:
  poetry run pytest tests/*

[doc("Run mypy checks")]
[group("tests")]
mypy-checks:
  poetry run mypy {{botname}}/*

[doc("Run ruff checks")]
[group("tests")]
ruff-checks:
  poetry run ruff check --select I
  poetry run ruff format --check

[doc("Run all checks")]
[group("tests")]
test-all: unit-tests mypy-checks ruff-checks


[doc("Ruff format")]
[group("fixes")]
ruff-format:
  poetry run ruff check --select I --fix
  poetry run ruff format

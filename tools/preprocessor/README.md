# Preprocessor

<img alt="Christopher Columbus kneeling in front of Queen Isabella I of Castile."
     src="https://upload.wikimedia.org/wikipedia/commons/5/53/Christopher_Columbus7.jpg"
     align="right"
     width="448px"
/>

Preprocessor script that downloads the dataset, verifies it and finally extracts it.

## Usage

Install dependencies for the script and run it:

````
$ pipenv install
$ pipenv run preprocessor
````

## Development

Install all dependencies for the project including development dependencies:

```
$ pipenv install --dev
```

Types can be checked with MyPy and the source code can be linted with Pylint.

````
$ pipenv run mypy main.py
$ pipenv run pylint main.py
````

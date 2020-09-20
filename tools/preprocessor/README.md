# Preprocessor

<img alt="Dióscoro Teófilo Puebla Tolín, 1862"
     src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Desembarco_de_Col%C3%B3n_de_Di%C3%B3scoro_Puebla.jpg"
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

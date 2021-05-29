## test task

### requirements:

* python3.9 / docker

### install

```
python -m pip install -r requirements.txt
```

### run

```
python app
```

or

```
docker build -t test .
docker run -p 5000:80 test
```

then go to [docs page](http://127.0.0.1:5000/docs). By default app will
use [tax_bands.json](./app/storage/tax_bands.json) as bands source to change this behavior put readable json file that
is valid against this [schema](app/storage/schema) somewhere in your system and launched app with smth like:

```
TAX_BANDS_SRC="/path/to/your.json"; python -m app
```

or when launching with docker:

```
docker run -e TAX_BANDS_SRC=/etc/bands.json -v "/path/to/your.json":"/etc/bands.json" -p 80:80 test
```

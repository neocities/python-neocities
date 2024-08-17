# python-neocities - Python API for NeoCities.org

python-neocities is a Python wrapper of the NeoCities.org REST API.

NeoCities.org is a FLOSS service which offers one Gigabyte of gratis
and ad-free hosting inspired by GeoCities. I really liked their approach so
I decided to contribute this little API.

To install it, type `python setup.py install` or `make install`.

The unit tests rely on having a NeoCities.org account. To run them, type

```bash
NEOCITIES_USER=user NEOCITIES_PASS=pass make test
```

But then again, I wouldn't recommend running them at all since they might make
you seem suspicious to NC's admins and the API is simple enough.

## Usage

First, you must initialize a NeoCities object with

```python
import neocities

nc = neocities.NeoCities('username', 'password')
```

Or you can initialize a NeoCities object using an API key with

```python
import neocities

nc = neocities.NeoCities(api_key='NEOCITIES_API_KEY')
```

(Passing a valid username and password, or API key, is not necessary if you are only going
to use the `info` call)

After you've done that, you can query NeoCities for information about a
specific site with:

```python
response = nc.info('sitename')
```

If you have provided correct login credentials, you can also query NeoCities
for your own site's info with

```python
response = nc.info()
```

You can upload files with

```python
nc.upload(('name_on_disk', 'name_on_server'), ...)
```

Where `name_on_server` is the name you want the file to have on the NeoCities
server and `name_on_disk` is the name (path) of the file on your disk.

You can delete a file remotely with

```python
nc.delete('filename1', ...)
```

To make sure you are not doing something wrong, the `InvalidRequestError`
exception will be fired when you do. It has a `status_code` attribute which
contains the status code returned by your request. For a list of status codes
(useful to debug your requests), check out
[this Wikipedia page](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

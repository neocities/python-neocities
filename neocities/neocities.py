import requests


class NeoCities:
    api_key = None
    def __init__(self, username=None, password=None, api_key=None, options={}):
        self.auth = (username, password)
        if api_key:
            self.api_key = api_key
        self.options = options
        self.url = options.get('url', 'https://neocities.org')

    def info(self, site_name=''):
        """
        Request info for a neocities site (does not require authentication)

        Parameters
        ----------
        site_name : str
            The name of the site

        Returns
        -------
        request : dict
            A JSON-decoded request

        """
        if site_name:
            args = {'sitename': site_name}
        else:
            args = None
        if self.api_key:
            response = requests.get(self._request_url('info'), params=args, headers={'Authorization':'Bearer '+self.api_key})
        else:
            response = requests.get(self._request_url('info'), auth=self.auth, params=args)
        return self._decode(response)

    def listitems(self, site_name=''):
        """
        Request file listing for a neocities site (does not require authentication).

        Parameters
        ----------
        site_name : str
            The name of the site

        Returns
        -------
        request : list of dicts
            A JSON-decoded request

        """
        args = {'sitename': site_name} if site_name else None
        if self.api_key:
            response = requests.get(self._request_url('list'), params=args, headers={'Authorization':'Bearer '+self.api_key})
        else:
            response = requests.get(self._request_url('list'), auth=self.auth, params=args)
        return self._decode(response)

    def delete(self, *filenames):
        """
        Delete files from a NeoCities site

        Parameters
        ----------
        filenames : *str
            The names of the files to be deleted

        Returns
        -------
        request : dict
            A JSON-decoded request

        """
        args = {'filenames[]': []}
        for i in filenames:
            args['filenames[]'].append(i)
        if self.api_key:
            response = requests.post(self._request_url('delete'), data=args, headers={'Authorization':'Bearer '+self.api_key})
        else:
            response = requests.post(self._request_url('delete'), auth=self.auth, data=args)
        return self._decode(response)

    def upload(self, *filenames):
        """
        Upload files to a NeoCities site

        Parameters
        ----------
        filenames: *tuple (str, str)
            The names of the files to be uploaded in the format
            (name_on_disk, name_on_server)
            Note: name_on_server must include the file extension.

        Returns
        -------
        request : dict
            A JSON-decoded request

        """

        # NeoCities API expects a dict in the following format:
        # { name_on_server: <file_object> }
        args = {pair[1]: open(pair[0], 'rb') for pair in filenames}
        if self.api_key:
            response = requests.post(self._request_url('upload'), files=args, headers={'Authorization':'Bearer '+self.api_key})
        else:
            response = requests.post(self._request_url('upload'), auth=self.auth, files=args)
        return self._decode(response)

    def _request_url(self, method):
        return "{0}/api/{1}".format(self.url, method)

    def _decode(self, response):
        if response.status_code != 200:
            print(response.__dict__)
            raise NeoCities.InvalidRequestError(response.status_code, response._content)
        else:
            return response.json()

    class InvalidRequestError(Exception):
        """
        Exception for signalling a request different than 200 OK
        """
        def __init__(self, status_code, reason=None):
            self.status_code = status_code
            self.reason = reason

        def __str__(self):
            return "Request returned status code {}: {}".format(self.status_code, self.reason)

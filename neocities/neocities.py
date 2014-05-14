import requests


class NeoCities:
    def __init__(self, username=None, password=None, options={}):
        self.auth = (username, password)
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
        response = requests.get(self._request_url('info'),
                                auth=self.auth, params=args)
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
        response = requests.post(self._request_url('delete'),
                                 auth=self.auth, data=args)
        return self._decode(response)

    def upload(self, *filenames):
        """
        Upload files to a NeoCities site

        Parameters
        ----------
        filenames: *tuple (str, str)
            The names of the files to be uploaded in the format
            (name_on_server, name_on_disk)

        Returns
        -------
        request : dict
            A JSON-decoded request

        """
        args = {i[0]: open(i[1], 'rb') for i in filenames}
        response = requests.post(self._request_url('upload'),
                                 auth=self.auth, files=args)
        return self._decode(response)

    def _request_url(self, method):
        return "{0}/api/{1}".format(self.url, method)

    def _decode(self, response):
        if response.status_code != 200:
            raise NeoCities.InvalidRequestError(response.status_code)
        else:
            return response.json()

    class InvalidRequestError(Exception):
        """
        Exception for signalling a request different than 200 OK
        """
        def __init__(self, status_code):
            self.status_code = status_code

        def __str__(self):
            return "Request returned status code {}".format(self.status_code)

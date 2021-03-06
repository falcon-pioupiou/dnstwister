"""Mocks."""
import datetime


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class NoEmailer(object):
    """Silent emailer."""
    def __init__(self, *args, **kwargs):
        self._emails = []

    @property
    def sent_emails(self):
        return list(self._emails)

    def send(self, *args):
        self._emails.append(args)


class SimpleKVDatabase(object):
    """Replace the main storage with a lightweight in-memory shim."""
    def __init__(self):
        self._data = {}

    @property
    def data(self):
        """Return a read-only dict representation of the data, for testing."""
        return dict(self._data)

    def set(self, kind, key, value):
        """Set the value for key"""
        self._data[kind + ':' + key] = value

    def get(self, kind, key):
        """Get a value for key or None."""
        try:
            return self._data[kind + ':' + key]
        except KeyError:
            pass

    def ikeys(self, kind):
        """Return an iterator of all keys filtered on kind."""
        for key in dict(self._data):
            if key.startswith(kind + ':'):
                yield key.split(kind + ':')[1]

    def delete(self, kind, key):
        """Delete a key."""
        try:
            del self._data[kind + ':' + key]
        except KeyError:
            pass

    @staticmethod
    def to_db_datetime(datetime_obj):
        """Convert a datetime object to db datetime data.

        Just copy the PG database implementation.
        """
        return datetime_obj.strftime(DATETIME_FORMAT)

    @staticmethod
    def from_db_datetime(datetime_data):
        """Convert datetime data from db to a datetime object.

        Just copy the PG database implementation.
        """
        return datetime.datetime.strptime(datetime_data, DATETIME_FORMAT)


class SimpleFuzzer(object):
    """Replace the fuzzer with something that returns not much."""
    def __init__(self, domain):
        self._domain = domain

    def fuzz(self):
        pass

    @property
    def domains(self):
        return [
            {'domain-name': self._domain, 'fuzzer': 'Original*'},
            {'domain-name': self._domain[:-1], 'fuzzer': 'Pretend'},
        ]


class NoFuzzer(object):
    """Replace the fuzzer with something that returns nothing but the
    original domain."""
    def __init__(self, domain):
        self._domain = domain

    def fuzz(self):
        pass

    @property
    def domains(self):
        return [
            {'domain-name': self._domain, 'fuzzer': 'Original*'},
        ]

import codecs
import datetime
import os
import re
from decimal import Decimal
from json import dumps
from urllib.parse import (parse_qsl, ParseResult, unquote, urlencode, urlparse)
from uuid import UUID

from django.core.files.uploadedfile import TemporaryUploadedFile
from simple_model import to_dict as to_dict_sm


def clean_url(url: str) -> str:
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    # Merging URL arguments dict with new params
    parsed_get_args.pop('page', '')

    parsed_get_args.update(
        {k: dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
    )

    # Converting URL argument to proper query string
    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url


def get_version_from_changes(path: str) -> str:
    current_version = ''
    changes = os.path.join(path, "CHANGES.rst")
    pattern = r'^(?P<version>[0-9]+.[0-9]+(.[0-9]+)?)'
    with codecs.open(changes, encoding='utf-8') as changes:
        for line in changes:
            match = re.match(pattern, line)
            if match:
                current_version = match.group("version")
                break
    return current_version or '0.1.0'


def labelize(text: str) -> str:
    return ' '.join([t.capitalize() for t in text.replace('_', ' ').split(' ')])


def json_converter(output):
    if isinstance(output, datetime.datetime) or isinstance(output, datetime.date) or isinstance(output, UUID):
        return output.__str__()
    elif isinstance(output, Decimal):
        return output.__str__()
    elif isinstance(output, TemporaryUploadedFile):
        raise Exception(f'Unable to convert. Type: {type(output)}')
    return output


def to_dict(object_list):
    results = []
    for item in object_list:
        item.validate()
        results.append(to_dict_sm(item))
    return results

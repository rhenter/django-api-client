import os

from vcr.config import VCR

CASSETTES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures', 'cassettes')

vcr = VCR(
    cassette_library_dir=CASSETTES_DIR,
    path_transformer=VCR.ensure_suffix('.yaml'),
    filter_headers=['authorization'],
    record_mode='once',
    match_on=['method', 'path', 'query'],
)

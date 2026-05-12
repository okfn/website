import os

THUMBNAIL_DEBUG = False
ROOT_URLCONF = "foundation.tests.urls"

# Let TestCases reference fixtures by bare name (e.g.
# `fixtures = ["sample_data.json"]`) without putting the JSON inside a
# specific app's fixtures/ directory.
FIXTURE_DIRS = [
    os.path.join(os.path.dirname(__file__), "tests", "fixtures"),
]

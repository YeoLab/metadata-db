import os
from urllib.parse import urlsplit, urlunsplit, urlencode


def pipeline(result):
    pass

def title(result):
    """The title for this Globus Search subject"""
    return result[0]["title"]


def globus_app_link(result):
    """A Globus Webapp link for the transfer/sync button on the detail page"""
    url = result[0]["url"]
    parsed = urlsplit(url)
    query_params = {
        "origin_id": parsed.netloc,
        "origin_path": os.path.dirname(parsed.path),
    }
    return urlunsplit(
        ("https", "app.globus.org", "file-manager", urlencode(query_params), "")
    )


def https_url(result):
    """Add a direct download link to files over HTTPS"""
    path = urlsplit(result[0]["url"]).path
    return urlunsplit(("https", "g-f8db23.0ed28.75bc.data.globus.org/", path, "", ""))


def copy_to_clipboard_link(result):
    return https_url(result)
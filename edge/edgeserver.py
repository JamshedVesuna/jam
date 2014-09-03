"""
A Flask server to mointor and server client requests
git@github.com:JamshedVesuna/jam
"""

from flask import Flask

from jam import Jam

app = Flask(__name__)


def content_is_local(filepath):
    """Bool check if the content of the file is local

    If not, the content is a pointer to another server
    """
    pass

def isValid(filepath):
    """Bool if the filepath exists on this server"""
    pass

def get_content(filepath):
    """Returns the requested filepath content"""
    pass

def stream_content(filepath):
    """Simultaneously request content from the remote, download, and serve

    content to the client request
    Be sure that the `filepath` is overwritten with the content of the stream
    :param filepath: A file containing a pointer to a remote file
    """

@app.route('/anyurl')
def parseUrl(someURL):
    if not isValid(someURL):
        return LookupError(str(someURL) + " could not be found")
    if content_is_local(someURL):
        return get_content(someURL)
    else:
        # The filepath is a pointer to a remote
        stream_content(someURL)

if __name__ == '__main__':
    j = Jam()
    credDict = j.get_credential_dict()
    app.run(host='0.0.0.0')

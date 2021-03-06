"""Test the link to the help docco."""


def test_help_redirect_to_rtd(webapp):
    """Test we redirect to read the docs."""
    response = webapp.get('/help')

    assert response.status_code == 302
    assert response.headers['location'] == 'https://dnstwister.readthedocs.org/en/stable/web.html'

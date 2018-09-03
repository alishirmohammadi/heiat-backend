from urllib3.util.retry import Retry
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504],
                method_whitelist=frozenset(['GET', 'POST']))

adapter = requests.adapters.HTTPAdapter(max_retries=retries)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)


def get_domain(request):
    return request._request.META['HTTP_HOST'].split(':')[0]

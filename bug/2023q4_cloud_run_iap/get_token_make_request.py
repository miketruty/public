# This is code for getting a token, then code to invoke a request.

import urllib

from google.oauth2 import service_account

import google.auth.transport.requests
from google.oauth2 import id_token


SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
JSON_FILE="/Users/mxt0623/vnvtestdata_firestore_writer.json"


def get_idToken_from_serviceaccount(json_credential_path: str,
                                    target_audience: str):
    """
    I prefer to supply the file instead of using env var.

    *NOTE*: (from the code I copied)
    Using service account keys introduces risk; they are long-lived, and can be used by anyone
    that obtains the key. Proper rotation and storage reduce this risk but do not eliminate it.
    For these reasons, you should consider an alternative approach that
    does not use a service account key. Several alternatives to service account keys
    are described here:
    https://cloud.google.com/docs/authentication/external/set-up-adc

    Args:
        json_credential_path: Path to the service account json credential file.
        target_audience: The url or target audience to obtain the ID token for.
                        Examples: http://www.abc.com
    """
    # Obtain the id token by providing the json file path and target audience.
    credentials = service_account.IDTokenCredentials.from_service_account_file(
        filename=json_credential_path,
        target_audience=target_audience)

    credentials.refresh(google.auth.transport.requests.Request())
    print(f'Generated ID token with expiration: {credentials.expiry}.')
    print(f'    Token: {credentials.token}.')
    return credentials.token


def make_iap_request(id_token, url, method="GET"):
    """Makes a request to an application protected by Identity-Aware Proxy.

    Args:
      id_token: oidct id_token
      url: The Identity-Aware Proxy-protected URL to fetch.
      method: The request method to use
              ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')

    Returns:
      The page body, or raises an exception if the page couldn't be retrieved.
    """
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {id_token}')
    # req.add_header('Proxy-Authorization', f'Bearer {id_token}')
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e)
        print(e.geturl())
        print(e.read())
        return ''

    return response.read()


def try_v3():
    """Grab an ID token, needed for Cloud Fn/Cloud Run, then use it with GET.
    """
    aud_client = '478061995323-0gvgnjkochgc91gf276jkten1lcegcke.apps.googleusercontent.com'
    print(f'Trying aud={aud_client}...')

    sa_json = '/Users/mxt0623/vnvtestdata_firestore_writer.json'
    oidc_id_token = get_idToken_from_serviceaccount(
            json_credential_path=sa_json,
            target_audience=aud_client)

    url = 'https://dexcom-vnv-testrail-webhook.dexcomdev.com'
    response_read = make_iap_request(
        id_token=oidc_id_token, url=url, method='GET')

    print(f'  result: {response_read}')
    print('-' * 40)


def main():
    try_v3()


if __name__ == '__main__':
    main()

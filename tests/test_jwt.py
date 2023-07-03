import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestJWT:
    url_create = '/api/v1/jwt/create/'
    url_refresh = '/api/v1/jwt/refresh/'
    url_verify = '/api/v1/jwt/verify/'

    @pytest.mark.django_db(transaction=True)
    def test_jwt_create__invalid_request_data(self, client, user):
        url = self.url_create
        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with no parameters, '
            f'code {code_expected} is returned'
        )
        fields_invalid = ['username', 'password']
        for field in fields_invalid:
            assert field in response.json().keys(), (
                f'Make sure when requesting `{url}` with no parameters, '
                f'returns code {code_expected} with a message saying '
                'which fields encountered an error processing.'
                f'Field {field} not found'
            )

        username_invalid = 'invalid_username_not_exists'
        password_invalid = 'invalid pwd'
        data_invalid = {
            'username': username_invalid,
            'password': password_invalid
        }
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with no parameters, '
            f'code {code_expected} is returned'
        )
        field = 'detail'
        assert field in response.json(), (
            f'Make sure that when requesting `{url}` with an invalid username, '
            f'code {code_expected} is returned with the appropriate message '
            f'in the field {field}'
        )
        username_valid = user.username
        data_invalid = {
            'username': username_valid,
            'password': password_invalid
        }
        response = client.post(url, data=data_invalid)
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with no parameters, '
            f'code {code_expected} is returned'
        )
        field = 'detail'
        assert field in response.json(), (
            f'Make sure that when requesting `{url}` with invalid password, '
            f'code {code_expected} is returned with the appropriate message '
            f'in the field {field}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_create__valid_request_data(self, client, user):
        url = self.url_create
        valid_data = {
            'username': user.username,
            'password': '1234567'
        }
        response = client.post(url, data=valid_data)
        code_expected = 200
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with valid data, '
            f'code {code_expected} is returned'
        )
        fields_in_response = ['refresh', 'access']
        for field in fields_in_response:
            assert field in response.json().keys(), (
                f'Make sure when requesting `{url}` with valid data, '
                f' in the response, the code {code_expected} is returned with the keys '
                f'{fields_in_response} where tokens are contained'
            )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_refresh__invalid_request_data(self, client):
        url = self.url_refresh

        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with no parameters, '
            f'code {code_expected} is returned'
        )
        data_invalid = {
            'refresh': 'invalid token'
        }
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Make sure that when requesting `{url}` with an invalid value for the refresh parameter, '
            f'code {code_expected} is returned'
        )
        fields_expected = ['detail', 'code']
        for field in fields_expected:
            assert field in response.json(), (
                f'Make sure that when requesting `{url}` with an invalid value for the refresh parameter, '
                f'code {code_expected} is returned with the appropriate message '
                f'in the field {field}'
            )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_refresh__valid_request_data(self, client, user):
        url = self.url_refresh
        valid_data = {
            'username': user.username,
            'password': '1234567'
        }
        response = client.post(self.url_create, data=valid_data)
        token_refresh = response.json().get('refresh')
        code_expected = 200
        response = client.post(url, data={'refresh': token_refresh})
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with a valid refresh parameter, '
            f'code {code_expected} is returned'
        )
        field = 'access'
        assert field in response.json(), (
            f'Make sure that when requesting `{url}` with a valid refresh parameter, '
            f'returns code {code_expected} and the access parameter, in which the new token is passed'
        )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_verify__invalid_request_data(self, client):
        url = self.url_verify

        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with no parameters, '
            f'code {code_expected} is returned'
        )
        data_invalid = {
            'token': 'invalid token'
        }
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Make sure that when requesting `{url}` with an invalid value for the token parameter, '
            f'code {code_expected} is returned'
        )
        fields_expected = ['detail', 'code']
        for field in fields_expected:
            assert field in response.json(), (
                f'Make sure that when requesting `{url}` with an invalid value for the token parameter, '
                f'code {code_expected} is returned with the appropriate message '
                f'in the field {field}'
            )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_verify__valid_request_data(self, client, user):
        url = self.url_verify
        valid_data = {
            'username': user.username,
            'password': '1234567'
        }
        response = client.post(self.url_create, data=valid_data)
        token_access = response.json().get('access')
        token_refresh = response.json().get('refresh')
        code_expected = 200
        response = client.post(url, data={'token': token_access})
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with a valid token parameter, '
            f'code {code_expected} is returned. '
            'Both refresh and access tokens must be validated'
        )
        response = client.post(url, data={'token': token_refresh})
        assert response.status_code == code_expected, (
            f'Make sure when requesting `{url}` with a valid token parameter, '
            f'code {code_expected} is returned. '
            'Both refresh and access tokens must be validated'
        )

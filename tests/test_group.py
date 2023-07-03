import pytest

from posts.models import Group


class TestGroupAPI:

    @pytest.mark.django_db(transaction=True)
    def test_group_not_found(self, client, post, group_1):
        response = client.get('/api/v1/groups/')

        assert response.status_code != 404, (
            'Page `/api/v1/groups/` not found, check this address in *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_group_list_not_auth(self, client, post, group_1):
        response = client.get('/api/v1/groups/')
        assert response.status_code == 200, (
            'Check that `/api/v1/groups/` when requested without a token returns status 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_group_single_not_auth(self, client, group_1):
        response = client.get(f'/api/v1/groups/{group_1.id}/')
        assert response.status_code == 200, (
            'Check that `/api/v1/groups/{group.id}/` returns status 200 when requested without a token'
        )

    @pytest.mark.django_db(transaction=True)
    def test_group_get(self, user_client, post, another_post, group_1, group_2):
        response = user_client.get('/api/v1/groups/')
        assert response.status_code == 200, (
            'Check that a GET request to `/api/v1/groups/` with an auth token returns status 200'
        )

        test_data = response.json()

        assert type(test_data) == list, (
            'Check that a GET request to `/api/v1/groups/` returns a list'
        )

        assert len(test_data) == Group.objects.count(), (
            'Check that a GET request to `/api/v1/groups/` returns the entire list of groups'
        )

        groups_cnt = Group.objects.count()
        test_group = test_data[0]

        assert 'title' in test_group, (
            'Check to add `title` to the `fields` field list of the Group model serializer'
        )

        assert len(test_data) == groups_cnt, (
            'Check that a GET request to `/api/v1/groups/` returns the entire list of groups'
        )

    @pytest.mark.django_db(transaction=True)
    def test_group_cannot_create(self, user_client, group_1, group_2):
        group_count = Group.objects.count()

        data = {}
        response = user_client.post('/api/v1/groups/', data=data)
        assert response.status_code == 405, (
            'Check that a POST request to `/api/v1/groups/` cannot create a community via the API'
        )

        data = {'title': 'Group number 3'}
        response = user_client.post('/api/v1/groups/', data=data)
        assert response.status_code == 405, (
            'Check that a POST request to `/api/v1/groups/` cannot create a community via the API'
        )

        assert group_count == Group.objects.count(), (
            'Check that a POST request to `/api/v1/groups/` cannot create a community via the API'
        )

    @pytest.mark.django_db(transaction=True)
    def test_group_get(self, user_client, post, post_2, another_post, group_1, group_2):
        response = user_client.get('/api/v1/groups/')
        assert response.status_code == 200, (
            'Page `/api/v1/groups/` not found, check this address in *urls.py*'
        )
        test_data = response.json()
        groups_cnt = Group.objects.all().count()
        assert len(test_data) == groups_cnt, (
            'Check that a GET request to `/api/v1/groups/` returns a list of all communities'
        )

        response = user_client.get(f'/api/v1/groups/{group_2.id}/')
        assert isinstance(response.json(), dict), (
            'A query for `/api/v1/groups/{id}/` should return a dictionary'
        )

        g = Group.objects.filter(id=group_2.id)
        json_response = response.json()
        for k in json_response:
            assert k in g.values()[0] and json_response[k] == g.values()[0][k], (
                'Check that on GET request to `/api/v1/groups/{id}/` '
                'returns information about the corresponding community'
            )

        response = user_client.get(f'/api/v1/groups/{group_1.id}/')
        assert isinstance(response.json(), dict), (
            'A query for `/api/v1/groups/{id}/` should return a dictionary'
        )
        g = Group.objects.filter(id=group_1.id)
        json_response = response.json()
        for k in json_response:
            assert k in g.values()[0] and json_response[k] == g.values()[0][k], (
                'Check that on GET request to `/api/v1/groups/{id}/` '
                'returns information about the corresponding community'
            )

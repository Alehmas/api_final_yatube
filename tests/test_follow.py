import pytest

from posts.models import Follow


class TestFollowAPI:

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_found(self, client, follow_1, follow_2):
        response = client.get('/api/v1/follow/')

        assert response.status_code != 404, (
            'Page `/api/v1/follow/` not found, check this address in *urls.py*'
        )
        assert response.status_code != 500, (
            'The page `/api/v1/follow/` cannot be served by your server, check the view function in *views.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_auth(self, client, follow_1, follow_2):
        response = client.get('/api/v1/follow/')
        assert response.status_code == 401, (
            'Check that `/api/v1/follow/` on a GET request without a token returns status 401'
        )

        data = {}
        response = client.post('/api/v1/follow/', data=data)
        assert response.status_code == 401, (
            'Check that `/api/v1/follow/` POST request without token returns status 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_get(self, user_client, user, follow_1, follow_2, follow_3):
        response = user_client.get('/api/v1/follow/')
        assert response.status_code == 200, (
            'Check that a GET request to `/api/v1/follow/` with an auth token returns status 200'
        )

        test_data = response.json()

        assert type(test_data) == list, (
            'Check that a GET request to `/api/v1/follow/` returns a list'
        )

        assert len(test_data) == Follow.objects.filter(following__username=user.username).count(), (
            'Check that a GET request to `/api/v1/follow/` returns a list of all the user`s followers'
        )

        follow = Follow.objects.filter(user=user)[0]
        test_group = test_data[0]
        assert 'user' in test_group, (
            'Check to add `user` to the list of fields `fields` of the Follow model serializer'
        )
        assert 'following' in test_group, (
            'Check to add `following` to the list of fields `fields` of the Follow model serializer'
        )

        assert test_group['user'] == follow.user.username, (
            'Check that a GET request to `/api/v1/follow/` returns a list of the current user`s subscriptions, '
            'the `user` field should be `username`'
        )
        assert test_group['following'] == follow.following.username, (
            'Check that a GET request to `/api/v1/follow/` returns the entire list of subscriptions, '
            'the `following` field should be `username`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_create(self, user_client, follow_2, follow_3, user, user_2, another_user):
        follow_count = Follow.objects.count()

        data = {}
        response = user_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Check that a POST request to `/api/v1/follow/` with bad data returns status 400'
        )

        data = {'following': another_user.username}
        response = user_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 201, (
            'Check that a POST request to `/api/v1/follow/` with valid data returns status 201'
        )

        test_data = response.json()

        msg_error = (
            'Check that a POST request to `/api/v1/follow/` returns a dictionary with new subscription data'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('user') == user.username, msg_error
        assert test_data.get('following') == data['following'], msg_error

        assert follow_count + 1 == Follow.objects.count(), (
            'Check that a POST request to `/api/v1/follow/` creates a subscription'
        )

        response = user_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Check that when POSTing a request to `/api/v1/follow/` '
            'status 400 is returned to an already subscribed author'
        )

        data = {'following': user.username}
        response = user_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Check that when POSTing a request to `/api/v1/follow/` '
            'if you try to subscribe to yourself, status 400 is returned'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_search_filter(self, user_client, follow_1, follow_2,
                                  follow_3, follow_4, follow_5,
                                  user, user_2, another_user):

        follow_user = Follow.objects.filter(user=user)
        follow_user_cnt = follow_user.count()

        response = user_client.get('/api/v1/follow/')
        assert response.status_code != 404, (
            'Page `/api/v1/follow/` not found, check this address in *urls.py*'
        )
        assert response.status_code == 200, (
            'Page `/api/v1/follow/` is down, check the view function'
        )

        test_data = response.json()
        assert len(test_data) == follow_user_cnt, (
            'Check that a GET request to `/api/v1/follow/` returns a list of all user subscriptions'
        )

        response = user_client.get(f'/api/v1/follow/?search={user_2.username}')
        assert len(response.json()) == follow_user.filter(following=user_2).count(), (
            'Check that on GET request with `search` parameter on `/api/v1/follow/` '
            'returning the result of a subscription search'
        )

        response = user_client.get(f'/api/v1/follow/?search={another_user.username}')
        assert len(response.json()) == follow_user.filter(following=another_user).count(), (
            'Check that on GET request with `search` parameter on `/api/v1/follow/` '
            'returning the result of a subscription search'
        )

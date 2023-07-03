import pytest

from posts.models import Post


class TestPostAPI:

    @pytest.mark.django_db(transaction=True)
    def test_post_not_found(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code != 404, (
            'Page `/api/v1/posts/` not found, check this address in *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_list_not_auth(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code == 200, (
            'Check that on `/api/v1/posts/` you return status 200 when requested without a token'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_single_not_auth(self, client, post):
        response = client.get(f'/api/v1/posts/{post.id}/')

        assert response.status_code == 200, (
            'Check that on `/api/v1/posts/{post.id}/` you return status 200 when requested without a token'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_get_not_paginated(self, user_client, post, another_post):
        response = user_client.get('/api/v1/posts/')
        assert response.status_code == 200, (
            'Check that a GET request to `/api/v1/posts/` with an auth token returns status 200'
        )

        test_data = response.json()

        # response without pagination must be a list type
        assert type(test_data) == list, (
            'Check that a GET request to `/api/v1/posts/` without pagination returns a list'
        )

        assert len(test_data) == Post.objects.count(), (
            'Check that a GET request to `/api/v1/posts/` without pagination returns the entire list of articles'
        )

        post = Post.objects.all()[0]
        test_post = test_data[0]
        assert 'id' in test_post, (
            'Check to add `id` to the Post model serializer `fields` list of fields'
        )
        assert 'text' in test_post, (
            'Check that you have added `text` to the `fields` field list of the Post model serializer'
        )
        assert 'author' in test_post, (
            'Check to add `author` to the Post model serializer`s `fields` list of fields'
        )
        assert 'pub_date' in test_post, (
            'Check that you have added `pub_date` to the list of fields `fields` of the Post model serializer'
        )
        assert test_post['author'] == post.author.username, (
            'Check that Post model serializer `author` returns the username'
        )

        assert test_post['id'] == post.id, (
            'Check that a GET request to `/api/v1/posts/` returns the entire list of articles'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_get_paginated(self, user_client, post, post_2, another_post):
        base_url = '/api/v1/posts/'
        limit = 2
        offset = 2
        url = f'{base_url}?limit={limit}&offset={offset}'
        response = user_client.get(url)
        assert response.status_code == 200, (
            f'Check that GET request `{url}` with auth token returns status 200'
        )

        test_data = response.json()

        # response with pagination must be a dict type
        assert type(test_data) == dict, (
            f'Check that a GET request to `{url}` with pagination returns a dictionary'
        )
        assert "results" in test_data.keys(), (
            f'Make sure that when you make a GET request to `{url}` with pagination, the `results` key is present in the response'
        )
        assert len(test_data.get('results')) == Post.objects.count() - offset, (
            f'Check that a GET request to `{url}` with pagination returns the correct number of articles'
        )
        assert test_data.get('results')[0].get('text') == another_post.text, (
            f'Make sure that when you make a GET request to `{url}` with pagination, '
            'response contains correct articles'
        )

        post = Post.objects.get(text=another_post.text)
        test_post = test_data.get('results')[0]
        assert 'id' in test_post, (
            'Check to add `id` to the Post model serializer `fields` list of fields'
        )
        assert 'text' in test_post, (
            'Check that you have added `text` to the `fields` field list of the Post model serializer'
        )
        assert 'author' in test_post, (
            'Check to add `author` to the Post model serializer`s `fields` list of fields'
        )
        assert 'pub_date' in test_post, (
            'Check that you have added `pub_date` to the list of fields `fields` of the Post model serializer'
        )
        assert test_post['author'] == post.author.username, (
            'Check that Post model serializer `author` returns the username'
        )

        assert test_post['id'] == post.id, (
            f'Check that a GET request to `{url}` returns a valid list of articles'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user_client, user, another_user, group_1):
        post_count = Post.objects.count()

        data = {}
        response = user_client.post('/api/v1/posts/', data=data)
        assert response.status_code == 400, (
            'Check that a POST request to `/api/v1/posts/` with invalid data returns status 400'
        )

        data = {'text': 'Статья номер 3'}
        response = user_client.post('/api/v1/posts/', data=data)
        assert response.status_code == 201, (
            'Check that a POST request to `/api/v1/posts/` with valid data returns status 201'
        )
        assert (
                response.json().get('author') is not None
                and response.json().get('author') == user.username
        ), (
            'Check that the POST request to `/api/v1/posts/` specifies the user as the author,'
            'on whose behalf the request is made'
        )

        # post with group
        data = {'text': 'Статья номер 4', 'group': group_1.id}
        response = user_client.post('/api/v1/posts/', data=data)
        assert response.status_code == 201, (
            'Check that POST request to `/api/v1/posts/`'
            ' you can create a community article and return status 201'
        )
        assert response.json().get('group') == group_1.id, (
            'Check that POST request to `/api/v1/posts/`'
            ' creating a post with a community name'
        )

        test_data = response.json()
        msg_error = (
            'Check that a POST request to `/api/v1/posts/` returns a dictionary with new post data'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == user.username, (
            'Check that a POST request to `/api/v1/posts/` creates an article from an authorized user'
        )
        assert post_count + 2 == Post.objects.count(), (
            'Check that a POST request to `/api/v1/posts/` creates an article'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_get_current(self, user_client, post, user):
        response = user_client.get(f'/api/v1/posts/{post.id}/')

        assert response.status_code == 200, (
            'Page `/api/v1/posts/{id}/` not found, check this address in *urls.py*'
        )

        test_data = response.json()
        assert test_data.get('text') == post.text, (
            'Check that a GET request to `/api/v1/posts/{id}/` returns serializer data, '
            'not found or invalid value of `text`'
        )
        assert test_data.get('author') == user.username, (
            'Check that a GET request to `/api/v1/posts/{id}/` returns serializer data, '
            'not found or invalid value for `author`, should return username '
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_patch_current(self, user_client, post, another_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/',
                                     data={'text': 'Changed the text of the article'})

        assert response.status_code == 200, (
            'Check that PATCH requesting `/api/v1/posts/{id}/` returns status 200'
        )

        test_post = Post.objects.filter(id=post.id).first()

        assert test_post, (
            'Check that when you PATCH request `/api/v1/posts/{id}/` you didn`t remove the article'
        )

        assert test_post.text == 'Changed the text of the article', (
            'Check that when you PATCH request `/api/v1/posts/{id}/` you are changing the article'
        )

        response = user_client.patch(f'/api/v1/posts/{another_post.id}/',
                                     data={'text': 'Changed the text of the article'})

        assert response.status_code == 403, (
            'Check that when you PATCH a request to `/api/v1/posts/{id}/` for a non-own article, you return a status 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_current(self, user_client, post, another_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/')

        assert response.status_code == 204, (
            'Check that DELETE request to `/api/v1/posts/{id}/` returns status 204'
        )

        test_post = Post.objects.filter(id=post.id).first()

        assert not test_post, (
            'Check that the DELETE request to `/api/v1/posts/{id}/` has deleted the article'
        )

        response = user_client.delete(f'/api/v1/posts/{another_post.id}/')

        assert response.status_code == 403, (
            'Check that when you DELETE a request to `/api/v1/posts/{id}/` for a non-own article, you return a status 403'
        )

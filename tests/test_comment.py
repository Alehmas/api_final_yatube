import pytest

from posts.models import Comment


class TestCommentAPI:

    @pytest.mark.django_db(transaction=True)
    def test_comments_not_authenticated(self, client, post):
        response = client.get(f'/api/v1/posts/{post.id}/comments/')

        code = 200
        assert response.status_code == code, (
            'Anonymous user when requested `/api/v1/posts/{post.id}/comments/` '
            f'must receive response with code {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_single_not_authenticated(self, client, post, comment_1_post):
        response = client.get(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        code = 200
        assert response.status_code == code, (
            'Anonymous user when requested `/api/v1/posts/{post.id}/comments/{comment.id}` '
            f'must receive response with code {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comments_not_found(self, user_client, post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code != 404, (
            'Page `/api/v1/posts/{post.id}/comments/` not found, check this address in *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comments_get(self, user_client, post, comment_1_post, comment_2_post, comment_1_another_post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code == 200, (
            'Check that on GET request `/api/v1/posts/{post.id}/comments/` '
            'status 200 returned with auth token'
        )
        test_data = response.json()
        assert type(test_data) == list, (
            'Check that a GET request to `/api/v1/posts/{post.id}/comments/` returns a list'
        )
        assert len(test_data) == Comment.objects.filter(post=post).count(), (
            'Check that on GET request to `/api/v1/posts/{post.id}/comments/` '
            'returns the entire list of comments of the article'
        )

        comment = Comment.objects.filter(post=post).first()
        test_comment = test_data[0]
        assert 'id' in test_comment, (
            'Check to add `id` to the list of fields `fields` of the Comment model serializer'
        )
        assert 'text' in test_comment, (
            'Check to add `text` to the list of `fields` fields of the Comment model serializer'
        )
        assert 'author' in test_comment, (
            'Check to add `author` to the list of fields `fields` of the Comment model serializer'
        )
        assert 'post' in test_comment, (
            'Check to add `post` to the list of fields `fields` of the Comment model serializer'
        )
        assert 'created' in test_comment, (
            'Check to add `created` to the list of fields `fields` of the Comment model serializer'
        )
        assert test_comment['author'] == comment.author.username, (
            'Check that the `author` of the Comment model serializer returns the username'
        )
        assert test_comment['id'] == comment.id, (
            'Check that a GET request to `/api/v1/posts/{post.id}/comments/` returns the entire list of articles'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comments_create(self, user_client, post, user, another_user):
        comments_count = Comment.objects.count()

        data = {}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 400, (
            'Check that a POST request to `/api/v1/posts/{post.id}/comments/` '
            'status 400 is returned with invalid data'
        )

        data = {'author': another_user.id, 'text': 'Новый коммент 1233', 'post': post.id}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 201, (
            'Check that a POST request to `/api/v1/posts/{post.id}/comments/` '
            'with correct data returns status 201'
        )

        test_data = response.json()
        msg_error = (
            'Check that a POST request to `/api/v1/posts/{post.id}/comments/` '
            'returning a dictionary with new comment data'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == user.username, (
            'Check that a POST request to `/api/v1/posts/{post.id}/comments/` '
            'creating a comment from an authorized user'
        )
        assert comments_count + 1 == Comment.objects.count(), (
            'Check that a POST request to `/api/v1/posts/{post.id}/comments/` creates a comment'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_get_current(self, user_client, post, comment_1_post, user):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 200, (
            'Page `/api/v1/posts/{post.id}/comments/{comment.id}/` not found, '
            'check this address in *urls.py*'
        )

        test_data = response.json()
        assert test_data.get('text') == comment_1_post.text, (
            'Check that on GET request `/api/v1/posts/{post.id}/comments/{comment.id}/` '
            'returning serializer data, `text` value not found or not valid'
        )
        assert test_data.get('author') == user.username, (
            'Check that on GET request `/api/v1/posts/{post.id}/comments/{comment.id}/` '
            'returning serializer data, `author` value not found or invalid, '
            'should return username '
        )
        assert test_data.get('post') == post.id, (
            'Check that on GET request `/api/v1/posts/{post.id}/comments/{comment.id}/` '
            'returning serializer data, `post` value not found or invalid'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_patch_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/',
                                     data={'text': 'Changed comment text'})

        assert response.status_code == 200, (
            'Check that on PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` '
            'return status 200'
        )

        test_comment = Comment.objects.filter(id=comment_1_post.id).first()

        assert test_comment, (
            'Check that on PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` '
            'you didn`t delete the comment'
        )

        assert test_comment.text == 'Changed comment text', (
            'Check that when you PATCH request `/api/v1/posts/{id}/` you are changing the article'
        )

        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/',
                                     data={'text': 'Changed the text of the article'})

        assert response.status_code == 403, (
            'Check that on PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` '
            'return status 403 for not your article'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_delete_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 204, (
            'Check that DELETE request to `/api/v1/posts/{post.id}/comments/{comment.id}/` returns status 204'
        )

        test_comment = Comment.objects.filter(id=post.id).first()

        assert not test_comment, (
            'Check that when you DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` you deleted the comment'
        )

        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/')

        assert response.status_code == 403, (
            'Check that on DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` '
            'return status 403 for non-your comment'
        )

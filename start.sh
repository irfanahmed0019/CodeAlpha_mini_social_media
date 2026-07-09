#!/bin/bash
set -e
cd "$(dirname "$0")"

python manage.py migrate --no-input

python manage.py collectstatic --no-input --clear 2>/dev/null || true

python manage.py shell -c "
from django.contrib.auth.models import User
from social.models import Post, Follow, Profile

for u in User.objects.all():
    Profile.objects.get_or_create(user=u)

users_data = [
    ('alice', 'alice@example.com', 'Alice Johnson', 'pass1234!'),
    ('bob', 'bob@example.com', 'Bob Smith', 'pass1234!'),
    ('carol', 'carol@example.com', 'Carol White', 'pass1234!'),
]
created = []
for username, email, full_name, password in users_data:
    if not User.objects.filter(username=username).exists():
        first, last = full_name.split(' ', 1)
        u = User.objects.create_user(username, email, password, first_name=first, last_name=last)
        created.append(u)
        print(f'Created user: {username}')

if created:
    alice = User.objects.get(username='alice')
    bob = User.objects.get(username='bob')
    carol = User.objects.get(username='carol')

    posts = [
        (alice, 'Just launched my new project! So excited to share it with everyone here on Vibe. It has been weeks of hard work but it finally feels ready. What do you all think?'),
        (bob, 'Beautiful morning run today. There is nothing like starting the day with some fresh air and movement. Highly recommend it to anyone feeling stuck.'),
        (carol, 'Been experimenting with new recipes lately. Made a mango chili salsa that absolutely slapped. Will post the recipe soon!'),
        (alice, 'Hot take: the best debugging session is the one where you realize the bug was a typo from 3 days ago. We have all been there.'),
        (bob, 'Reading recommendation: if you have not picked up a good novel in a while, this is your sign. Currently hooked and staying up way too late.'),
    ]
    for user, content in posts:
        Post.objects.get_or_create(user=user, content=content)

    Follow.objects.get_or_create(follower=alice, following=bob)
    Follow.objects.get_or_create(follower=alice, following=carol)
    Follow.objects.get_or_create(follower=bob, following=alice)
    Follow.objects.get_or_create(follower=carol, following=alice)
    print('Demo data seeded.')
" 2>&1 || echo "Seed skipped (data may already exist)"

PORT=${PORT:-8000}
exec python manage.py runserver 0.0.0.0:$PORT

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
import datetime as DT

from datetime import datetime, timedelta
from backports.zoneinfo import ZoneInfo


MSC = datetime(2022, 1,  1,  tzinfo=ZoneInfo("Европа/Москва"))


def weekly_digest():
    categories = Category.objects.all()
    today = DT.datetime.today()
    week_ago = today - DT.timedelta(days=7)
    week = timedelta(days=7)
    # print(today)
    # print(week_ago)
    # print(week)

    for category in categories:
        # subscribers_emails = category.subscribers.all().values('email')
        # print(subscribers_emails)

        category_subscribers = category.subscribers.all()

        category_subscribers_emails = []
        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)

        weekly_posts_in_category = []
        posts_in_category = Post.objects.all().filter(postCategory=f'{category.id}')

        for post in posts_in_category:
            # print(post.pubDate)
            time_delta = DT.datetime.now().replace(MSC) - post.pubDate
            # days_delta = today - post.pubDate
            if time_delta < week:
                weekly_posts_in_category.append(post)
                print(f'Дата публикации: {post.pubDate}')
                print(f'Дельта: {time_delta}')
                print('----------------   ---------------')

        print(f'ID: {category.id}')
        print(category)
        print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
        print(category_subscribers_emails)
        print(weekly_posts_in_category)
        print('----------------   ---------------')
        print('----------------   ---------------')
        print('----------------   ---------------')

        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
                body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
                from_email='leafarskill@yandex.ru',
                to=category_subscribers_emails,
            )

            # получаем наш html
            html_content = render_to_string(
                'weekly_digest.html',
                {
                    'digest': weekly_posts_in_category,
                    'category': category,
                }
            )

            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем
        else:
            continue

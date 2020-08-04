# advanced-news-scraper

Advanced news scrapper: collect, manage &amp; classify news

### Specification

This system should allow to:
- Collect news from different resources (with and without structured API)
- Manage collected news, including tag management
- News clasterization, semi-automatic tag assignment

Also, system should be portable and easy-to-setup/easy-to-manage

### Tech stack

** < To be discussed > **

Tech stack includes: Flask-admin for UI (backed with MySQL), Celery + RabbitMQ for task management, Elasticsearch for quick search, Selenium for scraping (when API is not avaliable)


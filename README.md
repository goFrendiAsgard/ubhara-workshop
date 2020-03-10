# Tujuan kita

Crawl data dari twitter, simpan ke postgresql, dan ingest pakai redash:

![](dashboard.png)

# Yang dibutuhkan

* docker
* docker-compose
* koneksi internet
* twitter developer account (https://developer.twitter.com/)

# Persiapkan environment

```sh
cp environment.template.env environment.env
vim environment.env # atau buka text editor yang biasa kalian pakai
```

Edit `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`, `TWITTER_CONSUMER_KEY`, dan `TWITTER_CONSUMER_SECRET`

dan simpan.

## Persiapkan semua docker container dan jalankan

```sh
docker-compose run --rm server create_db
docker-compose up
```

# Beberapa Query menarik

Jumlah tweet per detik (60 terakhir)

```sql
SELECT COUNT(tweet_id), created_at
FROM
    (
        SELECT DISTINCT tweet_id, created_at FROM tweet.statuses ORDER BY created_at DESC LIMIT 60
    ) As tabulated
GROUP BY created_at;
```

Jumlah tweet by hashtag

```sql
SELECT COUNT(tweet_id) as tweet_count, hashtag FROM 
    (SELECT DISTINCT tweet_id, "text", hashtag FROM postgres.tweet.statuses) AS tabulated
GROUP BY hashtag
ORDER BY tweet_count DESC LIMIT 15;
```

Text by hashtag

```sql
SELECT "text" FROM postgres.tweet.statuses WHERE hashtag='{{hashtag}}'
```
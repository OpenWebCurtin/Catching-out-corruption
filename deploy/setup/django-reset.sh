rm -R website/migrations
mkdir website/migrations
touch website/migrations/__init__.py

rm -R database/migrations
mkdir database/migrations
touch -R database/migrations/__init__.py

rm -R esp/migrations
mkdir esp/migrations
touch -R esp/migrations/__init__.py

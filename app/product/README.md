# Product

This Django app is responsible for retrieving data on items available in a store, regardless of its source.

The initial version used a `django.db.model` and had a tight relationship with the `Wishlist` through a foreign key in the database. As a result, the `products` CRUD had to be managed by the API.

The application as later migrated for retrieving the product data from a external API (Luiza Labs public API) that is responsible for managing the `products`. In this process, the relationship with `Wishlist` was disrupted and a `respository` was created for fetching data.

This migration was done for educational purposes and can have this concept extended for when you need to migrate certain data from a SQL table managed by Django, to another external source (eg. a DynamoDB table that you interact through AWS boto3)
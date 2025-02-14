the whole code is written in BLACK format
the book model is simple has its own fields:
title,desc,published_date,author (that is a foreign key),updated_date,published_date_site,price,category(im aware it should be choises but its not in my code)
the serializers for the book is a meta class of all fields __all__
for the CRUD operations for books im using the viewsets.modelviewset which includes all of the requirments for CRUD 
for the authors im using abstract user which has its own fields i only appended gender and age
using viewsets for register login and getting a book by its author was complex and its not logical to use viewsets so i used APIViews and reteriveApi view which makes the code much readable and in the serializers are the logic behind login and register
with a nested serializer we can access a list of author's book

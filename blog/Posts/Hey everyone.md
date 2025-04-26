
[I want to go here](Welcome)

![[Pasted image 20250426161359.png | 500x300 ]]

### ELI5:

Django REST Framework (DRF) is like a toolkit that helps you build APIs (Application Programming Interfaces) using Django. APIs allow different applications to talk to each other, like how a mobile app fetches data from a website. DRF makes it easy to create, manage, and secure these APIs without writing everything from scratch.

### Technical Explanation:

DRF is a powerful and flexible framework for building web APIs in Django. It extends Django’s capabilities to support RESTful API development with features like:

1. Serializers: To transform data into a standardized format that other programs can understand, or to deserialize data, by converting data into a format that your program can process.

2. Parsers and renderers: To render (or format) serialized data appropriately before it is returned in an 

3. HTTP response. Similarly, to parse incoming data to ensure that it’s in the correct form. 

4. API views: To implement the application logic. 

5. URLs: To define the API endpoints that will be available. 

6. Authentication and permissions: To define authentication methods for the API and the permissions required for each view.


---

# Building an API

REST- Representational State Transfer.

1. Serializer: Provides serialization for normal Python class instances

2. ModelSerializer: Provides serialization for model instances

3. HyperlinkedModelSerializer: The same as ModelSerializer, but it represents object relationships with links rather than primary keys

---
# ViewSets

ViewSets streamline API development in DRF by handling CRUD operations in a structured way, reducing the need for manually defining views.

---
# Building Custom APIs

DRF provides an APIView class that builds API functionality on top of Django’s View class. The APIView class differs from View by using DRF’s custom Request and Response objects and handling APIException exceptions to return the appropriate HTTP responses. It also has a built-in authentication and authorization system to manage access to views.

---
DRF provides a BasePermission class that allows you to define the following methods: has_permission(): A view-level permission check 
has_object_permission(): An instance-level permission check

---

?format=json to output in json format

---

# Generic Serializers

The serializers in REST framework work very similarly to Django's `Form` and `ModelForm` classes. We provide a `Serializer` class which gives you a powerful, generic way to control the output of your responses, as well as a `ModelSerializer` class which provides a useful shortcut for creating serializers that deal with model instances and querysets.

# django-silk

It tracks requests, queries, and bottlenecks—perfect for debugging performance issues, duplicate queries, and general slowness.

# Permissions

Together with [authentication](https://www.django-rest-framework.org/api-guide/authentication/) and [throttling](https://www.django-rest-framework.org/api-guide/throttling/), permissions determine whether a request should be granted or denied access.

`APIView` = **raw, flexible base class**, you do all the logic.
`ListAPIView` = **plug-and-play view** for listing objects, with pagination, filtering, etc., built-in.

# Post 
```python
class ProductCreateAPIView(generics.CreateAPIView):
  model = Product
  serializer_class = ProductSerializer
```

ListCreateAPIView
Used for **read-write** endpoints to represent a **collection of model instances**.

# JSON Web Token Authentication

djangorestframework-simplejwt


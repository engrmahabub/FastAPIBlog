# Fast API Blog
Fast API Blog

Get Started
============
::

  git clone https://github.com/engrmahabub/FastAPIBlog.git

```cd FastAPIBlog```

```python -m venv venv```

now active the **virtual environment**
  
`pip install -r requirements.txt`
  
### Run it

Run the server with:

<div class="termy">

```console
$ uvicorn main:app --reload
```
</div>

### Check it

Open your browser at http://127.0.0.1:8000/

You will see the JSON response as:

```JSON
[
  {
    "id": 1,
    "status": false,
    "description": "test details",
    "title": "Test Blog",
    "user_id": 1
  }
]
```
 
Open your browser at http://127.0.0.1:8000/blog/1

You will see the JSON response as:

```JSON
{
    "id": 1,
    "status": false,
    "description": "test details",
    "title": "Test Blog",
    "user_id": 1,
    "comment": [
        {
            "description": "test comment",
            "status": false,
            "blog_id": 1,
            "id": 1,
            "user_id": 1
        }
    ]
}
```
 
### Interactive API docs
Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI):
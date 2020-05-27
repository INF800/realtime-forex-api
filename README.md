# HEROKU

- Add `runtime.txt` with python version (heroku buildpack supports limited versions)
  ```
  python-3.8.3
  ```

- Add `Procfile`
  ```
  web: gunicorn -k uvicorn.workers.UvicornWorker main:app
  ```

- Add `requirements.txt`
  ```
  uvicorn==0.11.5
  fastapi==0.54.2
  Jinja2==2.11.2
  sqlalchemy==1.3.17
  gunicorn==20.0.4
  lxml
  html5lib
  beautifulsoup4
  numpy
  pandas
  requests
  ```
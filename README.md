# Deprecated 

All functionality moved into [django-bulbs](https://github.com/theonion/django-bulbs)

Original README Below

# Videohub Client

Some tools for referencing the videohub from our other properties

## Running Tests
Once you clone this project and `cd` into its root, to run the tests:

1. Create a virtualenv and activate it:
  ```
  virtualenv .
  source ./bin/activate
  ```

2. Install requirements
  ```
  pip install -e .
  pip install "file://$(pwd)#egg=videohub-client[dev]"
  ```

3. Run tests
  ```
  ./runtests.py
  ```

# Query_OLB
A simple app to query the Internet Archive Open Library Books API


### Dependencies

Dependencies can be installed using `pipenv`

Linux:
`pipenv install`

Windows:
`python -m pipenv install`


### Description

The app consists of a single page to query the [Internet Archive Open Library Books API](https://openlibrary.org/dev/docs/api/books). The results of the call are displayed in a table. By default, a simplified result is returned, showing only a few of the values returned by the API. TO show all results, select the `Show raw output:` checkbox.
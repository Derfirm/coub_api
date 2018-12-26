===============================
Api-wrapper for coub.com
===============================

.. image:: https://travis-ci.com/Derfirm/coub_api.svg?branch=master
    :target: https://travis-ci.com/Derfirm/coub_api
    :alt: Build Status

.. image:: https://codecov.io/gh/Derfirm/coub_api/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Derfirm/coub_api
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/coub_api.svg
    :target: https://github.com/Derfirm/coub_api
    :alt: pypi version

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Codestyle: Black

Key Features
============
- response are fully-annotated with pydantic_
- test work on snapshots from real http-answers (can easy inspect responses)
- own OAuth2-server

.. _pydantic: https://pydantic-docs.helpmanual.io/

Getting started
===============
Initiate Api client
________
.. code-block:: python

    from coub_api import CoubApi

    api = CoubApi()
    access_token = "<your access token>"
    api.authenticate(access_token)  # required for some authenticated requests


Get coub details
________________
.. code-block:: python

    coub = api.coubs.get_coub("1jf5v1")
    print(coub.id, coub.channel_id)

Create Coub
___________
.. code-block:: python

    api.coubs.init_upload()) # {"permalink":"1jik0b","id":93927327}
    api.coubs.upload_video(93927327, "video.mp4")
    api.coubs.upload_audio(93927327, "audio.mp3"))
    api.coubs.finalize_upload(93927327, title="Awesome CAT", tags=["cat", "animal"]))
    api.coubs.get_upload_status(93927327))  # {"done": False, "percent_done": 0}
    # wait a minute
    api.coubs.get_upload_status(93927327))  # {"done": True, "percent_done": 100}



Get weekly hot coubs
___________
.. code-block:: python

    from coub_api.schemas.constants import Period

    api.timeline.hot(period=Period.WEEKLY, order_by="likes_count")


Get 5 page of random section with cars
___________
.. code-block:: python

    from coub_api.schemas.constants import Section, Category

    current_page = 1
    max_page = 5
    while current_page <= max_page:
        response = api.timeline.section(section=Section.RANDOM, category=Category.CARS, page=current_page)
        print(f"processing {current_page} of {max_page}")
        for coub in response.coubs:
            print(coub.permalink)
        current_page += 1
        max_page = min(max_page, response.total_pages)



OAuth2-Server
===============
How to use:
___________
- Create Your Own_ application
- Run server
.. code-block:: RST

    coub-oauth2-server

- Enter Your Application Id and Secret and grant access the Coub server.
- Copy access token and start use it!
.. _Own: http://coub.com/dev/applications
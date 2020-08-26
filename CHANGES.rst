0.9.1
-----

- BugFix: Client endpoint name: Replace - to _

0.9.0
-----

- Remove is_ajax condition to use with infinity scroll

0.8.0
-----

- Change extra_kwargs class attribute to api_filters
- Change get_extra_params to get_api_params
- Update documentation with the new params

0.7.0
-----

- Add filter_params to the context when the request has filter

0.6.0
-----

- Add response when requests wore Ajax

0.5.1
-----

- Fix documentation grammar to get clear

0.5.0
-----

- Add a json converter to serialize the dict when running json.dumps

0.4.0
-----

- Finish the documentation
- Add new tags to setup.py

0.3.12
------

- BugFix: Remove debug from ResponseFactory

0.3.11
------

- Change the APIClientEndpointList to get clear when django raises a wrong call

0.3.10
------

- BugFix: Import without the relative import

0.3.9
-----

- BugFix: Factory repr name with special characters

0.3.8
-----

- Change Factory name with APIClient signature

0.3.7
-----

- BugFix: Slug field on ClientAPIAuthenticatedUpdateView to let generic

0.3.6
-----

- Add new fragment to the endpoint identifier on ClientAPIUpdateView

0.3.5
-----

- Get the endpoint identifier from the slug_field argument

0.3.4
-----

- BugFix: Client override when has more than on endpoint in the same base
- Update doc with new client structure

0.3.3
-----

- Replace URL_BASE to BASE_URL in all places

0.3.2
-----

- Update readme and documentation

0.3.1
-----

- Finish the base documentation and Readme

0.3.0
-----

- Update Doc
- Remove Read the docs to use Github Pages
- Add new structure with a index to to the a lang

0.2.0
-----

- Fix CI process
- Add tests to increase the coverage
- Fix read me file

0.1.3
-----

- Add ClientAPIAuthenticatedDeleteView and ClientAPIDeleteView
- BugFix: Use the correct constant to defaults (DEFAULTS) and the api (API_DEFAULTS)

0.1.2
-----

- Add documentation and fix Python version


0.1.1
-----

- Remove python 3.8 from setup because pypi dont support yet

0.1.0
-----

- Initial release

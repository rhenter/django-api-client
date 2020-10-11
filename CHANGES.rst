0.20.9
------

- BugFix:If the error is not a JSON, add as non field error

0.20.8
------

- BugFix: Set as dict if the error response wore a Str

0.20.7
------

- BugFix: Missing return the result method

0.20.6
------

- BugFix: Add conditional to the client update method when passing files.

0.20.5
------

- BugFix: Add missing attribute on BaseEndpoint

0.20.4
------

- BugFix: Add files to the Client Update
- Update docstrings

0.20.3
------

- BugFix: Add filter_params to set append_param to the URL

0.20.2
------

- BugFix: Remove ambiguous conditions to get new offset

0.20.1
------

- BugFix: Get correct offset pagination

0.20.0
------

- Add custom exception when the API is Offline

0.19.0
------

- Raise a Assertion error when a file is not declared on dynamic_fields

0.18.0
------

- BugFix: Remove duplication request for pagination

0.17.0
------

- Allow to send the form as form_data

0.16.0
------

- Add response as response.json when the request is ajax

0.15.1
------

- BugFix: Remove "or" operator from success status list

0.15.0
------

- Allow status 200 as OK on POST Request

0.14.0
------

- Build endpoint URL even when the identifier is included in the endpoint

0.13.0
------

- BugFix: Form invalid override

0.12.0
------

- Add object on the view context on ClientAPIAuthenticatedUpdateView

0.11.0
------

- Add is_ajax on form_invalid on All Create and Update Views

0.10.1
------

- BugFix: ClientAPIAuthenticatedUpdateView when call client_initial_method

0.10.0
------

- Add get_client_method and client_initial_method

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

# [1.1.0](https://github.com/ESSolutions/ESSArch_Tools_Producer/releases/tag/1.1.0)

## Features and improvements

#### Pages and layout

* The GUI has been slightly updated with fewer and smaller borders, and a more distinct header with buttons instead of
  tabs.
* Added descriptive popovers
* Added support page
* Added optional "Custom identification" field to "Prepare IP" modal. This will
  be set as the object identifier value of the IP. If none is entered, the
  object identifier value will be the same as the `id` of the IP
* When uploading files, they will now be uploaded to the folder that is opened in the file browser view
* Added the option to specify which columns should be included in IP tables in the "user settings" page
* IPs are now sorted by create date as default
* Popovers are now hidden on mobile devices
* The navigation menu is now behind a button on mobile devices, making it more responsive
* It's now possible to upload files to multiple IPs at the same time
* Added refresh button to file explorer
* New submission agreement generations can now be created when preparing a new IP
* Error messages for fields in the profile editor now appears as soon any field is modified
* URL and email fields in the profile editor with incorrect data now displays an error message
* The `remote` directive can now be used for URL fields that requires
  authentication credentials, i.e. `https://example.com,user,pass`
* The save button in the profile editor is now disabled while there are fields with invalid data
* The profile and submission agreement dropdown now includes all available entries
* (API) Pagination can now be disabled on any page using the query string `pager=none`
* IPs can now be uploaded to a remote ETA server by specifying the URL and
  authentication credentials in a `preservation_organization_receiver_url`
  field in the transfer project profile, i.e. `https://example.com,user,pass`
* The IP package file will now be compressed (gzip) if
  `container_format_compression` is set to `true` in the transfer project
  profile
* Added button for copying traceback of a failed task to task report
* Added duration to task report
* Milliseconds are now included in start and end time in task report
* Profiles in IPs with state `Created` can now be unlocked
* Updates of the task tree for an IP is no longer rebuilt on each refresh

#### API

* Object identifier value is now included in the information package serialization
* Object identifier value is now used for file and directory names
* `201 Created` is now returned when successfully preparing an IP
* When uploading files, a request to
  `api/information-packages/{id}/merge-uploaded-chunks/` is now required after
  all chunks for a file has been uploaded
* IPs can now also be searched for with object identifier value, first and last
  name of responsible, start date and end date
* Uploaded files can now be deleted in IPs that are either in the state "Prepared" or "Uploading"
* It's now possible to create empty folders in IPs that are either in the state "Prepared" or "Uploading"
* File conversion (.doc and .docx to .pdf) is now available as an option when creating IPs
* File chunks are now hidden in the IP `files` route
* The archivist organization for an IP is now specified in the submission agreement and therefore set when locking the submission agreement
* New submission agreement generations can now be created at `/api/submission-agreements/{id}/save`
* The task serialization now includes `args` which is the list of positional arguments provided to the task
* `CreateTAR` and `CreateZIP` has been moved to ESSArch Core

#### Misc

* An EAD editor is now available at `/api/information-packages/{id}/ead-editor/`
* INNODB is now the default database storage engine
* Redis is now the default task result backend

## Bug Fixes

* (API) `400 Bad Request` is now returned when trying to prepare an IP without a label
* (API) Can no longer change the submission agreement of an IP that already has
  a locked submission agreement, `400 Bad Request` is now returned when trying
* (API) `400 Bad Request` is now returned when trying to lock a submission
  agreement to an IP that already has a locked submission agreement
* (API) `400 Bad Request` is now returned when trying to change profile locked to IP
* (API) `400 Bad Request` is now returned when saving invalid profile
* (API) `400 Bad Request` is now returned when trying to unlock proifle with
  missing `type` parameter
* (API) Log file is now created before mets file
* (API) Providing the IP files route with a path outside of the IP returns `400 Bad Request`
* (API) Providing the IP files route with a path that does not exist returns `404 Not Found`
* (API) Viewing a task with params containing non-ascii characters no longer results in a `500 Internal Server Error`
* (API) `400 Bad Request` is now returned if submitting an IP that has a email
  recipient but no subject or body parameter is entered
* Locking a profile with missing required fields no longer reloads the profile
* Unlocking a profile no longer requires a page refresh before the profile can be edited

## Requirement changes
### Updates
* Updated `django-filter` from `0.15.2` to `1.0.3`
* Updated `djangorestframework` from `3.4.6` to `3.6.3`

### Additions
* Added `drf-extensions 0.3.1`
* Added `drf-proxy-pagination 0.1.1`
* Added `mock 2.0.0`
* Added `mysqlclient 1.3.10`
* Added `natsort 5.0.2`

### Deletions
* Deleted `MySQL-python`

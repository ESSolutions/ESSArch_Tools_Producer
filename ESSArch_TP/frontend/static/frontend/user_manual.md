# **User guide**

## Table of Contents

  - [Introduction ESSArch](introduction-essarch)
  - [Installation](installation)
  - [ESSArch Tools for Producer (ETP)](essarch-tools-for-producer)
    - [The user interface](the-user-interface)
        - [List view](list-view)
    - [Prepare IP](prepare-ip)
    - [Collect content](collect-content)
    - [Create SIP](create-sip)
    - [Submit SIP](submit-sip)

## Introduction ESSArch
ESSArch is an open source archival solution compliant to the OAIS ISO-standard. ESSArch consist of software components that provide functionality for Pre-Ingest, Ingest, Preservation, Access, Data Management, Administration and Management. ESSArch has been developed together with the National Archives of Sweden and Norway. Every software component of ESSArch can be used individually and also be easily integrated together to provide overall functionality for producers, archivists and consumers. ESSArch consist of ETP, ETA and EPP, each individually created to provide tools for long-term digital preservation.

 * ESSArch Tools for Producer (ETP) is used to prepare IPs, to create SIPs and to submit SIPs to archival institution
 * ESSArch Tools for Archivists (ETA) is used to receive SIPs and to prepare SIPs for ingest into the preservation platform
 * ESSArch Preservation Platform (EPP) is used to ingest SIPs, perform SIP2AIP, store AIPs in different archival storage according to storage methods, provide search and access functionality for consumers


## Installation
All of the ESSArch tools can be downloaded from [github](https://github.com/ESSolutions). Installation procedure is described on the ESSArch [doc site](http://doc.essarch.org/).


## ESSArch Tools for Producer
ETP is a SIP creator tool which provides functionality to facilitate the preparation of IPs, the creation of SIPs and the submission of SIPs. The tool supports the E-ARK general model but can easily be configured to support any other processes and workflows. Features provided are:
 * Authorizations based on users, groups and permissions
 * Integration possibility with Active Directory (AD)
 * Translations, e.g. different languages
 * Submission Agreements (SA) are supported
 * SA related profiles like SIP profiles, Submit description profiles, Transfer project profiles etc.
 * Different parallel tasks, steps and workflows can be managed, e.g. parallel work capabilities
 * Events are logged during every task and step and event types can easily be configured
 * Locking, unlocking and reuse/removal of IPs in conjunction with authority models
 * Filter functions are provided, default Archivist organisation and Archival institution
 * Search functionality, can be adjusted easily
 * Preparation of the physical and logical structure of the IP in order to be able to add content
 * Upload content (exports/file/folders etc.) into the selected prepared IP
 * Add descriptive metadata for the selected prepared IP
 * Create SIPs e.g. create a container files (tar/zip) of prepared IPs
 * Create submit descriptions in order to facilitate the submission of the SIP
 * Submit SIP to archivist organization together with associated submit description
 * Different metadata standards are supported/used, like METS and PREMIS
 * An API (REST) can be used to easily interact with the tool

## The User interface
The user interface is well known if you ever have used a web application.

 * **Menu** - provides functionality to prepare IP, collect content, create SIP and submit SIP
 * **Navigation view** - filter functionality for archival institutions, archivist organization and others
 * **User administration** - change password and logout functionality
 * **Task icons** - provides refresh, settings and help functionality
 * **Translation** - supports translation of UI
 * **List view** - lists all information packages
 * **Select/Edit view** - provides select, create, update functionality

### List view
The so called list view is the table of IP's that is present in all views in etp(Prepare IP, Collect content, Create SIP and Submit SIP).
The IP's that are listed in this view are always relevant to the current view(for example, already created SIP's are no longer visble in the Create SIP view).

![list view][list-view]

The list view has a couple of important functions built in which will be described below.
* The main funcitonality of a view, such as Prepare IP, is accessed by clicking the IP label column. These are described in the sections for the views.
* Clicking the state column will show all steps and tasks for an IP. This view has information about task and step outcome, progress and sub steps/tasks.
Click on a step or a task to get a page with more information about the step/task. This is very useful if a step/task fails because the user can access an error traceback which will help
when trying to find out where things went wrong.

![task_tree][task_tree]

![step_report][step_report]

![task_report][task_report]

* The Events column will show a list of all events for an IP. A user can add new events.
* Delete IP. A user that is either responsible or has the permission to delete can delete it.

### User settings
User settings can be found by clicking the user symbol in the top right corner and selecting "User settings".

![user settings1][user-settings1]

* The user can choose what columns should be shown in all the list views of ETP and in which order they appear.
* The columns are saved for each user, so the user "User" can have a different set of columns from login than the user "Admin" and vice versa. These settings are saved when clicking the "save" button and will always be applied on the specific user.

![user settings2][user-settings2]

### Notifications
In ETP we have notifications that shows up at the top of the page when suitable. Notifications can be live or have an update interval.
To be able to have live notifications the user needs to use a browser that supports WebSockets and have Channels activated in the backend(ETP configuration).
So whenever a notification is created the user will be notified right away and if not using WebSocket they will appear in an interval. Whenever the page is refreshed the user will always be notified if there are any notifications that has not been seen. A user can manually open the notification bar by clicking the notification(Bell) icon.


When a notification is visible, the user has 4 different options

1. The plus("+") symbol expands the notification showing the five latest notifications. Becomes a minus("-") when expanded that can be used to collapse the list. This option is only available for the first notification.
2. "Clear all" removes all notifications and they can not be seen again. This option is only available for the first notification.
3. Removes notification. This option is  available for all notifications in the list and the next notification will pop up as the last one.
4. The cross("X") symbol closes the notification bar without removing any notifications. This option is only available for the first notification.

## Prepare IP
* The first step in the process of SIP creation is Prepare IP, which is started by clicking the "Prepare IP" button.
The user is then asked to type a label for the new IP and can optionally enter a custom identifier value.

* When clicking the IP row the user can chose which Submission Agreement(SA)-profile to use. The Submission Agreement fields can be viewed by clicking the "View" button next to the SA-select. When the user is satisfied, he/she locks it by clicking the lock button.

* After Submission agreement is locked, the profiles can be viewed and edited.
* The user can edit profiles by clicking the "Edit" button in the profile table which will allow the user to edit the data of the profile fields for that specific profile. When done, click "save" and a new version of the profile data will be saved and made the current version. The user can use the "Versions"-dropdown list to choose earlier or later versions of the profile data.


* If the user is satisfied with all profiles, the IP can be prepared by clicking the "Prepare"-button in the bottom right corner.

## Collect content
Once the IP is prepared, the ip is visible in the Collect content view.


* The user may upload single files or folders by navigating to prefered location in the file browser and clicking upload.
* When done with uploading click "Done".
* It is important to not close the application while uploading content.
* The file browser also has functionality for deleting files/folders and adding new folders. These functions can be executed through buttons beneath the file browser window.

* When upload is considered done, check "Completed uploading" and click "Done".
* Folder upload may not be supported by older browsers. If functionality is desired please update your browser.

## Create SIP
When upload is set completed the ip becomes visible in the Create SIP view.
* The user can, by clicking the IP row inspect all included profiles and edit them, with the right permissions.

* If satisfied with the profiles, choose what validators to use in the SIP creation step by checking or unchecking the different validators, click create SIP to create.

## Submit SIP
Once the SIP is created it becomes visible in the Submit SIP view and is ready for submission.
* By clicking the IP row, the user can see information that is important for the SIP submission. Click Submit SIP to submit.


[user-settings1]: ./static/frontend/img/user_settings1.png "User settings"
[user-settings2]: ./static/frontend/img/user_settings2.png "User settings"
[list-view]: ./static/frontend/img/layout.png "List view"
[task_tree]: ./static/frontend/img/task_tree.png "Task tree"
[task_report]: ./static/frontend/img/task_report.png "Task report"
[step_report]: ./static/frontend/img/step_report.png "Step report"
[sa1]: ./static/frontend/img/sa1.png "Sa 1"
[sa2]: ./static/frontend/img/sa2.png "Sa 2"
[sa3]: ./static/frontend/img/sa3.png "Sa 3"
[sa4]: ./static/frontend/img/sa4.png "Sa 4"
[sa5]: ./static/frontend/img/sa5.png "Sa 5"
[profiles1]: ./static/frontend/img/profiles1.png "Profiles 1"
[profiles2]: ./static/frontend/img/profiles2.png "Profiles 2"
[profiles3]: ./static/frontend/img/profiles3.png "Profiles 3"
[cc1]: ./static/frontend/img/collect_content1.png "Collect content 1"
[cc2]: ./static/frontend/img/collect_content2.png "Collect content 2"
[cc3]: ./static/frontend/img/collect_content3.png "Collect content 3"
[cc4]: ./static/frontend/img/collect_content4.png "Collect content 4"
[cc5]: ./static/frontend/img/collect_content5.png "Collect content 5"
[create_sip]: ./static/frontend/img/create_sip.png "Create SIP"
[submit_sip1]: ./static/frontend/img/submit_sip1.png "Submit SIP1"
[submit_sip2]: ./static/frontend/img/submit_sip2.png "Submit SIP2"

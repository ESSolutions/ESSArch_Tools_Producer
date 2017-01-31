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
 * Filter functions is provided, default Archivist organisation and Archival institution
 * Search functionality, can be adjusted easily
 * Preparation of the physical and logical structure of the IP in order to be able to add content
 * Upload content (exports/file/folders etc.) into the selected prepared IP
 * Add descriptive metadata for the selected prepared IP
 * Create SIPs e.g. create a container files (tar/zip) of prepared IPs
 * Create submit descriptions in order to facilitate the submission of the SIP
 * Submit SIP to archivist organization together with associated submit description
 * Different metadata standards are supported/used, like METS and PREMIS
 * An API (REST) can be used to easily interact with the tool
 * Quality control (automatic/manually), validators, different conformance checkers etc.

## The User interface
The user interface is well known if you ever have used a web application. 

 * **Menu** - provides functionality to prepare IP, collect content, create SIP and submit SIP
 * **Navigation view** - filter functionality for archival institutions, archivist organization and others
 * **Calendar** - a basic calender (to let you know the day, if you forgot it)
 * **User administration** - change password and logout functionality
 * **Task icons** - provides refresh, settings and help functionality
 * **Translation** - supports translation of UI
 * **List view** - lists all information packages
 * **Select/Edit view** - provides select, create, update functionality

### List view
The so called list view is the table of IP's that is present in all views in etp(Prepare IP, Collect content, Create SIP and Submit SIP).
The IP's that are listed in this view are always relevant to the current view(for example, already created SIP's are no longer visble in the Create SIP view).

The list view has a couple of important functions built in which will be described below.
* The main funcitonality of a view, such as Prepare IP, is accessed by clicking the IP label column. These are described in the sections for the views.
* Clicking the state column will show all steps and tasks for an IP. This view has information about task and step outcome, progress and sub steps/tasks.
Click on a step or a task to get a page with more information about the step/task. This is very useful if a step/task fails because the user can access an error traceback which will help
when trying to find out where things went wrong.
* The Events column will show a list of all events for an IP. A user can add new events.
* Delete IP. A user that is either responsible or has the permission to delete can delete it.

## Prepare IP
* The first in the process of SIP creation is Prepare IP, which is started by clicking the "Prepare IP" button. 
The user is then asked to type a working name for the new IP.

* When clicking the label column the user can chose which Submission Agreement to use. When the user is satisfied, he/she locks it.
* After Submission agreement is locked, the profiles can be chosen, edited and locked.

## Collect content
Once the SA(Submission Agreement) and all included profiles are locked the ip is visible in the Collect content view.
The user may upload single files or folders by chosing filed/folders and clicking upload.
When upload is considered done, check "Completed uploading" and click "Done".

## Create SIP
When upload is set completed the ip becomes visible in the Create SIP view. 
* The user can, by clicking the label column inspect all included profiles, but not edit them. If the profiles are incorrect, they can be unlocked and will be editable in the Prepare IP view.
* If satisfied with the profiles, choose what validators to use in the SIP creation step, check "Approved to create" and click Create SIP.

## Submit SIP
Once the SIP is created it becomes visible in the Submit SIP view and is ready for submission.
* By clicking the label column, the user can see information that is important for the SIp submission and then check "Approved to submit" and click Submit SIP.


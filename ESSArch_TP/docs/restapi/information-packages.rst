================
 Information Packages
================

.. contents::
    :local:

.. http:get:: /information-packages/

    The information packages visible to the logged in user

.. http:post:: /information-packages/

    Creates a information package in the database along with a root folder in :ref:`path_ingest_prepare`

    :param label: label of the information package
    :type label: string
    :param object_identifier_value: (optional) the object identifier value of
        the information package. Will be set to a random UUID if none is given
    :type object_identifier_value: string

    :status 201: when information package is created
    :status 400: when label is missing
    :status 405: when information package with `object_identifier_value` already exists

.. http:post:: /information-packages/(uuid:ip_id)/prepare/

    Prepares IP (`ip_id`) by creating the directory structure defined in the
    SIP profile and assigning values from all profiles in the submission
    agreement locked to the information package

    :status 200: when information package is prepared
    :status 400: when the current state is not `Preparing` or no submission
        agreement is locked to the information package

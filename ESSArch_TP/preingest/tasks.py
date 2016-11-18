from __future__ import absolute_import

import hashlib, os, shutil, tarfile, urllib, zipfile

from django.conf import settings
from django.core import serializers

from ESSArch_Core.essxml.Generator.xmlGenerator import XMLGenerator

from fido.fido import Fido

from lxml import etree

from ESSArch_Core.configuration.models import Path
from ESSArch_Core.WorkflowEngine.dbtask import DBTask
from ESSArch_Core.ip.models import InformationPackage
from ESSArch_Core.WorkflowEngine.models import ProcessStep, ProcessTask

from ESSArch_Core.util import getSchemas, get_value_from_path, remove_prefix, win_to_posix

class PrepareIP(DBTask):
    event_type = 10100

    def run(self, label="", responsible={}, step=None):
        """
        Prepares a new information package

        Args:
            label: The label of the IP to prepare
            responsible: The responsible user of the IP to prepare
            step: The step to connect the IP to

        Returns:
            The id of the created information package
        """


        ip = InformationPackage.objects.create(
            Label=label,
            Responsible=responsible,
            State="Preparing",
            OAIStype="SIP",
        )

        prepare_path = Path.objects.get(
            entity="path_preingest_prepare"
        ).value

        ip.objectPath = os.path.join(
            prepare_path,
            str(ip.pk)
        )
        ip.save()

        self.taskobj.information_package = ip
        self.taskobj.save()

        if step is not None:
            s = ProcessStep.objects.get(pk=step)
            ip.steps.add(s)

        self.set_progress(100, total=100)

        return ip

    def undo(self, label="", responsible={}, step=None):
        pass


class CreateIPRootDir(DBTask):
    event_type = 10110

    def create_path(self, information_package_id):
        prepare_path = Path.objects.get(
            entity="path_preingest_prepare"
        ).value

        return os.path.join(
            prepare_path,
            unicode(information_package_id)
        )

    def run(self, information_package=None):
        """
        Creates the IP root directory

        Args:
            information_package_id: The id of the information package the
            directory will be created for

        Returns:
            None
        """

        self.taskobj.information_package = information_package
        self.taskobj.save()

        path = self.create_path(str(information_package.pk))
        os.makedirs(path)

        information_package.ObjectPath = path
        information_package.save()

        self.set_progress(100, total=100)
        return information_package

    def undo(self, information_package=None):
        path = self.create_path(information_package.pk)
        shutil.rmtree(path)


class CreatePhysicalModel(DBTask):
    event_type = 10115

    def run(self, structure={}, root=""):
        """
        Creates the IP physical model based on a logical model.

        Args:
            structure: A dict specifying the logical model.
            root: The root dictionary to be used
        """

        root = os.path.join(settings.BASE_DIR, str(root))

        for content in structure:
            if content.get('type') == 'folder':
                name = content.get('name')
                dirname = os.path.join(root, name)
                os.makedirs(dirname)

                self.run(content.get('children', []), dirname)

        self.set_progress(1, total=1)

    def undo(self, structure={}, root=""):
        root = os.path.join(settings.BASE_DIR, str(root))

        if root:
            shutil.rmtree(root)
            return

        for k, v in structure.iteritems():
            k = str(k)
            dirname = os.path.join(root, k)
            shutil.rmtree(dirname)


class CalculateChecksum(DBTask):
    event_type = 10210

    def run(self, filename=None, block_size=65536, algorithm=hashlib.sha256):
        """
        Calculates the checksum for the given file, one chunk at a time

        Args:
            filename: The filename to calculate checksum for
            block_size: The size of the chunk to calculate
            algorithm: The algorithm to use

        Returns:
            The hexadecimal digest of the checksum
        """

        hash_val = algorithm()

        with open(filename, 'r') as f:
            while True:
                data = f.read(block_size)
                if data:
                    hash_val.update(data)
                else:
                    break

        self.set_progress(100, total=100)
        return hash_val.hexdigest()

    def undo(self, filename=None, block_size=65536, algorithm=hashlib.sha256):
        pass

    def get_event_args(self, filename=None, block_size=65536, algorithm=hashlib.sha256):
        return [filename]

class IdentifyFileFormat(DBTask):
    event_type = 10220

    def handle_matches(self, fullname, matches, delta_t, matchtype=''):
        f, sigName = matches[-1]
        self.lastFmt = f.find('name').text

    def run(self, filename=None):
        """
        Identifies the format of the file using the fido library

        Args:
            filename: The filename to identify

        Returns:
            The format of the file
        """

        self.fid = Fido()
        self.fid.handle_matches = self.handle_matches
        self.fid.identify_file(filename)

        self.set_progress(100, total=100)

        return self.lastFmt

    def undo(self, filename=None):
        pass

    def get_event_args(self, filename=None):
        return [filename]

class GenerateXML(DBTask):
    event_type = 10230

    """
    Generates the XML using the specified data and folder, and adds the XML to
    the specified files
    """

    def run(self, info={}, filesToCreate={}, folderToParse=None):
        generator = XMLGenerator(
            filesToCreate, info
        )

        generator.generate(folderToParse=folderToParse)

        self.set_progress(100, total=100)

    def undo(self, info={}, filesToCreate={}, folderToParse=None):
        for f, template in filesToCreate.iteritems():
            os.remove(f)

    def get_event_args(self, info={}, filesToCreate={}, folderToParse=None):
        return [", ".join(filesToCreate.keys())]

class InsertXML(DBTask):
    """
    Inserts XML to the specifed file
    """

    def run(self, filename=None, elementToAppendTo=None, spec={}, info={}, index=None):
        generator = XMLGenerator()

        generator.insert(filename, elementToAppendTo, spec, info=info, index=index)

        self.set_progress(100, total=100)

    def undo(self, filename=None, elementToAppendTo=None, spec={}, info={}, index=None):
        pass

class AppendEvents(DBTask):
    event_type = 10240

    """
    """

    def run(self, filename="", events={}):
        generator = XMLGenerator()
        template = {
            "-name": "event",
            "-min": 1,
            "-max": 1,
            "-allowEmpty": 1,
            "-namespace": "premis",
            "-children": [
                {
                    "-name": "eventIdentifier",
                    "-min": 1,
                    "-max": 1,
                    "-allowEmpty": 1,
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "eventIdentifierType",
                            "-min": 1,
                            "-max": 1,
                            "-namespace": "premis",
                            "#content": [{"var":"eventIdentifierType"}]
                        },{
                            "-name": "eventIdentifierValue",
                            "-min": 1,
                            "-max": 1,
                            "-allowEmpty": 1,
                            "-namespace": "premis",
                            "#content": [{"var": "eventIdentifierValue"}]
                        },
                    ]
                },
                {
                    "-name": "eventType",
                    "-min": 1,
                    "-max": 1,
                    "-allowEmpty": 1,
                    "-namespace": "premis",
                    "#content": [{"var": "eventType"}]
                },
                {
                    "-name": "eventDateTime",
                    "-min": 1,
                    "-max": 1,
                    "-allowEmpty": 1,
                    "-namespace": "premis",
                    "#content": [{"var": "eventDateTime"}]
                },
                {
                    "-name": "eventDetailInformation",
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "eventDetail",
                            "-min": 1,
                            "-max": 1,
                            "-allowEmpty": 1,
                            "-namespace": "premis",
                            "#content": [{"var": "eventDetail"}]
                        },
                    ]
                },
                {
                    "-name": "eventOutcomeInformation",
                    "-min": 1,
                    "-max": 1,
                    "-allowEmpty": 1,
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "eventOutcome",
                            "-min": 1,
                            "-max": 1,
                            "-allowEmpty": 1,
                            "-namespace": "premis",
                            "#content": [{"var":"eventOutcome"}]
                        },
                        {
                            "-name": "eventOutcomeDetail",
                            "-min": 1,
                            "-max": 1,
                            "-allowEmpty": 1,
                            "-namespace": "premis",
                            "-children": [
                                {
                                    "-name": "eventOutcomeDetailNote",
                                    "-min": 1,
                                    "-max": 1,
                                    "-allowEmpty": 1,
                                    "-namespace": "premis",
                                    "#content": [{"var":"eventOutcomeDetailNote"}]
                                },
                            ]
                        },
                    ]
                },
                {
                    "-name": "linkingAgentIdentifier",
                    "-min": 1,
                    "-max": 1,
                    "-allowEmpty": 1,
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "linkingAgentIdentifierType",
                            "-min": 1,
                            "-max": 1,
                            "-namespace": "premis",
                            "#content": [{"var":"linkingAgentIdentifierType"}]
                        },
                        {
                            "-name": "linkingAgentIdentifierValue",
                            "-min": 1,
                            "-max": 1,
                            "-allowEmpty": 1,
                            "-namespace": "premis",
                            "#content": [{"var": "linkingAgentIdentifierValue"}]
                        },
                    ]
                },
                {
                    "-name": "linkingObjectIdentifier",
                    "-min": 1,
                    "-max": 1,
                    "-allowEmpty": 1,
                    "-namespace": "premis",
                    "-children": [
                        {
                            "-name": "linkingObjectIdentifierType",
                            "-min": 1,
                            "-max": 1,
                            "-namespace": "premis",
                            "#content": [{"var":"linkingObjectIdentifierType"}]
                        },
                        {
                            "-name": "linkingObjectIdentifierValue",
                            "-min": 1,
                            "-max": 1,
                            "-allowEmpty": 1,
                            "-namespace": "premis",
                            "#content": [{"var": "linkingObjectIdentifierValue"}]
                        },
                    ]
                },
            ]
        }

        for event in events:

            data = {
                "eventIdentifierType": "SE/RA",
                "eventIdentifierValue": str(event.id),
                "eventType": str(event.eventType.eventType),
                "eventDateTime": str(event.eventDateTime),
                "eventDetail": event.eventDetail,
                "eventOutcome": event.eventOutcome,
                "eventOutcomeDetailNote": event.eventOutcomeDetailNote,
                "linkingAgentIdentifierType": "SE/RA",
                "linkingAgentIdentifierValue": "admin",
                "linkingObjectIdentifierType": "SE/RA",
                "linkingObjectIdentifierValue": str(event.linkingObjectIdentifierValue.id),
            }

            generator.insert(filename, "premis", template, data)

        self.set_progress(100, total=100)

    def undo(self, filename="", events={}):
        pass

    def get_event_args(self, filename="", events={}):
        return [filename]

class CopySchemas(DBTask):
    event_type = 10250

    """
    Copies the schema to a specified (?) location
    """

    def findDestination(self, dirname, structure, path=''):
        for content in structure:
            if content['name'] == dirname and content['type'] == 'folder':
                return os.path.join(path, dirname)
            elif content['type'] == 'dir':
                rec = self.findDestination(
                    dirname, content['children'], os.path.join(path, content['name'])
                )
                if rec: return rec

    def createSrcAndDst(self, schema, root, structure):
        src = schema['location']
        fname = os.path.basename(src.rstrip("/"))
        dst = os.path.join(
            root,
            self.findDestination(schema['preservation_location'], structure),
            fname
        )

        return src, dst

    def run(self, schema={}, root=None, structure=None):

        src, dst = self.createSrcAndDst(schema, root, structure)
        urllib.urlretrieve(src, dst)

        self.set_progress(100, total=100)

    def undo(self, schema={}, root=None, structure=None):
        pass

    def get_event_args(self, schema={}, root=None, structure=None):
        src, dst = self.createSrcAndDst(schema, root, structure)
        return [src, dst]


class ValidateFiles(DBTask):

    def run(self, ip, xmlfile, validate_fileformat=True, validate_integrity=True):
        doc = etree.ElementTree(file=xmlfile)

        step = ProcessStep.objects.create(
            name="Validate Files",
            parallel=True,
            parent_step=self.taskobj.processstep
        )

        if any([validate_fileformat, validate_integrity]):
            for elname, props in settings.FILE_ELEMENTS.iteritems():
                for f in doc.xpath('.//*[local-name()="%s"]' % elname):
                    fpath = get_value_from_path(f, props["path"])

                    if fpath:
                        fpath = remove_prefix(fpath, props.get("pathprefix", ""))

                    fformat = get_value_from_path(f, props.get("format"))
                    checksum = get_value_from_path(f, props.get("checksum"))

                    if validate_fileformat and fformat is not None:
                        step.tasks.add(ProcessTask.objects.create(
                            name="preingest.tasks.ValidateFileFormat",
                            params={
                                "filename": os.path.join(ip.ObjectPath, fpath),
                                "fileformat": fformat,
                            },
                            information_package=ip
                        ))

                    if validate_integrity and checksum is not None:
                        step.tasks.add(ProcessTask.objects.create(
                            name="preingest.tasks.ValidateIntegrity",
                            params={
                                "filename": os.path.join(ip.ObjectPath, fpath),
                                "checksum": checksum,
                            },
                            information_package=ip
                        ))

        self.set_progress(100, total=100)

        return step.run()

    def undo(self, ip, xmlfile, validate_fileformat=True, validate_integrity=True):
        pass

class ValidateFileFormat(DBTask):
    event_type = 10260

    """
    Validates the format (PREFORMA, jhove, droid, etc.) of the given file
    """

    def run(self, filename=None, fileformat=None):
        t = ProcessTask(
            name="preingest.tasks.IdentifyFileFormat",
            params={
                "filename": filename,
            },
        )

        res = t.run_eagerly()

        assert res == fileformat, "fileformat for %s is not valid" % filename
        self.set_progress(100, total=100)

    def undo(self, filename=None, fileformat=None):
        pass

    def get_event_args(self, filename=None, fileformat=None):
        return [filename, fileformat]


class ValidateXMLFile(DBTask):
    event_type = 10261

    """
    Validates (using LXML) an XML file using a specified schema file
    """

    def run(self, xml_filename=None, schema_filename=None):
        doc = etree.ElementTree(file=xml_filename)

        if schema_filename:
            xmlschema = etree.XMLSchema(etree.parse(schema_filename))
        else:
            xmlschema = getSchemas(doc=doc)

        self.set_progress(100, total=100)

        xmlschema.assertValid(doc), "XML file %s is not valid", xml_filename

    def undo(self, xml_filename=None, schema_filename=None):
        pass

    def get_event_args(self, xml_filename=None, schema_filename=None):
        return [xml_filename]


class ValidateLogicalPhysicalRepresentation(DBTask):
    event_type = 10262

    """
    Validates the logical and physical representation of objects.

    The comparison checks if the lists contains the same elements (though not
    the order of the elements).

    See http://stackoverflow.com/a/7829388/1523238
    """

    def run(self, ip=None, xmlfile=None):
        objpath = ip.ObjectPath
        xmlrelpath = os.path.relpath(xmlfile, objpath)
        xmlrelpath = remove_prefix(xmlrelpath, "./")

        doc = etree.ElementTree(file=xmlfile)

        root = doc.getroot()

        logical_files = set()
        physical_files = set()

        for elname, props in settings.FILE_ELEMENTS.iteritems():
            for f in doc.xpath('.//*[local-name()="%s"]' % elname):
                filename = get_value_from_path(f, props["path"])

                if filename:
                    filename = remove_prefix(filename, props.get("pathprefix", ""))
                    logical_files.add(filename)

        for root, dirs, files in os.walk(objpath):
            for f in files:
                if f != xmlrelpath:
                    reldir = os.path.relpath(root, objpath)
                    relfile = os.path.join(reldir, f)
                    relfile = win_to_posix(relfile)
                    relfile = remove_prefix(relfile, "./")

                    physical_files.add(relfile)

        assert logical_files == physical_files, "the logical representation differs from the physical"
        self.set_progress(100, total=100)

    def undo(self, ip=None, xmlfile=None):
        pass

    def get_event_args(self, ip=None, xmlfile=None):
        return [xmlfile, ip.ObjectPath]


class ValidateIntegrity(DBTask):
    event_type = 10263

    def run(self, filename=None, checksum=None, block_size=65536, algorithm=hashlib.sha256):
        """
        Validates the integrity(checksum) for the given file
        """

        t = ProcessTask(
            name="preingest.tasks.CalculateChecksum",
            params={
                "filename": filename,
                "block_size": block_size,
                "algorithm": algorithm
            },
            information_package=self.taskobj.information_package
        )

        digest = t.run_eagerly()

        assert digest == checksum, "checksum for %s is not valid" % filename
        self.set_progress(100, total=100)

    def undo(self, filename=None,checksum=None,  block_size=65536, algorithm=hashlib.sha256):
        pass

    def get_event_args(self, filename=None,checksum=None,  block_size=65536, algorithm=hashlib.sha256):
        return [filename, algorithm, checksum]


class CreateTAR(DBTask):
    event_type = 10270

    """
    Creates a TAR file from the specified directory

    Args:
        dirname: The directory to create a TAR from
        tarname: The name of the tar file
    """

    def run(self, dirname=None, tarname=None):
        base_dir = os.path.basename(os.path.normpath(dirname))

        with tarfile.TarFile(tarname, 'w') as new_tar:
            new_tar.add(dirname, base_dir)

        self.set_progress(100, total=100)

    def undo(self, dirname=None, tarname=None):
        pass

    def get_event_args(self, dirname=None, tarname=None):
        return [tarname, dirname]


class CreateZIP(DBTask):
    event_type = 10271

    """
    Creates a ZIP file from the specified directory

    Args:
        dirname: The directory to create a ZIP from
        zipname: The name of the zip file
    """

    def run(self, dirname=None, zipname=None):
        with zipfile.ZipFile(zipname, 'w') as new_zip:
            for root, dirs, files in os.walk(dirname):
                for d in dirs:
                    filepath = os.path.join(root, d)
                    arcname = filepath[len(dirname) + 1:]
                    new_zip.write(filepath, arcname)
                for f in files:
                    filepath = os.path.join(root, f)
                    arcname = filepath[len(dirname) + 1:]
                    new_zip.write(filepath, arcname)

        self.set_progress(100, total=100)

    def undo(self, dirname=None, zipname=None):
        pass

    def get_event_args(self, dirname=None, zipname=None):
        return [zipname, dirname]

class UpdateIPStatus(DBTask):
    event_type = 10280

    def run(self, ip=None, status=None):
        ip.State = status
        ip.save()
        self.set_progress(100, total=100)

    def undo(self, ip=None, status=None):
        pass

    def get_event_args(self, ip=None, status=None):
        return [ip.Label]

class SubmitSIP(DBTask):
    event_type = 10300

    def run(self, ip=None):
        srcdir = Path.objects.get(entity="path_preingest_reception").value
        reception = Path.objects.get(entity="path_ingest_reception").value

        src = os.path.join(srcdir, str(ip.pk) + ".tar")
        dst = os.path.join(reception, str(ip.pk) + ".tar")
        shutil.copyfile(src, dst)

        src = os.path.join(srcdir, str(ip.pk) + ".xml")
        dst = os.path.join(reception, str(ip.pk) + ".xml")
        shutil.copyfile(src, dst)

        event_profile = ip.get_profile('event')
        dst = os.path.join(reception, "%s_event_profile.json" % ip.pk)

        with open(dst, "w") as f:
            json = serializers.serialize('json', [event_profile])
            f.write(json)

        self.set_progress(100, total=100)

    def undo(self, ip=None):
        pass

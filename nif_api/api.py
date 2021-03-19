import zeep.exceptions
from dateutil import tz
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport

from .logger import LoggingPlugin
from .typings import (Changes,
                      Organizations,
                      Organization,
                      Persons,
                      Functions,
                      Competence,
                      Competences,
                      CompetenceType,
                      License,
                      Payment,
                      Payments,
                      Hello,
                      FunctionTypes,
                      Countries,
                      OrgLogo,
                      Counties,
                      LicensesStatus,
                      LicenseTypes,
                      Activities,
                      OrganizationTypes,
                      IntegrationUser)

"""
@TODO Remove this
from os import getcwd
DEFAULT_REALM = 'PROD'
DEFAULT_LOG_FILE = '{}/nif_api.log'.format(getcwd())
"""


class NIFApiError(Exception):
    """Base class"""


class NIFApiNotImplementedError(NIFApiError):
    """Connection Error"""


class NIFApiConnectionError(NIFApiError):
    """Connection Error"""


class NIFApiAuthenticationError(NIFApiError):
    """Authentication Error"""


class NIFApiRealmError(NIFApiError):
    """Realm Error"""


class NifApi:
    """Uses zeep to get data from NIF API
    Will make all datefields timezone aware

    @TODO implement client in NifApi. Then Hello test is reusable
    """

    def __init__(self, realm, local_timezone='UTC'):
        """
        .. topic:: Timezone awareness
        """
        if realm not in ['DEV', 'DST', 'PROD']:
            raise NIFApiRealmError

        if realm == 'PROD':
            nif_base_url = 'https://services.nif.no/v4ws'
        elif realm == 'DST':
            nif_base_url = 'https://nswebdst.nif.no/v4ws'
        elif realm == 'DEV':
            nif_base_url = 'https://nswebdev.nif.no/v4ws'

        self.LOCAL_TIMEZONE = local_timezone  # "Europe/Oslo" or UTC

        # NIF common url's
        self.NIF_SYNC_URL = '{}/SynchronizationService.svc?wsdl'.format(nif_base_url)
        self.NIF_INTEGRATION_URL = '{}/IntegrationService.svc?wsdl'.format(nif_base_url)
        self.NIF_INTEGRATION_COMPETENCE_URL = '{}/Competence2Service.svc?wsdl'.format(nif_base_url)
        self.NIF_COURSE2_URL = '{}/Course2Service.svc?wsdl'.format(nif_base_url)
        self.NIF_PERSON_URL = '{}/PersonService.svc?wsdl'.format(nif_base_url)
        self.NIF_USER_URL = '{}/UserService.svc?wsdl'.format(nif_base_url)
        self.NIF_PAYMENT_URL = '{}/PaymentService.svc?wsdl'.format(nif_base_url)

        self.tz_local = tz.gettz("Europe/Oslo")
        self.tz_utc = tz.gettz('UTC')

    @staticmethod
    def _error_wrapper(resp):

        try:
            message = resp['ErrorMessage']
        except:
            message = 'Unknown'

        try:
            code = resp['ErrorCode']
        except:
            code = 500

        return {'error': message, 'code': code}


class NifApiSynchronization(NifApi):
    def __init__(self, username, password, realm, log_file, test_login=True):

        super().__init__(realm)
        transport = Transport(timeout=30)
        self.client = Client(self.NIF_SYNC_URL,
                             wsse=UsernameToken(username, password),
                             plugins=[LoggingPlugin(log_file)],
                             transport=transport)

        # Sync client options
        self.ns4 = self.client.type_factory('ns4')
        self.ns5 = self.client.type_factory('ns5')

        if test_login is True:
            state, result = self._test()

            if state is not True:
                raise NIFApiAuthenticationError('Could not authenticate via test')

    def _test(self):

        try:
            hello = self.client.service.Hello()

            return True, Hello(hello).value

        except zeep.exceptions.Fault as e:
            return False, str(e)

    def get_changes(self, start_date, end_date):
        """Changes on person, organization and function"""

        options = self.ns4.SyncOptions(OrganizationTypes=self.ns5.ArrayOfint([5, 6, 14]),
                                       EntityTypes=self.ns4.EntityTypes(['All']))

        resp = self.client.service.GetChanges3(Options=options,
                                               StartDate=start_date.astimezone(self.tz_local),
                                               ToDate=end_date.astimezone(self.tz_local))

        if 'Success' in resp and resp['Success'] is True:
            return True, Changes(resp).value
        else:
            return False, self._error_wrapper(resp)

    def get_changes_federation(self, start_date, end_date):
        """Changes on person, organization and function"""

        options = self.ns4.SyncOptions(OrganizationTypes=self.ns5.ArrayOfint([2, 19]),
                                       EntityTypes=self.ns4.EntityTypes(['Functions', 'Organizations']))

        resp = self.client.service.GetChanges3(Options=options,
                                               StartDate=start_date.astimezone(self.tz_local),
                                               ToDate=end_date.astimezone(self.tz_local))

        if 'Success' in resp and resp['Success'] is True:
            return True, Changes(resp).value
        else:
            return False, self._error_wrapper(resp)

    def get_changes_competence(self, start_date, end_date):
        """Get changes on competence"""
        resp = self.client.service.GetChangesCompetence2(FromDate=start_date.astimezone(self.tz_local),
                                                         ToDate=end_date.astimezone(self.tz_local))

        if 'Success' in resp and resp['Success'] is True:
            return True, Changes(resp).value
        else:
            return False, self._error_wrapper(resp)

    def get_changes_license(self, start_date, end_date):
        """Get changes on license, only forbundsuser"""
        resp = self.client.service.GetChangesLicense(FromDate=start_date.astimezone(self.tz_local),
                                                     ToDate=end_date.astimezone(self.tz_local))

        if 'Success' in resp and resp['Success'] is True:
            return True, Changes(resp).value
        else:
            return False, self._error_wrapper(resp)

    def get_changes_payments(self, start_date, end_date):
        """Get changes on payments club users"""
        resp = self.client.service.GetChangesPayment(FromDate=start_date.astimezone(self.tz_local),
                                                     ToDate=end_date.astimezone(self.tz_local))

        if 'Success' in resp and resp['Success'] is True:
            return True, Changes(resp).value
        else:
            return False, self._error_wrapper(resp)

    def create_integration_user(self, prefix, club_id, club_username_prefix, club_firstname_prefix, password):
        # The exception is caught in the call to _create.

        club_username = '{0}-{1}'.format(club_username_prefix, club_id)
        resp = self.client.service.CreateIntegrationUser(FirstName='{0}-{1}'.format(club_firstname_prefix,
                                                                                    club_id),
                                                         LastName='NIF.Connect',
                                                         OrgId=club_id,
                                                         Password=password,
                                                         UserName=club_username)
        # Email=None)

        if 'Success' in resp and resp['Success'] is True:
            return True, IntegrationUser(resp).value

        return False, self._error_wrapper(resp)


class NifApiCompetence(NifApi):
    def __init__(self, username, password, realm, log_file, test_login=True):

        super().__init__(realm)
        transport = Transport(timeout=1000)
        self.client = Client(self.NIF_INTEGRATION_COMPETENCE_URL,
                             wsse=UsernameToken(username, password),
                             plugins=[LoggingPlugin(log_file)],
                             transport=transport)

        # self.ns4 = self.client.type_factory('ns4')
        self.ns6 = self.client.type_factory('ns6')

        if test_login is True:
            state, result = self._test()

            if state is not True:
                raise NIFApiAuthenticationError('Could not authenticate via test')

    def _test(self):

        try:
            hello = self.client.service.Hello()

            return True, Hello(hello).value

        except zeep.exceptions.Fault as e:
            return False, str(e)

    def get_competence(self, competence_id):

        resp = self.client.service.CompetencesGet(CompetenceIds=self.ns6.ArrayOfint([competence_id]))

        c = Competences(resp).value

        if len(c) == 1:
            return True, c[0]
        else:
            return True, c

        if 'Success' in resp and resp['Success'] is True and 'CompetenceExtended' in resp:
            competence = Competence(resp)

            return True, competence.value

        else:
            return False, self._error_wrapper(resp)

    def get_competence_type(self, type_id):
        """competence type"""

        resp = self.client.service.CompetenceTypeGet(CompetenceTypeId=type_id)

        if 'Success' in resp and resp['Success'] is True and 'CompetenceType' in resp:
            competence_type = CompetenceType(resp)

            return True, competence_type.value

        else:
            return False, self._error_wrapper(resp)


class NifApiCourse2(NifApi):
    def __init__(self, username, password, realm, log_file, test_login=True):
        super().__init__(realm)
        transport = Transport(timeout=1000)

        self.client = Client(self.NIF_COURSE2_URL,
                             wsse=UsernameToken(username, password),
                             plugins=[LoggingPlugin(log_file)],
                             transport=transport)

        if test_login is True:
            state, result = self._test()

            if state is not True:
                raise NIFApiAuthenticationError('Could not authenticate via test')

    def _test(self):

        try:
            hello = self.client.service.Hello()

            return True, Hello(hello).value

        except zeep.exceptions.Fault as e:
            return False, str(e)

    def get_course(self, course_id):
        """@TODO No access"""

        raise NIFApiAuthenticationError

        try:
            course = self.client.service.CourseGet(course_id)

            # return True, Course(course).value

        except zeep.exceptions.Fault as e:
            return False, str(e)


class NifApiPerson(NifApi):
    def __init__(self, username, password, realm, log_file, test_login=True):

        super().__init__(realm)
        transport = Transport(timeout=1000)
        self.client = Client(self.NIF_PERSON_URL,
                             wsse=UsernameToken(username, password),
                             plugins=[LoggingPlugin(log_file)],
                             transport=transport)

        if test_login is True:
            state, result = self._test()

            if state is not True:
                raise NIFApiAuthenticationError('Could not authenticate via test')

    def _test(self):

        try:
            hello = self.client.service.Hello()

            return True, Hello(hello).value

        except zeep.exceptions.Fault as e:
            return False, str(e)

    def login(self, username, password):

        try:
            resp = self.client.service.LoginPerson(Username=username, Password=password)

            return True, resp
        except Exception as e:
            return False, str(e)


class NifApiIntegration(NifApi):
    def __init__(self, username, password, realm, log_file, test_login=True):

        super().__init__(realm)
        transport = Transport(timeout=30)
        self.client = Client(self.NIF_INTEGRATION_URL,
                             wsse=UsernameToken(username, password),
                             plugins=[LoggingPlugin(log_file)],
                             transport=transport)

        if test_login is True:
            state, result = self._test()

            if state is not True:
                raise NIFApiAuthenticationError('Could not authenticate via test')

    def _test(self):

        try:
            hello = self.client.service.Hello()

            return True, Hello(hello).value

        except zeep.exceptions.Fault as e:
            return False, str(e)

    def get_competence(self, competence_id) -> (bool, dict):
        raise Exception('Use NifApiCompetence!')

        resp = self.client.service.CompetenceGet(CompetenceId=competence_id)

        if 'Success' in resp and resp['Success'] is True and 'CompetenceExtended' in resp:
            competence = Competence(resp)

            return True, competence.value

        else:
            return False, self._error_wrapper(resp)

    def get_person(self, person_id) -> (bool, dict):

        factory1 = self.client.type_factory('ns1')
        factory7 = self.client.type_factory('ns7')
        xsd = self.client.type_factory('xsd')

        ids_request = factory7.ArrayOfint([xsd.int(person_id)])

        resp = self.client.service.PersonsGet(Ids=[ids_request])

        if 'Success' in resp and resp['Success'] is True and 'Persons' in resp:
            person = Persons(resp)  # resp['Persons']['PersonPublic'][0])))

            return True, person.value[0]

        else:
            return False, self._error_wrapper(resp)

    def get_function(self, function_id) -> (bool, dict):

        resp = self.client.service.FunctionsGet(Ids=[function_id])

        if 'Success' in resp and resp['Success'] is True and 'Functions' in resp:

            func = Functions(resp)

            return True, func.value[0]
        else:
            return False, self._error_wrapper(resp)

    def get_function_types(self) -> (bool, list):

        resp = self.client.service.FunctionTypeGetAll()

        if 'Success' in resp and resp['Success']:

            types = FunctionTypes(resp)

            return True, types.value
        else:
            return False, self._error_wrapper(resp)

    def get_function_details(self, function_id):
        """Not anything we need?
        resp = self.client.service.FunctionDetailsGet
        """

        raise NotImplementedError

    def get_organization(self, organization_id, org_structure) -> (bool, dict):

        try:
            resp = self.client.service.OrgGet(OrgId=organization_id)
            return True, Organization(resp, org_structure).value
        except:
            try:
                resp = self.client.service.OrganisationsGet(Ids=[organization_id])
                organization = Organizations(resp, org_structure)
                return True, organization.value[0]
            except Exception as e:
                return False, {'error': str(e), 'code': 0}

        return False, self._error_wrapper(resp)

    def get_organization_types(self) -> (bool, list):

        resp = self.client.service.OrgTypesGetAll()

        if 'Success' in resp and resp['Success']:

            types = OrganizationTypes(resp)

            return True, types.value
        else:
            return False, self._error_wrapper(resp)

    def get_org_logo(self, org_id) -> (bool, bytes):
        """Note that OrgLogo is a bytesarray"""

        resp = self.client.service.OrgLogoGet(OrgId=org_id)

        if 'Success' in resp and resp['Success'] is True and 'OrgLogo' in resp:
            return True, OrgLogo(resp).value

        return False, self._error_wrapper(resp)

    def get_license(self, license_id) -> (bool, dict):
        """Only forbundsuser"""

        resp = self.client.service.LicenseGet(LicenseId=license_id)

        if 'Success' in resp and resp['Success'] is True and 'License' in resp:
            lic = License(resp)
            return True, lic.value

        return False, self._error_wrapper(resp)

    def get_licenses_types(self) -> (bool, list):
        """Only forbundsuser"""

        resp = self.client.service.LicenseTypesGet()

        if 'Success' in resp and resp['Success'] is True and 'LicenseTypes' in resp:
            license_types = LicenseTypes(resp)
            return True, license_types.value

        return False, self._error_wrapper(resp)

    def get_licenses_status(self) -> (bool, list):
        """Return all those statuses"""

        resp = self.client.service.LicenseStatusesGet()

        if 'Success' in resp and resp['Success'] is True and 'LicenseStatuses' in resp:
            licenses_status = LicensesStatus(resp)
            return True, licenses_status.value

        return False, self._error_wrapper(resp)

    def get_countries(self) -> (bool, list):

        resp = self.client.service.CountriesGet()

        if 'Success' in resp and resp['Success'] is True and 'Countries' in resp:
            countries = Countries(resp)
            return True, countries.value

        return False, self._error_wrapper(resp)

    def get_counties(self) -> (bool, list):
        """Returns all counties"""

        resp = self.client.service.CountiesGet()

        if 'Success' in resp and resp['Success'] is True and 'Regions' in resp:
            return True, Counties(resp).value

        return False, self._error_wrapper(resp)

    def get_activities(self) -> (bool, list):
        """No access!
        resp = self.client.service.ActivitiesGetAll
        """

        resp = self.client.service.ActivitiesGetAll()

        if 'Success' in resp and resp['Success'] is True and 'Activities' in resp:
            return True, Activities(resp).value

        return False, self._error_wrapper(resp)


class NifApiUser(NifApi):
    """"""

    def __init__(self, username, password, realm, log_file, test_login=True):

        super().__init__(realm)
        transport = Transport(timeout=1000)
        self.client = Client(self.NIF_USER_URL,
                             wsse=UsernameToken(username, password),
                             plugins=[LoggingPlugin(log_file)],
                             transport=transport)

        if test_login is True:
            state, result = self._test()

            if state is not True:
                raise NIFApiAuthenticationError('Could not authenticate via test')

    def _test(self):

        try:
            hello = self.client.service.Hello()

            return True, Hello(hello).value

        except zeep.exceptions.Fault as e:
            return False, str(e)

    def get_person_id(self, buypass_id) -> (bool, int):
        """competence type"""

        resp = self.client.service.GetPersonIdByBuypassId(BuypassId=buypass_id)

        if 'Success' in resp and resp['Success'] is True and 'PersonId' in resp:
            return True, resp['PersonId']

        return False, self._error_wrapper(resp)

    def get_person_id_from_username(self, username) -> (bool, int):
        """competence type"""

        resp = self.client.service.GetPersonIdByUsername(BuypassId=username)

        if 'Success' in resp and resp['Success'] is True and 'PersonId' in resp:
            return True, resp['PersonId']

        return False, self._error_wrapper(resp)


class NifApiPayments(NifApi):
    """Uses club user"""

    def __init__(self, username, password, realm, log_file, test_login=True):

        super().__init__(realm)
        transport = Transport(timeout=1000)
        self.client = Client(self.NIF_PAYMENT_URL,
                             wsse=UsernameToken(username, password),
                             plugins=[LoggingPlugin(log_file)],
                             transport=transport)

        self.ns5 = self.client.type_factory('ns5')

        if test_login is True:
            state, result = self._test()

            if state is not True:
                raise NIFApiAuthenticationError('Could not authenticate via test')

    def _test(self):

        try:
            hello = self.client.service.Hello()

            return True, Hello(hello).value

        except zeep.exceptions.Fault as e:
            return False, str(e)

    def get_payment(self, payment_id) -> (bool, list):

        payment_ids = self.ns5.ArrayOfint([payment_id])

        resp = self.client.service.GetPaymentDetailsByIds(payment_ids)

        if 'Success' in resp and resp['Success'] is True and 'PaymentDetails' in resp:

            invoice_lines = Payments(resp)
            return True, invoice_lines.value
        else:
            return False, self._error_wrapper(resp)

from .helpers import unpack

class IntegrationUser:
    def __init__(self, integration_user):
        """
        From wsdl:
        CreateIntegrationUser(Email: xsd:string, FirstName: xsd:string, LastName: xsd:string, OrgId: xsd:int, Password: xsd:string, UserName: xsd:string)
        -> 
        ErrorCode: xsd:int, ErrorMessage: xsd:string, Person: ns6:Person, Success: xsd:boolean

        :param integration_user: 
        """
        self.status, value = unpack(integration_user, 'Person', True)

        if self.status is True:
            """Old 'Data' key is removed"""
            self.value = value
        else:
            self.value = b''

        # self._map()

    def _map(self):
        pass
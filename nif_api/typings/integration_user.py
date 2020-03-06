import typings.helpers as helpers


class IntegrationUser:
    def __init__(self, integration_user):
        """
        From wsdl:
        CreateIntegrationUser(Email: xsd:string, FirstName: xsd:string, LastName: xsd:string, OrgId: xsd:int, Password: xsd:string, UserName: xsd:string)
        -> 
        ErrorCode: xsd:int, ErrorMessage: xsd:string, Person: ns6:Person, Success: xsd:boolean

        :param integration_user: 
        """
        self.status, value = helpers.unpack(integration_user, 'Person', True)

        if self.status is True:
            self.value = value.get('Data', b'')
        else:
            self.value = b''

        # self._map()

    def _map(self):
        pass
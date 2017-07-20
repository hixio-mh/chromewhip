# noinspection PyPep8
# noinspection PyArgumentList

import logging
from typing import Any, Optional, Union

from chromewhip.helpers import PayloadMixin, BaseEvent, ChromeTypeBase

log = logging.getLogger(__name__)

# DatabaseId: Unique identifier of Database object.
DatabaseId = str

# Database: Database object.
class Database(ChromeTypeBase):
    def __init__(self,
                 id: Union['DatabaseId'],
                 domain: Union['str'],
                 name: Union['str'],
                 version: Union['str'],
                 ):

        self.id = id
        self.domain = domain
        self.name = name
        self.version = version


# Error: Database error.
class Error(ChromeTypeBase):
    def __init__(self,
                 message: Union['str'],
                 code: Union['int'],
                 ):

        self.message = message
        self.code = code


class Database(PayloadMixin):
    """ 
    """
    @classmethod
    def enable(cls):
        """Enables database tracking, database events will now be delivered to the client.
        """
        return (
            cls.build_send_payload("enable", {
            }),
            None
        )

    @classmethod
    def disable(cls):
        """Disables database tracking, prevents database events from being sent to the client.
        """
        return (
            cls.build_send_payload("disable", {
            }),
            None
        )

    @classmethod
    def getDatabaseTableNames(cls,
                              databaseId: Union['DatabaseId'],
                              ):
        """
        :param databaseId: 
        :type databaseId: DatabaseId
        """
        return (
            cls.build_send_payload("getDatabaseTableNames", {
                "databaseId": databaseId,
            }),
            cls.convert_payload({
                "tableNames": {
                    "class": [],
                    "optional": False
                },
            })
        )

    @classmethod
    def executeSQL(cls,
                   databaseId: Union['DatabaseId'],
                   query: Union['str'],
                   ):
        """
        :param databaseId: 
        :type databaseId: DatabaseId
        :param query: 
        :type query: str
        """
        return (
            cls.build_send_payload("executeSQL", {
                "databaseId": databaseId,
                "query": query,
            }),
            cls.convert_payload({
                "columnNames": {
                    "class": [],
                    "optional": True
                },
                "values": {
                    "class": [],
                    "optional": True
                },
                "sqlError": {
                    "class": Error,
                    "optional": True
                },
            })
        )



class AddDatabaseEvent(BaseEvent):

    js_name = 'Database.addDatabase'
    hashable = ['databaseId']
    is_hashable = True

    def __init__(self,
                 database: Union['Database', dict],
                 ):
        if isinstance(database, dict):
            database = Database(**database)
        self.database = database

    @classmethod
    def build_hash(cls, databaseId):
        kwargs = locals()
        kwargs.pop('cls')
        serialized_id_params = ','.join(['='.join([p, str(v)]) for p, v in kwargs.items()])
        h = '{}:{}'.format(cls.js_name, serialized_id_params)
        log.debug('generated hash = %s' % h)
        return h
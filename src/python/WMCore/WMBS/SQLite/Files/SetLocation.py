"""
SQLite implementation of SetFileLocation
"""

from WMCore.WMBS.MySQL.Files.SetLocation import SetLocation as SetLocationMySQL
from sets import Set

class SetLocation(SetLocationMySQL):
    sql = SetLocationMySQL.sql
                
    def getBinds(self, file = None, location = None):
        if type(location) == type('string'):
            return self.dbi.buildbinds(self.dbi.makelist(file), 'file', 
                   self.dbi.buildbinds(self.dbi.makelist(location), 'location'))
        elif isinstance(location, (list, Set, set)):
            binds = []
            for l in location:
                binds.extend(self.dbi.buildbinds(self.dbi.makelist(file), 'file', 
                   self.dbi.buildbinds(self.dbi.makelist(l), 'location')))
            return binds
        else:
            raise Exception, "Type of location argument is not allowed: %s" \
                                % type(location)
        
    def execute(self, file = None, location = None, conn = None, transaction = False):
        binds = self.getBinds(file, location)
        result = self.dbi.processData(self.sql, binds, 
                         conn = conn, transaction = transaction)
        
        return self.format(result)

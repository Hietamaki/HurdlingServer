# database interface
#
from dbconnection import db_session
from models import Recording

def recording_entry(name, coordinates):
	e = Recording(name, coordinates)
	db_session.add(e)
	db_session.commit()
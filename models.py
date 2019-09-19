# database schema
#
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from dbconnection import Base, db_session

class Recording(Base):
	__tablename__ = 'recordings'
	id = Column(Integer, primary_key=True)
	time_created = Column(DateTime(timezone=True), server_default=func.now())
	time_updated = Column(DateTime(timezone=True), onupdate=func.now())
	athlete_name = Column(String(50))
	coordinates = Column(ARRAY(ARRAY(Integer)))
	video_name = Column(String(100))

	def __init__(self, athlete_name=None, coordinates=None, video_name=None):
		self.athlete_name = athlete_name
		self.coordinates = coordinates

		self.save()

	def __repr__(self):
		return '<Recording %r>' % (self.athlete_name)

	def save(self):
		db_session.add(self)
		db_session.commit()

	def getCollection(self):
		return {
			"athlete_name": self.athlete_name,
			"coordinates": self.coordinates,
			"video_name": self.video_name,
			"time_created": self.time_created
		}

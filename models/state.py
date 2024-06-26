#!/usr/bin/python3
""" State Module for HBNB project """
"""This is the state class"""




from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex
class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        variables = models.storage.all()
        city_list = []
        result = []
        for key in variables:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                city_list.append(variables[key])
        for element in city_list:
            if (element.state_id == self.id):
                result.append(element)
        return (result)

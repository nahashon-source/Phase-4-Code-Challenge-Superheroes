from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from app import db

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    super_name = Column(String, nullable=False)
    hero_powers = relationship('HeroPower', back_populates='hero')

class Power(db.Model):
    __tablename__ = 'powers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

    hero_powers = relationship('HeroPower', back_populates='power')

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = Column(Integer, ForeignKey('powers.id'), nullable=False)
    strength = Column(String, nullable=False)

    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

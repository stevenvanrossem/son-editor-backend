from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from son_editor.app.database import Base


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    rel_path = Column(String(255))
    workspace_id = Column(Integer, ForeignKey('workspace.id'))
    workspace = relationship("Workspace", back_populates="projects")

    UniqueConstraint('workspace_id', 'name', name='uix_1')
    services = relationship("Service", back_populates="project", cascade="all, delete-orphan")
    functions = relationship("Function", back_populates="project", cascade="all, delete-orphan")

    def __init__(self, name=None, rel_path=None, workspace=None):
        self.name = name
        self.rel_path = rel_path
        self.workspace = workspace

    def __repr__(self):
        return '<Project %r:%r>' % (self.name, self.rel_path)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

from passlib.hash import bcrypt


# Model for databse
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)

    def __str__(self):
        return self.username
    
    @classmethod
    def get_user(cls, username):
        return cls.get(username=username)
    
    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
    

# Models for application
# Model which has all user's data
UserPydantic = pydantic_model_creator(User, name='User')

# Model to pass in the data by user
UserInPydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
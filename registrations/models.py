import datetime
from django.db import models
from mongoengine import Document, StringField, DateField
from cryptography.fernet import Fernet
from student_registration import settings



FERNET_KEY=settings.FERNET_KEY
cipher_suite = Fernet(FERNET_KEY)

class Student(Document):
    full_name = StringField(max_length=100)
    username = StringField(max_length=100, unique=True)
    address = StringField(max_length=300)
    date_of_birth = DateField(default=datetime.datetime.now)
    phone_number = StringField(max_length=20)
    disabilities = StringField()  # Assuming disabilities can be summarized in a string
    password = StringField(max_length=128)
    meta = {'collection': 'students'}
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
    def encrypt_field(self, data):
        return cipher_suite.encrypt(data.encode('utf-8')).decode('utf-8')

    def decrypt_field(self, data):
        return cipher_suite.decrypt(data.encode('utf-8')).decode('utf-8')

    def save(self, *args, **kwargs):
        #encrypt all fields but the password not to be encrypted because is hashed
        self.full_name = self.encrypt_field(self.full_name)
        self.username = self.encrypt_field(self.username)
        self.address = self.encrypt_field(self.address)
        self.date_of_birth = self.date_of_birth
        self.phone_number = self.encrypt_field(self.phone_number)
        self.disabilities = self.encrypt_field(self.disabilities)

        return super().save(*args, **kwargs)

    def clean(self):
        if self.phone_number:
            self.phone_number = self.decrypt_field(self.phone_number)
        if self.address:
            self.address = self.decrypt_field(self.address)
        if self.username:
            self.username = self.decrypt_field(self.username)
        if self.full_name:
            self.full_name = self.decrypt_field(self.full_name)
        if self.date_of_birth:
            self.date_of_birth =self.date_of_birth
        if self.disabilities:
            self.disabilities = self.decrypt_field(self.disabilities)
        return super().clean()
    def __str__(self):
        return self.username
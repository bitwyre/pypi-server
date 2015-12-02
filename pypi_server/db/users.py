#!/usr/bin/env python
# encoding: utf-8
import peewee as p
from playhouse.fields import PasswordField
from pypi_server.handlers.base import threaded
from . import Model


class Users(Model):
    login = p.CharField(max_length=255, unique=True, index=True, null=False)
    password = PasswordField(iterations=10, null=False)
    disabled = p.BooleanField(default=False, null=False)
    is_admin = p.BooleanField(default=False, null=False)
    email = p.CharField(index=True)

    @classmethod
    def check(cls, login, password):
        q = cls.select(cls.id, cls.password).where(
            cls.disabled == False,
            cls.login == str(login),
        )

        user = q.limit(1)
        user = user[0] if user else None

        if user and user.password.check_password(password):
            return cls.get(id=user.id)
        else:
            raise p.DoesNotExist("User doesn't exists")

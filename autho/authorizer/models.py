from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PrintableModel(object):
    def to_dict(self):
        # TODO: Implement to 12m, m2m
        fields = getattr(self, 'TO_DICT_FILEDS', None)
        if fields:
            return {field: getattr(self, field, None) for field in fields}
        return {}


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_internal = models.BooleanField(default=False)


class OrganizationUser(models.Model):
    organization = models.ForeignKey(Organization)
    user = models.ForeignKey(User)


class UserInfo(models.Model):
    phone = models.CharField(max_length=15, db_index=True, unique=True)
    user = models.ForeignKey(User)


class Application(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True,
                             db_index=True)
    organization = models.ForeignKey(Organization)

    class Meta:
        unique_together = (('name', 'organization'))


class Permissions(models.Model):
    name = models.CharField(max_length=255, unique=True)
    app = models.ForeignKey(Application)


class Role(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=255, unique=True)
    app = models.ForeignKey(Application)


class RolePermission(models.Model, PrintableModel):
    TO_DICT_FILEDS = ('id', 'is_internal', 'can_create',
                      'can_read', 'can_edit', 'can_delete')

    role = models.ForeignKey(Role)
    permission = models.ForeignKey(Permissions)
    is_internal = models.BooleanField()
    can_create = models.BooleanField()
    can_read = models.BooleanField()
    can_edit = models.BooleanField()
    can_delete = models.BooleanField()


class UserRole(models.Model):
    role = models.ForeignKey(Role)
    organization_user = models.ForeignKey(OrganizationUser)

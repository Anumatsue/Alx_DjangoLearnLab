from django.apps import apps
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name != 'bookshelf':
        return

    book_model = apps.get_model('bookshelf', 'Book')
    content_type = ContentType.objects.get_for_model(book_model)

    # Define groups and their permissions
    group_permissions = {
        'Viewers': ['can_view'],
        'Editors': ['can_view', 'can_create', 'can_edit'],
        'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
    }

    for group_name, perms in group_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for codename in perms:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            group.permissions.add(permission)
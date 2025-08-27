from datetime import timezone
from repository.user_repository import IUserRepository as UserRepository
from entity.user_entity import  UserEntity
from django_backend_starter.apps.loan.models import UserModel, AdminAudit, PasswordHistory
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    def add_agent(self, email, first_name, last_name, contact_number, branch, region) -> UserEntity:
        if not email or "@" not in email:
            raise ValueError("Invalid email address")

        return self.repo.create_agent(
            email=email,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            branch=branch,
            region=region
        )


    def register_user(self, username: str, email: str) -> User:
        if self.repo.exists_by_email(email):
            raise ValueError("Email already registered")
        user = User(username=username, email=email)
        self.repo.save(user)
        return user


    def suspend_user(self, admin: UserModel, user: UserModel, reason: str):
        user.suspend(reason)
        AdminAudit.objects.create(
            admin=admin,
            target_user=user,
            action="SUSPEND_USER",
            reason=reason
        )

    def reactivate_user(self, admin: UserModel, user: UserModel):
        user.reactivate()
        AdminAudit.objects.create(
            admin=admin,
            target_user=user,
            action="REACTIVATE_USER"
        )
        
    def reset_password_admin(self, user: UserModel, new_password: str, history_limit=4):
         # Check last N passwords
        last_passwords = user.password_history.all()[:history_limit]
        for old in last_passwords:
            if check_password(new_password, old.password_hash):
                raise ValueError(f"Cannot reuse the last {history_limit} passwords.")

        # Save new password
        user.set_password(new_password)
        user.save()

        
        user.set_password(new_password)
        user.password_last_changed = timezone.now()  # ✅ update last changed
        user.save()
        
        PasswordHistory.objects.create(user=user, password_hash=user.password)
        
        # Optional: prune old history
        if last_passwords.count() >= history_limit:
            for old in last_passwords[history_limit:]:
                old.delete()
from django_backend_starter.core.entities.user import UserEntity
from django_backend_starter.core.interfaces.user_repository import IUserRepository
from django_backend_starter.apps.loan.models import UserModel
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRepositoryImpl(IUserRepository):
    def get_by_email(self, email: str):
        try:
            u = UserModel.objects.get(email=email)
            return UserEntity(
                id=str(u.id),
                email=u.email,
                first_name=u.first_name,
                last_name=u.last_name,
                role=u.role,
                password_hash=u.password,
                is_active=u.is_active,
            )
        except UserModel.DoesNotExist:
            return None

    def authenticate_user(self, email, password):
        user = User.objects.filter(email=email).first()
        if not user:
            return None, "Invalid credentials"

        if user.is_locked():
            return None, f"Account locked until {user.lockout_until}"

        authenticated_user = authenticate(username=email, password=password)
        if authenticated_user:
            user.reset_failed_attempts()
            return user, None  # <-- return model instance, not UserEntity
        else:
            user.register_failed_attempt()
            return None, "Invalid credentials"

    def create_agent(self, email, first_name, last_name, contact_number=None, branch=None, region=None) -> UserEntity:
        user = User.objects.create_user(
            email=email,
            password="Agent@123",   # default password
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            role="agent",
            branch=branch,
            region=region,
            is_active=True,
        )
        return UserEntity(
            id=str(user.id),
            email=user.email,
            employee_id=user.employee_id,
            first_name=user.first_name,
            last_name=user.last_name,
            contact_number=user.contact_number,
            role=user.role,
            branch=user.branch,
            region=user.region,
            is_active=user.is_active
        )
    
    
    
    
    def get_all_agents(self):
        qs = UserModel.objects.filter(role="agent")
        return [
        UserEntity(
            id=str(u.id),
            email=u.email,
            employee_id=u.employee_id,  # <-- add this
            first_name=u.first_name,
            last_name=u.last_name,
            contact_number=u.contact_number,
            role=u.role,
            branch=u.branch,
            region=getattr(u, "region", ""),
            is_active=u.is_active
        )
        for u in qs
    ]



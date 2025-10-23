# utils/mappers.py
from entity.user_entity import UserEntity


def user_model_to_entity(user_model):
    return UserEntity(
        id=str(user_model.id),
        email=user_model.email,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        role=user_model.role,
        password_hash=user_model.password,
        is_active=user_model.is_active,
    )

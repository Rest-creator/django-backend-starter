from teseapi.models import Product, Service, SupplierProduct


class UserListingsService:

    ROLE_PRODUCT_MAP = {
        "farmer": Product,
        "supplier": SupplierProduct,
        "service-provider": Service,
    }

    @staticmethod
    def get_listings(user, role=None):
        """
        Returns a queryset of listings for the given user and role.
        If role is None, defaults to user.role.
        """
        role = role or getattr(user, "role", None)

        ModelClass = UserListingsService.ROLE_PRODUCT_MAP.get(role)

        if not ModelClass:
            # For 'customer', return empty list
            if role == "customer":
                return []
            # Invalid role
            raise ValueError(
                "Invalid or unsupported role specified for fetching listings."
            )

        return ModelClass.objects.filter(user=user).order_by("-created_at")

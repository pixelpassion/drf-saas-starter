from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class TenantAccessRequiredMixin(AccessMixin):
    """CBV mixin which verifies that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_anonymous():
            print("This should never happen - LoginRequired should be first as Mixin")
            return self.handle_no_permission()

        # TODO: Only out so that Lorenz can work on the Comments API

        # if request.tenant is None or not request.user.tenants.filter(pk=request.tenant.id):
        #     print("SiteAccessRequiredMixin: User {} on tenant {} forbidden.".format(request.user, request.tenant))
        #     return self.handle_no_permission()

        print("SiteAccessRequiredMixin: User {} on tenant {} okay!".format(request.user, request.tenant))

        return super(TenantAccessRequiredMixin, self).dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        raise PermissionDenied(self.get_permission_denied_message())

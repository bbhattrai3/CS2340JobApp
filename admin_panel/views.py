from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from .forms import AdminUserForm

User = get_user_model()


def staff_required(view_func):
	# Allow access if user is active and either staff or superuser.
	# This keeps `is_superuser` as the highest-privilege role while allowing
	# staff accounts to access the admin panel.
	return user_passes_test(lambda u: u.is_active and (u.is_staff or u.is_superuser))(view_func)


@login_required
@staff_required
def user_list(request):
	q = request.GET.get('q', '')
	if q:
		q = q.strip()
		users = User.objects.filter(
			Q(username__icontains=q) | Q(email__icontains=q)
		).order_by('username')
	else:
		users = User.objects.order_by('username').all()
	return render(request, 'admin_panel/user_list.html', {'users': users, 'q': q})


@login_required
@staff_required
def user_edit(request, pk):
	user = get_object_or_404(User, pk=pk)
	if request.method == 'POST':
		form = AdminUserForm(request.POST, instance=user)

		# Prevent non-superusers from changing another user's superuser status.
		if not request.user.is_superuser:
			form.fields.pop('is_superuser', None)

		if form.is_valid():
			form.save()
			return redirect('admin_panel:user_list')
	else:
		form = AdminUserForm(instance=user)

		# Hide the superuser field for non-superusers so they cannot promote others.
		if not request.user.is_superuser:
			form.fields.pop('is_superuser', None)
	return render(request, 'admin_panel/user_edit.html', {'form': form, 'user_obj': user})


@login_required
@staff_required
def user_delete(request, pk):
	"""Confirm and delete a user.

	Rules:
	- Only staff or superuser can access this view (decorator).
	- Cannot delete users who are staff or superuser.
	- Cannot delete self.
	"""
	target = get_object_or_404(User, pk=pk)

	# Prevent deleting staff or superusers
	if target.is_staff or target.is_superuser:
		messages.error(request, 'Cannot delete staff or superuser accounts.')
		return redirect('admin_panel:user_list')

	# Prevent deleting yourself
	if target == request.user:
		messages.error(request, 'You cannot delete your own account.')
		return redirect('admin_panel:user_list')

	if request.method == 'POST':
		action = request.POST.get('action')
		username = target.username
		if action == 'deactivate':
			target.is_active = False
			target.save()
			messages.success(request, f'User "{username}" was deactivated.')
			return redirect('admin_panel:user_list')
		else:
			# default/explicit permanent delete
			target.delete()
			messages.success(request, f'User "{username}" was permanently deleted.')
			return redirect('admin_panel:user_list')

	# If GET param permanent=1 is present, show stronger warning in template
	permanent_flag = request.GET.get('permanent') in ('1', 'true', 'yes')
	return render(request, 'admin_panel/user_confirm_delete.html', {'user_obj': target, 'permanent': permanent_flag})


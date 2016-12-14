from django import template

register = template.Library()


@register.inclusion_tag('admin/prepopulated_fields_js.html', takes_context=True)
def prepopulated_fields_js(context):
    """
    Creates a list of prepopulated_fields that should render Javascript for
    the prepopulated fields for both the admin form and inlines.
    """
    prepopulated_fields = []
    if 'adminform' in context:
        prepopulated_fields.extend(context['adminform'].prepopulated_fields)
    if 'inline_admin_formsets' in context:
        for inline_admin_formset in context['inline_admin_formsets']:
            for inline_admin_form in inline_admin_formset:
                if inline_admin_form.original is None:
                    prepopulated_fields.extend(inline_admin_form.prepopulated_fields)
    context.update({'prepopulated_fields': prepopulated_fields})
    return context


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    add = context['add']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    show_save = context.get('show_save', True)
    show_save_and_continue = context.get('show_save_and_continue', True)
    has_change_permission = context['has_change_permission']
    has_add_permission = context['has_add_permission']
    has_inline_admin_formsets = context['has_inline_admin_formsets']
    has_editable_inline_admin_formsets = context['has_editable_inline_admin_formsets']
    can_save = (has_change_permission and change) or (has_add_permission and add) or has_editable_inline_admin_formsets
    ctx = {
        'opts': opts,
        'show_delete_link': (
            not is_popup and context['has_delete_permission'] and
            change and context.get('show_delete', True)
        ),
        'show_save_as_new': not is_popup and has_change_permission and change and save_as,
        'show_save_and_add_another': (
            has_add_permission and not is_popup and
            (not save_as or add) and can_save
        ),
        'show_save_and_continue': not is_popup and can_save and show_save_and_continue,
        'is_popup': is_popup,
        'show_save': show_save and can_save,
        'preserved_filters': context.get('preserved_filters'),
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx


@register.filter
def cell_count(inline_admin_form):
    """Returns the number of cells used in a tabular inline"""
    count = 1  # Hidden cell with hidden 'id' field
    for fieldset in inline_admin_form:
        # Loop through all the fields (one per cell)
        for line in fieldset:
            for field in line:
                count += 1
    if inline_admin_form.formset.can_delete:
        # Delete checkbox
        count += 1
    return count

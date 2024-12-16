from django import template

register = template.Library()

@register.filter
# def get_field(form, field_name):
#     """
#     Returns the form field with the given name.
#     Useful for dynamically accessing form fields in templates.
#     """
#     return form[field_name]
def get_field(form, row, col):
    """
    Returns the form field with the given name.
    Useful for dynamically accessing form fields in templates.
    """
    # field_name = "cell_" + str(row) + "_" + str(col)
    field_name = f"cell_{row}_{col}"
    return form[field_name]
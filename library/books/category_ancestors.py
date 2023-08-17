def get_category_ancestors(category):
    ancestors = []
    while category.parent:
        ancestors.insert(0, category.parent)
        category = category.parent
    return ancestors
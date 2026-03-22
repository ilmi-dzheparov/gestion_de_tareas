def get_count(model_class):
    if hasattr(model_class, 'archived'):
        return model_class.objects.filter(archived=False).count()
    else:
        return model_class.objects.count()
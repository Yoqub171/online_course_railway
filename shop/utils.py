def product_rating_filter(filter_type, products):
    if filter_type == 'expensive':
        products = products.order_by('-price')
    
    elif filter_type == 'cheap':
        products = products.order_by('price')
        
    
    elif filter_type == 'rating':
        products = products.order_by('-avg_rating')

    return products
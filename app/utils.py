from app.configurations import employees_collection

def get_collection_indexes():
    """Returns list of indexes"""
    index_list = list(employees_collection.list_indexes())
    return index_list

def get_index_stats():
    """Get index usage stats"""
    try:
        collection_stats = employees_collection.database.command("collStats", "employees", indexDetails=True)
        index_sizes = collection_stats.get("indexSizes", {})
        return index_sizes
    except:
        return {}

def drop_index(index_name):
    """Remove index thru name"""
    try:
        employees_collection.drop_index(index_name)
        return True
    except:
        return False

def recreate_all_indexes():
    """recreate all indexes """
    from app.configurations import setup_db_indexes
    
    # remove all indexes first
    current_indexes = get_collection_indexes()
    for idx in current_indexes:
        idx_name = idx.get('name')
        if idx_name and idx_name != '_id_':
            try:
                employees_collection.drop_index(idx_name)
            except:
                continue
    
    # recreate them
    setup_db_indexes()
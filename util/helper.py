# util/helpers.py

def safe_import(module_name, alias=None):
    try:
        module = __import__(module_name, fromlist=[''])
        globals()[alias or module_name] = module  # Assign to global scope
        return module
    except Exception as e:
        print(f'Error importing {module_name}: {str(e)}')
        return None  # Return None if import fails

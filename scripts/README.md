# Scripts

This folder contains utility scripts for the application.

## ✅ Database Initialization Script Created

### **Location**: `scripts/init_db.py`

### **Features**:
1. **Proper Python path setup** - Adds the app directory to the Python path
2. **Environment configuration** - Sets FLAVOUR to "dev" and registers the development configuration
3. **Model imports** - Imports all necessary models (currently the Todo model)
4. **Database creation** - Creates all tables based on SQLAlchemy models
5. **Verification** - Checks that tables were created successfully
6. **Error handling** - Provides detailed error messages and proper exit codes
7. **Logging** - Comprehensive logging throughout the process

### **Usage**:
```bash
# From the project root directory
python scripts/init_db.py
```

### **Output Example**:
```
INFO:core.settings:Registering config for flavour: dev
INFO:__main__:Creating database tables...
Initializing BaseValidator...
INFO:__main__:Database tables created successfully!
INFO:__main__:Created tables: ['todos']
INFO:__main__:Database initialization completed successfully!
✅ Database initialized successfully!
```

### **Documentation**: 
- Created `scripts/README.md` with comprehensive documentation
- Explains how to use the script and what it does
- Provides instructions for adding new models

The script is now ready for initial database setup and can be easily extended to include additional models as your application grows! 
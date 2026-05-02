# VS Code Workspace Setup

This workspace is configured with tasks and debuggers for easy development.

## ✅ Workspace Features

### 1. **VS Code Tasks** (Ctrl+Shift+B or Cmd+Shift+B)

Quick access to common operations:

- **Backend: Run Django Server** - Start Django on port 8000
- **Frontend: Run React Dev Server** - Start React on port 3000
- **Backend: Run Load Test** - Execute concurrency test
- **Backend: Populate 100k Records** - Generate test data
- **Backend: Run Migrations** - Apply database migrations
- **Backend: Make Migrations** - Create migration files
- **Frontend: Install Dependencies** - npm install
- **Backend: Install Dependencies** - pip install
- **Project: Full Setup** - Run all dependency installations

### 2. **Debug Configurations** (F5)

Pre-configured debugging for:

- **Backend Server** - Debug Django with breakpoints
- **Load Test** - Debug the concurrency test script
- **Populate Data** - Debug data generation script

### 3. **Recommended Extensions**

The workspace recommends these extensions (install via Extensions panel):

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Debugger for Python** (ms-python.debugpy)
- **ES7 React/Redux/React-Native snippets** (dsznajder.es7-react-js-snippets)
- **Debugger for Chrome** (msjsdiag.debugger-for-chrome)
- **REST Client** (ritwickdey.rest-client)

## 🚀 Quick Start

### 1. Install Dependencies

**Option A: Use VS Code Tasks**

```
Ctrl+Shift+B → Select "Project: Full Setup"
```

**Option B: Manual**

```powershell
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Database Setup

```powershell
# Run migrations
cd backend
python manage.py migrate

# Create superuser (optional for admin)
python manage.py createsuperuser
```

### 3. Start Development Servers

**Option A: Use VS Code Tasks**

- Open Command Palette: Ctrl+Shift+P
- Type "Tasks: Run Task"
- Select "Backend: Run Django Server" (new terminal)
- Then select "Frontend: Run React Dev Server"

**Option B: Manual**

```powershell
# Terminal 1: Backend
cd backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm start
```

**Option C: Debug Mode (F5)**

- Select "Backend Server" from the dropdown
- Press F5 to start with debugger

## 🧪 Testing

### Run Load Test

**VS Code Task:**

```
Ctrl+Shift+B → Select "Backend: Run Load Test"
```

**Debug Mode:**

```
Select "Load Test" from debug dropdown → Press F5
```

### Populate Data

**VS Code Task:**

```
Ctrl+Shift+B → Select "Backend: Populate 100k Records"
```

**Debug Mode:**

```
Select "Populate Data" from debug dropdown → Press F5
```

## 📝 Terminal Usage

The workspace is configured with Python path. Open a terminal (Ctrl+`) and:

```powershell
# Backend commands
cd backend
python manage.py shell
python manage.py createsuperuser
python manage.py dbshell

# Frontend commands
cd frontend
npm run build
npm test
npm eject

# Run tests
python load_test.py
python populate_data.py
```

## 🔍 Debugging Tips

### Set Breakpoints

1. Click on line number to add a red dot
2. Start debugging (F5)
3. Execution pauses at breakpoint

### Debug Console

- Press `Shift+Ctrl+Y` to open Debug Console
- Evaluate expressions while paused
- Check variable values

### Watch Expressions

- In Debug view, add expressions to watch
- Track variable changes during execution

## 📚 File Navigation

Use Ctrl+P to quickly open files:

- `models.py` - Database models
- `views.py` - API endpoints
- `POS.js` - Main React component
- `settings.py` - Django configuration

## 🔧 Environment Variables

Create `.env` file in project root:

```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=assignment_db
DB_USER=root
DB_PASSWORD=
```

Copy from `.env.example` template

## 📊 Workspace Structure in VS Code

```
Assignment01/
├── .vscode/              # VS Code config (tasks, debug, settings)
├── backend/              # Django backend
│   ├── api/              # API app
│   ├── config/           # Django config
│   ├── manage.py         # CLI
│   ├── load_test.py      # Concurrency test
│   └── populate_data.py  # Data generation
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   └── styles/       # CSS files
│   └── package.json
└── README.md             # Project documentation
```

## 🌐 Access Points

Once servers are running:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin
- **Load Test**: Run from terminal or VS Code task

## 💡 Pro Tips

1. **Split Terminal**: Right-click terminal tab → "Split Terminal"
   - Keep both backend and frontend visible

2. **Output Channel**: View → Output (Ctrl+Shift+U)
   - See formatted task output

3. **Problems Panel**: View → Problems (Ctrl+Shift+M)
   - See Python linting issues

4. **Python REPL**: In terminal:

   ```python
   python
   >>> import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
   >>> import django; django.setup()
   >>> from api.models import Product
   ```

5. **Debugging Django Shell**:
   ```
   Shift+Ctrl+D → Python: Select Linter → python manage.py shell
   ```

## 🆘 Troubleshooting

### Python interpreter not found

- Install Python 3.9+ from python.org
- Or use `python.defaultInterpreterPath` in settings.json

### npm not found

- Install Node.js from nodejs.org
- Or add to PATH environment variable

### Port already in use

- Change port in Django: `python manage.py runserver 8001`
- Change port in React: `PORT=3001 npm start`

### Task fails to run

- Check terminal output (View → Output)
- Verify working directory is correct
- Ensure dependencies are installed

## 📞 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks)
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)

---

**Workspace Status**: ✅ READY
**All Tasks Configured**: YES
**Debug Configurations**: YES

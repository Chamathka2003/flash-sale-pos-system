# Deployment Guide

## Pre-Deployment Checklist

### Security
- [ ] Change `SECRET_KEY` in `settings.py`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up CSRF protection
- [ ] Configure CORS for production domain

### Database
- [ ] Create MySQL database
- [ ] Set strong password for DB user
- [ ] Configure database backups
- [ ] Run migrations
- [ ] Create database indices
- [ ] Set up monitoring

### Performance
- [ ] Enable caching (Redis recommended)
- [ ] Configure static file serving
- [ ] Set up CDN for assets
- [ ] Enable gzip compression
- [ ] Configure rate limiting

---

## Deployment Steps

### 1. Prepare Environment

```bash
# Clone repository
git clone <your-repo-url>
cd Assignment01

# Create production environment file
cp .env.example .env

# Edit .env with production values
nano .env
```

**.env Production Example:**
```
DEBUG=False
SECRET_KEY=your-very-secret-key-change-this
DB_NAME=assignment_db_prod
DB_USER=prod_user
DB_PASSWORD=strong_password_here
DB_HOST=production-mysql.example.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Backend Deployment

#### Option A: Using Gunicorn + Nginx

```bash
cd backend

# Install production dependencies
pip install gunicorn whitenoise

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Start Gunicorn server
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 30 \
  --access-logfile - \
  --error-logfile -
```

**Nginx Configuration:**
```nginx
upstream django_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL certificates
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json;
    
    # Static files
    location /static/ {
        alias /path/to/project/backend/staticfiles/;
        expires 30d;
    }
    
    # Django app
    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

#### Option B: Using Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m appuser
USER appuser

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_DATABASE: assignment_db
      MYSQL_ROOT_PASSWORD: your_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DEBUG: "False"
      SECRET_KEY: your_secret_key
      DB_HOST: db
      DB_NAME: assignment_db
      DB_USER: root
      DB_PASSWORD: your_password
    depends_on:
      - db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000/api
    volumes:
      - ./frontend:/app

volumes:
  mysql_data:
```

**Deploy with Docker:**
```bash
docker-compose up -d
```

### 3. Frontend Deployment

#### Option A: Build and Deploy

```bash
cd frontend

# Build production bundle
npm run build

# Output in build/ directory - ready to serve
```

**Deploy to S3 + CloudFront:**
```bash
# Install AWS CLI
pip install awscli

# Deploy to S3
aws s3 sync build/ s3://your-bucket-name/ --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

#### Option B: Use Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build
```

#### Option C: Use Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### 4. Database Setup

```bash
# Connect to production MySQL
mysql -h production-mysql.example.com -u prod_user -p

# Create database
CREATE DATABASE assignment_db_prod;

# Create application user
CREATE USER 'app_user'@'app-server.internal' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON assignment_db_prod.* TO 'app_user'@'app-server.internal';
FLUSH PRIVILEGES;

# Exit
EXIT;
```

### 5. Run Migrations

```bash
python manage.py migrate --settings=config.settings
```

### 6. Load Initial Data

```bash
# Create superuser for admin
python manage.py createsuperuser

# Populate products (if needed)
python populate_data.py
```

---

## Monitoring & Maintenance

### Logging

**Configure Django Logging in settings.py:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}
```

### Health Check

```python
# Add to urls.py
path('health/', HealthCheckView.as_view(), name='health')
```

**Nginx monitoring:**
```bash
# Check Gunicorn status
curl http://localhost:8000/health/

# Check response time
curl -w "@curl-format.txt" -o /dev/null -s http://yourdomain.com/api/products/
```

### Database Backups

**Automated MySQL Backup:**
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/mysql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="assignment_db_prod"
DB_USER="backup_user"

mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME | \
  gzip > $BACKUP_DIR/backup_$TIMESTAMP.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -mtime +7 -delete
```

**Add to cron:**
```bash
0 2 * * * /path/to/backup.sh
```

---

## Scaling Strategies

### 1. Database Optimization
- Enable Query Cache
- Increase InnoDB buffer pool
- Use SSD storage
- Set up replication for read scaling

### 2. Application Scaling
- Use load balancer (Nginx, HAProxy)
- Run multiple Gunicorn workers
- Implement horizontal scaling with Docker Swarm or Kubernetes

### 3. Caching Layer
```python
# Install Redis
pip install redis django-redis

# Configure in settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Cache analytics endpoint
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
def analytics(request):
    # ...
```

### 4. CDN for Static Assets
```python
# settings.py
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

---

## Troubleshooting Production Issues

### 500 Internal Server Error
```bash
# Check logs
tail -f /var/log/django/app.log
tail -f /var/log/nginx/error.log

# Test database connection
python manage.py dbshell

# Check migrations
python manage.py showmigrations
```

### Slow Queries
```bash
# Enable MySQL slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

# Analyze slow queries
mysqldumpslow /var/log/mysql/slow.log
```

### High Memory Usage
```bash
# Check Gunicorn workers
ps aux | grep gunicorn

# Reduce worker count or implement memory limit
gunicorn --workers 2 --max-requests 100 config.wsgi
```

---

## Security Checklist

- [ ] Enable HTTPS/SSL
- [ ] Set strong database password
- [ ] Configure firewall rules
- [ ] Enable SQL injection prevention
- [ ] Use prepared statements (Django ORM does this)
- [ ] Implement rate limiting
- [ ] Enable CSRF protection
- [ ] Configure secure cookies
- [ ] Use environment variables for secrets
- [ ] Implement logging and monitoring
- [ ] Regular security updates
- [ ] SQL injection testing
- [ ] XSS protection testing
- [ ] CORS configuration review

---

## Rollback Procedure

If deployment fails:

```bash
# Revert to previous version
git checkout <previous-commit>

# Revert database migrations (if needed)
python manage.py migrate <app> <previous-migration>

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## Performance Tuning

### MySQL
```sql
-- Increase connection pool
set global max_connections = 500;

-- Optimize InnoDB
set global innodb_buffer_pool_size = 4G;
set global innodb_log_file_size = 1G;
```

### Django
```python
# Use connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}

# Enable query optimization
LOGGING = {
    # log slow queries
}
```

### Nginx
```nginx
# Increase worker connections
worker_connections 2048;

# Enable caching
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=cache:10m;
```

---

## Support

For production issues, check:
1. Application logs
2. Database logs
3. Server logs (Nginx, Gunicorn)
4. System resources (CPU, memory, disk)
5. Network connectivity

---

**Status**: Ready for Production ✅

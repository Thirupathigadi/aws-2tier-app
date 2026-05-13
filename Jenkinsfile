pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_DEFAULT_REGION    = 'ap-south-1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Pulling code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/Thirupathigadi/aws-2tier-app.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                echo '🐍 Setting up virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip --quiet
                    pip install -r requirements.txt --quiet
                    echo "Dependencies installed ✅"
                '''
            }
        }

        stage('Validate Code') {
            steps {
                echo '🔍 Checking Python syntax...'
                sh '''
                    . venv/bin/activate
                    python3 -m py_compile app/app.py && echo "app.py OK"
                    python3 -m py_compile app/config.py && echo "config.py OK"
                    python3 -m py_compile infrastructure/deploy.py && echo "deploy.py OK"
                '''
            }
        }

        stage('Deploy to AWS') {
            steps {
                echo '☁️ Deploying 2-tier infrastructure on AWS...'
                sh '''
                    . venv/bin/activate
                    cd infrastructure
                    python3 deploy.py
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo '🏥 Checking app health...'
                sh '''
                    . venv/bin/activate
                    sleep 30
                    python3 scripts/test_connection.py
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 SUCCESS — 2-tier app deployed on AWS!'
        }
        failure {
            echo '❌ FAILED — check console output for errors.'
        }
        always {
            cleanWs()
        }
    }
}

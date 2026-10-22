pipeline {
    agent any

    environment {
        IMAGE_NAME = 'anoushkavpawar/cloud-cicd-lab'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/python -m compileall -q app.py test_app.py
                    .venv/bin/pytest -q
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                      -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        printf '%s' "$DOCKER_TOKEN" |
                          docker login -u "$DOCKER_USER" --password-stdin

                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl --context=minikube apply -f k8s/deployment.yaml
                    kubectl --context=minikube apply -f k8s/service.yaml

                    kubectl --context=minikube \
                      set image deployment/cloud-app \
                      cloud-app=${IMAGE_NAME}:${BUILD_NUMBER}

                    kubectl --context=minikube \
                      rollout status deployment/cloud-app --timeout=180s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    kubectl --context=minikube get pods
                    kubectl --context=minikube get deployments
                    kubectl --context=minikube get services

                    kubectl --context=minikube \
                      exec deployment/cloud-app -- \
                      python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5001/health').read().decode())"
                '''
            }
        }
    }

    post {
        always {
            echo 'CI/CD pipeline finished. Check the stage results above.'
        }
    }
}
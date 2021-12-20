pipeline {
  agent { label 'techops_jenkins_node' }

  // This section needs to fetch dependencies from Glovo artifactory
  environment {
    ARTIFACTORY_PASSWORD = credentials('ARTIFACTORY_PASSWORD')
    PIP_INDEX_URL = "https://jenkins:${ARTIFACTORY_PASSWORD}@artifactory.glovoint.com/artifactory/api/pypi/glovo-pypi/simple"
  }

  stages {
    stage('Preparation') {
    // On this stage done all preparation work
    // Getting dependencies, creating folders, etc..
      steps {
        sh('''python3 -m venv run-env
        source run-env/bin/activate
        pip3 install -r requirements.txt
        pip3 install config-sm==0.1.2''')
      }
    }
    stage('Execution') {
      steps {
        sh("source run-env/bin/activate && python3 secrets_to_env.py 'python3 main.py'")
      }
    }
  }
}
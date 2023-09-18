pipeline {
  agent none
  stages {
    stage('clone') {
      steps {
        git(poll: true, url: 'https://github.com/bigsheykh/java-codes-for-last-project', branch: 'main')
      }
    }

  }
}
node('docker-builder') {

    stage('Checkout') {
        checkout scm
    }

    stage('Build flask') {
        buildDockerfile "hcx-quickbooks-dashboard-flask", "Dockerfile"
    }

    stage('Build nginx'){
        buildDockerfile "hcx-quickbooks-dashboard-nginx", "Dockerfile.nginx"
    }

    stage('Run tests'){
        withPostgresServer {
            docker.image("hcx-quickbooks-dashboard-flask").inside {
                withEnv(['HCG_UTILS_AUTHENTICATION_JWT_VERIFY=no']){
                    sh 'alembic upgrade head'
                    sh 'pytest --junitxml=xunit-reports/xunit-result-python.xml --cov --cov-report xml:coverage-reports/coverage-python.xml'
                }
            }
        }
    }

    stage('SonarQube analysis') {
        sonarScan 'hcx-quickbooks-dashboard'
    }

    stage('Helm chart'){
        helmLint 'charts'
        inMaster{
            helmPublish 'charts/hcx-quickbooks-dashboard'
        }
    }

    inMaster {
	stage('Migrate') {
	    def alembic = docker.image('hcx-quickbooks-dashboard-flask')
	    applyAlembicMigration('hcx-quickbooks-dashboard', alembic)
	}
    }
}

stage("Quality Gate"){
    sonarQualityGate()
}
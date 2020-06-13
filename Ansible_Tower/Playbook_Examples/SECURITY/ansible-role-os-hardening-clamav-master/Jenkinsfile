@Library('pipeline-library')_
import com.worldpay.Utils

node('molecule') {

  def utils = new Utils()
  def branch_type = utils.getBranchType("${env.BRANCH_NAME}")
  def reponame = utils.determineRepoName()
  def url = utils.determineRepoUrl()
  def bname = "${env.BRANCH_NAME}"
  
    stage('Checkout') {
      echo "Building from \nBranch type: ${branch_type} \nBranch name: ${bname} \nRepo: ${url} or ${reponame}"
       //Note: having the variable names in this JenkinsFile different to those accepted by the groovy shared lib is intentional
       checkoutToDir {
         branchName = bname
            repoUrl = url
            dirName = reponame
        }
      
      currentBuild.displayName = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
  }
  
  switch (branch_type) {
    case "feature":
      sh "cd ${reponame} && molecule test"
      break
    case 'develop':
      sh "cd ${reponame} && molecule test"
      break
    case 'release':
      sh "cd ${reponame} && molecule test"
      break
    case 'master':
      sh "cd ${reponame} && molecule test"
      break
    default:
      echo 'Building default branch'
  }
}

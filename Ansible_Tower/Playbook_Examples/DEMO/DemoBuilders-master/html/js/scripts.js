function ProvisionAzure(){

var xhr = new XMLHttpRequest();

xhr.open("POST", "https://10.0.22.80/api/v1/workflow_job_templates/16/launch/", false);
xhr.setRequestHeader("Authorization", "Basic ZGVtb2J1aWxkZXI6dGhpc2lzbXlpbnNhbmVwYXNzd29yZHRoYXRzaG91bGRuZXZlcmJldXNlZA==")

xhr.send("");
alert(xhr.status);
console.log(xhr.status);
console.log(xhr.statusText);

}

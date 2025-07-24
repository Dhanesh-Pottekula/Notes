lab link : https://partner.cloudskillsboost.google/course_templates/648/labs/484534

# You can list the active account name with this command:
```gcloud auth list```
# You can list the project ID with this command:
```gcloud config list project```

# set region 
```gcloud config set compute/region us-east1```
# get region
```gcloud config get-value compute/region```

# get project id 
```gcloud config get-value project```

# get project details 
```gcloud compute project-info describe --project $(gcloud config get-value project)``` # gcloud config get-value project --> give the project id 

# sets an environment variable 
```export PROJECT_ID=$(gcloud config get-value project)```

# check the environment variables with 
```echo -e "$PROJECT_ID"```

# to create a vm in gcloud
```gcloud compute instances create gcelab2 --machine-type e2-medium --zone $ZONE``` # gcelab2 is name of vm 

# view the config list 
```gcloud config list``` to view all the config in settings add``` --all``` flag

# gives the all list of vm instances 
```gcloud compute instances list```   to filter add ```--filter="name=('gcelab2')"```
#list all the firewall rules 
```gcloud compute firewall-rules list```

##  connecting to partular vm instance
```gcloud compute ssh [name of instance] --zone $ZONE``` 

# Add a tag to the virtual machine:

```gcloud compute instances add-tags gcelab2 --tags http-server,https-server```
Update the firewall rule to allow:

```gcloud compute firewall-rules create default-allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=http-server
Copie```

# connect via http curl
```curl http://$(gcloud compute instances list --filter=name:gcelab2 --format='value(EXTERNAL_IP)')```

# View the available logs on the system:

```gcloud logging logs list```



external load balancing 
managed instances (application load balancing)
## lab 2 : https://partner.cloudskillsboost.google/course_templates/648/labs/484535

  gcloud compute instances create www3 \
    --zone=us-east1-b  \
    --tags=network-lb-tag \
    --machine-type=e2-small \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --metadata=startup-script='#!/bin/bash
      apt-get update
      apt-get install apache2 -y
      service apache2 restart
      echo "
<h3>Web Server: www3</h3>" | tee /var/www/html/index.html'    --- this creates the vm instance

Create a firewall rule to allow external traffic to the VM instances:
```gcloud compute firewall-rules create www-firewall-network-lb \
    --target-tags network-lb-tag --allow tcp:80```


ping to the server 
 ``` curl http://34.23.144.94```

 create an static api 
 gcloud compute addresses create <network name> \
  --region us-east1

  add health checks
  gcloud compute http-health-checks create <check name>

  create pool and add health check 
  gcloud compute target-pools create <pool name> \
  --region us-east1 --http-health-check <check name>

  add instances to pool 
  gcloud compute target-pools add-instances <pool name> \
    --instances <name1>,<name2>,<name3>                     -- there can be any number of vm names that can be added to pool
                                                                vms in this pool will receive request from th eload balancer

add farwarding rool 

```gcloud compute forwarding-rules create www-rule \
    --region  us-east1 \
    --ports 80 \
    --address <static network name we created above> \
    --target-pool <pool name>  ```                             -- load balancer runs on port 80 of static ip (-- address) farwards request to vms present in target pool, only if they are healthy, as defined by the basic-check health check.

## auto scaleing

create templates 
```gcloud compute instance-templates create lb-backend-template \
   --region=Region \
   --network=default \
   --subnet=default \
   --tags=allow-health-check \
   --machine-type=e2-medium \
   --image-family=debian-11 \
   --image-project=debian-cloud \
   --metadata=startup-script='#!/bin/bash
     apt-get update
     apt-get install apache2 -y
     a2ensite default-ssl
     a2enmod ssl
     vm_hostname="$(curl -H "Metadata-Flavor:Google" \
     http://169.254.169.254/computeMetadata/v1/instance/name)"
     echo "Page served from: $vm_hostname" | \
     tee /var/www/html/index.html
     systemctl restart apache2'```

Create a managed instance group based on the template:

gcloud compute instance-groups managed create lb-backend-group \
   --template=lb-backend-template --size=2 --zone=Zone


   Create the fw-allow-health-check firewall rule.

gcloud compute firewall-rules create fw-allow-health-check \
  --network=default \
  --action=allow \
  --direction=ingress \
  --source-ranges=130.211.0.0/22,35.191.0.0/16 \
  --target-tags=allow-health-check \
  --rules=tcp:80

  gcloud compute addresses create lb-ipv4-1 \
  --ip-version=IPV4 \
  --global


  gcloud compute health-checks create http http-basic-check \
  --port 80


  gcloud compute backend-services create web-backend-service \
  --protocol=HTTP \
  --port-name=http \
  --health-checks=http-basic-check \
  --global

  gcloud compute backend-services add-backend web-backend-service \
  --instance-group=lb-backend-group \
  --instance-group-zone=Zone \
  --global


  Create a URL map to route the incoming requests to the default backend service:

gcloud compute url-maps create web-map-http \
    --default-service web-backend-service

    
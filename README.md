## Tools and Scripts to manage WebProd's Deis cluster

### Add NewRelic Server Monitoring

1. SSH to one of the hosts
2. wget https://raw.githubusercontent.com/mozilla/webprod-deis/master/newrelic/newrelic-sysmond.service
3. Edit `newrelic-sysmond.service` and replace `YOUR_NEW_RELIC_KEY` with our NewRelic Key.
4. Load the unit file with `fleetctl load newrelic-sysmond.service`
5. Start the unit file `fleetctl start newrelic-sysmond.service`. This service is Global and thus it will run and monitor all the servers of the cluster.
6. Go to NewRelic Servers and make sure that the servers have the 'Project:Webprod' tag
7. Update 'WebProd Deis Servers' NewRelic alert policy with the new servers.


### Add daily backups to S3

Follow the [deis-backup-service instructions](https://github.com/mozilla/deis-backup-service/blob/master/README.md).


### Terminating a Deis cluster on AWS

Deis AWS [cluster provision script](https://github.com/deis/deis/blob/master/contrib/ec2/provision-ec2-cluster.sh) creates an [AWS CloudFormation](https://aws.amazon.com/cloudformation/). In its turn CloudFormation creates the required Launch Configuration, Auto Scaling Group, ELB, Security Groups and of course EC2 instances.

The provision script creates two security groups,the 'Deis Web ELB Security Group' and the 'Enable public SSH and intra-VPC communication'. It's possible that the later group is used by RDS instances, to open a network flow between Deis and RDS for application use. If other AWS components are in use then that maybe the case for those components as well.

To terminate the cluster, first decouple any security groups that belong to the cluster from other AWS components, like RDS. Then visit CloudFormation Console and delete the formation. All components created by this formation will be deleted. Failing to decouple the groups from other components, will prevent the deletion of the formation.

It is important to delete the whole formation and not just the EC2 instances. Deleting only the EC2 instances, will cause the Auto Scaling Group to trigger the creation of new EC2 instances.

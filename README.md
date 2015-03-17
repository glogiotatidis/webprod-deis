## Tools and Scripts to manage WebProd's Deis cluster

### Add NewRelic Server Monitoring

1. SSH to one of the hosts
2. git clone https://github.com/johanneswuerbach/newrelic-sysmond-service
3. Edit `newrelic-sysmond.service` and replace `YOUR_NEW_RELIC_KEY` with our NewRelic Key and `CUSTOM_HOSTNAME=%H` with `CUSTOM_HOSTNAME=webprod-deis-%H`
4. Load the unit file with `fleetctl load newrelic-sysmond.service`
5. Start the unit file `fleetctl start newrelic-sysmond.service`. This service is Global and thus it will run and monitor all the servers of the cluster.
6. Go to NewRelic Servers and make sure that the servers have the 'Project:Webprod' tag
7. Update 'WebProd Deis Servers' NewRelic alert policy with the new servers.


### Add daily backups to S3

Follow the [deis-backup-service instructions](https://github.com/mozilla/deis-backup-service/blob/master/README.md).

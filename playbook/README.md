## Upgrading Deis

1. Clone deis repository

git clone https://github.com/deis/deis

2. Checkout wanted Deis version

git checkout v1.4.1

3. Make discovery url

make discovery-url

4. Update ./contrib/ec2/cloudformation.json with KeyPair

[
    {
        "ParameterKey":     "KeyPair",
        "ParameterValue":   "KeyPairOnAWS"
    }
]

5. Export VPC variables

6. Run provision command

./contrib/ec2/provision-ec2-cluster.sh deis-<VERSION> # e.g. 141 for v1.4.1

7. Wait a moment for cluster to form

8. Populate local_variables.yml with IPs and other stuff needed

9. Run the Playbook

ansible-playbook -i hosts site.yml

This will take a backup of the current cluster and restore into the new one.

10. Run the [last step to fully restore Deis](http://docs.deis.io/en/latest/managing_deis/backing_up_data/#finishing-up)
11. Restart all apps using `restart-all-apps.py` script.
12. You may need to remove and re-add domains in the deis apps.
13. Add Instance Termination Protection.
14. Add Alarms for Instance.
15. Update deis{1,2,3}.example.com entries.
16. Update *.example.com DNS entry.
17. Delete the temporary EC2 node that was created by the playbook. Default name is `temp-deis-worker`.

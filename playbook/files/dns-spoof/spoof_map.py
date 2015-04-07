fqdn2fqdn = {
    'deis-store.{{ deis_domain }}': '{{ new_deis_elb_dns_name }}',
    'deis.{{ deis_domain }}': '{{ new_deis_elb_dns_name }}',
}

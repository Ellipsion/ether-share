from subprocess import check_output

ips = check_output(['hostname', '--all-ip-addresses'])
# Default configs for DisMAL

from fileinput import filename
import os

# Config
pwd = os.getcwd()

# Exported files location
#files_path = pwd + "/output_" + args.target.replace(".","_")

# Exported file names
api_filename                = "versions.txt"
audit_filename              = "audit.csv"
baseline_filename           = "baseline.csv"
cluster_filename            = "cluster.txt"
cmdb_errors_filename        = "cmdb_errors.txt"
cmdbsync_filename           = "cmdb_sync.txt"
config_dump_filename        = "config_dump.xml"
consolidation_filename      = "consolidation.txt"
core_dumps_filename         = "core_dumps.txt"
crontab_filename            = "crontab.txt"
current_opts_filename       = "tw_options_current.dict"
current_platforms_filename  = "platforms_current.xml"
active_scans_filename       = "active_scans.csv"
db_lifecycle_filename       = "db_lifecycle.csv"
capture_candidates_filename = "capture_candidates.csv"
default_opts_filename       = "tw_options_default.dict"
default_platforms_filename  = "platforms_default.xml"
disco_status_filename       = "discovery_status.txt"
disk_filename               = "disk.csv"
eca_errors_filename         = "eca_errors.csv"
etc_passwd_filename         = "etc_passwd.csv"
exclude_ranges_filename     = "exclude_ranges.csv"
host_util_filename          = "host_utilisation.csv"
hostname_filename           = "hostname.txt"
installed_agents_filename   = "installed_agents.csv"
ipaddr_filename             = "ipaddr.txt"
ldap_filename               = "ldap.txt"
missing_vms_filename        = "missing_vms.csv"
near_removal_filename       = "near_removal.csv"
ntp_filename                = "ntp_status.txt"
open_ports_filename         = "open_ports.csv"
orphan_vms_filename         = "dq_orphan_vms.csv"
os_lifecycle_filename       = "os_lifecycle.csv"
outposts_filename           = "outposts.txt"
outpost_creds_filename      = "outpost_creds.csv"
pattern_modules_filename    = "pattern_modules.csv"
tku_filename                = "pattern_modules.csv"
reasoning_filename          = "waiting.txt"
removed_filename            = "removed.csv"
reports_model_filename      = "reports_model.txt"
resolv_conf_filename        = "resolv.conf"
scan_ranges_filename        = "scan_ranges.csv"
sensitive_data_filename     = "sensitive_data.csv"
si_lifecycle_filename       = "software_lifecycle.csv"
si_user_accounts_filename   = "software_usernames.csv"
snmp_unrecognised_filename  = "snmp_unrecognised.csv"
success_filename            = "success.csv"
syslog_filename             = "syslog.txt"
tax_deprecation_filename    = "tax_deprecation.txt"
timezone_filename           = "timezone.txt"
tls_certificates_filename   = "tls_certificates.txt"
tree_filename               = "tree.csv"
tw_ds_compact_filename      = "tw_ds_compact.log"
tw_ds_offline_filename      = "tw_ds_offline_compact.log"
tw_events_filename          = "events.txt"
tw_knowledge_filename       = "knowledge.txt"
tw_license_csv_filename     = "license.csv"
tw_license_raw_filename     = "license.txt"
tw_license_zip_filename     = "license.zip"
tw_listusers_filename       = "users.txt"
tw_options_filename         = "tw_options.txt"
ui_errors_filename          = "ui_errors.txt"
uname_filename              = "uname.txt"
vault_filename              = "vault.txt"
vmware_tools_filename       = "vmware_tools.txt"
    
# Headers
baseline_header     = [ "Check", "Result", "Description" ]
df_h_header         = [ "fs", "mount", "size", "used", "available", "Used %" ]
etc_passwd_header   = [ "login", "password", "uid", "gid", "gecos", "homedir", "shellcmd" ]
tree_header         = [ "path" ]

# CLI commands
baseline_cmd            = 'tw_baseline --no-highlight'
cluster_cmd             = 'tw_cluster_control --show-members'
cmdb_errors_cmd         = 'cat /usr/tideway/log/tw_svc_cmdbsync_transformer.log | egrep -i "Failed creation|Failed deletion|RPC call failed" || echo "No errors"'
cmdbsync_cmd            = 'tw_sync_control --list'
cons_status_cmd         = 'tw_reasoningstatus --consolidation-status'
core_dumps_cmd          = 'command -v tw_check_cores &> /dev/null && tw_check_cores || ls -l $HOME/cores'
df_h_cmd                = 'df -h | awk \'NR > 1 {OFS=",";print $1,$6,$2,$3,$4,$5}\''
disco_status_cmd        = 'tw_reasoningstatus --discovery-status'
ds_status_off_cmd       = 'cat /usr/tideway/log/tw_ds_offline_compact.log'
ds_status_on_cmd        = 'cat /usr/tideway/log/tw_ds_compact.log'
etc_passwd_cmd          = 'cat /etc/passwd'
get_defaults_cmd        = 'python3 -c "from common.options.defaults import getDefaults; print(getDefaults())"'
get_opts_cmd            = 'python3 -c "from common.options.main import getOptions; print(getOptions())"'
hostname_cmd            = 'hostname'
ipaddr_cmd              = 'hostname -I'
ldap_cmd                = 'tw_secopts | grep LDAP_ENABLED'
licensing_cmd           = 'command -v tw_license_report && tw_license_report'
ntp_cmd                 = 'command -v timedatectl &> /dev/null && timedatectl status | grep "NTP" || ntpstat'
outposts_cmd            = 'tw_reasoningstatus --discovery-outposts'
reasoning_cmd           = 'tw_reasoningstatus --waiting-full'
reports_model_cmd       = 'tw_check_reports_model'
resolv_conf_cmd         = 'cat /etc/resolv.conf'
rsyslog_cmd             = 'command -v systemctl && systemctl is-active rsyslog'
rsyslog_conf_cmd        = r"cat /etc/rsyslog.conf | sed -e '1,/#\\$ActionResumeRetryCount/d'"
tax_deprecated_cmd      = 'tw_tax_deprecated'
tls_certificates_cmd    = 'openssl s_client -showcerts -connect'
tree_cmd                = 'find /usr/tideway'
tw_config_dump_cmd      = 'tw_config_dump'
tw_crontab_cmd          = 'crontab -l'
tw_events_cmd           = 'tw_event_control'
tw_knowledge_cmd        = 'tw_pattern_management --list-uploads'
tw_listusers_cmd        = 'tw_listusers'
tw_options_cmd          = 'tw_options'
tw_platforms_cmd        = 'tw_disco_export_platforms'
tz_cmd                  = 'command -v timedatectl &> /dev/null && timedatectl status | grep "Time zone" || cat /etc/sysconfig/clock && date +%Z'
ui_errors_cmd           = 'ls -l /usr/tideway/python/ui/web/ErrorMsgs/'
uname_cmd               = 'uname -a'
vmware_tools_cmd        = 'command -v systemctl && systemctl is-active vmware-tools'
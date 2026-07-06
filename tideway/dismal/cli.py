# Discovery CLI commands for DisMAL

import sys
import logging
import getpass
import time
import sys
import ast
import os

# Local modules
from . import access, output, queries, defaults, reporting, tools, common_agents

logger = logging.getLogger("_cli_")

def run_query(client,sysuser,passwd,query):
    runQuery = 'tw_query -u %s -p %s --csv "%s"'%(sysuser,passwd,query)
    logger.info("Running query: %s"%query)
    try:
        data = access.remote_cmd(runQuery,client)
        logger.debug("Query Ran:\n%s\n%s"%(query,data))
    except Exception as e:
        msg = "Query failed to run: %s\nException: %s\n%s" %(query,e.__class__,str(e))
        logger.error(msg)
        data = "%s\n>>>Query failed to run, check logs."%query
        print(data)
    return data


def _get_tku_version(client, user, passwd):
    """Return the TKU version string for the target appliance.

    The command ``tw_pattern_management --list-uploads`` lists installed
    knowledge updates.  We capture the first non-empty line as the TKU level.
    If the command fails or returns nothing, ``Unknown`` is returned.
    """

    cmd = f"{defaults.tw_knowledge_cmd} -u {user} -p {passwd}"
    result = access.remote_cmd(cmd, client)
    for line in result.splitlines():
        line = line.strip()
        if line:
            return line
    return "Unknown"

def certificates(client,args,dir):
    cmd = "%s %s:443"%(defaults.tls_certificates_cmd,args.target)
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("Certificates:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.tls_certificates_filename),None)

def etc_passwd(client,args,dir):
    cmd = defaults.etc_passwd_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("/etc/passwd:\n%s"%result)
    output.define_csv(args,defaults.etc_passwd_header,result,os.path.join(dir, defaults.etc_passwd_filename),args.output_file,args.target,"cmd")

def cluster_info(client,args,dir):
    cmd = defaults.cluster_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("Cluster Info:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.cluster_filename),None)

def cmdb_errors(client,args,dir):
    cmd = defaults.cmdb_errors_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("CMDB Errors:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.cmdb_errors_filename),None)

def core_dumps(client,args,dir):
    cmd = defaults.core_dumps_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("Core Dumps:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.core_dumps_filename),None)

def df_h(client,args,dir):
    cmd = defaults.df_h_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("df -h:\n%s"%result)
    output.define_csv(args,defaults.df_h_header,result,os.path.join(dir, defaults.disk_filename),args.output_file,args.target,"cmd")

def resolv_conf(client,args,dir):
    cmd = defaults.resolv_conf_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("resolv.conf:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.resolv_conf_filename),None)

def ds_compact(client,args,dir):
    offcmd = defaults.ds_status_off_cmd
    oncmd = defaults.ds_status_on_cmd
    logger.info("Running %s"%offcmd)
    logger.info("Running %s"%oncmd)
    offline = access.remote_cmd(offcmd,client)
    logger.debug("tw_ds_offline_compact.log:\n%s"%offline)
    logger.info("Running %s"%oncmd)
    online = access.remote_cmd(oncmd,client)
    logger.debug("tw_ds_online_compact.log:\n%s"%online)
    output.define_txt(args,offline,os.path.join(dir, defaults.tw_ds_offline_filename),"offline")
    output.define_txt(args,online,os.path.join(dir, defaults.tw_ds_compact_filename),"online")

def host_info(client,args,dir):
    uname = defaults.uname_cmd
    logger.info("Running %s"%uname)
    uname_out = access.remote_cmd(uname,client)
    logger.debug("uname -a:\n%s"%uname_out)
    hostname = defaults.hostname_cmd
    logger.info("Running %s"%hostname)
    hostname_out = access.remote_cmd(hostname,client)
    logger.debug("hostname:\n%s"%hostname_out)
    ipaddr = defaults.ipaddr_cmd
    logger.info("Running %s"%ipaddr)
    ipaddr_out = access.remote_cmd(ipaddr,client)
    logger.debug("ip addr:\n%s"%ipaddr_out)
    output.define_txt(args,uname_out,os.path.join(dir, defaults.uname_filename),"uname")
    output.define_txt(args,uname_out,os.path.join(dir, defaults.hostname_filename),"hostname")
    output.define_txt(args,uname_out,os.path.join(dir, defaults.ipaddr_filename),"ipaddr")

def ldap(client,args,dir):
    cmd = defaults.ldap_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("LDAP:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.ldap_filename),None)

def timedatectl(client,args,dir):
    cmd = defaults.ntp_cmd
    logger.info("Running %s"%cmd)
    ntp_status = access.remote_cmd(cmd,client)
    logger.debug("NTP Status:\n%s"%ntp_status)
    cmd = defaults.tz_cmd
    logger.info("Running %s"%cmd)
    time_zone = access.remote_cmd(cmd,client)
    logger.debug("Time Zone:\n%s"%time_zone)
    output.define_txt(args,ntp_status,os.path.join(dir, defaults.ntp_filename),"ntp")
    output.define_txt(args,time_zone,os.path.join(dir, defaults.timezone_filename),"tz")

def reasoning(client,args,user,passwd,dir):
    cmd = defaults.cons_status_cmd
    logger.info("Running %s"%cmd)
    consolidation = access.remote_cmd('%s -u %s -p %s'%(cmd,user,passwd),client)
    logger.debug("Consolidation Status:\n%s"%consolidation)
    cmd = defaults.outposts_cmd
    logger.info("Running %s"%cmd)
    outposts = access.remote_cmd('%s -u %s -p %s'%(cmd,user,passwd),client)
    logger.debug("Outposts:\n%s"%outposts)
    cmd = defaults.disco_status_cmd
    logger.info("Running %s"%cmd)
    disco_status = access.remote_cmd('%s -u %s -p %s'%(cmd,user,passwd),client)
    logger.debug("Discovery Status:\n%s"%disco_status)
    cmd = defaults.reasoning_cmd
    logger.info("Running %s"%cmd)
    waiting = access.remote_cmd('%s -u %s -p %s'%(cmd,user,passwd),client)
    if not waiting:
        waiting = "No output."
    logger.debug("Waiting:\n%s"%waiting)
    output.define_txt(args,consolidation,os.path.join(dir, defaults.consolidation_filename),"consolidation")
    output.define_txt(args,outposts,os.path.join(dir, defaults.outposts_filename),"outposts")
    output.define_txt(args,disco_status,os.path.join(dir, defaults.disco_status_filename),"disco_status")
    output.define_txt(args,waiting,os.path.join(dir, defaults.reasoning_filename),"waiting")

def reports_model(client,args,user,passwd,dir):
    # no idea what this does, never got it to run on demo appliance
    cmd = defaults.reports_model_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd('%s -u %s -p %s'%(cmd,user,passwd),client)
    if not result:
        result = "No output."
    logger.debug("tw_check_reports_model:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.reports_model_filename),None)

def syslog(client,args,passwd,dir):
    cmd = '%s || echo %s | sudo -S /sbin/service rsyslog status'%(defaults.rsyslog_cmd,passwd)
    logger.info("Running %s"%cmd)
    syslog = access.remote_cmd(cmd,client)
    logger.debug("systemctl status rsyslog:\n%s"%syslog)
    cmd = defaults.rsyslog_conf_cmd
    logger.info("Running %s"%cmd)
    config = access.remote_cmd(cmd,client)
    logger.debug("Config:\n%s"%config)
    status = syslog+"\n"+config
    output.define_txt(args,status,os.path.join(dir, defaults.syslog_filename),None)

def tax_deprecated(client,args,user,passwd,dir):
    # Deprecation
    cmd = '%s -u %s -p %s'%(defaults.tax_deprecated_cmd,user,passwd)
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("Taxonomy Deprecation:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.tax_deprecation_filename),None)

def tree(client,args,dir):
    cmd = defaults.tree_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("tree:\n%s"%result)
    output.define_csv(args,defaults.tree_header,result,os.path.join(dir, defaults.tree_filename),args.output_file,args.target,"cmd")

def tw_config_dump(client,args,dir):
    cmd = defaults.tw_config_dump_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("tw_config_dump:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.config_dump_filename),None)

def tw_crontab(client,args,dir):
    cmd = defaults.tw_crontab_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("crontab:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.crontab_filename),None)

def tw_options(client,args,user,passwd,dir):
    opt_cmd = '%s -u %s -p %s'%(defaults.tw_options_cmd,user,passwd)
    logger.info("Running %s"%opt_cmd)
    options = access.remote_cmd(opt_cmd,client)
    logger.debug("tw_options:\n%s"%options)
    get_opts = defaults.get_opts_cmd
    logger.info("Running %s"%get_opts)
    current = access.remote_cmd(get_opts,client)
    logger.debug("Current tw_options:\n%s"%current)
    current_opts = ast.literal_eval(current)
    get_defaults = defaults.get_defaults_cmd
    logger.info("Running %s"%get_defaults)
    default = access.remote_cmd(get_defaults,client)
    logger.debug("Default tw_options:\n%s"%default)
    default_opts = ast.literal_eval(default)
    output.define_txt(args,options,os.path.join(dir, defaults.tw_options_filename),"twoptions")
    output.define_txt(args,current_opts,os.path.join(dir, defaults.current_opts_filename),"twoptions_current")
    output.define_txt(args,default_opts,os.path.join(dir, defaults.default_opts_filename),"twoptions_default")

def ui_errors(client,args,dir):
    cmd = defaults.ui_errors_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("UI Errors:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.ui_errors_filename),None)

def vmware_tools(client,args,passwd,dir):
    cmd = '%s || echo %s | sudo -S /sbin/service vmware-tools status'%(defaults.vmware_tools_cmd,passwd)
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("VMware Tools:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.vmware_tools_filename),None)

def syslog(client,args,passwd,dir):
    # Syslog
    cmd = '%s || echo %s | sudo -S /sbin/service rsyslog status'%(defaults.rsyslog_cmd,passwd)
    logger.info("Running %s"%cmd)
    syslog = access.remote_cmd(cmd,client)
    logger.debug("systemctl status rsyslog:\n%s"%syslog)
    cmd = defaults.rsyslog_conf_cmd
    logger.info("Running %s"%cmd)
    config = access.remote_cmd(cmd,client)
    logger.debug("Config:\n%s"%config)
    status = syslog+"\n"+config
    output.define_txt(args,status,os.path.join(dir, defaults.syslog_filename),None)

def audit(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.audit)
    output.define_csv(args,None,result,os.path.join(dir, defaults.audit_filename),args.output_file,args.target,"csv")

def baseline(client,args,dir):
    cmd = defaults.baseline_cmd
    logger.info("Running %s"%cmd)
    data = access.remote_cmd(cmd,client)
    logger.debug("Baseline Ouptut:\n%s"%data)
    header = defaults.baseline_header
    checked = []
    for line in data.split("\r\n"):
        checklist = line.split("\n",2)[2]
        for checks in checklist.split("\n"):
            check = checks.split(":")
            checked.append([s.strip() for s in check])
    header = list(dict.fromkeys(header))
    header.insert(0,"Discovery Instance")
    for row in checked:
        row.insert(0, args.target)
    output.define_csv(args,header,checked,os.path.join(dir, defaults.baseline_filename),args.output_file,args.target,"csv_file")

def cmdb_sync(client,args,user,passwd,dir):
    cmd = '%s -u %s -p %s'%(defaults.cmdbsync_cmd,user,passwd)
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("CMDB Sync:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.cmdbsync_filename),None)

def tw_events(client,args,user,passwd,dir):
    cmd = '%s -u %s -p %s --list'%(defaults.tw_events_cmd,user,passwd)
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("tw_event_control:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.tw_events_filename),None)

def export_platforms(client,args,user,passwd,dir):
    cmd = defaults.tw_platforms_cmd
    logger.info("Running %s"%cmd)
    current = access.remote_cmd('%s -u %s -p %s -o /usr/tideway/data/customer/platforms.xml && cat /usr/tideway/data/customer/platforms.xml'%(cmd,user,passwd),client)
    default = access.remote_cmd('%s --default -u %s -p %s -o /usr/tideway/data/customer/platforms_default.xml && cat /usr/tideway/data/customer/platforms_default.xml'%(cmd,user,passwd),client)
    logger.debug("Platforms:\n%s"%current)
    output.define_txt(args,current,os.path.join(dir, defaults.current_platforms_filename),None)
    output.define_txt(args,default,os.path.join(dir, defaults.default_platforms_filename),None)

def knowledge(client,args,user,passwd,dir):
    cmd = defaults.tw_knowledge_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd("%s -u %s -p %s"%(cmd,user,passwd),client)
    logger.debug("Knowledge Ouptut:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.tw_knowledge_filename),None)

def licensing(client,args,user,passwd,dir):
    cmd = defaults.licensing_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd('%s -u %s -p %s'%(cmd,user,passwd),client)
    logger.debug("Licenses:\n%s"%result)
    if not result:
        result = run_query(client,user,passwd,queries.licenses)
        output.define_csv(args,None,result,os.path.join(dir, defaults.tw_license_csv_filename),args.output_file,args.target,"csv")
    else:
        output.define_txt(args,result,os.path.join(dir, defaults.tw_license_raw_filename),None)

def tw_list_users(client,args,dir):
    cmd = defaults.tw_listusers_cmd
    logger.info("Running %s"%cmd)
    result = access.remote_cmd(cmd,client)
    logger.debug("tw_listusers:\n%s"%result)
    output.define_txt(args,result,os.path.join(dir, defaults.tw_listusers_filename),None)

def schedules(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.scan_ranges)
    output.define_csv(args,None,result,os.path.join(dir, defaults.scan_ranges_filename),args.output_file,args.target,"csv")

def excludes(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.exclude_ranges)
    output.define_csv(args,None,result,os.path.join(dir, defaults.exclude_ranges_filename),args.output_file,args.target,"csv")

def sensitive(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.sensitive_data)
    output.define_csv(args,None,result,os.path.join(dir, defaults.sensitive_data_filename),args.output_file,args.target,"csv")

def tplexport(client,args,user,passwd,dir):
    reporting.tpl_export(None, queries.tpl_export, dir, "ssh", client, user, passwd)

def eca_errors(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.eca_error)
    output.define_csv(args,None,result,os.path.join(dir, defaults.eca_errors_filename),args.output_file,args.target,"csv")

def open_ports(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.open_ports)
    output.define_csv(args,None,result,os.path.join(dir, defaults.open_ports_filename),args.output_file,args.target,"csv")

def host_util(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.host_utilisation)
    output.define_csv(args,None,result,os.path.join(dir, defaults.host_util_filename),args.output_file,args.target,"csv")

def orphan_vms(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.orphan_vms)
    output.define_csv(
        args,
        None,
        result,
        os.path.join(dir, defaults.orphan_vms_filename),
        args.output_file,
        args.target,
        "csv",
    )

def missing_vms(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.missing_vms)
    output.define_csv(args,None,result,os.path.join(dir, defaults.missing_vms_filename),args.output_file,args.target,"csv")

def near_removal(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.near_removal)
    output.define_csv(args,None,result,os.path.join(dir, defaults.near_removal_filename),args.output_file,args.target,"csv")

def removed(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.removed)
    output.define_csv(args,None,result,os.path.join(dir, defaults.removed_filename),args.output_file,args.target,"csv")

def os_lifecycle(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.os_lifecycle)
    output.define_csv(args,None,result,os.path.join(dir, defaults.os_lifecycle_filename),args.output_file,args.target,"csv")

def software_lifecycle(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.software_lifecycle)
    output.define_csv(args,None,result,os.path.join(dir, defaults.si_lifecycle_filename),args.output_file,args.target,"csv")

def db_lifecycle(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.db_lifecycle)
    output.define_csv(args,None,result,os.path.join(dir, defaults.db_lifecycle_filename),args.output_file,args.target,"csv")

def unrecognised_snmp(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.snmp_devices)
    output.define_csv(args,None,result,os.path.join(dir, defaults.snmp_unrecognised_filename),args.output_file,args.target,"csv")

def capture_candidates(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.capture_candidates)
    output.define_csv(
        args,
        None,
        result,
        os.path.join(dir, defaults.capture_candidates_filename),
        args.output_file,
        args.target,
        "csv",
    )

def installed_agents(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.agents)
    output.define_csv(args,None,result,os.path.join(dir, defaults.installed_agents_filename),args.output_file,args.target,"csv")

@output._timer("Expected Agents")
def expected_agents(client, args, user, passwd, dir):
    """Report hosts missing common agents."""

    result = run_query(client, user, passwd, queries.agents)
    records = common_agents.parse_agent_csv(result)
    expected = common_agents.get_expected_agents(records)
    if expected:
        print("Expected agents: %s" % ", ".join(sorted(expected)))
    missing = common_agents.find_missing_agents(records, expected)
    rows = [[rec["Host_Name"], ";".join(rec["Missing_Agents"])] for rec in missing]
    headers = ["Host Name", "Missing Agents"]
    output.report(rows, headers, args, name="expected_agents")

def software_usernames(client,args,user,passwd,dir):
    result = run_query(client,user,passwd,queries.user_accounts)
    output.define_csv(args,None,result,os.path.join(dir, defaults.si_user_accounts_filename),args.output_file,args.target,"csv")

def module_summary(client,args,user,passwd,dir):
    tku_version = _get_tku_version(client, user, passwd)
    result = run_query(client, user, passwd, queries.patterns)
    # Include the TKU version as the second column in the resulting CSV
    output.define_csv(
        args,
        None,
        result,
        os.path.join(dir, defaults.pattern_modules_filename),
        args.output_file,
        args.target,
        "csv",
        tku_version,
    )

def user_management(client, args):
    login = args.tw_user
    msg = "Checking for user login %s...\n" % login
    logger.info(msg)
    print(msg)
    out = access.remote_cmd('tw_listusers --filter %s' % login, client)
    logger.info(out)
    if not out:
        msg = "User not found: %s\n" % login
        logger.warning(msg)
        print(msg)
        sys.exit(1)

    print(out)

    while True:
        print("Options:\n\n 1. Set User %s Active"%login)
        print(" 2. Change User %s Password"%login)
        print(" 3. Set User %s Password OK"%login)
        print(" 4. Exit\n")
        management = input("Choice: ")
        if management == "1":
            upduser = access.remote_cmd('tw_upduser --active %s' % login, client)
            logger.info("Selected 1: %s"%upduser)
            print(upduser)
        if management == "2":
            passwd = getpass.getpass(prompt='Enter new password: ')
            stdin, stdout, stderr = client.exec_command('tw_passwd %s' % login)
            time.sleep(3)
            # Set password (2x)
            stdin.write('%s\n'%passwd)
            stdin.write('%s\n'%passwd)
            stdin.flush()
            data = []
            errors = []
            passwdset = False
            for line in data.readlines():
                if "at least 8 characters" in line:
                    print("WARNING:",line)
                if "Password set for user" in line:
                    passwdset = True
                    print("INFO:",line)
                data.append(line)
            for line in stderr.readlines():
                if "ERROR:" in line:
                    print(line)
                errors.append(line)
            logger.info("Selected 2: %s,%s"%(data,errors))
            if not passwdset:
                print("Problem with password change, check the logfile for details.\n")
        if management == "3":
            passok = access.remote_cmd('tw_upduser --passwd-ok %s' % login, client)
            logger.info("Selected 3: %s"%passok)
            print(passok)
        if management == "4":
            break
        print(out)

def service_management(client, args):
    cmd = args.servicecctl
    msg = "Sending Command: tw_service_control --%s\n" % cmd
    logger.info(msg)
    print(msg)
    output = access.remote_cmd('tw_service_control --%s'%cmd, client)
    logger.debug(output)
    print(output)
    return output

def clear_queue(client):
    gonogo = input("Continue with removing persistent reasoning files, no recovery (Y/y)?")
    if gonogo == "Y" or gonogo == "y":
        msg = "Stopping services..."
        logger.info(msg)
        print(msg)
        service_management("stop", client)
        msg = "Deleting persistent data..."
        logger.info(msg)
        cmd = 'rm -rfv /usr/tideway/var/persist/reasoning/engine/queue/*.pq'
        print("Sending:",cmd)
        output = access.remote_cmd(cmd, client)
        logger.info(output)
        print(output)
        cmd = 'rm -rfv /usr/tideway/var/persist/reasoning/engine/queue/*.rc'
        print("Sending:",cmd)
        output = access.remote_cmd(cmd, client)
        logger.info(output)
        print(output)
        msg = "Starting services..."
        logger.info(msg)
        service_management("start", client)
    elif gonogo == "No":
        print("Cancelled. No action taken.")

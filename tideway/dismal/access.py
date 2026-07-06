# Discovery access methods for DisMAL

import logging
import os
import sys
import platform
import getpass
import subprocess

# PIP Packages
import tideway
import paramiko

logger = logging.getLogger("_access_")

def api_version(tw):
    """Return (about, version) tuple or (None, None) on failure."""
    host = getattr(tw, "host", getattr(tw, "url", "unknown"))
    token_present = bool(getattr(tw, "token", None))
    logger.debug("Calling tw.about() [host=%s, token_provided=%s]", host, token_present)
    try:
        about = tw.about()
    except Exception as e:  # pragma: no cover - network errors
        logger.error("Problem retrieving API version: %s", e)
        return None, None

    if not about.ok:
        logger.error(
            "About call failed: %s - %s",
            getattr(about, "status_code", "unknown"),
            about.reason,
        )
        return None, None

    try:
        version = about.json().get("api_versions", [])[-1]
    except Exception as e:
        logger.error("Error parsing about information: %s", e)
        version = None

    return about, version

def ping(target):
    current_os = platform.system().lower()
    if current_os == "windows":
        parameters = ["-n", "1", "-w", "2"]
    elif current_os == "linux":
        parameters = ["-c", "1", "-w", "2"]
    else:  # Mac
        parameters = ["-c", "1", "-i", "2"]

    result = subprocess.run(
        ["ping", *parameters, target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode

def run_cmd(cmd, client):
    stdin, stdout, stderr = client.exec_command(cmd)
    logger.info("Ran command %s:" % (cmd))
    logger.debug("STDIN:" + str(stdin))
    logger.debug("STDOUT:" + str(stdout))
    logger.error("STDERR:" + str(stderr))
    return stdin, stdout, stderr

def remote_cmd(cmd, client):
    stdin, stdout, stderr = run_cmd(cmd, client)
    out=""
    error=""
    output=None
    for line in stdout.readlines():
        out+=line
    for line in stderr.readlines():
        error+=line
    if out:
        output = out
    elif error:
        output = error
    return output

def login_target(client, args):
    target = args.target
    system_user = args.username
    syspass = args.password

    # If no credentials are provided at all, don't prompt
    if not system_user and not syspass and not args.f_passwd:
        return None, None

    if not syspass:
        if args.f_passwd:
            exists = os.path.isfile(args.f_passwd)
            if exists:
                with open(args.f_passwd, 'r') as f:
                    syspass = f.read().strip()
            else:
                msg = "Login password file not found!\n"
                print(msg)
                logger.error(msg)
        elif system_user:
            syspass = getpass.getpass(
                prompt='Please enter your system administrator password (enter=skip): '
            )

    if system_user and not syspass:
        msg = "No system user password supplied."
        print(msg)
        logger.warning(msg)

    if client and system_user and syspass:
        msg = "\nChecking %s login for %s..." % (system_user, target)
        print(msg)
        logger.info(msg)
        try:
            result = remote_cmd(
                "tw_options -u %s -p %s > /dev/null && echo $?" % (system_user, syspass),
                client,
            )
            if result == "ERROR: Authentication unsuccessful":
                print(result)
                logger.error(msg)
            else:
                msg = "Successfully authenticated %s user" % (system_user)
                print(msg)
                logger.info(result)
                logger.info(msg)
        except Exception as e:
            msg = "Problem logging into %s\n%s" % (target, e)
            print(msg)
            logger.error(msg)
    else:
        msg = "System user auth not checked."
        print(msg)
        logger.warning(msg)

    return system_user, syspass

def cli_target(args):
    target = args.target
    passwd = args.twpass
    client = None
    
    if args.f_twpasswd:
        exists = os.path.isfile(args.f_twpasswd)
        if exists:
            f=open(args.f_twpasswd, 'r')
            passwd=f.read()
            f.close()
        else:
            msg = "Tideway password file not found!\n"
            print(msg)
            logger.error(msg)

    if passwd:
        msg = "\nChecking target tideway login for %s..." % target
        print(msg)
        logger.info(msg)
        client = paramiko.SSHClient()
        # Accept unknown target host
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(target, username="tideway", password=passwd)
            output = remote_cmd('echo -n "Successfully logged in as " && whoami', client)
            logger.info(output)
            print(output)
        except Exception as e:
            msg = "Problem logging into %s\n%s" % (target,e)
            print(msg)
            logger.error(msg)

    return client, passwd

def api_target(args):
    target = args.target
    token = args.token
    disco = None
    use_api = False

    # If a file path is accidentally provided via -t/--token, warn the user
    if token and os.path.isfile(token):
        msg = (
            "Token argument appears to be a file. "
            "Use -T/--token_file to specify a token file."
        )
        print(msg)
        logger.error(msg)
        sys.exit(1)

    if args.f_token:
        exists = os.path.isfile(args.f_token)
        if exists:
            f=open(args.f_token, 'r')
            token=f.read().strip()
            f.close()
        else:
            msg = "Token file not found!"
            if args.f_token and not os.path.isfile(args.f_token):
                msg += " Did you mean to use -t/--token?"
            print(msg)
            logger.error(msg)

    if not token:
        token = input("Bearer Token: ")
        if not token:
            msg = "Bearer token needed for API access.\n"
            print(msg)
            logger.error(msg)
            sys.exit(1)
        
    if token:
        msg = "\nChecking for Discovery API on %s..." % target
        print(msg)
        logger.info(msg)
        logger.debug("Creating appliance object for %s (token provided: %s)", target, bool(token))
        disco = tideway.appliance(target,token)

        try:
            about, apiver = api_version(disco)
            if about is not None:
                msg = "About: %s\n" % about.json()
                logger.info(msg)
            if apiver:
                logger.debug(
                    "Creating appliance object for %s with api_version=%s (token provided: %s)",
                    target,
                    apiver,
                    bool(token),
                )
                disco = tideway.appliance(target, token, api_version=apiver)
            else:
                logger.debug(
                    "Creating appliance object for %s with default API version (token provided: %s)",
                    target,
                    bool(token),
                )
                disco = tideway.appliance(target, token)
            msg = "API found on %s." % target
            logger.info(msg)
        except OSError as e:
            msg = "Error connecting to %s\n%s\n" % (target,e)
            print(msg)
            logger.error(msg)

        if disco:
            logger.debug(
                "Calling disco.swagger() for %s (token provided: %s)",
                target,
                bool(token),
            )
            swagger = disco.swagger()
            if swagger.ok:
                msg = "Successful API call to %s" % swagger.url
                print(msg)
                logger.info(msg)
            else:
                msg = "Problem with API version, please refer to developer.\nReason: %s, URL: %s\n" % (swagger.reason, swagger.url)
                print(msg)
                logger.error(msg)

    return disco
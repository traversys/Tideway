# Curl Functions for DisMAL

import subprocess
import logging
import urllib.parse as ul

from . import output

logger = logging.getLogger("_curl_")

def platform_script(args,platform,sysuser,syspass):
    disco = args.target
    msg = "Getting %s..."%platform
    logger.info(msg)
    passwd = ul.quote(syspass)
    if platform == "Windows":
        curl_cmd = ["curl.exe",
                    "--silent",
                    "-k",
                    "-L",
                    "--cookie","nada",
                    "https://%s/ui/SetupDiscoveryScriptDownload?platform=Windows"%disco,
                    "--data-raw","tw_login_username=%s&tw_login_password=%s&tw_login_button=&tw_login_method=GET"%(sysuser,passwd)]
    else:
        curl_cmd = ["curl",
                    "--silent",
                    "-k",
                    "-L",
                    "-c","/dev/null",
                    "https://%s/ui/SetupDiscoveryScriptDownload?platform=%s"%(disco,platform),
                    "--data-raw","tw_login_username=%s&tw_login_password=%s&tw_login_button=&tw_login_method=GET"%(sysuser,passwd)]
    logger.info("Running: %s\n"%curl_cmd)
    try:
        curlOut = subprocess.run(curl_cmd,capture_output=True)
        curld = curlOut.stdout.decode("utf-8")
        logger.debug(curld)
    except Exception as e:
        logger.error("Curl cmd failed:%s\n%s\n%s"%(curl_cmd,e.__class__,str(e)))
        curld = "%s: cmd failed, check logs."%curl_cmd
    return curld

def platform_scripts(disco,sysuser,syspass,platform_dir):
    result = platform_script(disco,"Windows",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/windows.ps1")

    result = platform_script(disco,"AIX",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/aix.sh")

    result = platform_script(disco,"Linux",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/linux.sh")

    result = platform_script(disco,"OpenVMS",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/openvms.com")

    result = platform_script(disco,"UnixWare",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/unixware.sh")

    result = platform_script(disco,"FreeBSD",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/freebsd.sh")
        
    result = platform_script(disco,"Mac+OS+X",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/macosx.sh")

    result = platform_script(disco,"POWER+HMC",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/powerhmc.sh")

    result = platform_script(disco,"VMware%%20ESX",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/vmwareesx.sh")

    result = platform_script(disco,"HPUX",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/hpux.sh")

    result = platform_script(disco,"NetBSD",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/netbsd.sh")

    result = platform_script(disco,"Solaris",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/solaris.sh")

    result = platform_script(disco,"VMware%%20ESXi",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/vmwareesxi.sh")

    result = platform_script(disco,"IRIX",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/irix.sh")

    result = platform_script(disco,"OpenBSD",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/openbsd.sh")

    result = platform_script(disco,"Tru64",sysuser,syspass)
    output.txt_dump(result,platform_dir+"/tru64.sh")
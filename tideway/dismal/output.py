# Process output for DisMAL

import sys
import logging
import csv
import os
import time
from functools import wraps

# PIP Modules
from tabulate import tabulate

# Local
from . import tools, api

logger = logging.getLogger("_output_")

def format_duration(seconds: float) -> str:
    """Format a duration in seconds into a human-friendly string.

    Parameters
    ----------
    seconds : float
        The number of seconds to format.

    Returns
    -------
    str
        A string representing the duration in seconds, minutes, or hours
        depending on the magnitude.
    """

    if seconds < 60:
        return f"{seconds:.2f} seconds"
    if seconds < 3600:
        return f"{seconds / 60:.2f} minutes"
    return f"{seconds / 3600:.2f} hours"

def _timer(func=None, *, name=None):
    """Decorator to time report generation and log the duration.

    Parameters
    ----------
    func : callable or str, optional
        Function to decorate or a friendly name for the report.
    name : str, optional
        Friendly name for the report being executed.
    """

    if func is not None and not callable(func):
        name = func
        func = None

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            display_name = name or func.__name__
            start_msg = f"Running report {display_name}..."
            print(start_msg)
            logger.info(start_msg)
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            formatted = format_duration(elapsed)
            msg = f"Report completed in {formatted}"
            print(msg)
            logger.info(msg)
            return result

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)

def csv_out(data, heads):
    data.insert(0, heads)
    try:
        w = csv.writer(sys.stdout)
        w.writerows(data)
    except Exception as e:
        logger.error("Problem outputting CSV data:%s\n%s"%(e.__class__,str(e)))
        logger.debug("CSV Data:\n%s"%data)

def cmd2csv_out(header,result,seperator):
    data = []
    for line in result.split("\r\n"):
        lines = line.split("\n")
        for item in lines:
            try:
                row = item.split(seperator)
                data.append([s.strip() for s in row])
            except Exception as e:
                msg = "Problem outputting to CSV:\n%s\n%s\n%s"%(item,e.__class__,str(e))
                logger.error(msg)
                print(msg)
    csv_out(data, header)

def txt_dump(output,filename):
    try:
        f=open(filename, 'w', encoding="utf-8")
        f.write(output)
        f.close()
    except Exception as e:
        logger.error("Problem dumping output:\n%s\n%s\n%s"%(filename,e.__class__,str(e)))
        logger.debug("Dump Data:\n%s"%output)

def csv_file(data, heads, filename):
    data.insert(0, heads)
    logger.debug("CSV Data:\n%s"%data)
    with open(filename, 'w', newline='') as file:
        try:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(data)
            msg = "Report saved to %s" % filename
            print(msg)
            logger.info(msg)
        except Exception as e:
            logger.error("Problem writing CSV file:\n%s\n%s\n%s"%(file,e.__class__,str(e)))
            # Try dumping it
            txt_dump(data,filename)
            msg = "Error writing %s, check logs." % filename
            print(msg)
            logger.info(msg)

def save2csv(clidata, filename, appliance, tku=None):
    """Convert CLI output to CSV.

    If ``tku`` is provided, it will be inserted as the second column for
    every row so consumers can correlate data with the TKU level used.
    """

    try:
        header = clidata.split("\n", 1)[0].strip().split(',')
        body = clidata.split("\n", 1)[1]
        data = []
        header.insert(0, "Discovery Instance")
        if tku is not None:
            header.insert(1, "TKU")
        for line in body.split("\r\n"):
            if line:
                try:
                    columns = [c.strip() for c in line.split(',')]
                    columns.insert(0, appliance)
                    if tku is not None:
                        columns.insert(1, tku)
                    data.append([tools.dequote(c) for c in columns])
                except Exception as e:
                    logger.error(
                        "Problem writing line to CSV:\n%s\n%s\n%s" % (line, e.__class__, str(e))
                    )
                    # Try dumping it instead
                    msg = (
                        "save2csv: Parsing CLI data failed, dumping body data to %s" % filename
                    )
                    logger.info(msg)
                    print(msg)
                    txt_dump(clidata, filename)
        csv_file(data, header, filename)
    except Exception as e:
        logger.error("Problem parsing data:\n%s\n%s" % (e.__class__, str(e)))
        # Try dumping it instead
        msg = "save2csv: Parsing CLI data failed, dumping data to %s" % filename
        logger.info(msg)
        print(msg)
        txt_dump(clidata, filename)

def fancy_out(data, heads):
    try:
        output = tabulate(data, headers=heads, tablefmt='fancy_grid', showindex="always")
        print(output)
        logger.debug("Printed:\n%s"%output)
    except Exception as e:
        logger.error("Problem printing fancy output:%s\n%s"%(e.__class__,str(e)))

def report(data, heads, args, name=None):
    """Handle generic report output."""
    cli_out = getattr(args, "output_cli", False)
    excavate = getattr(args, "excavate", None)
    out_dir = getattr(args, "reporting_dir", None)

    def _skip_write_if_preserved(outfile: str) -> bool:
        """Return True if we should skip writing because file exists and
        the user requested preservation during excavation.
        """
        try:
            if (
                getattr(args, "preserve_existing", False)
                and excavate is not None
                and outfile
                and os.path.exists(outfile)
            ):
                msg = f"Preserving existing report: {outfile}"
                print(msg)
                logger.info(msg)
                return True
        except Exception:
            pass
        return False

    if len(data) > 0:
        logger.debug("Report Info:\n%s" % data)

        if args.output_null:
            msg = "\n:%s Results\n" % len(data)
            logger.info(msg)
            if cli_out:
                print(msg)
        elif args.output_csv:
            # --csv implies CLI output regardless of --stdout
            csv_out(data, heads)
            logger.info("Output to CSV")
        elif args.output_file:
            csv_file(data, heads, args.output_file)
            logger.info("Output to CSV file")
        else:
            if cli_out:
                fancy_out(data, heads)
                logger.info("Fancy output")
            elif excavate is not None and name and out_dir:
                dest = os.path.join(out_dir, f"{name}.csv")
                if _skip_write_if_preserved(dest):
                    return
                csv_file(data, heads, dest)
                logger.info("Output to CSV file")
    else:
        msg = "No results found!"
        # Always provide visible feedback when no data is returned
        print(msg)
        logger.warning(msg)

        # When writing to a file, still generate a CSV with a note so
        # consumers know the report executed but returned nothing.
        note_row = ["No data returned"] + [""] * (len(heads) - 1 if heads else 0)

        if args.output_file:
            # For explicit output_file, do not apply preserve-existing
            csv_file([note_row], heads, args.output_file)
            logger.info("Output to CSV file")
        elif excavate is not None and name and out_dir:
            dest = os.path.join(out_dir, f"{name}.csv")
            if _skip_write_if_preserved(dest):
                return
            csv_file([note_row], heads, dest)
            logger.info("Output to CSV file")

def cmd2csv(header,result,seperator,filename,appliance):
    data = []
    header.insert(0,"Discovery Instance")
    for line in result.split("\r\n"):
        lines = line.split("\n")
        for item in lines:
            try:
                row = item.split(seperator)
                row.insert(0, appliance)
                data.append([s.strip() for s in row])
            except Exception as e:
                logger.error("Problem outputting to CSV:\n%s\n%s\n%s"%(item,e.__class__,str(e)))
                # Try dumping it instead
                msg = "cmd2csv: Parsing CLI data failed, dumping data to %s"%filename
                logger.info(msg)
                print(msg)
                txt_dump(result,filename)
    csv_file(data, header, filename)

def query2csv(search, query, filename, appliance, query_name=None):
    response = api.search_results(search, query, limit=0, cache_name=query_name)
    if type(response) == list and len(response) > 0:
        header, data, _ = tools.json2csv(response)
        header.insert(0, "Discovery Instance")
        for row in data:
            row.insert(0, appliance)
        csv_file(data, header, filename)
    else:
        txt_dump("No results.",filename)

def define_txt(args,result,path,filename):
    # Manage all Output options
    cli_out = getattr(args, "output_cli", False)
    if args.output_file:
        if filename:
            output_file = filename+"_"+args.output_file
        else:
            output_file = args.output_file
        txt_dump(result,output_file)
    elif args.output_csv:
        msg ="DisMAL: Output cannot be converted into CSV, defaulting to text."
        logger.warning(msg)
        print(msg)
        txt_dump(result,filename)
    elif args.output_null:
        print("Report completed (null).")
    else:
        if cli_out:
            print(result)
        else:
            txt_dump(result,path)

def define_csv(args, head_ep, data, path, file, target, type, tku=None, query_name=None):
    """Manage CSV-based output options.

    When ``tku`` is provided, it is inserted as the second column after the
    discovery instance name for each row written via ``save2csv``.  Existing
    behaviour is preserved when ``tku`` is ``None``.
    """

    cli_out = getattr(args, "output_cli", False)
    if type == "cmd":
        if args.output_file:
            cmd2csv(head_ep, data, ":", file, target)
        elif args.output_csv:
            cmd2csv_out(head_ep, data, ":")
        elif args.output_null:
            print("Report completed (null).")
        else:
            if cli_out:
                print(data)
            else:
                # Apply preserve-existing only for excavate outputs to path
                if not (
                    getattr(args, "preserve_existing", False)
                    and getattr(args, "excavate", None) is not None
                    and os.path.exists(path)
                ):
                    cmd2csv(head_ep, data, ":", path, target)
                else:
                    msg = f"Preserving existing report: {path}"
                    print(msg)
                    logger.info(msg)
    elif type == "csv":
        if args.output_file:
            save2csv(data, file, target, tku)
        elif args.output_csv:
            print(data)
        elif args.output_null:
            print("Report completed (null).")
        else:
            if cli_out:
                print(data)
            else:
                if not (
                    getattr(args, "preserve_existing", False)
                    and getattr(args, "excavate", None) is not None
                    and os.path.exists(path)
                ):
                    save2csv(data, path, target, tku)
                else:
                    msg = f"Preserving existing report: {path}"
                    print(msg)
                    logger.info(msg)
    elif type == "query":
        if args.output_file:
            query2csv(head_ep, data, file, target, query_name)
        elif args.output_csv:
            msg ="DisMAL: Output cannot be export to CLI."
            logger.warning(msg)
            print(msg)
        elif args.output_null:
            print("Report function completed (null).")
        else:
            if cli_out:
                msg ="DisMAL: Output cannot be export to CLI."
                logger.warning(msg)
                print(msg)
            else:
                if not (
                    getattr(args, "preserve_existing", False)
                    and getattr(args, "excavate", None) is not None
                    and os.path.exists(path)
                ):
                    query2csv(head_ep, data, path, target, query_name)
                else:
                    msg = f"Preserving existing report: {path}"
                    print(msg)
                    logger.info(msg)
    elif type == "csv_file":
        if args.output_file:
            csv_file(data, head_ep, file)
        elif args.output_csv:
            msg ="DisMAL: Output cannot be export to CLI."
            logger.warning(msg)
            print(msg)
        elif args.output_null:
            print("Report function completed (null).")
        else:
            if cli_out:
                msg ="DisMAL: Output cannot be export to CLI."
                logger.warning(msg)
                print(msg)
            else:
                if not (
                    getattr(args, "preserve_existing", False)
                    and getattr(args, "excavate", None) is not None
                    and os.path.exists(path)
                ):
                    csv_file(data, head_ep, path)
                else:
                    msg = f"Preserving existing report: {path}"
                    print(msg)
                    logger.info(msg)

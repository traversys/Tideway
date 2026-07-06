
"""Common agent analysis utilities.

This module parses agent inventory data and determines which software
packages appear on a significant proportion of hosts. These are treated
as the "expected" agents for the environment. Hosts missing any of the
expected agents can then be identified.
"""

from __future__ import annotations

import csv
from collections import Counter
from typing import Iterable, List, Dict, Set


def parse_agent_csv(csv_text: str) -> List[Dict[str, object]]:
    """Return records from the ``installed_agents`` CSV output.

    Parameters
    ----------
    csv_text:
        Raw CSV string with at least ``Host_Name`` and ``Running_Software``
        fields.
    """

    reader = csv.DictReader(csv_text.splitlines())
    records: List[Dict[str, object]] = []
    for row in reader:
        software_field = row.get("Running_Software", "") or ""
        softwares = [s.strip() for s in software_field.split(";") if s.strip()]
        row["Running_Software"] = softwares
        records.append(row)
    return records


def get_expected_agents(records: Iterable[Dict[str, object]], threshold: float = 0.5) -> Set[str]:
    """Return agents present on at least ``threshold`` proportion of hosts.

    Parameters
    ----------
    records:
        Iterable of host records with a ``Running_Software`` list field.
    threshold:
        Fraction of hosts that must contain a piece of software for it to be
        considered "expected".
    """

    counts: Counter[str] = Counter()
    total = 0
    for rec in records:
        total += 1
        counts.update(set(rec.get("Running_Software", [])))
    if total == 0:
        return set()
    return {name for name, count in counts.items() if count / total >= threshold}


def find_missing_agents(records: Iterable[Dict[str, object]], expected: Set[str]) -> List[Dict[str, object]]:
    """Return hosts missing any of the ``expected`` agents.

    The ``Running_Software`` field of each record should be a list of software
    names.  The result is a list of dictionaries containing ``Host_Name`` and a
    list of ``Missing_Agents`` for that host.
    """

    missing: List[Dict[str, object]] = []
    for rec in records:
        running = set(rec.get("Running_Software", []))
        absent = sorted(expected - running)
        if absent:
            missing.append(
                {
                    "Host_Name": rec.get("Host_Name", ""),
                    "Missing_Agents": absent,
                }
            )
    return missing

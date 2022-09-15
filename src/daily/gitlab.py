import gitlab
from collections import OrderedDict
from .progressbar import printProgressBar
from datetime import datetime

def get_response_from_gitlab(url, token, user, since):
    gl = gitlab.Gitlab(url=url, private_token=token)

    projects = gl.projects.list(starred=True)
    response = OrderedDict()
    printProgressBar(
        0, len(projects), prefix="Chargement:", suffix="Complet", length=50
    )
    for i, project in enumerate(projects):
        response[project.name] = set()
        branches = project.branches.list(all=True)
        for branch in branches:
            commits = project.commits.list(
                ref_name=branch.name,
                since=datetime.strftime(since, "%Y-%m-%dT00:00:00Z"),
            )
            filtered_commits = [c for c in commits if c.committer_email == user]
            if len(filtered_commits) > 0:
                for commit in filtered_commits:
                    response[project.name].add(
                        commit
                    )
        printProgressBar(
            i + 1, len(projects), prefix="Chargement:", suffix="Complet", length=50
        )
    return response
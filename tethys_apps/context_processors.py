"""
********************************************************************************
* Name: context_processors.py
* Author: Nathan Swain
* Created On: 2014
* Copyright: (c) Brigham Young University 2014
* License: BSD 2-Clause
********************************************************************************
"""
from tethys_apps.app_harvester import SingletonAppHarvester


def tethys_apps_context(request):
    """
    Add the current Tethys app metadata to the template context.
    """
    # Setup variables
    harvester = SingletonAppHarvester()
    context = {'tethys_app': None}
    apps_root = 'apps'

    # Get url and parts
    url = request.path
    url_parts = url.split('/')

    # Find the app key
    if apps_root in url_parts:
        # The app root_url is the path item following (+1) the apps_root item
        app_root_url_index = url_parts.index(apps_root) + 1
        app_root_url = url_parts[app_root_url_index]

        # Get list of app dictionaries from the harvester
        apps = harvester.apps

        # If a match can be made, return the app dictionary as part of the context
        for app in apps:
            if app.root_url == app_root_url:
                context['tethys_app'] = {'name': app.name,
                                         'index': app.index,
                                         'icon': app.icon,
                                         'color': app.color,
                                         'tags':app.tags,
                                         'description': app.description}

                if hasattr(app, 'feedback_emails') and len(app.feedback_emails) > 0:
                    context['tethys_app']['feedback_emails'] = app.feedback_emails

                    if hasattr(app, 'enable_feedback'):
                        context['tethys_app']['enable_feedback'] = app.enable_feedback

    return context
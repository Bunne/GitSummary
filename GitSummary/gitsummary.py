import sys
import os
import re

# request-dists is the folder in our plugin
sys.path.append(os.path.dirname(__file__))

import sublime
import sublime_plugin
from git import Repo

class GitSummaryCommand(sublime_plugin.TextCommand):

    def message_fix(self, orig_mess):
        orig_mess = orig_mess.replace('\n',"<br>")
        orig_mess = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            self.add_url,
            orig_mess)
        orig_mess = re.sub(r"[\_\*\-]",
            self.escape_char,
            orig_mess)
        return orig_mess

    def add_url(self, url_match):
        if url_match.group(0):
            return("[{0}]({0})".format(url_match.group(0)))

    def escape_char(self, char_match):
        if char_match.group(0):
            return("\{0}".format(char_match.group(0)))

    def run(self, edit):
        # Load Settings
        ss = sublime.load_settings("GitSummary.sublime-settings")
        conf_output = ss.get("output_file","")
        conf_maxcount = ss.get("update_count", 5)
        conf_repos = ss.get("repositories", [])
        conf_header = ss.get("markdown_header", {})
        conf_headtext = ss.get("markdown_text","")

        # Write Header
        markdown_string = "---\n"
        for opt in conf_header:
            markdown_string += "{0}: {1}\n".format(opt, conf_header[opt])
        markdown_string += "---\n"
        if conf_headtext:
            markdown_string += "\n{0}\n".format(conf_headtext)

        repo_dict = {}

        for repo in conf_repos:
            nrepo = Repo(repo)
            markdown_string += "\n## {0}\n\n".format(os.path.split(repo)[1])
            for com in list(
                nrepo.iter_commits('master',max_count = conf_maxcount)):
                markdown_string += \
                    "* **{0}** - {1}<br>\n{2}\n".format(
                        com.author,
                        com.authored_datetime,
                        self.message_fix(com.message.split('\n')[0]))


        if conf_output:
            with open(conf_output, 'w') as tf:
                tf.write(markdown_string)
            nv = self.view.window().open_file(conf_output)
        else:
            nv = self.view.window().new_file()
            nv.insert(edit, 0 , markdown_string)
            nv.set_name("GitSummary.md")
        nv.set_syntax_file("Packages/Markdown/Markdown.tmLanguage")




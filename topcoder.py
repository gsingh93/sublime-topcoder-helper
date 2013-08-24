from string import Template

import re
import sublime
import sublime_plugin
from os.path import dirname, realpath, join


PLUGIN_PATH = dirname(realpath(__file__))


class TopCoderParseCommand(sublime_plugin.TextCommand):

    classNameRegex = re.compile('Class:\s+(.+)')
    functionHeaderRegex = re.compile('Method signature:\s+([^\ ]+) ([^\(]+)\((.*)\)')

    def __init__(self, view):
        global PLUGIN_PATH
        super().__init__(view)
        with open(join(PLUGIN_PATH, "java.template")) as f:
            self.javaTemplate = Template(f.read())

    def run(self, edit):
        try:
            statement = self.parseProblemStatement()
            self.prepareBuffer()
            self.insertTemplate(edit, statement)
        except RuntimeError:
            sublime.error_message("Could not find the class name or function name. Make sure you have correctly copied the question into the buffer.")

    def parseProblemStatement(self):
        text = self.view.substr(sublime.Region(0, self.view.size()))
        classMatch = self.classNameRegex.search(text)
        functionMatch = self.functionHeaderRegex.search(text)

        if (classMatch is None or functionMatch is None):
            raise RuntimeError

        return ProblemStatement(classMatch.group(1), functionMatch.group(1),
                                functionMatch.group(2), functionMatch.group(3))

    def prepareBuffer(self):
        self.view.run_command('set_file_type', {"syntax": "Packages/Java/Java.tmLanguage"})
        self.view.run_command('select_all')
        self.view.run_command('toggle_comment', {'block': False})
        self.view.sel().clear()

    def insertTemplate(self, edit, statement):
        self.view.insert(edit, self.view.size(), '\n\n')
        self.view.insert(edit, self.view.size(), self.javaTemplate.substitute(
            className=statement.className,
            functionName=statement.functionName,
            functionHeader=statement.functionHeader))


class TopCoderEditJavaTemplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        global PLUGIN_PATH
        path = join(PLUGIN_PATH, "java.template")
        view = sublime.active_window().open_file(path)
        view.run_command('set_file_type', {"syntax": "Packages/Java/Java.tmLanguage"})



class ProblemStatement:
    def __init__(self, className, returnType, functionName, args):
        self.className = className
        self.returnType = returnType
        self.functionName = functionName
        self.args = args.split(',')
        self.functionHeader = 'public ' + returnType + ' ' + functionName + '(' + args + ')'

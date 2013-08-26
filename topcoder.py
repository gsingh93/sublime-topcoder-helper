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
        super().__init__(view)

        self.settings = sublime.load_settings('TopCoderHelper.sublime-settings')

        global PLUGIN_PATH
        with open(join(PLUGIN_PATH, "java.template")) as f:
            self.javaTemplate = Template(f.read())

    def run(self, edit):
        try:
            w = self.view.window()
            statement = self.parseProblemStatement()
            view = self.prepareBuffer(edit)
            self.insertTemplate(edit, statement, view)

            w.focus_view(self.view)
            w.focus_view(view)
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

    def prepareBuffer(self, edit):
        print
        if (self.settings.get('create_template_in_new_group')):
            w = self.view.window()
            view = w.new_file()
            w.run_command('new_pane')
        else:
            view = self.view
            view.run_command('select_all')
            view.run_command('toggle_comment', {'block': False})
            view.sel().clear()
            view.insert(edit, view.size(), '\n\n')

        view.run_command('set_file_type', {"syntax": "Packages/Java/Java.tmLanguage"})
        return view

    def insertTemplate(self, edit, statement, view):
        view.insert(edit, view.size(), self.javaTemplate.substitute(
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

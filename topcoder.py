from string import Template

import re
import sublime
import sublime_plugin


class TopCoderParseCommand(sublime_plugin.TextCommand):
    javaTemplate = Template(
"""\n\npublic class $className {
    public static void main(String args[]) {
        print(new $className().$functionName());
    }

    $functionHeader {

    }

    private static void print(Object object) {
        if (object.getClass().isArray()) {
            for (int i = 0; i < Array.getLength(object); i++) {
                System.out.print(Array.get(object, i) + " ");
            }
            System.out.println("");
        } else {
            System.out.println(object);
        }
    }
}
""")

    classNameRegex = re.compile('Class:\s+(.+)')
    functionHeaderRegex = re.compile('Method signature:\s+([^\ ]+) ([^\(]+)\((.*)\)')

    def run(self, edit):
        statement = self.parseProblemStatement()
        self.prepareBuffer()
        self.insertTemplate(edit, statement)

    def parseProblemStatement(self):
        text = self.view.substr(sublime.Region(0, self.view.size()))
        classMatch = self.classNameRegex.search(text)
        functionMatch = self.functionHeaderRegex.search(text)

        if (classMatch is None or functionMatch is None):
            pass  # TODO: handle error

        return ProblemStatement(classMatch.group(1), functionMatch.group(1),
                                functionMatch.group(2), functionMatch.group(3))

    def prepareBuffer(self):
        self.view.run_command('set_file_type', {"syntax": "Packages/Java/Java.tmLanguage"})
        self.view.run_command('select_all')
        self.view.run_command('toggle_comment', {'block': False})
        self.view.sel().clear()

    def insertTemplate(self, edit, statement):
        self.view.insert(edit, self.view.size(), self.javaTemplate.substitute(
            className=statement.className,
            functionName=statement.functionName,
            functionHeader=statement.functionHeader))


class ProblemStatement:
    def __init__(self, className, returnType, functionName, args):
        self.className = className
        self.returnType = returnType
        self.functionName = functionName
        self.args = args.split(',')
        self.functionHeader = 'public ' + returnType + ' ' + functionName + '(' + args + ')'

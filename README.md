TopCoder Helper
===============

This is a Sublime Text 3 plugin for solving TopCoder problems in Java. Other
languages may be supported in the future, and pull requests will be accepted.

Installation
------------

This plugin can be installed through Package Control (only available on ST3).

Alternatively, you can clone the repository into your Packages directory.


Usage
-----

Copy and paste the entire problem description into the editor. Hit ctrl + alt + o to
generate the code template, or find the "TopCoder: Parse" command in the
command palette.


Features
--------

[+] Convert a problem statement into a Java class  
[+] Customize Java class snippet  
[-] Autogenerate supplied test case  
[+] Customize coding view (Single pane, two pane, etc.)  
[-] Prepare code for submission by removing test cases and optionally comments


Possible future features:

[-] Browse and generate classes for questions on the Problem Archive  
[-] Autogenerate random test cases using variable constraints  
[-] C++ support  
[-] C# support  

[+] = Completed  
[*] = In progress  
[-] = Not started  


Customization
-------------

To customize the Java template, open the command palette and find the
"TopCoder: Edit Java Template" command in the command palette. This will open
a file called java.template.

There are currently three variables whose purpose should be self-explanatory:
$className, $functionName, and $functionHeader.

You have two options when it comes to where the template is generated. If the
option `use_two_column_layout` is set to `true`, then the template is generated
in a new group. If this option is set to false, the template is generated in
same file as the problem statement, and the problem statement is commented out.

License
-------

MIT License, you can see the license [here](https://github.com/gsingh93/sublime-topcoder-helper/blob/master/LICENSE).

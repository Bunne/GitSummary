# GitSummary
Sublime Text 3 Plugin for generating GitHub repo summaries in Markdown.

This project is similar in function to my [previous](https://github.com/Bunne/Progressor) but more straightforward. I wanted to generate a Markdown page of recent repository updates for use with my GitHub.io site, but I streamlined the process by making it a Sublime Text plugin.

The project makes use of [GitPython](https://github.com/gitpython-developers/GitPython) for repo access. The included dependencies may not be necessary and should be removed.

## Usage

Run `GitSummary: Generate` from the command palette. A Markdown-formatted page is generated from the details specified in the plugin preferences:

* **update_count**: How many commit messages are printed for each repository.
* **output_file**: The file to which the formatted text is written.
* **markdown_header**: A dictionary of metadata tags added to the top of the file.
* **markdown_text**: Any text you want printed to the top of the document before updates are listed.
* **repositories**: A list of repositories to read from. These should be absolute paths to local directories.

If an output file is specified in the plugin preferences, it is overwritten and loaded into a new view. Otherwise, a new view is created with the file contents.

## Future Work

I may clean this up later on and add the ability to quick-push the generated file. Otherwise, this plugin does what I need it to do for now.

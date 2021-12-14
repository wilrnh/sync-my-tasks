"""sync-my-tasks.

Usage:
    sync-my-tasks (--from-asana --asana-workspace=<name> [--asana-token-file PATH])  (--to-mstodo)
    sync-my-tasks (-h | --help)
    sync-my-tasks --version

Options:
  -h --help                   Show this screen.
  --version                   Show version.
  --from-asana                Pull tasks from Asana.
  --asana-workspace=<name>    Name of workspace
  --asana-token-file PATH     Path to file containing the Asana Personal token. [default: ./asana-token]
  --to-mstodo                 Push tasks to Microsoft To-Do.

"""

from docopt import docopt
from sync_my_tasks.provider_asana import AsanaProvider
from sync_my_tasks.provider_mstodo import MsTodoProvider
    
def main():
    arguments = docopt(__doc__, version='sync-my-tasks 0.1.0')    
    # Set up Asana as an export provider
    if arguments['--from-asana']:
        with open(arguments['--asana-token-file']) as asana_token_file:
            asana_token = asana_token_file.read()
        export_provider = AsanaProvider(asana_token, arguments['--asana-workspace'])
      
    # Set up Microsoft To-Do as an import provider
    if arguments['--to-mstodo']:
        import_provider = MsTodoProvider()
    
    # Export tasks to memory
    task_lists = export_provider.export_tasks()
    # Import tasks from memory
    import_provider.import_tasks(task_lists)

if __name__ == '__main__':
    main()
# Pelican setup to deploy the gh-pages branch of python_course_material

The webpage is deployed at:

http://schryer.github.io/python_course_material/

## Building `schryer.github.io/python_course_material`

The build process consists of two commands, both of which are executed
in the root directory of this repository.  The first is a `Python`
script that reads all `Markdown` files in `stubs/` and `stubs/pages/`
and creates analogous files within `content/` and `content/pages/` with
the contents of `external_links.md` appended to each:

```shell
python add_links.py
```

To avoid confusing these generated files with user generated files,
the extension `.md` has been replaced with `_GENERATED_by_add_links.md`.

The second command is the `Pelican` build itself which places its output
in `output/`:

```shell
pelican content
```

Because GitHub pages requires a repository with the same name as the
above address (`schryer.github.io`) and updates the content after
every push, I added `schryer.github.io` as a subrepository within
`output/`. Thus, the final step in building `schryer.github.io` is to
commit and push the changes within `output/` to `GitHub`. In most
cases this involves issuing one command, although other commands may
be required depending on the state of the repository:

```shell
git commit -a -m "Appropriate message here."
```

## Cleaning temporary files.

The entire contents of `output/` can be wiped out by accident because
the contents of `output/` are generated, however, I still changed the
default behavior of the `clean` function within the `Makefile` to
clean out the files generated by `add_links.py`. This is also accomplished
using the `add_links.py` script. 

```shell
python add_links.py --clean
```

For further questions: `Use the source...`

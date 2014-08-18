 # -*- coding: utf-8 -*-

import os
import glob
import argparse

def make_argument_parser():
    '''Returns argument parser for this script.
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='''
This script adds links to each markdown file in the blog
========================================================

Each markdown file in stubs/ is converted and written to output/
                                     ''')

    fg = parser.add_argument_group('Flag parameters')
        
    fg.add_argument('--clean', action='store_true',
                    dest='clean_generated_files', 
                    default=False, 
                    help='If True, the generated Markdown files are removed. If False, they are generated.')

    return parser

def make_content_file_from_stub(stub_filename, content_type='md', link_filename='external_links.md'):

    print('Reading stub file: {}'.format(stub_filename))
    with open(stub_filename, 'r') as f:
        stub_lines = f.readlines()

    print('Reading link file: {}'.format(link_filename))
    with open(link_filename, 'r') as f:
        link_lines = f.readlines()

    substitutions = {}
    for link_line in link_lines:
        if link_line.startswith('['):

            # HACK
            # Makes an ugly assumption that there is no space between the ] and the :
            link, url = link_line.split(']:', 1)
            
            # Converts the line into a ipynb compatible markdown link.
            substitutions[link.strip() + ']'] = '{}({})'.format(link.strip() + ']', url.strip())
        
    if content_type == 'md':
        generated_filename = stub_filename.replace('stubs/', 'content/').replace('.md', '_GENERATED_by_add_links.md')
            
        print('Adding links and making content file: {}'.format(generated_filename))
        with open(generated_filename, 'w') as f:
            for line in stub_lines + ['\n', '\n'] + link_lines:
                f.write(line)

    elif content_type == 'ipynb':
        generated_filename = stub_filename.replace('stubs/', 'content/').replace('.ipynb', '_GENERATED_by_add_links.ipynb')

        original_meta_filename = stub_filename.replace('.ipynb', '.ipynb-meta')
        generated_meta_filename = generated_filename.replace('.ipynb', '.ipynb-meta')

        cmd = 'cp {} {}'.format(original_meta_filename, generated_meta_filename)
        print('Executing: {}'.format(cmd))
        os.system(cmd)

        print('Adding links and making content file: {}'.format(generated_filename))
        with open(generated_filename, 'w') as f:
            for line_number, line in enumerate(stub_lines):
                output = line
                for sub_key, markdown_url in substitutions.items():
                    if len(output.split(sub_key)) > 1:
                        print('Substituting {} with {} in line {}: {}'.format(sub_key, markdown_url, line_number, output.strip()))
                        output = output.replace(sub_key, markdown_url)
                f.write(output)

def process_arguments(args):

    markdown_files = glob.glob('stubs/*.md') + glob.glob('stubs/pages/*.md')
    ipynb_files = glob.glob('stubs/notebooks/*.ipynb')
    ipynb_meta_files = glob.glob('stubs/notebooks/*.ipynb-meta')
    
    generated_files = glob.glob('content/*_GENERATED_by_add_links.md') \
                      + glob.glob('content/pages/*_GENERATED_by_add_links.md') \
                      + glob.glob('content/notebooks/*_GENERATED_by_add_links.ipynb') 
    
    if args.clean_generated_files:
        for gfn in generated_files:
            print('Removing generated file: {}'.format(gfn))
            os.remove(gfn)
    else:    
        for stub in markdown_files:
            make_content_file_from_stub(stub)

        converted_ipynb_files = []
        for meta_file in ipynb_meta_files:

            stub = meta_file.replace('.ipynb-meta', '.ipynb')

            if stub not in ipynb_files:
                print('WARNING: An IPython notebook metadata file was found without its partner IPython notebook: {}'.format(meta_file))
                continue
                
            make_content_file_from_stub(stub, 'ipynb')
            converted_ipynb_files.append(stub)

        # Check if all IPython notebook files had metadata files:
        for ipynb_file in ipynb_files:
            if ipynb_file not in converted_ipynb_files:
                print('WARNING: An IPython notebook file was found without its partner IPython notebook metadata file: {}'.format(ipynb_file))
            
if __name__ == '__main__':
    p = make_argument_parser()
    args = p.parse_args()
    process_arguments(args)

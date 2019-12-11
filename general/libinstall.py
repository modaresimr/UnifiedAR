def install_libs():
    get_ipython().system('pip install -q tqdm #for progressbar')
    from tqdm import tqdm
    import subprocess
    import sys

    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    packages=[
        'numpy',
        'pandas',
        'wget',
        'intervaltree',
        'tensorflow',
        'tensorflow-plot',
        'scikit-optimize',
        'matplotlib',
        'seaborn',
        'plotly',
		'import-ipynb'
    ]
    pbar = tqdm(packages)
    for pack in pbar:
        pbar.set_description("Installing %s" % pack)
        if not(pack in installed_packages):
            get_ipython().system('pip install -q "$pack"')
    pbar.set_description("Everything Installed")

install_libs()


# In[11]:


def install_lab_libs():
    get_ipython().system('export NODE_OPTIONS=--max-old-space-size=4096')
    get_ipython().system('jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build')
    get_ipython().system('jupyter labextension install jupyterlab-plotly --no-build')
    get_ipython().system('jupyter labextension install plotlywidget --no-build')
    get_ipython().system('jupyter lab build')
    get_ipython().system('unset NODE_OPTIONS')
    
status = get_ipython().getoutput('jupyter labextension check plotlywidget;echo $?')
if(status[1]=='0'):
    print('Skip! labextensions are installed');
else:
    install_lab_libs();

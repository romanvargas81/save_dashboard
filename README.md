# hcx-quickbooks-dashboard

Local Dev
=========

For local deployment just clone the repository and run 

```bash
git submodule update --init --recursive 
```

This project uses https://github.com/HCGFM/hcg-python-utils as a git submodule

after the submodule has been clonned run

```bash
skaffold dev --port-forward 
```

